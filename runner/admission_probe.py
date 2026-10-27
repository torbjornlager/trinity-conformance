"""Diagnostic-only query capture; no acceptance result is inferred from errors."""
import copy
import run as actor

class RecordingHarness(actor.Harness):
    def __init__(self,candidate):
        super().__init__(candidate)
        self.transcript=[]
    def send(self,command):
        self.transcript.append(dict(direction='send',message=copy.deepcopy(command)))
        super().send(command)
    def recv(self,expected_type=None):
        event=super().recv()
        self.transcript.append(dict(direction='receive',message=copy.deepcopy(event)))
        if expected_type:
            actor.require(event.get('type')==expected_type,repr(event))
        return event

def terminal(harness):
    for _ in range(64):
        event=harness.recv()
        if event.get('type') in {'success','failure','error'}:
            return event
        harness.acknowledge_output(event)
    raise actor.ConformanceFailure('no terminal response within 64 events')

def observe(case,url,timeout,token):
    candidate=actor.Candidate(url,'actor',timeout,token,None,False,())
    harness=RecordingHarness(candidate)
    result=dict(complete=False,transcript=harness.transcript)
    try:
        with harness:
            harness.spawn_shell('[session(true)]')
            goal='(self(ProbeSelf),ProbeSelf!admission_probe_entered,('+case['goal']+')),ProbeComplete=completed'
            harness.call(goal,'[limit(1)]')
            result['terminal']=terminal(harness)
            if result['terminal'].get('more') is True:
                harness.send({'command':'toplevel_stop','pid':harness.shell})
                harness.recv_type('stop',limit=64)
            # Same shell, no output marker. A persistent admission error must
            # leave no marker; execution queues it before the selected goal.
            harness.call('receive({admission_probe_entered->ProbeEntry=yes},[timeout(0),on_timeout(ProbeEntry=no)])','[limit(1)]')
            entry=terminal(harness)
            result['entry_response']=entry
            if entry.get('type')!='success':
                raise actor.ConformanceFailure('entry follow-up did not succeed')
            marker=actor.row_value(entry,'ProbeEntry')
            actor.require(marker in {'yes','no'},'unexpected entry marker '+repr(marker))
            actor.require(entry.get('more') is False,'entry follow-up left alternatives')
            result['execution_entered']=marker=='yes'
            harness.halt()
            result['complete']=True
    except Exception as error:
        result['probe_error']=type(error).__name__+': '+str(error)
    return result
