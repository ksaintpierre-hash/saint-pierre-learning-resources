"""Package generic-built PPTX decks (tmp/ela-build/*.pptx) into the same
ZIP format as the existing rl7-* products: PPTX + rendered PDF +
START-HERE license note, with real SHA-256/byte verification wired into
server/ela-upload-manifest.json and data/ela-release.json.
"""
import hashlib, json, subprocess, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / 'tmp/ela-build'
RELEASE_DIR = ROOT / 'resources/ela-release'
PRODUCT_FILES = ROOT / 'product-files'
PREVIEWS = ROOT / 'public/product-previews'
THUMBS = ROOT / 'public/product-thumbnails'
sys.path.insert(0, str(Path(__file__).resolve().parent))

JOBS = [
    ('nc-g7-rl76-character-perspectives', 'rl76-character-perspectives-ppt', 'rl76-character-perspectives', 'Character Perspectives', 'RL.7.6', '7'),
    ('nc-g7-rl77-text-vs-media', 'rl77-text-vs-media-ppt', 'rl77-text-vs-media', 'Text vs. Media', 'RL.7.7', '7'),
    ('nc-g7-rl79-fiction-vs-history', 'rl79-fiction-vs-history-ppt', 'rl79-fiction-vs-history', 'Fiction vs. History', 'RL.7.9', '7'),
    ('nc-g7-ri71-evidence-informational', 'ri71-evidence-informational-ppt', 'ri71-evidence-informational', 'Evidence in Informational Text', 'RI.7.1', '7'),
    ('nc-g7-ri72-central-ideas-summary', 'ri72-central-ideas-summary-ppt', 'ri72-central-ideas-summary', 'Central Ideas and Summary', 'RI.7.2', '7'),
    ('nc-g7-ri73-interactions-informational', 'ri73-interactions-informational-ppt', 'ri73-interactions-informational', 'Interactions in Informational Text', 'RI.7.3', '7'),
    ('nc-g7-ri74-word-meaning-tone', 'ri74-word-meaning-tone-ppt', 'ri74-word-meaning-tone', 'Word Meaning and Tone in Informational Text', 'RI.7.4', '7'),
    ('nc-g7-ri75-text-structure', 'ri75-text-structure-ppt', 'ri75-text-structure', 'Text Structure in Informational Text', 'RI.7.5', '7'),
    ('nc-g7-ri76-point-of-view-purpose', 'ri76-point-of-view-purpose-ppt', 'ri76-point-of-view-purpose', "Author's Point of View and Purpose", 'RI.7.6', '7'),
    ('nc-g7-ri77-text-vs-multimedia', 'ri77-text-vs-multimedia-ppt', 'ri77-text-vs-multimedia', 'Text vs. Multimedia', 'RI.7.7', '7'),
    ('nc-g7-ri78-tracing-arguments', 'ri78-tracing-arguments-ppt', 'ri78-tracing-arguments', 'Tracing and Evaluating Arguments', 'RI.7.8', '7'),
    ('nc-g8-rl81-textual-evidence', 'rl81-textual-evidence-ppt', 'rl81-textual-evidence', 'Evidence and Inference Lab', 'RL.8.1', '8'),
    ('nc-g8-ri81-evidence-informational', 'ri81-evidence-informational-ppt', 'ri81-evidence-informational', 'Strongest Evidence Workshop', 'RI.8.1', '8'),
    ('nc-g8-rl82-theme-central-idea', 'rl82-theme-central-idea-ppt', 'rl82-theme-central-idea', 'Theme Through the Wreckage', 'RL.8.2', '8'),
    ('nc-g8-ri82-central-ideas-summary', 'ri82-central-ideas-summary-ppt', 'ri82-central-ideas-summary', 'Tracing the Central Idea', 'RI.8.2', '8'),
]


def sha256_bytes(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def main():
    import fitz
    manifest_path = ROOT / 'server/ela-upload-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    release_path = ROOT / 'data/ela-release.json'
    release = json.loads(release_path.read_text())
    release_ids = {p['id'] for p in release}

    for content_id, ppt_stem, product_id, title, code, grade in JOBS:
        pptx_path = BUILD / (ppt_stem + '.pptx')
        pdf_path = BUILD / (product_id + '.pdf')
        subprocess.run([sys.executable, str(ROOT / 'scripts/pptx_to_pdf.py'),
                         str(pptx_path), str(pdf_path)], check=True)
        doc = fitz.open(str(pdf_path))
        n_slides = len(doc)
        doc[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(str(THUMBS / (product_id + '.png')))
        preview_page = min(6, n_slides - 1)
        doc[preview_page].get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(str(PREVIEWS / (product_id + '.png')))

        start_here = BUILD / ('START-HERE-' + product_id + '.txt')
        start_here.write_text(
            f'SAINT PIERRE LEARNING RESOURCES\n{title} — Grade {grade} ELA ({code})\n\n'
            f'Includes the original editable PowerPoint and a PDF of all {n_slides} slides.\n'
            'Use the PDF when sharing across devices to preserve layout. In PowerPoint, preview after editing or changing fonts.\n'
            'Single-teacher license: one purchaser may use with their own students, including in a password-protected classroom. Do not resell, publicly post, or redistribute the source files.\n\n'
            'TEACHING NOTES\n'
            'Read the passage aloud or have students read independently before the guided-practice questions.\n'
            'Work through guided practice together, then release students to partner discussion and independent practice.\n'
            'Small-group intervention and enrichment questions let you differentiate; the answer key covers all items with reasoning.\n'
        )

        zip_path = BUILD / (product_id + '.zip')
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=0) as zf:
            zf.write(pptx_path, product_id + '.pptx')
            zf.write(pdf_path, product_id + '.pdf')
            zf.write(start_here, 'START-HERE.txt')

        for dest_dir in (RELEASE_DIR, PRODUCT_FILES):
            (dest_dir / (product_id + '.zip')).write_bytes(zip_path.read_bytes())

        n_bytes, digest = sha256_bytes(zip_path)
        manifest[product_id] = {'name': product_id + '.zip', 'bytes': n_bytes, 'sha256': digest}

        entry = {
            'id': product_id, 'title': title, 'level': f'Grade {grade}', 'subject': 'Reading',
            'standard': 'CCSS.ELA-LITERACY.' + code,
            'source': f'Common Core State Standards: https://www.thecorestandards.org/ELA-Literacy/{code.split(".")[0]}/{grade}/',
            'description': f'A complete {code} lesson: passage, warm-up, guided practice, partner discussion, independent practice, small-group work, exit ticket, and full answer key.',
            'priceCents': 699, 'pages': n_slides, 'slides': n_slides, 'approved': True,
            'formats': ['PDF', 'PPTX'], 'distributionFormat': 'ZIP',
            'resourceType': 'Editable lesson slides and task cards',
            'minutes': '45–90 minutes; split across lessons as needed',
            'included': [f'{n_slides}-slide editable PowerPoint', f'{n_slides}-page PDF of the slides',
                         'Original passage(s) and guided/independent practice', 'Answer explanations and exit ticket',
                         'START-HERE teaching notes and single-teacher license'],
            'collections': [f'Grade {grade} ELA', 'Reading Literature' if code.startswith('RL') else 'Reading Informational Text'],
            'audience': f'Grade {grade} teachers and tutors',
            'answerKey': 'Answer explanations are included after task cards; read START-HERE for teaching clarifications.',
            'previewDescription': 'An actual passage or practice slide from this lesson. The complete PDF and editable PowerPoint are delivered together in a ZIP after purchase.',
            'previews': [{'src': '/product-previews/' + product_id + '.png', 'alt': f'Sample slide from {title}', 'page': preview_page + 1}],
        }
        if product_id in release_ids:
            release = [entry if p['id'] == product_id else p for p in release]
        else:
            release.append(entry)
            release_ids.add(product_id)
        print(content_id, '->', product_id, n_slides, 'slides,', n_bytes, 'bytes', flush=True)

    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    release_path.write_text(json.dumps(release, ensure_ascii=False, indent=2) + '\n')
    print('Packaged', len(JOBS), 'PPTX products.')


if __name__ == '__main__':
    main()
