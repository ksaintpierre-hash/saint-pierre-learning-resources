"""Publish metadata and samples only; full resources remain in the server payload."""
from pathlib import Path
import sys,json,base64,hashlib,re
import fitz
ROOT=Path(__file__).resolve().parents[1]
payload=json.loads((ROOT/'server/resource-payload.json').read_text())
lookup={hashlib.sha256(base64.b64decode(s)).hexdigest():i for i,s in enumerate(payload['chunks'])}
def intern(b):
 h=hashlib.sha256(b).hexdigest()
 if h not in lookup:lookup[h]=len(payload['chunks']);payload['chunks'].append(base64.b64encode(b).decode())
 return lookup[h]
def pack(path):
 raw=path.read_bytes();parts=[];pos=0
 for m in re.finditer(rb'\bstream\r?\n(.*?)endstream',raw,re.S):parts.extend([raw[pos:m.start(1)],m.group(1)]);pos=m.end(1)
 parts.append(raw[pos:]);ids=[intern(b) for b in parts if b]
 assert b''.join(base64.b64decode(payload['chunks'][i]) for i in ids)==raw
 payload['files'][path.name]={'chunks':ids,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'contentType':'application/pdf'}
 payload['products'][path.stem]={'default':path.name,'pdf':path.name}
def samples(id,path,pages):
 d=fitz.open(path);d[0].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(ROOT/'public/product-thumbnails'/f'{id}.png')
 previews=[]
 for n,pg in enumerate(pages):
  name=id+('' if n==0 else '-'+str(n+1))+'.png';d[pg-1].get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False).save(ROOT/'public/product-previews'/name)
  previews.append({'src':'/product-previews/'+name,'page':pg,'alt':f'Actual student practice page {pg}; sample from {id.replace("-"," ")}.'})
 return len(d),previews
release=json.loads((ROOT/'data/catalog-expansion-2026-09-15.json').read_text())
for p in release:p['publicationStatus']='Available for purchase. Full files unlock after verified payment.'
daily=json.loads((ROOT/'server/daily-drafts-2026-09-15.json').read_text())
for original in daily:
 p={k:v for k,v in original.items() if k not in ['pdf','thumbnail','thumbnailFile','files','researchNotes','previewPages','ready']}
 p.update(approved=True,status='published',publicationStatus='Available for purchase. Full PDF unlocks after verified payment.',description=p['summary'],accessibility=p['differentiation'],digitalNotes=p['digitalUse'],originality=p['originalContent'],distributionFormat='PDF',source='; '.join(s['url'] for s in p['sources']),thumbnailAlt=f'KSP-branded cover of {p["title"]}.')
 p['included']=[s for s in p['included'] if 'storefront thumbnail' not in s]
 p['collections']=['Classwork','Independent Work','Small-Group Work','Exit Tickets','Worksheets']
 p['pages'],p['previews']=samples(p['id'],ROOT/original['pdf'],original['previewPages'])
 release.append(p)
old=json.loads((ROOT/'resources/released-2026-09-15/metadata.json').read_text())
for d in old:
 id=d['slug'];path=ROOT/'resources/released-2026-09-15'/f'{id}.pdf';pack(path);pages,previews=samples(id,path,[3,4])
 college=d['level'].startswith('College');state='State-neutral' if college else d['state'];collections=['Classwork','Independent Work','Worksheets','Exit Tickets']
 if 'cards' in d['rtype'].lower():collections.append('Task Cards')
 if d['rtype']=='Warm-Ups':collections.append('Warm-Ups')
 if d['rtype']=='Small-Group Work':collections.append('Small-Group Work')
 if d['rtype']=='Homework':collections.append('Homework')
 release.append(dict(id=id,title=d['title'],level=d['level'],grades=['College'] if college else [d['level']],states=[] if college else [state],state=state,subject=d['subject'],standard=d['standard'],objective=d['focus'],resourceType=d['rtype'],collections=collections,approved=True,status='published',publicationStatus='Available for purchase. Full PDF unlocks after verified payment.',distributionFormat='PDF',formats=['PDF'],pages=pages,slides=0,priceCents=round(float(d['price'].strip('$'))*100),minutes=d['time'],description=d['focus'],summary=d['focus'],detailedDescription='A focused practice and reflection resource with teacher guidance, a model prompt, four pages of bordered practice cards, a reflection ticket, and answer guidance. '+d['focus'],included=[f'{pages}-page printable PDF','Teacher guide and first-prompt model','16 bordered practice prompts across four pages','Five-question reflection exit ticket','Teacher answer guidance and local reflection criteria','Differentiation, sources, and single-teacher license'],source=d['source'],studentDirections='Show work or explain each response. Use extra paper for extended responses.',teacherUse='Model first; assign one four-prompt block at a time. Keep the key separate.',answerKey='Answers and criteria for the sixteen prompts and reflection ticket.',accessibility={'AIG':'Use a second method or transfer example.','504':'Follow the learner’s plan for time, breaks, format, and copying.','EC':'Model steps and accept aligned response modes.','ESL':'Preview vocabulary, use bilingual references, and rehearse.'},preparation='Print practice separately from keys. Provide extra paper. '+('Qualified prior live or video signing instruction is required; no sign illustrations or videos are included.' if 'asl101' in id else ''),digitalNotes='US Letter, actual size. Optional annotation in a restricted LMS; not a fillable PDF.',license='Single-teacher use with their own learners. No resale, redistribution, or public posting.',originality='Original prompts and explanations; no released exam questions or third-party curriculum reproduced.',tags=[d['subject'],d['level'],d['rtype'],'answer guidance','printable'],thumbnailAlt=f'KSP-branded cover of {d["title"]}.',previews=previews))
assert len(release)==120 and len({p['id'] for p in release})==120
for p in release:
 name=payload['products'][p['id']]['default'];f=payload['files'][name];b=b''.join(base64.b64decode(payload['chunks'][i]) for i in f['chunks'])
 assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
(ROOT/'data/sales-release-2026-09-15.json').write_text(json.dumps(release,ensure_ascii=False,indent=2))
(ROOT/'server/resource-payload.json').write_text(json.dumps(payload,separators=(',',':')))
print('Prepared 120 approved release listings with verified private files and public samples.')
