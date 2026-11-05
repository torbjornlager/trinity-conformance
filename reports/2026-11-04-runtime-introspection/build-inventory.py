from pathlib import Path
import re,json,hashlib,subprocess
source=Path('/Users/lager/boken/author/appendix-B-current-manual.tex');lines=source.read_text().splitlines(keepends=True)
# Preserve original source spans. A unit is a prose paragraph, list item,
# or predicate signature. Blank/layout-only commands do not assert behavior.
rows=[];section='Introduction';label='sec:manual';entry=None;profile='isobase';buf=[];start=0;verbatim=False
layout=re.compile(r'^\\(?:index\{|vspace\{|[a-z]*skip\b|begingroup\b|endgroup\b|setlength\{|raggedright\b|begin\{(?:itemize|description|tabular)\}|end\{(?:itemize|description|tabular)\}|medskip\b)')
def plain(s):
 s=s.replace('\\begin{verbatim}','').replace('\\end{verbatim}','');s=re.sub(r'%[^\n]*','',s);s=s.replace('\\allowbreak{}','').replace('\\_','_').replace('\\,',' ').replace('\\noindent','').replace('\\smallskip','').replace('\\medskip','')
 s=re.sub(r'\\(?:label|index)\{[^}]*\}','',s);s=re.sub(r'\\(?:texttt|textbf|textsc|emph|raggedright|item|hfill|par|smallskip|medskip|begin|end|href|ref|index)\b','',s)
 s=re.sub(r'\\\\(?:begin|end)\{verbatim\}', '', s);s=s.replace('\\\\',' ');s=re.sub(r'[{}]','',s);return re.sub(r'\s+',' ',s).strip()
def flush(end):
 global buf,start
 if not buf:return
 text=''.join(buf);buf=[];description=plain(text)
 if not description or description in ['Valid options are:','The options are:','There is only one valid option:']:return
 if text.lstrip().startswith('\\begin{verbatim}'):
  inner=text.split('\\begin{verbatim}',1)[1].split('\\end{verbatim}',1)[0]
  if not (' is ' in inner or inner.lstrip().startswith(':- op') or inner.lstrip().startswith('error(')):return
  kind='signature' if ' is ' in inner else 'declaration'
 else:kind='requirement'
 # Exclude publication/navigation prose, not language constraints.
 if 'shared online reference' in description or description.startswith('Runtime setup, source-loading machinery') or description.startswith('The complete wire specification'):return
 raw=''.join(lines[start-1:end]);rows.append(dict(id=f'B-{len(rows)+1:03}',section=section,label=label,entry=entry,minimum_profile=profile,kind=kind,source=dict(start=start,end=end,sha256=hashlib.sha256(raw.encode()).hexdigest()),statement=description))
for number,line in enumerate(lines,1):
 t=line.strip()
 if verbatim:
  buf.append(line)
  if t=='\\end{verbatim}':verbatim=False;flush(number)
  continue
 m=re.search(r'\\(section|subsection|subsubsection)\*?\{([^}]+)\}',line)
 if m:
  flush(number-1);section=m.group(2);entry=None;profile='isobase';lm=re.search(r'\\label\{([^}]+)\}',line);label=lm.group(1) if lm else label;continue
 if '\\textbf{Predicate:}' in line:
  flush(number-1);entry=plain(line.split('\\hfill')[0]).split('Predicate:',1)[1].strip();pm=re.search(r'\\textsc\{([^}]+)\}',line)
  profile='actor' if (pm and pm.group(1) in ['actor','statechart builtin']) or (not pm and section in ['Predicates for programming with server actors','Predicates for programming with core actors']) else 'isobase'
  if 'node introspection' in section.lower():profile='relation'
  continue
 if entry=='' and t.startswith('\\texttt'):
  entry=plain(line.split('\\hfill')[0]);continue
 if t.startswith('\\hfill'):continue
 if not t or t=='\\par':flush(number-1);continue
 if t.startswith('%') or layout.match(t) or t.startswith('\\chapter{'):continue
 if t.startswith('\\item'):
  flush(number-1)
 if t=='\\begin{verbatim}':flush(number-1);verbatim=True
 if not buf:start=number
 buf.append(line)
flush(len(lines))
for r in rows:
 r['targets']={mode:{'status':'not_applicable' if mode=='gnu' and r['minimum_profile']=='actor' else 'unverified','evidence':[]} for mode in ['swi','trealla','gnu','wasm_worker','wasm_main']}
 r['evidence_candidates']=[]
pin=subprocess.check_output(['git','rev-parse','HEAD'],cwd=source.parents[1],text=True).strip()
d=dict(schema_version=1,inventory_version='0.1',scope='Source-span inventory of Appendix B prose requirements, declarations and signatures. Statements can contain multiple related obligations; unverified includes unassessed. External ISO semantics need a separate exhaustive inventory.',source=dict(repository='https://github.com/torbjornlager/boken.git',revision=pin,path='author/appendix-B-current-manual.tex',sha256=hashlib.sha256(source.read_bytes()).hexdigest(),line_count=len(lines)),targets=dict(swi='native SWI ACTOR standalone APIs',trealla='native Trealla ACTOR standalone APIs',gnu='GNU ISOBASE query process',wasm_worker='SWI-WASM Worker language APIs',wasm_main='SWI-WASM main language APIs'),status_definitions=dict(verified='Named shared assertions on identified sources cover this whole unit within their recorded boundary.',unverified='The complete unit has not been demonstrated on the selected target; candidate evidence is not a pass.',missing='Source inspection identifies an absent required facility; report/source evidence is required.',failing='A current identified execution violates this unit.',not_applicable='The target does not advertise the minimum public profile for this unit.'),requirements=rows)
out=Path('/Users/lager/trinity-conformance/requirements/appendix-b-0.1.json');out.write_text(json.dumps(d,indent=2)+'\n')
print('inventory units',len(rows))
for r in rows:print(r['id'],r['source']['start'],r['entry'],r['statement'][:100])
