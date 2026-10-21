#!/usr/bin/env python3
"""Validate repository report schemas using their small standard-library vocabulary.

This is deliberately not a general JSON Schema implementation. Unknown schema
keywords fail explicitly, so extending the vocabulary cannot silently skip checks.
"""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
KEYWORDS={'$schema','$id','title','type','const','enum','required','properties','additionalProperties','items','pattern','format','minimum'}
def validate(value,schema,location='$'):
    unknown=set(schema)-KEYWORDS
    if unknown:raise ValueError(f'unsupported schema keywords: {unknown}')
    def require(condition,message):
        if not condition:raise ValueError(location+': '+message)
    if 'type' in schema:
        kinds=schema['type'] if isinstance(schema['type'],list) else [schema['type']]
        matches={'object':isinstance(value,dict),'array':isinstance(value,list),
                 'string':isinstance(value,str),'integer':type(value) is int,
                 'null':value is None,'boolean':type(value) is bool}
        require(any(matches[k] for k in kinds),'wrong type')
    if 'const' in schema:require(value==schema['const'],'wrong constant')
    if 'enum' in schema:require(value in schema['enum'],'not in enum')
    if 'minimum' in schema:require(value>=schema['minimum'],'below minimum')
    if 'pattern' in schema:require(re.search(schema['pattern'],value) is not None,'pattern mismatch')
    if 'format' in schema:
        require(schema['format']=='date-time','unsupported format')
        require(datetime.fromisoformat(value.replace('Z','+00:00')).tzinfo is not None,'missing timestamp timezone')
    if isinstance(value,dict):
        require(set(schema.get('required',[]))<=set(value),'missing required property')
        properties=schema.get('properties',{})
        for key,item in value.items():
            if key in properties:validate(item,properties[key],location+'.'+key)
            else:
                additional=schema.get('additionalProperties',True)
                require(additional is not False,'unexpected property '+key)
                if isinstance(additional,dict):validate(item,additional,location+'.'+key)
    if isinstance(value,list) and 'items' in schema:
        for index,item in enumerate(value):validate(item,schema['items'],f'{location}[{index}]')
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('directory',type=Path);args=parser.parse_args()
    provenance=json.loads((args.directory/'provenance.json').read_text())
    for run in provenance['runs']:
        if not run['report']:raise ValueError('missing report: '+run['label'])
        report=json.loads((args.directory/run['report']).read_text())
        schema=json.loads((ROOT/'schemas'/f"report-v{report['schema_version']}.schema.json").read_text())
        validate(report,schema,run['label'])
        assert sum(report['counts'].values())==len(report['results']),run['label']
        for status,count in report['counts'].items():
            assert count==sum(row['status']==status for row in report['results']),run['label']
        ids=[row['id'] for row in report['results']];assert len(ids)==len(set(ids)),run['label']
    print(f"Validated {len(provenance['runs'])} reports and their accounting")
if __name__=='__main__':main()
