"""Test-only native return-admission gates, installed in disposable source copies."""
import hashlib
from pathlib import Path
import shutil

COMMON=r'''
return_gate_file(Name,File) :- getenv('RETURN_BARRIER_DIR',Dir),atom_concat(Dir,'/',Prefix),atom_concat(Prefix,Name,File).
return_gate_write(Name,Term) :- return_gate_file(Name,File),open(File,write,S),writeq(S,Term),write(S,'.'),nl(S),close(S).
return_gate_pause(Local,Origin,Token,Mode) :-
    Mode==open,Local==Origin,return_gate_file(arm,Arm),exists_file(Arm),!,
    delete_file(Arm),return_gate_write(token,Token),return_gate_write(entered,true),return_gate_wait(5000).
return_gate_pause(_,_,_,_).
return_gate_wait(N) :-
    (return_gate_file(continue,F),exists_file(F) -> true
    ; N>0,sleep(0.001),M is N-1,return_gate_wait(M)).
return_gate_record(Token,Mode,Result) :-
    (Mode==open,return_gate_file(token,F),exists_file(F),
     open(F,read,S),read(S,Stored),close(S),Stored==Token
    -> return_gate_write(result,Result),delete_file(F)
    ; true).
'''

def prepare(swi,trealla,directory):
    directory=Path(directory);outputs={};hashes={}
    for mode,root in [('swi',Path(swi)),('trealla',Path(trealla))]:
        dest=directory/mode;dest.mkdir()
        if mode=='swi':
            shutil.copytree(root/'prolog',dest/'prolog');rel='prolog/web_prolog/node_execution_context.pl'
            p=dest/rel;source=p.read_text();needle='resolve_client_lineage(Scope, LocalOrigin, Origin, Token, Queue, Mode, NS) :-'
            assert source.count(needle)==1
            wrapper=needle+'''
    return_gate_pause(LocalOrigin,Origin,Token,Mode),
    catch(resolve_client_lineage_impl(Scope,LocalOrigin,Origin,Token,Queue,Mode,NS),
          Error,(return_gate_record(Token,Mode,rejected(Error)),throw(Error))),
    return_gate_record(Token,Mode,accepted(NS)).
resolve_client_lineage_impl(Scope, LocalOrigin, Origin, Token, Queue, Mode, NS) :-'''
            p.write_text(source.replace(needle,wrapper)+COMMON)
        else:
            for f in root.glob('*.pl'):shutil.copyfile(f,dest/f.name)
            rel='receiver_lineage.pl';p=dest/rel;source=p.read_text()
            needle='wire_origin(Origin0,Origin),\n            with_mutex'
            assert source.count(needle)==1
            text=source.replace(needle,"wire_origin(Origin0,Origin),\n            web_prolog:current_node_url(Local),\n            (Command==lineage_close -> GateMode=close;GateMode=open),\n            return_gate_pause(Local,Origin,Token,GateMode),\n            with_mutex")
            needle='resolve_context(Origin,Token,Account,Relay,Command,NS) :-';assert text.count(needle)==1
            text=text.replace(needle,needle+'''
    (Command==lineage_close -> Mode=close;Mode=open),
    catch(resolve_context_impl(Origin,Token,Account,Relay,Command,NS),
          Error,(return_gate_record(Token,Mode,rejected(Error)),throw(Error))),
    return_gate_record(Token,Mode,accepted(NS)).
resolve_context_impl(Origin,Token,Account,Relay,Command,NS) :-''')
            p.write_text(text+COMMON)
        hashes[mode]={'path':rel,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'instrumented_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        outputs[mode]=dest
    return outputs,hashes
