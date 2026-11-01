#!/usr/bin/env python3
"""Read-only node/source check; no queries, credentials, deployment or gate rerun."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.parse
import urllib.request

PINS = {
    'swi': 'ce5aa98b28c4aca8744dbf8a01d86cffdf74f299',
    'trealla': '2ebaeb9ca78e8ec58578e58bf86dad02a37625b2',
}


def command(*args):
    return subprocess.check_output(args, text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repositories', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output must not exist')
    result = dict(checked_at=datetime.now(timezone.utc).isoformat(),
                  scope=__doc__, public_metadata=[], deployed_sources=[])
    for node in range(1, 6):
        with urllib.request.urlopen(f'https://n{node}.elfenbenstornet.se/node_info', timeout=15) as response:
            if node == 5:
                destination = urllib.parse.urlparse(response.geturl())
                assert destination.path == '/oauth2/sign_in', destination.path
                result['public_metadata'].append(dict(node='N5', unauthenticated='SSO sign-in redirect'))
            else:
                data = json.load(response)
                result['public_metadata'].append(dict(node=f'N{node}', status=response.status,
                    profile=data['profile'], self_url=data['self_url']))
    for node, engine, repository, root in [
        (3, 'swi', 'swi-prolog-node', '/opt/swi-prolog-node/'),
        (4, 'swi', 'swi-prolog-node', '/opt/swi-prolog-node/'),
        (5, 'trealla', 'trealla-port', '/app/'),
    ]:
        repo = args.repositories / repository
        paths = command('git', '-C', str(repo), 'ls-tree', '-r', '--name-only', PINS[engine]).splitlines()
        paths = [p for p in paths if p.endswith('.pl') and
                 (engine == 'trealla' or p == 'load.pl' or p.startswith('prolog/'))]
        container = f'deployment-wp_n{node}-1'
        inspect = json.loads(command('docker', 'inspect', container))[0]
        assert inspect['State']['Status'] == 'running', container
        if node == 5:
            assert inspect['State']['Health']['Status'] == 'healthy'
        raw = command('docker', 'exec', container, 'sha256sum', *[root + p for p in paths])
        actual = {line.split(None, 1)[1].strip()[len(root):]: line.split()[0] for line in raw.splitlines()}
        assert set(actual) == set(paths)
        for path, digest in actual.items():
            source = subprocess.check_output(['git', '-C', str(repo), 'show', PINS[engine] + ':' + path])
            assert hashlib.sha256(source).hexdigest() == digest, (container, path)
        version = command('docker', 'exec', container,
                          '/opt/trealla/tpl' if engine == 'trealla' else 'swipl', '--version')
        result['deployed_sources'].append(dict(node=f'N{node}', image=inspect['Image'],
            status=inspect['State']['Status'], health=inspect['State'].get('Health', {}).get('Status'),
            engine_version=version, compared_revision=PINS[engine], verified_prolog_files=len(actual),
            source_manifest_sha256=hashlib.sha256(json.dumps(actual, sort_keys=True).encode()).hexdigest()))
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print('Verified N1–N4 public metadata, N5 SSO, and matching live N3/N4/N5 Prolog source hashes.')


if __name__ == '__main__':
    main()
