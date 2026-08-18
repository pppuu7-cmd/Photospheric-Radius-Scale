#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt

from idempotent_dispatch_guard import parse_utc, satisfying_run, select_existing_run


def run(run_id, created_at, *, event='workflow_dispatch', branch='main'):
    return {
        'id': run_id,
        'created_at': created_at,
        'event': event,
        'head_branch': branch,
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

    assert satisfying_run(exact, req)
    assert satisfying_run(later, req)
    assert not satisfying_run(before, req)
    assert not satisfying_run(wrong_event, req)
    assert not satisfying_run(wrong_branch, req)
    assert not satisfying_run({'id': 99}, req)

    # Input API ordering must not matter: choose the earliest qualifying run,
    # which is the run most tightly associated with this request.
    rows = [much_later, wrong_event, later, before, wrong_branch, exact]
    selected = select_existing_run(rows, req)
    assert selected is not None and selected['id'] == 10

    req_feature = dict(req, ref='feature')
    feature = run(20, '2026-08-18T11:44:17+00:00', branch='feature')
    assert satisfying_run(feature, req_feature)
    assert select_existing_run([later, feature], req_feature)['id'] == 20

    # No valid run => dispatch is still required.
    assert select_existing_run([before, wrong_event, wrong_branch], req) is None

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
