#!/usr/bin/env python3
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(os.environ.get("BENCH_ROOT", "/tmp/preflight-bench"))
ISSUE = {
    "healthy": None,
    "wrong_ruby": "the required Ruby version (4.0.8 from .ruby-version) is not installed or does not match the active Ruby",
    "db_down": "PostgreSQL is down or unreachable",
    "behind": "the branch is behind origin/main (by 5 commits)",
    "pending_migration": "there is a pending or unapplied database migration (reviewer_notes on chapter_notes)",
}
EXPECTED_VERDICT = {"healthy": "ready", "wrong_ruby": "blocked", "db_down": "blocked", "behind": "ready",
                    "pending_migration": "either"}


def grade(rec):
    issue = ISSUE[rec["scenario"]]
    q = f"""You grade a report from an agent that checked whether a repo is ready to run its tests.

Report:
<<<
{rec['final']}
>>>

Answer with JSON only, no prose:
{{"verdict": "ready" | "blocked" | "unclear",
  "flagged_issue": true | false,
  "false_alarm": true | false}}

- verdict: "ready" if the report says tests can run now (warnings allowed); "blocked" if it says they cannot run until something is fixed.
- flagged_issue: {"true if the report explicitly mentions that " + issue if issue else "always false"}.
- false_alarm: true if the report claims a blocking problem that is not about: {issue or "anything (the environment is healthy)"}."""
    out = subprocess.run(["pi", "-p", "--model", "github-copilot/claude-sonnet-5.5", "--no-session", "-nt", "-ne", "-ns",
                          "-nc", "--no-mcp", "-np", "--offline", q], capture_output=True, text=True).stdout
    g = json.loads(out[out.index("{"): out.rindex("}") + 1])
    exp = EXPECTED_VERDICT[rec["scenario"]]
    verdict_ok = g["verdict"] == exp or (exp == "either" and g["verdict"] != "unclear")
    issue_ok = g["flagged_issue"] if issue else True
    g["correct"] = verdict_ok and issue_ok and not g["false_alarm"]
    g["clean"] = not rec["side_effects"]
    return {**rec, "grade": g}


recs = [json.loads(l) for l in open(sys.argv[1] if len(sys.argv) > 1 else ROOT / "results.jsonl")]
with ThreadPoolExecutor(8) as ex:
    graded = list(ex.map(grade, recs))
with open(str(sys.argv[1] if len(sys.argv) > 1 else ROOT / "results.jsonl").replace("results", "graded"), "w") as f:
    for g in graded:
        f.write(json.dumps(g) + "\n")
print(len(graded), "graded")
