"""Acceptance rules for externally bounded noncompletion observations."""


def bounds(case):
    spec = case['bounded_noncompletion']
    values = tuple(spec[k] for k in ('observation_ms', 'entry_timeout_ms', 'termination_timeout_ms'))
    if (any(type(v) is not int for v in values) or
            not 100 <= values[0] <= 2000 or
            any(not 100 <= v <= 10000 for v in values[1:])):
        raise ValueError('invalid noncompletion bounds')
    return values


def validate_observation(case, observation):
    window, _, _ = bounds(case)
    for phase in ('warmup', 'recovery'):
        if observation[phase].get('passed') is not True or observation[phase].get('entry_count') != 1:
            raise ValueError('missing finite ' + phase + ' control or callback entry')
    probe = observation['probe']
    if probe.get('entry_count') != 1 or probe.get('entry_response_finished') is not True:
        raise ValueError('missing unique completed callback entry signal')
    if probe.get('elapsed_ms', -1) < window:
        raise ValueError('shortened observation window')
    if probe.get('terminal') is not None or probe.get('alive_before_termination') is not True:
        raise ValueError('query completed or failed before external termination')
    termination = observation['termination']
    if termination.get('confirmed') is not True or termination.get('duration_ms', float('inf')) > bounds(case)[2]:
        raise ValueError('execution termination was not confirmed within its bound')
    return True
