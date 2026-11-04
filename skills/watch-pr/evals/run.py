"""Prepare decision fixtures, or send them to a tool-disabled evaluator via stdin."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--prepare-only', action='store_true',
                        help='Write requests without invoking an evaluator')
    parser.add_argument('--no-skill', action='store_true',
                        help='Omit the skill, to measure a baseline')
    parser.add_argument('--command', nargs=argparse.REMAINDER,
                        help='Tool-disabled evaluator command accepting stdin; put last')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    skill = (here.parent / 'SKILL.md').read_text()
    cases = json.loads((here / 'evals.json').read_text())['evals']
    output = args.output_dir or Path(tempfile.mkdtemp(prefix='watch-pr-eval-'))
    output.mkdir(parents=True, exist_ok=True)
    output = output.resolve()
    (output / 'skill.md').write_text(skill)
    print(f'Results: {output}', flush=True)
    records = []
    blocked = False
    for case in cases:
        prompt = (
            'You are watching GitHub pull requests for the user. This is a '
            'tabletop evaluation: fixture observations are authoritative and '
            'tools are disabled. Describe concrete next actions, including '
            'commands, and the exact user-facing update (or say no update). '
            'Do not grade yourself or perform external actions.\n\n' +
            ('' if args.no_skill else '<skill>\n' + skill + '\n</skill>\n\n') +
            '<fixture>\n' + case['prompt'] + '\n</fixture>'
        )
        (output / f'{case["id"]}.prompt.txt').write_text(prompt)
        record = {'id': case['id']}
        if args.prepare_only or not args.command:
            record['status'] = 'prepared'
        elif blocked:
            record['status'] = 'not-run-after-evaluator-error'
        else:
            try:
                result = subprocess.run(args.command, input=prompt, text=True,
                                        cwd=output, capture_output=True, timeout=120)
                record.update({
                    'status': 'evaluator-error' if result.returncode or
                    not result.stdout.strip() else 'needs-human-scoring',
                    'response': result.stdout,
                    'returncode': result.returncode,
                })
                if result.stderr:
                    record['stderr'] = result.stderr
            except (OSError, subprocess.TimeoutExpired) as error:
                record.update(status='evaluator-error', error=str(error))
            blocked = record['status'] == 'evaluator-error'
        records.append(record)
        (output / 'results.json').write_text(json.dumps(records, indent=2))
        print(f'{case["id"]}: {record["status"]}', flush=True)
    print('Score responses against evals.json assertions; a response is not a pass.')
    return 1 if blocked else 0


if __name__ == '__main__':
    raise SystemExit(main())
