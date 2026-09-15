"""Validate domain-only upstream rules, merge local additions, then publish MRS."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
from urllib.request import urlopen
import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ('Pixiv', 'LinkedIn', 'Threads')

def domains(payload):
    if not isinstance(payload, list) or not payload:
        raise ValueError('empty or invalid upstream payload')
    result = set()
    for rule in payload:
        parts = rule.split(',') if isinstance(rule, str) else []
        if len(parts) != 2 or parts[0] not in ('DOMAIN', 'DOMAIN-SUFFIX'):
            raise ValueError(f'unsupported rule, refusing partial conversion: {rule!r}')
        domain = parts[1].lower()
        if not domain or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-.' for c in domain) or '.' not in domain:
            raise ValueError(f'invalid domain: {domain!r}')
        result.add(('+.' if parts[0] == 'DOMAIN-SUFFIX' else '') + domain)
    return sorted(result)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mihomo', required=True)
    args = parser.parse_args()
    binary = str(Path(args.mihomo).resolve())
    additions = json.loads((ROOT / 'Rules/service-additions.json').read_text())
    staged = []
    with tempfile.TemporaryDirectory() as folder:
        temp = Path(folder)
        for service in SERVICES:
            url = f'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/{service}/{service}.yaml'
            with urlopen(url, timeout=60) as response:
                source = response.read(2_000_001)
            if len(source) > 2_000_000:
                raise ValueError('upstream exceeds size limit')
            parsed = yaml.safe_load(source)
            entries = domains(parsed.get('payload') if isinstance(parsed, dict) else None)
            extra = additions.get(service, [])
            if extra:
                entries = sorted(set(entries + domains(extra)))
            filename = service + '_Domain'
            yaml_path = temp / (filename + '.yaml')
            mrs_path = temp / (filename + '.mrs')
            yaml_path.write_text(f'# Source: {url}\n# Author: blackmatrix7; local additions: Rules/service-additions.json\n' + yaml.safe_dump({'payload': entries}, sort_keys=False))
            subprocess.run([binary, 'convert-ruleset', 'domain', 'yaml', str(yaml_path), str(mrs_path)], check=True)
            if mrs_path.stat().st_size == 0:
                raise ValueError('converter returned empty MRS')
            staged.extend([(yaml_path, ROOT / 'Rules' / yaml_path.name), (mrs_path, ROOT / 'MRS' / mrs_path.name)])
            print(f'{service}: {len(entries)} domains')
        # No repository outputs are replaced until every download/conversion succeeds.
        for source, destination in staged:
            destination.write_bytes(source.read_bytes())

if __name__ == '__main__':
    main()
