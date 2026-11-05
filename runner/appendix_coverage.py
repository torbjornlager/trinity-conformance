#!/usr/bin/env python3
"""Validate and render the pinned Appendix B source-unit coverage ledger."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STATUSES=('verified','unverified','missing','failing','not_applicable')
ALIASES={'swi':'swi','trealla':'trealla','gnu':'gnu','wasm_worker':'swi-wasm-worker','wasm_main':'swi-wasm-main'}

def validate(data,manual,root=ROOT):
    raw=manual.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=data['source']['sha256']:
        raise ValueError('Appendix B changed; review and migrate the inventory before reporting coverage')
    lines=raw.decode().splitlines(keepends=True);seen=set();cache={}
    for unit in data['requirements']:
        key=unit['id']
        if key in seen:raise ValueError('duplicate requirement '+key)
        seen.add(key);span=unit['source'];a,b=span['start'],span['end']
        if not 1<=a<=b<=len(lines):raise ValueError('invalid source span '+key)
        if hashlib.sha256(''.join(lines[a-1:b]).encode()).hexdigest()!=span['sha256']:
            raise ValueError('source span mismatch '+key)
        if set(unit['targets'])!=set(data['targets']):raise ValueError('incomplete target accounting '+key)
        for mode,cell in unit['targets'].items():
            status=cell['status']
            if status not in STATUSES:raise ValueError('unknown status '+key)
            if status=='not_applicable' and not (mode=='gnu' and unit['minimum_profile']=='actor'):
                raise ValueError('unsupported not_applicable waiver '+key)
            if status=='missing' and not cell.get('source_gap',{}).get('note'):
                raise ValueError('missing requires inspected source evidence '+key)
            if status not in ('verified','failing'):continue
            if not cell.get('evidence'):raise ValueError('execution evidence required '+key)
            observed=[]
            for evidence in cell['evidence']:
                path=root/evidence['report']
                if not path.resolve().is_relative_to(root.resolve()):raise ValueError('escaping report path')
                if path not in cache:cache[path]=json.loads(path.read_text())
                report=cache[path];candidate=evidence.get('candidate')
                if candidate!=ALIASES[mode]:raise ValueError('wrong target evidence '+key)
                if not evidence.get('cases'):raise ValueError('case IDs required '+key)
                for case in evidence['cases']:
                    rows=[r for r in report['results'] if r.get('id')==case and r.get('candidate',report.get('candidate'))==candidate]
                    if len(rows)!=1:raise ValueError('missing or duplicate case '+key+' '+case)
                    observed.append(rows[0]['status'])
            if status=='verified' and any(s!='pass' for s in observed):raise ValueError('non-passing case cannot verify '+key)
            if status=='failing' and not any(s=='fail' for s in observed):raise ValueError('failing requires an observed failure '+key)
    return {mode:dict(Counter(r['targets'][mode]['status'] for r in data['requirements'])) for mode in data['targets']}

def render(data,counts):
    modes=list(data['targets']);short={'verified':'V','unverified':'U','missing':'M','failing':'F','not_applicable':'—'}
    out=['# Appendix B requirement coverage','',
         'This is a development-source audit, not a release certificate. The latest public deployment retains its own recorded pins.',
         '',f"The inventory contains **{len(data['requirements'])} source units** from the pinned manuscript: prose groups, list items, declarations and predicate signatures. A unit can contain several related obligations. External ISO semantics are not expanded into a complete mode/error inventory. These counts are not a percentage of language conformance.",
         '', '**V** = verified within the named execution boundary; **U** = unverified or not yet assessed; **M** = a source-inspected missing facility; **F** = an observed failure; **—** = outside the target’s advertised profile. A candidate evidence link is not a pass.',
         '', 'Passing implementation suites do not automatically verify every paragraph. Most earlier case evidence still needs a clause-by-clause mapping. Capability declarations are checked here; the full lifetime meanings in their explanatory paragraph remain unverified.',
         '', '| Target | Verified | Unverified | Missing | Failing | Not applicable |','|---|---:|---:|---:|---:|---:|']
    for mode in modes:out.append('| '+mode+' | '+' | '.join(str(counts[mode].get(s,0)) for s in STATUSES)+' |')
    out+=['','The five columns describe runtime language modes. A local API result does not certify every public admission path, browser network policy, or lower-profile endpoint. GNU ISOBASE is not required to provide ACTOR APIs.',
          '', '## Priorities','',
          '1. **Native retained contexts:** the development repair passes all 51 scoped probes across both native runtimes and all four directed routes. Original failures and blocked source-export cases are resolved. Atomic last-attachment retirement also passes both orderings and negative controls. The public release verifies permitted routes and records nine unchanged-policy exclusions. Complete remaining lifetime/transport obligation mapping.',
          '2. **Standard library:** the required forms, described binding/solution semantics and exact callback errors are deployed across all five runtime modes. Complete the remaining external ISO mode/error inventory; see the standard-library release record.',
          '3. **Coverage mapping:** review remote lifecycle and monitor barriers, statechart invocation combinations, node settings, numeric/ISO semantics and real-browser lifetime/network behavior. Unverified is not a claim that these are broken.',
          '', '## Source and evidence','',
          f"Manuscript revision: `{data['source']['revision']}`; SHA-256: `{data['source']['sha256']}`.",
          '', '[Machine-readable ledger](../requirements/appendix-b-0.1.json) · [Introspection and diagnostic evidence](../reports/2026-11-04-runtime-introspection/README.md) · [Promise ownership repair](../reports/2026-11-05-promise-context/README.md) · [Standard-library repair](../reports/2026-11-05-standard-library/README.md) · [Native retained-context audit](../reports/2026-11-05-native-retained-context/README.md) · [Native retained-context repair](../reports/2026-11-05-native-retained-context-repair/README.md) · [Attachment repair qualification](../reports/2026-11-05-native-context-attachment-repair/README.md) · [Current public release](../reports/2026-11-05-native-context-release/README.md)',
          '', 'The validator checks manuscript drift, complete target accounting, applicable profiles, exact case IDs, candidate identity and outcomes. A whole-unit “verified” annotation still requires review that those assertions cover the complete statement.',
          '', '## Source-unit matrix','']
    last=None
    for r in data['requirements']:
        if last!=r['section']:
            last=r['section'];out+=['', '### '+last,'','| ID | Requirement | SWI | Trealla | GNU | Worker | Main |','|---|---|---|---|---|---|---|']
        u=data['source'];link=u['repository'].removesuffix('.git')+'/blob/'+u['revision']+'/'+u['path']+'#L'+str(r['source']['start'])
        statement=((('`'+r['entry']+'` — ') if r.get('entry') else '')+r['statement']).replace('|','\\|');out.append('| ['+r['id']+']('+link+') | '+statement+' | '+' | '.join(short[r['targets'][m]['status']] for m in modes)+' |')
    return '\n'.join(out)+'\n'

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,default=ROOT/'requirements/appendix-b-0.1.json');p.add_argument('--manual',type=Path,required=True);p.add_argument('--output',type=Path,default=ROOT/'docs/APPENDIX_B_COVERAGE.md');p.add_argument('--check',action='store_true');a=p.parse_args()
    try:
        d=json.loads(a.inventory.read_text());counts=validate(d,a.manual);text=render(d,counts)
        if a.check:
            if a.output.read_text()!=text:raise ValueError('rendered matrix is stale')
        else:a.output.write_text(text)
        print(json.dumps(dict(units=len(d['requirements']),targets=counts)))
    except (OSError,ValueError,KeyError) as e:p.exit(1,str(e)+'\n')
if __name__=='__main__':main()
