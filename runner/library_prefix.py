"""Bounded external paging of otherwise infinite library relations."""
from baseline import http_case


def prefix_spec(case):
    spec = case['bounded_prefix']
    size, pages, first = (spec[k] for k in ('page_size', 'pages', 'first'))
    if (any(type(v) is not int for v in (size, pages, first)) or
            not 1 <= size <= 16 or not 1 <= pages <= 4 or first != 1):
        raise ValueError('invalid bounded library prefix')
    return size, pages, first


def http_prefix(case, source, url):
    size, pages, first = prefix_spec(case)
    requests = []
    for page in range(pages):
        offset = page * size
        values = ','.join(str(first + offset + i) for i in range(size))
        requests.append(dict(params=dict(goal=case['goal'], template='LibraryCheck',
                                         format='prolog', limit=size, offset=offset,
                                         src_text=source),
                             expect_prolog=f'success([{values}],true).'))
    # HTTP pages are independent calls. This proves service recovery, not
    # internal producer reclamation; retained sessions additionally stop below.
    requests.append(dict(params=dict(goal='LibraryRecovered=passed',
                                     template='LibraryRecovered', format='prolog', limit=1),
                         expect_prolog='success([passed],false).'))
    return http_case(dict(requests=requests), url, 8, None, False)


def session_prefix(case, harness):
    size, pages, first = prefix_spec(case)
    observed = []
    harness.call(case['goal'], f'[limit({size})]')
    try:
        for page in range(pages):
            if page:
                harness.next()
            event = harness.recv_type('success')
            observed.append(event)
            expected = [str(first + page * size + i) for i in range(size)]
            actual = [row.get('LibraryCheck') for row in event.get('data', [])]
            if actual != expected or event.get('more') is not True:
                raise AssertionError(f'expected ordered prefix {expected} and more=true: {event!r}')
    finally:
        harness.send(dict(command='toplevel_stop', pid=harness.shell))
        observed.append(harness.recv_type('stop', limit=32))
    harness.call('LibraryRecovered=passed', '[limit(1)]')
    recovered = harness.recv_type('success')
    observed.append(recovered)
    if recovered.get('more') is not False or recovered.get('data') != [{'LibraryRecovered': 'passed'}]:
        raise AssertionError(f'query did not recover after stop: {recovered!r}')
    return observed
