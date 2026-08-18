#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import tempfile
from pathlib import Path

from idempotent_dispatch_guard import consume, parse_utc, satisfying_run, select_existing_run


def run(run_id, created_at, *, event='workflow_dispatch', branch='main', actor='github-actions[bot]'):
    return {
        'id': run_id,
        'created_at': created_at,
        'event': event,
        'head_branch': branch,
        'actor': {'login': actor},
        'html_url': f'https://example.invalid/{run_id}',
    }


def main():
    req = {
        'workflow': 'rtk-heavy.yml',
        'ref': 'main',
        'created_at': '2026-08-18T11:44:16Z',
    }

    # Z and explicit-offset parsing must describe the same instant.
    a = parse_utc('2026-08-18T11:44:16Z')
    b = parse_utc('2026-08-18T14:44:16+03:00')
    assert a == b == dt.datetime(2026, 8, 18, 11, 44, 16, tzinfo=dt.timezone.utc)

    exact = run(10, '2026-08-18T11:44:16Z')
    later = run(11, '2026-08-18T11:44:20Z')
    much_later = run(12, '2026-08-18T11:45:00Z')
    before = run(9, '2026-08-18T11:44:15Z')
    wrong_event = run(13, '2026-08-18T11:44:17Z', event='push')
    wrong_branch = run(14, '2026-08-18T11:44:18Z', branch='rtk-class-build')
    manual_actor = run(15, '2026-08-18T11:44:19Z', actor='pppuu7-cmd')

    assert satisfying_run(exact, req)
    assert satisfying_run(later, req)
    assert not satisfying_run(before, req)
    assert not satisfying_run(wrong_event, req)
    assert not satisfying_run(wrong_branch, req)
    assert not satisfying_run(manual_actor, req)
    assert not satisfying_run({'id': 99}, req)

    # Input API ordering must not matter: choose the earliest qualifying
    # Actions-bot run, which is the run most tightly associated with request.
    rows = [much_later, manual_actor, wrong_event, later, before, wrong_branch, exact]
    selected = select_existing_run(rows, req)
    assert selected is not None and selected['id'] == 10

    req_feature = dict(req, ref='feature')
    feature = run(20, '2026-08-18T11:44:17+00:00', branch='feature')
    assert satisfying_run(feature, req_feature)
    assert select_existing_run([later, feature], req_feature)['id'] == 20

    # No valid automation run => dispatch is still required.
    assert select_existing_run([before, wrong_event, wrong_branch, manual_actor], req) is None

    # Simulate the post-crash recovery path at file level: an existing bot run
    # is selected, the request is consumed, and its run id is persisted.
    with tempfile.TemporaryDirectory(prefix='rtk-dispatch-test-') as td:
        root = Path(td)
        request_path = root / 'dispatch_request.json'
        state_path = root / 'current.json'
        request_path.write_text(json.dumps(req) + '\n')
        state_path.write_text(json.dumps({'dispatch': dict(req), 'iteration': 7}) + '\n')
        consume(request_path, state_path, later, 'reused_existing_run')
        assert not request_path.exists()
        state = json.loads(state_path.read_text())
        assert state['dispatch']['status'] == 'submitted'
        assert state['dispatch']['run_id'] == 11
        assert state['dispatch']['html_url'].endswith('/11')
        assert state['dispatch']['idempotency_disposition'] == 'reused_existing_run'
        assert state['dispatch']['idempotency_guard'] == 'workflow_ref_created_at_actor_v2'

    # A malformed request timestamp must fail closed rather than silently
    # producing a second expensive workflow dispatch.
    try:
        parse_utc('')
    except ValueError:
        pass
    else:
        raise AssertionError('empty created_at did not fail closed')

    print('RTK_IDEMPOTENT_DISPATCH_GUARD_UNIT_PASS')


if __name__ == '__main__':
    main()
