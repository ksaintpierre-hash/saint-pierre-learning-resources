"""Build full-length introductory-college course packets: warm-up, reading
or worked-example content, guided practice, partner/lab discussion,
independent practice, small-group extension work, assessment, answer key.
Sized for a real college class session (the 'minutes' field on each row
sets the stated length), not a K-12 block period. Reuses the same
reportlab Book renderer and private-payload packing pattern as
build_ela_packet.py, so output slots directly into
data/sales-release-2026-09-15.json.
"""
import base64, hashlib, json, re, sys
from pathlib import Path
from reportlab.lib.colors import HexColor
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_math import Book, ROOT, TEAL, GRAY, NAVY, GOLD
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from watermark_previews import watermark

OUT = ROOT / 'resources/2026-09-18'
OUT.mkdir(parents=True, exist_ok=True)
PUB_PREVIEWS = ROOT / 'public/product-previews'
PUB_THUMBS = ROOT / 'public/product-thumbnails'


def draw_composition(c, kind, x=48, y=108, w=516, h=340):
    c.setStrokeColor(HexColor(GRAY))
    c.setLineWidth(1)
    c.rect(x, y, w, h, fill=0, stroke=1)
    if kind == 'calm':
        bands = ['#DCE7E6', '#C7DAD8', '#B7CFCE']
        band_h = 56
        gap = (h - len(bands) * band_h) / (len(bands) + 1)
        for i, col in enumerate(bands):
            by = y + h - gap - (i + 1) * band_h - i * gap
            c.setFillColor(HexColor(col))
            c.rect(x + 40, by, w - 80, band_h, fill=1, stroke=0)
        c.setStrokeColor(HexColor(TEAL))
        c.setLineWidth(1.5)
        c.line(x + w / 2, y + 16, x + w / 2, y + h - 16)
    elif kind == 'tension':
        c.setLineWidth(16)
        c.setStrokeColor(HexColor(NAVY))
        for i in range(4):
            xx = x + 70 + i * 95
            c.line(xx, y + 20, xx + 60, y + h - 20)
        c.setFillColor(HexColor('#8B3A2E'))
        c.rect(x + 36, y + 24, 150, 92, fill=1, stroke=0)
        c.setFillColor(HexColor(GOLD))
        c.circle(x + w - 96, y + h - 70, 22, fill=1, stroke=0)

SUPPORTS = {
    'Extension': 'Ask for a second method, a counterexample, or a short student-led extension of the concept, with a brief explanation of the choice.',
    'Accommodated seating/504': 'Follow the individual accommodation plan: extended time, breaks, enlarged print, reduced copying, or an alternate response method as documented.',
    'Additional support': 'Pre-teach key vocabulary or notation before class. Model the first guided item aloud. Accept oral or dictated responses when appropriate.',
    'Multilingual learners': 'Preview key terms with examples. Allow brief first-language discussion before independent writing. Provide sentence or solution starters.',
}


def pack(payload, lookup, path):
    raw = path.read_bytes()
    parts = []
    pos = 0
    if path.suffix == '.pdf':
        for m in re.finditer(rb'\bstream\r?\n(.*?)endstream', raw, re.S):
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
        'contentType': 'application/pdf' if path.suffix == '.pdf' else 'image/png',
    }
    return path.name


def build_one(row):
    slug = row['id']
    code, standard_text = row['standard'].split(' — ', 1)
    descriptor = f'{row["course"]} · {row["subject"]}'
    items = row['items']
    assert len(items) == 20, (slug, len(items))
    warm = items[0:2]
    guided = items[2:6]
    partner = items[6:9]
    indep = items[9:15]
    interv = items[15:17]
    enrich = items[17:19]
    exit_item = items[19:20]
    item_font = row.get('text_font') or 'Body'
    item_bold = 'Bold' if not row.get('text_font') else item_font
    title_font = row.get('text_font') or 'Title'

    b = Book(OUT / (slug + '.pdf'), row['title'], descriptor)
    b.cover(code, row['objective'] + f' A complete {row["minutes"]} packet with warm-up, guided practice, partner/lab work, independent practice, extension work, assessment, and a full answer key.', title_font=title_font)

    b.page('Plan the session', 'INSTRUCTOR GUIDE')
    y = 680
    for h, t in [
        ('Course and objective', descriptor + '; ' + row['standard']),
        ('What is included', 'Cover; instructor guide; key-term and concept preview; original reading or worked examples; warm-up (2 items); guided practice with organizer (4 items); partner/lab discussion (3 items); independent practice (6 items); small-group extension work (4 items); assessment; complete answer key; access and sources page.'),
        ('Suggested pacing (' + row['minutes'] + ')', row.get('pacing', 'Warm-up · reading or worked examples with guided practice · partner or lab discussion · independent practice · extension work · assessment.')),
        ('Preparation', 'Print student pages separately from the answer key, or distribute through a secure LMS. Review the reading/examples and organizer before class. No paid textbook or app is required.'),
        ('Student directions', 'Read or work through the material carefully. Support every answer with evidence, work shown, or clear reasoning.'),
    ]:
        y = b.text(h, 48, y, size=11.4, font='Bold', color=TEAL) - 5
        y = b.text(t, 48, y, size=10.3, font=item_font) - 14

    b.page('Before you begin', 'KEY TERMS & CONCEPT PREVIEW')
    y = 680
    y = b.text('Key terms', 48, y, size=12, font='Bold', color=TEAL) - 6
    for term, meaning in row.get('vocab', []):
        y = b.text(term + ' — ' + meaning, 48, y, size=10.6, font=item_font) - 10
    y -= 8
    y = b.text('Concept focus', 48, y, size=12, font='Bold', color=TEAL) - 6
    y = b.text(row['lesson'], 48, y, size=10.8, font=item_font) - 20
    y = b.text('Model 1 — ' + row['models'][0][0], 48, y, size=10.8, font=item_bold) - 5
    y = b.text(row['models'][0][1], 48, y, size=10.5, font=item_font) - 14
    y = b.text('Model 2 — ' + row['models'][1][0], 48, y, size=10.8, font=item_bold) - 5
    y = b.text(row['models'][1][1], 48, y, size=10.5, font=item_font) - 5

    b.questions('Warm-up', warm, per=2, kicker='WARM-UP',
                directions='Answer using what you already know or recall from the previous session.', font=item_font)

    compositions = row.get('compositions')
    for i, (title, body) in enumerate(row['texts']):
        b.page(title, 'ORIGINAL COURSE TEXT', title_font=title_font)
        if compositions:
            b.text(body, 48, 680, size=10.6, leading=15, font=item_font)
            draw_composition(b.c, compositions[i])
        else:
            b.text(body, 48, 680, size=11.6, leading=19, font=item_font)

    b.page('Guided practice · Reasoning organizer', 'GUIDED PRACTICE')
    y = 680
    y = b.text('Work through this organizer together before independent practice.', 48, y, size=10.3, color=GRAY) - 32
    cols = [('Given / Evidence', 'State the given information, quote, or data.'), ('Method / Reasoning', 'Explain the method or reasoning in your own words.'), ('Conclusion', 'State the answer or claim it supports.')]
    colw = 156
    box_top = y
    for i, (h, sub) in enumerate(cols):
        x = 48 + i * (colw + 12)
        b.c.setStrokeColor(__import__('reportlab.lib.colors', fromlist=['HexColor']).HexColor('#A3B3BE'))
        b.c.rect(x, box_top - 210, colw, 210)
        b.text(h, x + 8, box_top - 18, size=10.6, font='Bold', color=TEAL, w=colw - 16)
        b.text(sub, x + 8, box_top - 38, size=8.6, color=GRAY, w=colw - 16)
    y = box_top - 232
    for i, it in enumerate(guided):
        y = b.text(f'{i+1}. ' + it['q'], 48, y, size=10.8, font=item_font) - 4
        b.lines(y - 2, 1, w=516)
        y -= 26

    b.page('Partner / lab discussion', 'PARTNER · LAB DISCUSSION')
    y = 680
    y = b.text('Discuss each item with a partner or lab group before writing a joint response.', 48, y, size=10.3, color=GRAY) - 16
    for i, it in enumerate(partner):
        y = b.text(f'{i+1}. ' + it['q'], 48, y, size=11, font=item_font) - 6
        b.lines(y, 2, w=516)
        y -= 56

    b.questions('Independent practice', indep, per=3, kicker='INDEPENDENT PRACTICE',
                directions='Work independently. Show your work or cite evidence in every answer.', font=item_font)

    b.page('Small-group extension work', 'SMALL-GROUP · APPLICATION')
    y = 680
    y = b.text('Use for review or additional application practice.', 48, y, size=10.3, color=GRAY) - 16
    for i, it in enumerate(interv):
        y = b.text(f'{i+1}. ' + it['q'], 48, y, size=11, font=item_font) - 4
        b.lines(y, 2, w=516)
        y -= 60
    b.page('Small-group extension work', 'SMALL-GROUP · ENRICHMENT')
    y = 680
    y = b.text('Use for learners ready for additional challenge or synthesis.', 48, y, size=10.3, color=GRAY) - 16
    for i, it in enumerate(enrich):
        y = b.text(f'{i+1}. ' + it['q'], 48, y, size=11, font=item_font) - 4
        b.lines(y, 3, w=516)
        y -= 84

    b.questions('Assessment', exit_item, per=1, kicker='ASSESSMENT',
                directions='Complete independently to show what you learned today.', font=item_font)
    b.page('Assessment · self-assessment', 'ASSESSMENT')
    y = 680
    y = b.text('Rate today’s work:', 48, y, size=11.4, font='Bold', color=TEAL) - 10
    for level in ['4 — I can teach this to someone else.', '3 — I can do this independently.', '2 — I can do this with help.', '1 — I need to revisit this before the next session.']:
        y = b.text(level, 48, y, size=10.8) - 14

    all_items = warm + guided + partner + indep + interv + enrich + exit_item
    for offset in range(0, len(all_items), 5):
        b.page('Answer key', 'INSTRUCTOR ANSWER KEY')
        y = 679
        for j, item in enumerate(all_items[offset:offset + 5]):
            y = b.text(str(offset + j + 1) + '. ' + item['answer'], 48, y, size=10.6, font=item_font) - 18
        b.text('Accept equivalent, well-supported alternative answers throughout.', 48, 120, size=9.7, color=GRAY)

    b.page('Access, sources, and license', 'INSTRUCTOR NOTES')
    y = 680
    for label, body in SUPPORTS.items():
        y = b.text(label, 48, y, size=11, font='Bold', color=TEAL) - 4
        y = b.text(body, 48, y, size=10) - 12
    y -= 6
    y = b.text('Course-level alignment · accessed September 18, 2026', 48, y, size=10.6, font='Bold', color=TEAL) - 6
    y = b.text(row['standard'].rstrip('.') + '. The objective is original wording describing a focused part of the course-level goal.', 48, y, size=9.6, font=item_font) - 6
    y = b.text(row['source'], 48, y, size=8.6) - 12
    y = b.text('Original reading(s)/worked examples, questions, and answer explanations. No textbook or copyrighted course material reproduced.', 48, y, size=9.5) - 10
    b.text('Print US Letter at actual size. Keep the answer key separate from student pages. Single-instructor classroom or LMS use; no resale or redistribution of complete files.', 48, y, size=9.5)

    pages = b.finish()
    import fitz
    doc = fitz.open(b.path)
    thumb_path = OUT / (slug + '-thumbnail.png')
    doc[0].get_pixmap(matrix=fitz.Matrix(1.0, 1.0), alpha=False).save(thumb_path)
    preview_page = 5
    preview_path = OUT / (slug + '-preview.png')
    doc[preview_page].get_pixmap(matrix=fitz.Matrix(1.2, 1.2), alpha=False).save(preview_path)
    watermark(preview_path)
    return b.path, thumb_path, preview_path, pages, preview_page + 1


def main(slugs=None):
    from college_content import ROWS
    payload = json.loads((ROOT / 'server/resource-payload.json').read_text())
    lookup = {hashlib.sha256(base64.b64decode(v)).hexdigest(): i for i, v in enumerate(payload['chunks'])}
    sales = json.loads((ROOT / 'data/sales-release-2026-09-15.json').read_text())
    sales_ids = {p['id'] for p in sales}
    expansion = json.loads((ROOT / 'data/catalog-expansion-2026-09-15.json').read_text())
    built = []
    for row in ROWS:
        if slugs and row['id'] not in slugs:
            continue
        pdf_path, thumb_path, preview_path, pages, preview_page = build_one(row)
        pdfname = pack(payload, lookup, pdf_path)
        payload['products'][row['id']] = {'default': pdfname, 'pdf': pdfname}
        import shutil
        shutil.copy(thumb_path, PUB_THUMBS / (row['id'] + '.png'))
        shutil.copy(preview_path, PUB_PREVIEWS / (row['id'] + '.png'))
        entry = {
            'id': row['id'], 'title': row['title'],
            'level': row['course'], 'grades': ['College'], 'states': ['Not applicable'],
            'state': 'Not applicable', 'audience': 'College students and instructors', 'subject': row['subject'],
            'standard': row['standard'], 'objective': row['objective'],
            'resourceType': 'Complete course practice packet',
            'collections': ['College Resources', 'Worksheets', 'Classwork', 'Independent Work', 'Small-Group Work'],
            'formats': ['PDF'], 'distributionFormat': 'PDF', 'pages': pages, 'additionalPdfPages': 0,
            'priceCents': row['price'], 'approved': True,
            'publicationStatus': 'Available for purchase. Full PDF unlocks after verified payment.',
            'description': row['objective'],
            'summary': f'A complete {row["course"]} session packet with an original reading or worked-example set, warm-up, guided practice, partner/lab discussion, independent practice, extension work, assessment, and full answer key.',
            'minutes': row['minutes'],
            'source': row['source'], 'sources': [],
            'tags': [row['course'], row['subject'], 'college', 'worksheets'],
            'thumbnailAlt': f'Cover of {row["title"]}: {row["course"]} course practice packet.',
            'previews': [{'src': '/product-previews/' + row['id'] + '.png', 'page': preview_page, 'alt': f'Sample page from {row["title"]} packet.'}],
            'previewDescription': 'Actual practice pages from the printable packet. Full answer key and all pages are protected and unlock after verified payment.',
            'ready': True,
        }
        if row['id'] not in sales_ids:
            sales.append(entry)
            expansion.append(dict(entry))
        else:
            sales = [entry if p['id'] == row['id'] else p for p in sales]
            expansion = [entry if p['id'] == row['id'] else p for p in expansion]
        built.append((row['id'], pages))
        print(row['id'], pages, 'pages', flush=True)
    (ROOT / 'data/sales-release-2026-09-15.json').write_text(json.dumps(sales, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'data/catalog-expansion-2026-09-15.json').write_text(json.dumps(expansion, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'server/resource-payload.json').write_text(json.dumps(payload, separators=(',', ':')))
    print('Built', len(built), 'packets:', built)


if __name__ == '__main__':
    main(sys.argv[1:] or None)
