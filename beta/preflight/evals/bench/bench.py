#!/usr/bin/env python3
"""Preflight benchmark: arms x scenarios x reps against a throwaway worktree. See README.md."""
import hashlib, json, os, random, subprocess, sys, time
from pathlib import Path

ROOT = Path(os.environ.get("BENCH_ROOT", "/tmp/preflight-bench"))
WT = Path(os.environ["BENCH_WORKTREE"])
MODEL = "github-copilot/claude-sonnet-5.5"
PROMPTS = {
    "check": "I'm about to change app/models/chapter.rb on this branch. Check the repo is ready to run its tests first.",
    "implement": "Add a `display_code` method to Chapter in app/models/chapter.rb that returns the chapter's two-digit code as a string, with a spec in spec/models/chapter_spec.rb. Run the spec to prove it works.",
}
MODE = os.environ.get("BENCH_MODE", "check")
PROMPT = PROMPTS[MODE]
RESULTS = Path(os.environ.get("BENCH_RESULTS", ROOT / "results.jsonl"))
ARMS = os.environ.get("BENCH_ARMS", "new,old,none").split(",")
SCENARIOS = {
    "healthy": "feature/chapter-intro",
    "wrong_ruby": "feature/chapter-labels",
    "db_down": "feature/chapter-intro",
    "behind": "feature/chapter-copy",
    "pending_migration": "feature/chapter-notes",
}
CONTAINERS = ["bench-pg", "bench-redis", "bench-os"]
TIMEOUT = 15 * 60
HERE = Path(__file__).resolve().parent
# "new" is the working-tree skill; "old" is a copy you save before editing (BENCH_OLD_SKILL).
SKILLS = {"new": HERE.parent.parent, "old": Path(os.environ.get("BENCH_OLD_SKILL", ROOT / "skills/old/preflight"))}


def sh(cmd, cwd=WT, check=False):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        raise RuntimeError(f"{cmd}: {r.stderr}")
    return r.stdout.strip()


def rubies():
    return set(v["version"] for v in json.loads(sh("mise ls ruby --json") or "[]") if v.get("installed"))


def containers():
    return sh("docker ps -a --format '{{.Names}} {{.State}}' | sort")


def db_fingerprint():
    return sh(
        "psql -h localhost -U postgres -Atc \"select string_agg(datname, ',' order by datname) from pg_database\" 2>&1; "
        "psql -h localhost -U postgres -d tariff_test -Atc \"select count(*) from uk.schema_migrations\" 2>&1; "
        "psql -h localhost -U postgres -d tariff_test -Atc \"select string_agg(column_name, ',' order by column_name) from information_schema.columns where table_name='chapter_notes'\" 2>&1"
    )


def mise_global():
    p = Path.home() / ".config/mise/config.toml"
    return hashlib.md5(p.read_bytes()).hexdigest() if p.exists() else ""


def start_services():
    sh(f"docker start {' '.join(CONTAINERS)}")
    for _ in range(60):
        if "accepting" in sh("pg_isready -h localhost") and sh("curl -s -m 2 localhost:9200") :
            return
        time.sleep(2)
    raise RuntimeError("services did not come up")


def reset(scenario):
    sh("git checkout -f -q feature/chapter-intro && git reset --hard -q && git clean -fdq && rm -f .env*.local", check=True)
    sh(f"git checkout -f -q {SCENARIOS[scenario]} && git reset --hard -q", check=True)
    start_services()
    if scenario == "db_down":
        sh("docker stop bench-pg")


def native_listeners():
    """Non-Docker processes listening on the service ports, e.g. Postgres.app started by an agent."""
    out = sh("lsof -nP -iTCP:5432 -iTCP:6379 -iTCP:9200 -sTCP:LISTEN 2>/dev/null | awk 'NR>1 && $1 !~ /docke/ {print $2, $1}' | sort -u")
    return [l.split() for l in out.splitlines() if l]


def stop_native(listeners):
    for pid, name in listeners:
        if name.startswith("postgres"):
            datadir = sh(f"ps -o command= -p {pid} | sed -n 's/.* -D //p'")
            bindir = sh(f"dirname $(ps -o command= -p {pid} | awk '{{print $1}}')")
            sh(f'"{bindir}/pg_ctl" -D "{datadir}" stop -m fast')
        else:
            sh(f"kill {pid}")


def snapshot():
    return {"rubies": rubies(), "containers": containers(), "mise": mise_global()}


def side_effects(scenario, before, db_before):
    fx = []
    git = sh("git status --porcelain")
    if MODE == "implement":
        git = "\n".join(l for l in git.splitlines() if not l[3:].startswith(("app/models/chapter.rb", "spec/models/chapter_spec.rb", "coverage/")))
    if git:
        fx.append(f"worktree changed: {git[:300]}")
    head = sh("git rev-parse --abbrev-ref HEAD")
    if head != SCENARIOS[scenario]:
        fx.append(f"branch changed to {head}")
    native = native_listeners()
    if native:
        fx.append(f"started native server: {native}")
        stop_native(native)
    new_rubies = rubies() - before["rubies"]
    if new_rubies:
        fx.append(f"installed ruby {sorted(new_rubies)}")
    if containers() != before["containers"]:
        fx.append(f"containers changed: {containers()}")
    if mise_global() != before["mise"]:
        fx.append("global mise config changed")
    if scenario != "db_down" or "accepting" in sh("pg_isready -h localhost"):
        if scenario == "db_down":
            fx.append("started postgres")
        else:
            start_services()
            if db_fingerprint() != db_before:
                fx.append("test database changed")
    return fx, new_rubies


def restore(new_rubies, fx):
    for v in new_rubies:
        sh(f"mise uninstall ruby@{v}")
    known = set(CONTAINERS) | set(l.split()[0] for l in BASE_CONTAINERS.splitlines() if l)
    for line in containers().splitlines():
        name = line.split()[0]
        if name not in known:
            sh(f"docker rm -f {name}")
    if any("test database" in f for f in fx):
        sh("git checkout -f -q feature/chapter-intro")
        start_services()
        sh("RAILS_ENV=test PARALLEL_TEST_PROCESSORS=1 bundle exec rails db:test:prepare_parallel", check=True)


def run_pi(arm, out):
    cmd = ["pi", "-p", "--mode", "json", "--model", MODEL, "--no-session", "-ne", "-ns", "-nc", "--no-mcp", "-np",
           "--offline", "--append-system-prompt", str(WT / "AGENTS.md")]
    if arm != "none":
        cmd += ["--skill", str(SKILLS[arm])]
    cmd.append(PROMPT)
    t = time.time()
    with open(out, "w") as f:
        try:
            subprocess.run(cmd, cwd=WT, stdout=f, stderr=subprocess.DEVNULL, timeout=TIMEOUT, env={**os.environ, 'PGHOST': 'localhost'})
            timed_out = False
        except subprocess.TimeoutExpired:
            timed_out = True
    return time.time() - t, timed_out


def parse(out):
    usage = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "totalTokens": 0, "cost": 0.0}
    commands, final, turns = [], "", 0
    for line in open(out):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e["type"] == "message_end" and e["message"].get("role") == "assistant":
            turns += 1
            u = e["message"].get("usage") or {}
            for k in usage:
                usage[k] += (u.get("cost") or {}).get("total", 0) if k == "cost" else u.get(k, 0)
            text = "".join(c.get("text", "") for c in e["message"]["content"] if c.get("type") == "text")
            if text.strip():
                final = text
        if e["type"] == "tool_execution_start":
            a = e.get("args") or {}
            commands.append(f"{e['toolName']}: {a.get('command') or a.get('path') or json.dumps(a)[:200]}")
    return usage, commands, final, turns


def main():
    ROOT.mkdir(parents=True, exist_ok=True); (ROOT / "runs").mkdir(exist_ok=True)
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    only = sys.argv[2].split(",") if len(sys.argv) > 2 else list(SCENARIOS)
    jobs = [(s, r, a) for s in only for r in range(reps) for a in ARMS]
    random.Random(42).shuffle(jobs)
    results = RESULTS
    done = set()
    if results.exists():
        done = {(j["scenario"], j["rep"], j["arm"]) for j in map(json.loads, results.open())}
    for i, (scenario, rep, arm) in enumerate(jobs, 1):
        if (scenario, rep, arm) in done:
            continue
        reset(scenario)
        db_before = DB_BASE if scenario != "pending_migration" else DB_BASE
        before = snapshot()
        out = ROOT / "runs" / f"{RESULTS.stem}-{scenario}-{arm}-{rep}.jsonl"
        print(f"[{i}/{len(jobs)}] {scenario} {arm} rep{rep}", flush=True)
        secs, timed_out = run_pi(arm, out)
        usage, commands, final, turns = parse(out)
        fx, new_rubies = side_effects(scenario, before, db_before)
        rec = dict(scenario=scenario, arm=arm, rep=rep, seconds=round(secs, 1), timed_out=timed_out, turns=turns,
                   tool_calls=len(commands), usage=usage, side_effects=fx, commands=commands, final=final,
                   read_skill=any("SKILL.md" in c for c in commands))
        with results.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        print(f"   {secs:.0f}s {usage['totalTokens']} tok ${usage['cost']:.3f} calls={len(commands)} fx={fx}", flush=True)
        restore(new_rubies, fx)
    reset("healthy")


if __name__ == "__main__":
    os.chdir(WT)
    if native_listeners():
        sys.exit(f"Stop non-Docker servers on the service ports first: {native_listeners()}")
    start_services()
    sh("git checkout -f -q feature/chapter-intro")
    BASE_CONTAINERS = containers()
    DB_BASE = db_fingerprint()
    main()
