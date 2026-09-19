"""Pre-generate a pool of fresh practice-packet variants per math skill
profile, for the subscription Practice Packet Generator. Cloudflare Workers
cannot run reportlab, so a subscriber's "generate" click picks a random
not-yet-served variant from this pool rather than rendering a PDF live --
each variant still has fresh numbers and contexts (via a distinct seed),
so repeats are rare for normal use.
"""
import base64, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_math import Book, ROOT, TEAL, GRAY, NAVY
from math_content import PROFILES, task

OUT = ROOT / 'resources/2026-09-19/generator-pool'
OUT.mkdir(parents=True, exist_ok=True)
VARIANTS_PER_PROFILE = 15


def pack(payload, lookup, path):
    raw = path.read_bytes()
    parts = []
    pos = 0
    for m in __import__('re').finditer(rb'\bstream\r?\n(.*?)endstream', raw, __import__('re').S):
        parts.extend([raw[pos:m.start(1)], m.group(1)])
        pos = m.end(1)
    parts.append(raw[pos:])
    ids = []
    for b in parts:
        if not b:
            continue
        h = hashlib.sha256(b).hexdigest()
        if h not in lookup:
            lookup[h] = len(payload['chunks'])
            payload['chunks'].append(base64.b64encode(b).decode())
        ids.append(lookup[h])
    assert b''.join(base64.b64decode(payload['chunks'][i]) for i in ids) == raw
    payload['files'][path.name] = {
        'chunks': ids, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
        'contentType': 'application/pdf',
    }
    return path.name


def build_variant(p, profile_index, variant_index):
    grade, key, title, code, obj, strategy = p
    seed = 500000 + profile_index * 2000 + variant_index * 11
    warm = [task(p, seed + i) for i in range(2)]
    example = task(p, seed + 2)
    practice = [task(p, seed + 3 + i) for i in range(6)]
    exit_items = [task(p, seed + 9 + i) for i in range(2)]

    slug = f'gen-{key}-g{grade}-v{variant_index + 1}'
    b = Book(OUT / (slug + '.pdf'), title, f'Grade {grade} · Practice Packet Generator')
    b.cover(code, obj + ' A freshly generated practice packet: one worked example, a two-question warm-up, six independent practice questions, a two-question exit ticket, and a full answer key.')

    b.page('Worked example', 'MODEL')
    y = 680
    y = b.text(strategy, 48, y, size=11) - 20
    y = b.text(example['q'], 48, y, size=11.5, font='Bold') - 8
    b.text(example['work'], 48, y, size=11)

    b.questions('Warm-up', warm, per=2, kicker='WARM-UP')
    b.questions('Independent practice', practice, per=3, kicker='PRACTICE')
    b.questions('Exit ticket', exit_items, per=2, kicker='EXIT TICKET')
    b.key('Answer key', warm + [example] + practice + exit_items, per=6)

    pages = b.finish()
    return b.path, pages


def main():
    payload = {'chunks': [], 'files': {}}
    lookup = {}
    manifest = {}
    total = 0
    for i, p in enumerate(PROFILES):
        grade, key, title, code, obj, strategy = p
        variants = []
        for v in range(VARIANTS_PER_PROFILE):
            pdf_path, pages = build_variant(p, i, v)
            name = pack(payload, lookup, pdf_path)
            variants.append(name)
            total += 1
        manifest[key] = {'grade': grade, 'title': title, 'code': code, 'variants': variants}
        print(key, len(variants), 'variants', flush=True)
    (ROOT / 'server/generator-payload.json').write_text(json.dumps(payload, separators=(',', ':')))
    (ROOT / 'server/generator-manifest.json').write_text(json.dumps(manifest, indent=2))
    print('Built', total, 'variant packets across', len(manifest), 'profiles.')


if __name__ == '__main__':
    main()
