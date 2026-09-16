"""Render and losslessly package the original twenty-product private daily batch."""
import base64,gzip,hashlib,json,re,textwrap
from pathlib import Path
import fitz
from PIL import Image,ImageDraw
from daily_literacy_content import ROWS,NC,DE
from build_math import Book,ROOT,TEAL,GRAY

OUT=ROOT/'resources/private-drafts/2026-09-15';OUT.mkdir(parents=True,exist_ok=True)
QA=ROOT/'tmp/daily-literacy-qa';QA.mkdir(parents=True,exist_ok=True)
DATE='2026-09-15'
def supports(p):
 early=p.get('early',False)
 return {
 'AIG':('Ask the learner to invent a new rhyme pair or retell from another character’s view; explain the choice.' if early else 'Ask for a counterexample, an alternative supported interpretation, or a newly written item with an explanation. Add depth rather than speed.'),
 '504':'Follow the individual plan: breaks, enlarged print, extra time, reduced copying, or an alternative response method as documented. These are classroom options, not a statement of permitted test accommodations.',
 'EC':('Read all directions and stories aloud; model one response; use gestures, pictures drawn by the learner, or AAC. Record exact responses without demanding writing.' if early else 'Follow the IEP; show one task at a time, model the first decision, and permit dictated reasoning when appropriate. For decoding practice, distinguish an adult-read direction from an adult-read target word.'),
 'ESL':('Explain word meanings with gestures before rhyme listening. Invite home-language retelling first; compare the target English sounds without judging accent.' if early else 'Preview task verbs and key vocabulary, allow home-language planning, and offer “My answer is ___ because ___.” Evaluate the targeted skill separately from unrelated language errors. For French, retain the target French sentence while explaining directions in a familiar language.')}

def sources(p):
 s=[{'title':'Official state standard' if p['state'] else 'University teaching reference','url':p['source'],'accessed':DATE}]
 s += [{'title':'State-linked standard text','url':u,'accessed':DATE} for u in p.get('extraSources',[])]
 if p['state']=='North Carolina':
  s.append({'title':'NCDPI EOG released reading form (structure review only)','url':f'https://www.dpi.nc.gov/documents/accountability/testing/eog/eog-reading-grade-{p["grade"]}-released-form/open','accessed':DATE})
  s.append({'title':'NCDPI ELA implementation schedule','url':'https://www.dpi.nc.gov/districts-schools/classroom-resources/office-teaching-and-learning/standard-course-study/english-language-arts/standard-course-study-supporting-resources','accessed':DATE})
 elif p['state']=='Delaware':s.append({'title':'DDOE assessment overview','url':DE.replace('/standards/','/assessments/'),'accessed':DATE})
 return s

payload_path=ROOT/'server/resource-payload.json'
payload=json.loads(payload_path.read_text());pool=payload['chunks']
lookup={hashlib.sha256(base64.b64decode(b)).hexdigest():i for i,b in enumerate(pool)}
def intern(b):
 h=hashlib.sha256(b).hexdigest()
 if h not in lookup:lookup[h]=len(pool);pool.append(base64.b64encode(b).decode())
 return lookup[h]
def pack(path):
 raw=path.read_bytes();parts=[];pos=0
 if path.suffix=='.pdf':
  for m in re.finditer(rb'\bstream\r?\n(.*?)endstream',raw,re.S):parts.extend([raw[pos:m.start(1)],m.group(1)]);pos=m.end(1)
 parts.append(raw[pos:]);ids=[intern(b) for b in parts if b]
 assert b''.join(base64.b64decode(pool[i]) for i in ids)==raw
 payload['files'][path.name]={'chunks':ids,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'contentType':'application/pdf' if path.suffix=='.pdf' else 'image/png'}
 return path.name

metadata=[]
for p in ROWS:
 level=p['grade'] if p['grade'] in ['Pre-K','Kindergarten','College'] else 'Grade '+p['grade']
 descriptor=' • '.join(x for x in [level,p['state'],p['subject']] if x)
 b=Book(OUT/(p['id']+'.pdf'),p['title'],descriptor)
 b.cover(p['standard'],p['objective']+' Includes 16 practice tasks, a four-task exit check, two explained models, and complete answer guidance.')
 b.page('Plan a focused lesson','TEACHER GUIDE');y=680
 duration='Four 8–12-minute supported sessions and a 5-minute oral check.' if p.get('early') else 'Two 30–40-minute sessions plus a 10–15-minute exit check; extended writing or speech rehearsal may take longer.'
 direction='Listen to the adult, then speak, point, draw, or act your response. Ask to hear the words or story again.' if p.get('early') else 'Read the lesson and supplied text or reference. Attempt each task before viewing the key. Explain when asked. Use separate paper for full drafts or longer answers; the PDF is not a fillable form.'
 for h,t in [('Level and alignment',descriptor+'; '+p['standard']+'. Focus: '+p['objective']),('What is included',f'One cover; one teacher guide; one mini-lesson with two explained models; {len(p["texts"])} original text/reference section(s); 16 practice tasks on four pages; one four-task exit check; four answer-key pages covering all 20 tasks; two access/source/license pages. Student texts are original, not extracted from released tests.'),('Time and sequence',duration+' Model first; use tasks 1–4 to check readiness; practice the remainder in short groups; give tasks 17–20 without the key.'),('Preparation','Print student pages separately from teacher pages. Provide pencils and extra paper; oral-response learners need an adult recorder. Review word meanings and prerequisite decoding or sentence skills. No paid app, novel, or external reading is required.'),('Student directions',direction)]:
  y=b.text(h,48,y,size=11.4,font='Bold',color=TEAL)-5;y=b.text(t,48,y,size=10.5)-15
 b.page('Learn the move','MINI-LESSON • TWO MODELS');y=b.text(p['lesson'],48,678,size=12)-24
 for i,(q,a) in enumerate(p['models']):
  y=b.text(f'Model {i+1} • '+q,48,y,size=12,font='Bold',color=TEAL)-8;y=b.text(a,48,y,size=11.5)-26
 b.text('Try the task first. Then compare the reasoning, not just the final word.',48,135,size=10.5,color=GRAY)
 for title,body in p['texts']:
  b.page(title,'ORIGINAL STUDENT TEXT / REFERENCE');b.text(body,48,680,size=12.2,leading=18)
 start=b.n+1
 b.questions('Practice • Read, reason, respond',p['items'][:16],per=4,directions=direction)
 b.questions('Exit check • Apply the skill',p['items'][16:],start=17,per=4,directions=('Adult reads prompts; record independent responses with the usual access supports.' if p.get('early') else 'Try without the answer key. Show evidence or reasoning when asked. Use separate paper for longer responses.'))
 for offset in range(0,20,5):
  b.page('Answers and response criteria','TEACHER ANSWER KEY');y=679
  for j,item in enumerate(p['items'][offset:offset+5]):
   y=b.text(str(offset+j+1)+'. '+item['answer'],48,y,size=11.2)-20
  b.text('Accept equivalent correct answers and well-supported interpretations. Sample writing is guidance, not a required script.',48,120,size=10,color=GRAY)
 b.page('Access and next teaching steps','TEACHER GUIDE');y=679
 for label,body in supports(p).items():
  y=b.text(label,48,y,size=11.5,font='Bold',color=TEAL)-5;y=b.text(body,48,y,size=11)-15
 rubric='For each exit task, record 2 = accurate and complete for the stated prompt; 1 = partly accurate or missing a requested explanation; 0 = not yet demonstrated. Total 0–8 is a local teaching note, not a standardized score. For oral tasks do not penalize spelling or handwriting. Revisit the exact type of error rather than assigning a diagnostic label.'
 y=b.text('Use the exit evidence',48,y,size=11.5,font='Bold',color=TEAL)-5;y=b.text(rubric,48,y,size=10.5)-15
 b.text('Next lesson: model one missed decision, let the learner try a new example, and compare the explanation. Extend only after the learner can explain the targeted skill.',48,y,size=10.5)
 b.page('Alignment, sources, and license','TEACHER NOTES');y=680
 note='The objective is original wording describing a focused part of the cited standard; this is not a full curriculum or official practice test.'
 if p['state']=='Massachusetts' and p['grade']=='Pre-K':note+=' The source prints Pre-K Reading Foundations, standard 2, subsection a (PDF page 30); this reference preserves that structure rather than inventing a compact code.'
 if p['state']=='Maryland' and p['grade']=='3':note+=' The revised Grade 3 Language document labels this skill L1.a; the grade is supplied separately, as in the source.'
 if p['state']=='North Carolina':note+=' NCDPI states the 2017 ELA standards apply in 2026–27; the 2026 revision begins in 2027–28. Released-form review informed text-dependent item design only.'
 if p['state']=='Ohio':note+=' Uses the current 2026 revised standard; no claim is made that existing released tests have been updated to this revision.'
 if p['grade']=='College':note='Introductory college course-level skill practice; no accreditation, guaranteed transfer, credential, or universal course equivalency is claimed.'
 y=b.text(note,48,y,size=10.5)-18
 for s in sources(p):
  y=b.text(s['title']+' • accessed September 15, 2026',48,y,size=9.5,font='Bold',color=TEAL)-4;y=b.text(s['url'],48,y,size=8.5,leading=11.5)-13
 if p['state'] not in ['North Carolina','Delaware',''] and not (p.get('early') or p['grade'] in ['1','2']):
  y=b.text('Research limit: official released-assessment retrieval was unsuccessful in this run. This packet is standards-focused classroom instruction; it makes no released-test alignment, timing, or scoring claim.',48,y,size=9.7)-13
 y=b.text('Print US Letter at actual size. Text is selectable; enlarging or digital annotation is optional. This is not a tagged-accessibility-certified or fillable PDF. Keep teacher keys separate. No certified Lexile score is claimed.',48,y,size=9.7)-13
 y=b.text('Single-teacher license: the purchaser may make copies for their own students and use the file in a restricted class LMS. No resale, public posting, sharing of complete files, or redistribution. Original passages, questions, and teaching explanations; official standards and reference sources retain their owners’ rights. No agency endorsement. Official store logo reused unchanged.',48,y,size=9.7)-13
 b.text('PRIVATE DRAFT • Not approved for sale or customer distribution. © 2026 Saint Pierre Learning Resources.',48,y,size=9.7,font='Bold',color=TEAL)
 pages=b.finish();doc=fitz.open(b.path)
 thumb=OUT/(p['id']+'-thumbnail.png');doc[0].get_pixmap(matrix=fitz.Matrix(.45,.45),alpha=False).save(thumb)
 pdfname=pack(b.path);thumbname=pack(thumb);payload['products'][p['id']]={'default':pdfname,'pdf':pdfname,'thumbnail':thumbname}
 # Render every page, then build a per-product contact sheet for visual inspection.
 sheet=Image.new('RGB',(5*245,((pages+4)//5)*330),'#dce2e6');draw=ImageDraw.Draw(sheet)
 for i,page in enumerate(doc):
  pix=page.get_pixmap(matrix=fitz.Matrix(.38,.38),alpha=False);img=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
  sheet.paste(img,((i%5)*245,(i//5)*330));draw.text(((i%5)*245+8,(i//5)*330+305),f'{i+1}',fill='black')
  text=page.get_text();assert 'Saint Pierre Learning Resources' in text
  for word in page.get_text('words'):
   assert word[0]>=-1 and word[1]>=-1 and word[2]<=613 and word[3]<=793,(p['id'],i,word)
 sheet.save(QA/(p['id']+'.jpg'),quality=85)
 m={k:p[k] for k in ['id','title','state','grade','subject','standard','objective','resourceType']}
 m.update(level=level,grades=[level],states=[p['state']] if p['state'] else [],collections=[p['resourceType']],approved=False,ready=False,status='private_draft',publicationStatus='Private draft — awaiting Katia’s publication approval; not for sale.',priceCents=p.get('price',500),pages=pages,slides=0,formats=['PDF'],files=[{'format':'PDF','name':pdfname,'pages':pages,'sha256':payload['files'][pdfname]['sha256']}],thumbnailFile=thumbname,thumbnailAlt=f'Official KSP Haitian-flag book logo above {p["title"]}; {descriptor}; private draft cover.',summary=p['objective']+' Includes models, practice, exit check, and answer guidance.',detailedDescription=f'{p["title"]} gives {level} learners a focused route from explicit modeling to supported practice and independent application. '+p['lesson'],included=[f'1 print-ready {pages}-page PDF', '1 professional branded cover','1 teacher-use guide','1 mini-lesson with 2 explained models',f'{len(p["texts"])} original text/reference section(s): '+ '; '.join(t[0] for t in p['texts']),'16 original practice tasks across 4 pages','1 four-task exit check','4 teacher answer-key pages covering all 20 tasks','1 differentiation and local scoring page','1 sources, printing, and license page','1 storefront thumbnail (PNG)'],minutes=duration,studentDirections=direction,teacherUse='Model the two examples; use tasks 1–4 as a readiness check. Assign four tasks per practice block, then use the independent exit responses to select a specific reteaching move. For extended writing, supply separate paper. Keep answer pages separate.',answerKey='Answers or explicit acceptable-response criteria for all 20 tasks; two explained models; local 0–2-per-task exit rubric. Open-ended answers allow justified alternatives.',differentiation=supports(p),preparation='Print the selected pages; provide pencil and extra paper. Read the teacher guide and prerequisite vocabulary. Adult facilitation is required for Pre-K/Kindergarten. No outside novel, paid app, or external passage required.',printing='US Letter, actual size; print student pages separately from keys. Color branding remains legible in grayscale.',digitalUse='Selectable-text PDF for viewing or optional annotation; not a fillable form or certified tagged PDF. Use only a restricted classroom LMS.',license='Single teacher and their own students; private classroom/LMS use. No resale, public redistribution, or sharing of complete files.',originalContent='All student passages, practice tasks, model explanations, and answer guidance are original. No released questions or branded curriculum copied. Official logo reused unchanged.',sources=sources(p),researchNotes=note,tags=[level,p['state'] or 'college',p['subject'],p['resourceType'],p['standard'],'answer key','printable'],pdf=str(b.path.relative_to(ROOT)),thumbnail=str(thumb.relative_to(ROOT)),previewPages=[start,start+1])
 metadata.append(m);print(p['id'],pages,flush=True)

(ROOT/'server/daily-drafts-2026-09-15.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
payload_path.write_text(json.dumps(payload,separators=(',',':')))
tracker_path=ROOT/'data/product-tracker.json';tracker=json.loads(tracker_path.read_text());existing=tracker['completed']
existing=[p for p in existing if not str(p.get('id','')).startswith('daily-20260915-')]
assert not ({p['title'] for p in existing}&{p['title'] for p in metadata})
for p in metadata:existing.append({k:p[k] for k in ['id','title','state','grade','subject','standard','objective','resourceType','formats','status'] }|{'date':DATE})
tracker['completed']=existing;tracker['last_updated']=DATE
allstates='Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming'.split('|')
counts={s:sum(p.get('state')==s for p in existing) for s in allstates}
tracker['stateCoverageCounts']=counts
tracker['rotationNote']='Count only specifically aligned state products; nationwide teacher tools do not count as completed academic coverage for all states or grades. September 15 daily batch adds 18 K–8/Pre-K literacy resources across 9 states and 2 college resources, including 8 newly represented states. Next prioritize zero-count states, science/social studies/CTE/languages, and unrepresented high-school academic levels. Previous same-day 90-product expansion is a separate batch.'
tracker_path.write_text(json.dumps(tracker,ensure_ascii=False,indent=2))
stats={'date':DATE,'products':20,'pages':sum(p['pages'] for p in metadata),'practiceTasks':320,'exitTasks':80,'models':40,'thumbnails':20,'states':sorted({p['state'] for p in metadata if p['state']}),'newStateCoverage':8,'payloadGzipBytes':len(gzip.compress(payload_path.read_bytes())),'fileChecks':{p['id']:p['files'][0]['sha256'] for p in metadata}}
(ROOT/'docs/daily-review-2026-09-15.json').write_text(json.dumps(stats,indent=2))
lines=['# Daily review — September 15, 2026','','Twenty new private draft listings. Checkout disabled; no payment made. These are additional to the earlier 90-resource expansion, not recycled listings.','','| Title / PDF | Level | State | Standard or objective | Type | Price | Pages |','|---|---|---|---|---|---:|---:|']
for p in metadata:lines.append(f'| [{p["title"]}](sandbox:{ROOT/p["pdf"]}) | {p["level"]} | {p["state"] or "Not state-specific"} | {p["standard"] if p["state"] else p["objective"]} | {p["resourceType"]} | ${p["priceCents"]/100:.2f} | {p["pages"]} |')
lines+=['','## Included and checked','',f'{stats["pages"]} print-ready pages; 320 practice tasks, 80 exit tasks, 40 explained models, and 20 thumbnails. Every task has an answer or explicit response criteria. Every PDF page carries the official logo and copyright footer. All pages rendered; text bounds checked. Suggested prices are not active purchase offers.','', '## Rotation','',tracker['rotationNote'],'','## Research limits and safeguards','','North Carolina Grade 7 and Grade 8 released EOG reading forms were consulted for structure and skill demand only. Delaware’s official assessment overview was consulted. Some Michigan, Maryland, Connecticut, Ohio, and New Jersey released/practice-test endpoints could not be retrieved; affected resources claim verified standards-focused instruction, not verified assessment alignment. Pre-K and early-grade products do not claim state-test simulation. No copyrighted test material was copied.','', 'Massachusetts Pre-K reference preserves the source’s section/number/subsection notation. Maryland Grade 3 uses the revised source’s L1.a label. Connecticut uses the state sheet’s 4.RL.1 / 4.W.1 notation. Ohio uses the 2026 revision; North Carolina uses the 2017 standards still applicable in 2026–27. College packets make no accreditation or equivalency claim.','','This batch contains PDFs, not slide presentations; no PPTX files or slide counts are promised. PDFs are selectable-text but are not certified tagged-accessible or fillable files.','', '## Official sources consulted','']
seen=set()
for p in metadata:
 for s in p['sources']:
  if s['url'] not in seen:lines.append(f'- [{s["title"]} — {p["state"] or p["subject"]}]({s["url"]}) — accessed September 15, 2026.');seen.add(s['url'])
lines+=['','## Daily Learning Hub','', 'News: NCDPI’s September 14, 2026 announcement of a $3,990,756 grant to expand Skills for the Future. The news summary distinguishes planned participation from demonstrated outcomes.','', 'Article: A small portfolio can tell a clearer learning story. Teacher advice: define one observable criterion before collecting work. Parent advice: ask a child to explain one revision.','','## Deployment and access verification','','Pending final build/deployment checks; see the completion note appended after verification. Owner login/email delivery has not been end-to-end tested in this run; no password, security setting, or customer-access mode was changed.']
(ROOT/'docs/daily-review-2026-09-15.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(stats,indent=2))
