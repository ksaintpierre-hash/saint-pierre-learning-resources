"""Generic PPTX builder: turns a rl_ri_grade7_content.py ROW into a full
lesson deck using ela_deck.Deck, reusing the same 20-item pedagogical
breakdown as the PDF worksheets (warm-up / guided / partner / independent
/ small-group / exit) so both product lines share one source of content.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ela_deck import Deck

OUT = Path(__file__).resolve().parents[2] / 'tmp/ela-build'
OUT.mkdir(parents=True, exist_ok=True)


def chunk_text(body, max_chars=1450):
    paras = [p for p in body.split('\n\n')]
    chunks, cur, cur_len = [], [], 0
    for p in paras:
        if cur and cur_len + len(p) > max_chars:
            chunks.append(cur)
            cur, cur_len = [], 0
        cur.append(p)
        cur_len += len(p)
    if cur:
        chunks.append(cur)
    return chunks


def build(row, ppt_id, title_suffix=''):
    code = row['standard'].split(' — ')[0]
    d = Deck(code, row['title'])

    d.cover(f'GRADE 7  ·  READING {"LITERATURE" if code.startswith("RL") else "INFORMATIONAL TEXT"}  ·  {code}',
            row['title'], row['objective'],
            'Lesson Map  ·  Passage  ·  Guided · Partner · Independent Practice  ·  Small Group  ·  Answer Key')

    items = row['items']
    warm, guided, partner, indep, interv, enrich, exitq = (
        items[0:2], items[2:6], items[6:9], items[9:15], items[15:17], items[17:19], items[19:20])

    d.two_box('LESSON MAP', 'What You Will Learn Today',
              'Learning Goals',
              ['Understand ' + code + ': ' + row['objective'][:70] + ('...' if len(row['objective']) > 70 else ''),
               'Read an original passage closely',
               'Support every answer with text evidence',
               'Work through guided, partner, and independent practice'],
              'How the Lesson Runs',
              ['Warm-up and passage', 'Guided practice together', 'Partner discussion',
               'Independent + small-group work', 'Exit ticket and answer key'])

    d.guide_note('GUIDE NOTE', 'Unpacking the Standard', [row['lesson']])

    d.guide_note('WE DO TOGETHER', 'Modeled Example',
                  [row['models'][0][0], row['models'][0][1], '', row['models'][1][0], row['models'][1][1]])

    for ti, (ttitle, tbody) in enumerate(row['texts']):
        chunks = chunk_text(tbody)
        short_title = ttitle if len(ttitle) <= 44 else ttitle.split(' (')[0].split(': ', 1)[-1]
        for ci, chunk in enumerate(chunks):
            part = f' · PART {ci+1}' if len(chunks) > 1 else ''
            kicker = f'PASSAGE {chr(65+ti)}{part}' if len(row['texts']) > 1 else f'PASSAGE{part}'
            heading = short_title if ci == 0 else short_title + ', continued'
            d.passage(kicker, heading, chunk, size=11.5, space_after=10)

    d.open_questions('WARM-UP', 'Warm-up · Before You Read', warm, start=1)
    for offset in range(0, len(guided), 2):
        d.open_questions('GUIDED PRACTICE', 'Guided Practice', guided[offset:offset+2], start=3+offset)
    for offset in range(0, len(partner), 2):
        d.open_questions('PARTNER DISCUSSION', 'Partner Discussion', partner[offset:offset+2], start=7+offset)
    for offset in range(0, len(indep), 2):
        d.open_questions('INDEPENDENT PRACTICE', 'Independent Practice', indep[offset:offset+2], start=10+offset)
    d.open_questions('SMALL-GROUP · INTERVENTION', 'Small-Group Work', interv, start=16)
    d.open_questions('SMALL-GROUP · ENRICHMENT', 'Small-Group Work', enrich, start=18)
    d.open_questions('EXIT TICKET', 'Exit Ticket', exitq, start=20)

    all_items = warm + guided + partner + indep + interv + enrich + exitq
    for offset in range(0, len(all_items), 5):
        d.open_answer_key('TEACHER PAGE', f'Answer Key ({offset//5+1} of {(len(all_items)+4)//5})',
                            all_items[offset:offset+5], start=offset+1)

    d.exit_ticket('Answer on a sticky note',
                  ['Answer the exit-ticket question from today’s lesson.',
                   'Cite at least one piece of evidence from the passage.'],
                  'Remember',
                  ['Name your claim or answer', 'Quote or cite the evidence', 'Explain how it supports your answer'])

    out_path = OUT / (ppt_id + '.pptx')
    n = d.save(str(out_path))
    return out_path, n


if __name__ == '__main__':
    from rl_ri_grade7_content import ROWS
    ids = sys.argv[1:]
    rows_by_id = {r['id']: r for r in ROWS}
    for pid in ids:
        row = rows_by_id[pid]
        ppt_id = row['id'].replace('nc-g7-', '') + '-ppt'
        path, n = build(row, ppt_id)
        print(row['id'], '->', path, n, 'slides', flush=True)
