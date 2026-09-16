"""Store existing catalog PDFs losslessly without repeating identical PDF streams.

Run after refresh_catalog_assets.py creates its migration payload. This changes
storage only: every exported PDF must retain its exact original SHA-256 digest.
"""
import base64
import gzip
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root / 'server/private-products.ts'
text = source.read_text()
if 'export const privateProducts: Record<string,string> = ' not in text:
    raise SystemExit('Existing PDF payload is already packaged; refresh assets first to replace it.')
encoded = json.loads(text.split('export const privateProducts: Record<string,string> = ', 1)[1].strip().rstrip(';'))
chunks, lookup, files = [], {}, {}
for identifier, value in encoded.items():
    raw = base64.b64decode(value, validate=True)
    parts, offset = [], 0
    for match in re.finditer(rb'\bstream\r?\n(.*?)endstream', raw, re.S):
        parts.extend([raw[offset:match.start(1)], match.group(1)])
        offset = match.end(1)
    parts.append(raw[offset:])
    indices = []
    for part in parts:
        if not part:
            continue
        digest = hashlib.sha256(part).hexdigest()
        if digest not in lookup:
            lookup[digest] = len(chunks)
            chunks.append(base64.b64encode(part).decode())
        indices.append(lookup[digest])
    restored = b''.join(base64.b64decode(chunks[i]) for i in indices)
    assert restored == raw
    files[identifier] = {'chunks': indices, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
payload = json.dumps({'chunks': chunks, 'files': files}, separators=(',', ':'))
(root / 'server/legacy-resource-payload.json').write_text(payload + '\n')
source.write_text('''// Server-only exact original catalog files. Decoded only when provisioning.
import payload from './legacy-resource-payload.json';
export const privateProducts = Object.create(null) as Record<string,string>;
for (const [id,file] of Object.entries(payload.files)) {
 Object.defineProperty(privateProducts,id,{enumerable:true,get:()=>btoa(file.chunks.map(index=>atob(payload.chunks[index])).join(''))});
}
''')
print(f'Preserved {len(files)} existing PDFs byte-for-byte; compressed storage {len(gzip.compress(payload.encode()))} bytes.')
