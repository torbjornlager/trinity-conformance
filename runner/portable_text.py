"""Experimental portable-text 0.2 procedures; public protocol operations only."""
import contextlib
import re
import sys
from urllib.parse import urlsplit
import run as actor

# Only data can be spliced back into the equality assertion. In particular,
# reject trailing goals, directives, compounds, list tails and comments.
_ESCAPE = r"\\(?:x[0-9A-Fa-f]+\\|[0-7]+\\|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}|[\s\S])"
_SINGLE = r"'(?:''|" + _ESCAPE + r"|[^'\\])*'"
_DOUBLE = r'"(?:""|' + _ESCAPE + r'|[^"\\])*"'
_BARE = r"[^\s,\[\](){}|:'\"%]+"
_ELEMENT = '(?:' + _SINGLE + '|' + _DOUBLE + '|' + _BARE + ')'
_DATA = re.compile(r'\s*(?:' + _DOUBLE + r'|\[\s*(?:' + _ELEMENT + r'(?:\s*,\s*' + _ELEMENT + r')*)?\s*\])\s*\Z')
KINDS = {'goal','source_text','source_list','source_uri','round_trip','input','peer_goal'}

def scalar_text(text):
    return all(not 0xD800 <= ord(c) <= 0xDFFF for c in text)

def safe_text_term(text):
    return len(text) <= 16384 and scalar_text(text) and bool(_DATA.fullmatch(text)) and not any(
        marker in re.sub(_SINGLE+'|'+_DOUBLE, '', text) for marker in ('/*','*/'))

def validate(manifest, selected, peer=None, source_base=None):
    cases=manifest['cases'];ids=[c['id'] for c in cases]
    if len(ids)!=len(set(ids)):raise ValueError('duplicate portable-text case ID')
    def walk(value):
        if isinstance(value,str) and not scalar_text(value):raise ValueError('manifest contains a Unicode surrogate')
        if isinstance(value,dict):
            for item in value.values():walk(item)
        if isinstance(value,list):
            for item in value:walk(item)
    walk(manifest)
    for c in cases:
        if c['execution'] not in KINDS:raise ValueError('unknown portable-text procedure')
        if selected and c['id'] not in selected:continue
        if c['execution']=='peer_goal' and not peer:raise ValueError('selected remote text cases require --peer')
        if c['execution']=='source_uri' and not source_base:raise ValueError('selected URI text cases require --source-base')
    for value in (peer,source_base):
        if value is None:continue
        p=urlsplit(value)
        if p.scheme not in ('http','https') or not p.hostname or p.username or p.password or p.query or p.fragment:
            raise ValueError('text fixture addresses must be HTTP(S) bases without credentials, query or fragment')

@contextlib.contextmanager
def session(candidate, options):
    with actor.Harness(candidate) as h:
        try:
            h.spawn_shell(options)
            yield h
        finally:
            primary=sys.exc_info()[0]
            try:h.halt()
            except Exception:
                if primary is None:raise

def success(h):
    event=h.recv_type('success',limit=32)
    actor.require(event.get('more') is False,f'text assertion left a continuation: {event!r}')
    return event

def execute(candidate, case, peer=None, source_base=None):
    kind=case['execution'];options='[session(true)]';goal=case.get('goal')
    if kind=='source_text':options='[session(true),src_text('+actor.prolog_quote_atom(case['source'])+')]'
    elif kind=='source_list':options='[session(true),src_list('+case['clauses']+')]'
    elif kind=='source_uri':
        uri=source_base.rstrip('/')+'/'+case['fixture']
        options='[session(true),src_uri('+actor.prolog_quote_atom(uri)+')]'
    elif kind=='peer_goal':goal=goal.replace('__PEER__',actor.prolog_quote_atom(peer))
    with session(candidate,options) as h:
        if kind=='input':
            h.call("input('Portable text',Text),Text=="+case['expected'],'[limit(1)]')
            prompt=h.recv('prompt')
            actor.require(prompt.get('pid')==h.shell and prompt.get('data')=='Portable text',repr(prompt))
            h.send({'command':'toplevel_respond','pid':h.shell,'input':case['reply']})
            ack=False;answer=False
            for _ in range(32):
                event=h.recv();tag=event.get('type')
                actor.require(tag not in ('error','failure'),f'input text assertion failed: {event!r}')
                if tag=='responded':ack=True
                elif tag=='success':
                    actor.require(not answer and event.get('more') is False,repr(event));answer=True
                if ack and answer:return
            raise actor.ConformanceFailure('missing input acknowledgement or terminal answer')
        h.call(goal,'[limit(1)]');first=success(h)
        if kind=='round_trip':
            rendered=actor.row_value(first,'Text')
            actor.require(safe_text_term(rendered),f'not a bounded data-only serialized text term: {rendered!r}')
            # Resubmit the original spelling, not a Python-decoded replacement.
            h.call('('+rendered+')==('+case['expected']+')','[limit(1)]')
            success(h)
