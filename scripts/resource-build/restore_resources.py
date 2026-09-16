"""Restore the exact private teaching files from the versioned server payload.

The public website contains sample images only. Run this utility from a trusted
Site checkout; its output belongs in the ignored resources directory, never public/.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def restore(product_id=None):
    payload = json.loads((ROOT / 'server/resource-payload.json').read_text())
    output = ROOT / 'resources/2026-09-15'
    output.mkdir(parents=True, exist_ok=True)
    if product_id and product_id not in payload['products']:
        raise ValueError('Unknown resource identifier')
    names = set(payload['products'][product_id].values()) if product_id else payload['files']
    chunks = [base64.b64decode(chunk, validate=True) for chunk in payload['chunks']]
    for name in names:
        if Path(name).name != name:
            raise ValueError('Unsafe resource filename')
        metadata = payload['files'][name]
        data = b''.join(chunks[index] for index in metadata['chunks'])
        if len(data) != metadata['bytes'] or hashlib.sha256(data).hexdigest() != metadata['sha256']:
            raise ValueError(f'Integrity check failed: {name}')
        target = output / name
        if not target.exists() or target.read_bytes() != data:
            target.write_bytes(data)
    print(f'Restored and verified {len(names)} private files in {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--product', help='Restore one product and all of its file formats')
    restore(parser.parse_args().product)
