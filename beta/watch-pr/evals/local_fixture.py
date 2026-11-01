"""Local Git-backed fake GitHub for exercising watch-pr without a real PR."""

import argparse
import json
from pathlib import Path
import subprocess


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()


def setup(root):
    if root.exists():
        raise SystemExit('Choose a new directory; existing fixtures are never overwritten')
    root.mkdir(parents=True)
    (root / 'empty-hooks').mkdir()
    for name in ['lifecycle', 'external-update', 'interrupted-push']:
        case = root / name
        case.mkdir()
        remote, repo, work = case / 'remote.git', case / 'repo', case / 'work'
        git(case, 'init', '--bare', str(remote))
        git(case, 'init', '-b', 'pr', str(repo))
        git(repo, 'config', 'user.name', 'Local fixture')
        git(repo, 'config', 'user.email', 'fixture@example.invalid')
        git(repo, 'config', 'commit.gpgsign', 'false')
        git(repo, 'config', 'core.hooksPath', str(root / 'empty-hooks'))
        (repo / '.gitignore').write_text('__pycache__/\n')
        (repo / 'normalizer.py').write_text('def normalize(value):\n    return value.strip().lower()\n')
        (repo / 'test_normalizer.py').write_text(
            'import unittest\nfrom normalizer import normalize\n\n'
            'class NormalizerTests(unittest.TestCase):\n'
            '    def test_text(self):\n'
            '        self.assertEqual(normalize(" Hello "), "hello")\n'
        )
        (repo / 'lint.py').write_text(
            'import ast\nfrom pathlib import Path\n'
            'for p in Path(".").glob("*.py"):\n'
            '    text = p.read_text()\n    ast.parse(text)\n'
            '    assert all(line == line.rstrip() for line in text.splitlines()), p\n'
        )
        (repo / 'AGENTS.md').write_text(
            'Run tests with `python3 -m unittest -v`. Run lint with `python3 lint.py`.\n'
            'Use short imperative commit subjects. Never co-author commits.\n'
            'This fixture uses a local bare Git remote only. Never access the network.\n'
        )
        git(repo, 'add', '.gitignore', 'normalizer.py', 'test_normalizer.py', 'lint.py', 'AGENTS.md')
        git(repo, 'commit', '-m', 'Add normalizer fixture')
        original = git(repo, 'rev-parse', 'HEAD')
        git(repo, 'remote', 'add', 'origin', str(remote))
        git(repo, 'push', '-u', 'origin', 'pr')
        work.mkdir()
        fixture = {'name': name, 'url': f'https://github.invalid/local/{name}/pull/1',
                   'old_head': original, 'comments': [], 'ci': 'pending',
                   'required_checks': ['lint', 'tests'], 'isDraft': True}
        if name == 'lifecycle':
            (repo / 'README.md').write_text('Local test fixture.\n')
            git(repo, 'add', 'README.md')
            git(repo, 'commit', '-m', 'Document fixture')
            git(repo, 'push')
            fixture['ci'] = 'stale-green'
        else:
            (repo / 'normalizer.py').write_text(
                'def normalize(value):\n    if value is None:\n        return ""\n'
                '    return value.strip().lower()\n'
            )
            if name == 'external-update':
                patch = git(repo, 'diff', '--', 'normalizer.py')
                (case / 'pending.patch').write_text(patch + '\n')
            git(repo, 'add', 'normalizer.py')
            git(repo, 'commit', '-m', 'Handle missing input')
            git(repo, 'push')
            intended = git(repo, 'rev-parse', 'HEAD')
            fixture['comments'] = [review_comment(
                fixture, 'Handle None input by returning an empty string.',
                '2026-11-01T10:00:00Z')]
            if name == 'external-update':
                # Recreate the old-base worktree without resetting any branch.
                git(repo, 'worktree', 'add', '--detach', str(case / 'pending'), original)
                (case / 'pending' / 'normalizer.py').write_text((repo / 'normalizer.py').read_text())
                state = {'phase': 'validated-before-commit', 'head': original,
                         'attempts': 1, 'worktree': str(case / 'pending')}
            else:
                state = {'phase': 'pushing', 'head': original,
                         'intended_sha': intended, 'attempts': 1, 'last_reported': 'comment',
                         'comments': {'42': {'updated_at': '2026-11-01T10:00:00Z',
                                            'status': 'fixed', 'sha': intended}}}
            (work / 'watch.md').write_text('# Watch state\n\n```json\n' + json.dumps(state, indent=2) + '\n```\n')
        (case / 'fixture.json').write_text(json.dumps(fixture, indent=2))
        (case / 'initial-head.txt').write_text(git(remote, 'rev-parse', 'refs/heads/pr') + '\n')
    print(root)


def fake_gh(case, args):
    fixture = json.loads((case / 'fixture.json').read_text())
    with (case / 'calls.jsonl').open('a') as log:
        log.write(json.dumps(args) + '\n')
    head = git(case / 'remote.git', 'rev-parse', 'refs/heads/pr')
    failed = fixture['ci'] == 'failed' and head == fixture.get('ci_head')
    checks = [{'name': name, 'status': 'COMPLETED' if fixture['ci'] == 'stale-green' or failed else 'QUEUED',
               'conclusion': ('FAILURE' if name == 'tests' else 'SUCCESS') if failed else
               ('SUCCESS' if fixture['ci'] == 'stale-green' else None),
               'headSha': fixture['old_head'] if fixture['ci'] == 'stale-green' else head,
               'detailsUrl': fixture['url'].split('/pull/')[0] + '/actions/runs/303',
               'checkRun': {'headSha': fixture['old_head'] if fixture['ci'] == 'stale-green' else head}}
              for name in fixture['required_checks']]
    comments = fixture['comments']
    snapshot = {'url': fixture['url'], 'number': 1, 'state': 'OPEN',
                'isDraft': fixture['isDraft'], 'headRefName': 'pr', 'headRefOid': head,
                'baseRefName': 'main', 'mergeable': 'MERGEABLE', 'reviewDecision': 'APPROVED',
                'reviews': [], 'comments': [], 'statusCheckRollup': checks,
                'requiredChecks': fixture['required_checks']}
    threads = [{'id': 'thread-' + str(c['id']), 'isResolved': False, 'isOutdated': False,
                'comments': {'nodes': [c], 'pageInfo': {'hasNextPage': False, 'endCursor': None}}}
               for c in comments]
    if args[:2] == ['pr', 'view']:
        result = snapshot
    elif args[:2] == ['run', 'view'] and '--log-failed' in args:
        print('tests failed on ' + str(fixture.get('ci_head')) + '\n'
              'normalize(None)\nAttributeError: NoneType object has no attribute strip')
        return
    elif args[:2] in [['run', 'list'], ['run', 'view']]:
        run = {'databaseId': 303, 'headSha': fixture.get('ci_head', head),
               'headBranch': 'pr', 'status': 'completed' if failed else 'queued',
               'conclusion': 'failure' if failed else None, 'name': 'tests'}
        result = [run] if args[1] == 'list' else run
    elif args[:2] == ['pr', 'checks']:
        result = checks
    elif args[:2] == ['api', 'graphql']:
        result = {'data': {'repository': {'pullRequest': {**snapshot, 'reviewThreads': {
            'nodes': threads, 'pageInfo': {'hasNextPage': False, 'endCursor': None}}}}}}
    elif args and args[0] == 'api' and '/comments' in ' '.join(args):
        result = comments
    elif args and args[0] == 'api' and '/reviews' in ' '.join(args):
        result = []
    elif args and args[0] == 'api' and 'protection/required_status_checks' in ' '.join(args):
        result = {'contexts': fixture['required_checks']}
    elif args[:2] == ['pr', 'ready']:
        fixture['isDraft'] = False
        (case / 'fixture.json').write_text(json.dumps(fixture, indent=2))
        result = {'markedReady': True}
    else:
        raise SystemExit('Unsupported fake GitHub operation: ' + ' '.join(args))
    print(json.dumps(result, indent=2))


def review_comment(fixture, body, timestamp):
    return {'id': 42, 'node_id': 'comment42', 'body': body,
            'path': 'normalizer.py', 'line': 2,
            'updated_at': timestamp, 'created_at': '2026-11-01T10:00:00Z',
            'user': {'login': 'reviewer'}, 'author': {'login': 'reviewer'},
            'html_url': fixture['url'] + '#discussion_r42'}


def advance(case, event):
    path = case / 'fixture.json'
    fixture = json.loads(path.read_text())
    if event == 'failure':
        fixture['ci'] = 'failed'
        fixture['ci_head'] = git(case / 'remote.git', 'rev-parse', 'refs/heads/pr')
        body = 'Handle None input by returning an empty string. Add regression coverage.'
        timestamp = '2026-11-01T10:00:00Z'
    else:
        body = 'Also cover an empty string; the existing test only covers None.'
        timestamp = '2026-11-01T10:20:00Z'
    fixture['comments'] = [review_comment(fixture, body, timestamp)]
    path.write_text(json.dumps(fixture, indent=2))
    print('Advanced local fixture: ' + event)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='action', required=True)
    init = subs.add_parser('setup')
    init.add_argument('root', type=Path)
    gh = subs.add_parser('gh')
    gh.add_argument('case', type=Path)
    gh.add_argument('args', nargs=argparse.REMAINDER)
    step = subs.add_parser('advance')
    step.add_argument('case', type=Path)
    step.add_argument('event', choices=['failure', 'edited-comment'])
    args = parser.parse_args()
    if args.action == 'setup':
        setup(args.root.resolve())
    elif args.action == 'advance':
        advance(args.case.resolve(), args.event)
    else:
        fake_gh(args.case.resolve(), args.args)


if __name__ == '__main__':
    main()
