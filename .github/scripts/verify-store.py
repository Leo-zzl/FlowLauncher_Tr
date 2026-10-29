"""Smoke-check the settings template and Flow's isolated Python entry point."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
raw = (root / 'SettingsTemplate.yaml').read_bytes()
raw.decode('ascii')
settings = json.loads(raw.decode('ascii'))
defaults = {item['attributes']['name']: item['attributes']['defaultValue']
            for item in settings['body'] if 'defaultValue' in item['attributes']}
assert len(defaults) == 10
rpc = {'method': 'query', 'parameters': [''], 'settings': defaults}
result = subprocess.run([sys.executable, '-S', str(root / 'main.py'), json.dumps(rpc)],
                        check=True, capture_output=True, encoding='utf-8')
assert not result.stderr
response = json.loads(result.stdout)
assert response['result'] and response['result'][0]['Title']
print('ASCII-safe settings and isolated Python entry point: OK')
