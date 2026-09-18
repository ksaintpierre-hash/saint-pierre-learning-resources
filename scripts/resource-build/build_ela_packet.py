"""Build 80-minute Grade 7 NC ELA reading-standard packets: warm-up,
passage, guided practice, partner discussion, independent practice,
small-group work (intervention + enrichment), exit ticket, answer key.
Reuses the site's existing reportlab Book renderer (no LibreOffice
dependency) and the private-payload packing pattern from
prepare_sales_release.py, so output slots directly into
data/sales-release-2026-09-15.json the same way the 120 verified
products already there were built.
"""
import base64, hashlib, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_math import Book, ROOT, TEAL, GRAY, NAVY
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from watermark_previews import watermark

OUT = ROOT / 'resources/2026-09-18'
OUT.mkdir(parents=True, exist_ok=True)
PUB_PREVIEWS = ROOT / 'public/product-previews'
PUB_THUMBS = ROOT / 'public/product-thumbnails'

SUPPORTS = {
    'AIG': 'Ask for a second interpretation, a counterexample, or a student-written item at the same rigor, with an explanation of the choice.',
    '504': 'Follow the individual plan: extended time, breaks, enlarged print, reduced copying, or an alternate response method as documented.',
    'EC': 'Pre-teach key vocabulary before reading. Model the first guided-practice item aloud. Accept oral or dictated responses when appropriate.',
    'ESL': 'Preview key vocabulary with examples. Allow brief home-language discussion before independent writing. Provide sentence starters for open-response items.',
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
    descriptor = f'Grade {row["grade"]} · North Carolina · Reading'
    items = row['items']
    assert len(items) == 20, (slug, len(items))
    warm = items[0:2]
    guided = items[2:6]
    partner = items[6:9]
    indep = items[9:15]
    interv = items[15:17]
    enrich = items[17:19]
    exit_item = items[19:20]

    b = Book(OUT / (slug + '.pdf'), row['title'], descriptor)
    b.cover(code, row['objective'] + ' An 80-minute block-period packet with warm-up, guided practice, partner discussion, independent practice, small-group work, and a full answer key.')

    b.page('Plan the 80-minute block', 'TEACHER GUIDE')
    y = 680
    for h, t in [
        ('Level and alignment', descriptor + '; ' + row['standard']),
        ('What is included', 'Cover; teacher guide; vocabulary and lesson preview; original passage; warm-up (2 items); guided practice with organizer (4 items); partner discussion (3 items); independent practice (6 items); small-group intervention and enrichment (4 items); exit ticket; complete answer key; access and sources page.'),
        ('Suggested pacing (80 minutes)', 'Warm-up 8 min · passage + guided practice 25 min · partner discussion 12 min · independent practice 20 min · small-group work 10 min · exit ticket 5 min.'),
        ('Preparation', 'Print student pages separately from the answer key. Review the passage and organizer before class. No outside novel or paid app required.'),
        ('Student directions', 'Read the passage carefully. Use evidence from the text to support every answer. Quote or closely paraphrase the text and name the paragraph.'),
    ]:
        y = b.text(h, 48, y, size=11.4, font='Bold', color=TEAL) - 5
        y = b.text(t, 48, y, size=10.3) - 14

    b.page('Before you read', 'VOCABULARY & LESSON PREVIEW')
    y = 680
    y = b.text('Key vocabulary', 48, y, size=12, font='Bold', color=TEAL) - 6
    for term, meaning in row.get('vocab', []):
        y = b.text(term + ' — ' + meaning, 48, y, size=10.6) - 10
    y -= 8
    y = b.text('Lesson focus', 48, y, size=12, font='Bold', color=TEAL) - 6
    y = b.text(row['lesson'], 48, y, size=10.8) - 20
    y = b.text('Model 1 — ' + row['models'][0][0], 48, y, size=10.8, font='Bold') - 5
    y = b.text(row['models'][0][1], 48, y, size=10.5) - 14
    y = b.text('Model 2 — ' + row['models'][1][0], 48, y, size=10.8, font='Bold') - 5
    y = b.text(row['models'][1][1], 48, y, size=10.5) - 5

    b.questions('Warm-up · Before you read', warm, per=2, kicker='WARM-UP',
                directions='Answer using what you already know. Five minutes.')

    for title, body in row['texts']:
        b.page(title, 'ORIGINAL STUDENT TEXT')
        b.text(body, 48, 680, size=11.6, leading=17)

    b.page('Guided practice · Evidence organizer', 'GUIDED PRACTICE')
    y = 680
    y = b.text('Work through this organizer together before independent practice.', 48, y, size=10.3, color=GRAY) - 32
    cols = [('It Says', 'Quote or closely paraphrase the text.'), ('It Means', 'Explain the evidence in your own words.'), ('And So', 'State the inference or analysis it supports.')]
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
        y = b.text(f'{i+1}. ' + it['q'], 48, y, size=10.8) - 4
        b.lines(y - 2, 1, w=516)
        y -= 26

    b.page('Partner discussion', 'PARTNER DISCUSSION')
    y = 680
    y = b.text('Discuss each question with a partner before writing a joint response.', 48, y, size=10.3, color=GRAY) - 16
    for i, it in enumerate(partner):
        y = b.text(f'{i+1}. ' + it['q'], 48, y, size=11) - 6
        b.lines(y, 2, w=516)
        y -= 56

    b.questions('Independent practice', indep, per=3, kicker='INDEPENDENT PRACTICE',
                directions='Work independently. Cite evidence from the text in every answer.')

    b.page('Small-group work', 'SMALL-GROUP · INTERVENTION')
    y = 680
    y = b.text('Use with students who need additional support.', 48, y, size=10.3, color=GRAY) - 16
    for i, it in enumerate(interv):
        y = b.text(f'{i+1}. ' + it['q'], 48, y, size=11) - 4
        b.lines(y, 2, w=516)
        y -= 60
    b.page('Small-group work', 'SMALL-GROUP · ENRICHMENT')
    y = 680
    y = b.text('Use with students ready for additional challenge.', 48, y, size=10.3, color=GRAY) - 16
    for i, it in enumerate(enrich):
        y = b.text(f'{i+1}. ' + it['q'], 48, y, size=11) - 4
        b.lines(y, 3, w=516)
        y -= 84

    b.questions('Exit ticket', exit_item, per=1, kicker='EXIT TICKET',
                directions='Answer independently to show what you learned today.')
    b.page('Exit ticket · self-assessment', 'EXIT TICKET')
    y = 680
    y = b.text('Rate today’s work:', 48, y, size=11.4, font='Bold', color=TEAL) - 10
    for level in ['4 — I can teach this to someone else.', '3 — I can do this independently.', '2 — I can do this with help.', '1 — I need to revisit this with my teacher.']:
        y = b.text(level, 48, y, size=10.8) - 14

    all_items = warm + guided + partner + indep + interv + enrich + exit_item
    for offset in range(0, len(all_items), 5):
        b.page('Answer key', 'TEACHER ANSWER KEY')
        y = 679
        for j, item in enumerate(all_items[offset:offset + 5]):
            y = b.text(str(offset + j + 1) + '. ' + item['answer'], 48, y, size=10.6) - 18
        b.text('Accept equivalent, well-supported alternative answers throughout.', 48, 120, size=9.7, color=GRAY)

    b.page('Access, sources, and license', 'TEACHER NOTES')
    y = 680
    for label, body in SUPPORTS.items():
        y = b.text(label, 48, y, size=11, font='Bold', color=TEAL) - 4
        y = b.text(body, 48, y, size=10) - 12
    y -= 6
    y = b.text('Official alignment source · accessed September 18, 2026', 48, y, size=10.6, font='Bold', color=TEAL) - 6
    y = b.text(row['standard'] + '. The objective is original wording describing a focused part of the standard.', 48, y, size=9.6) - 6
    y = b.text(f'NC ELA Standard Course of Study, Grade {row["grade"]}: ' + row['source'], 48, y, size=8.6) - 12
    y = b.text('Original passage(s), questions, and answer explanations. No official released-test items or branded curriculum reproduced.', 48, y, size=9.5) - 10
    b.text('Print US Letter at actual size. Keep the answer key separate from student pages. Single-teacher classroom or LMS use; no resale or redistribution of complete files.', 48, y, size=9.5)

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
    from rl_ri_grade7_content import ROWS as ROWS7
    ROWS = list(ROWS7)
    try:
        from rl_ri_grade8_content import ROWS as ROWS8
        ROWS += ROWS8
    except ImportError:
        pass
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
        grade_label = f'Grade {row["grade"]}'
        entry = {
            'id': row['id'], 'title': row['title'],
            'level': f'{grade_label} • North Carolina', 'grades': [grade_label], 'states': ['North Carolina'],
            'state': 'North Carolina', 'audience': 'Students and educators', 'subject': 'Reading',
            'standard': row['standard'], 'objective': row['objective'],
            'resourceType': 'Complete ELA practice packet',
            'collections': ['Worksheets', 'Classwork', 'Homework', 'Independent Work', 'Small-Group Work', 'Exit Tickets', 'EOG & State Test Prep'],
            'formats': ['PDF'], 'distributionFormat': 'PDF', 'pages': pages, 'additionalPdfPages': 0,
            'priceCents': 699, 'approved': True,
            'publicationStatus': 'Available for purchase. Full PDF unlocks after verified payment.',
            'description': row['objective'],
            'summary': f'An 80-minute {row["standard"].split(" ")[0]} practice packet with an original passage, warm-up, guided practice, partner discussion, independent practice, small-group work, exit ticket, and full answer key.',
            'minutes': '80 minutes (full block period)',
            'source': row['source'], 'sources': [{'title': f'NC ELA Standard Course of Study {grade_label}', 'url': row['source']}],
            'tags': [grade_label, 'North Carolina', row['standard'].split(' ')[0], 'reading', 'worksheets', 'EOG prep', '80 minute'],
            'thumbnailAlt': f'Cover of {row["title"]}: {row["standard"].split(" ")[0]} {grade_label} ELA North Carolina 80-minute worksheet packet.',
            'previews': [{'src': '/product-previews/' + row['id'] + '.png', 'page': preview_page, 'alt': f'Sample page from {row["title"]} worksheet.'}],
            'previewDescription': 'Actual student practice pages from the printable packet. Full answer key and all pages are protected and unlock after verified payment.',
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
