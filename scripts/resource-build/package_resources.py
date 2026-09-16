"""Package exact private files and build public metadata; never expose paid files as assets.

PDF streams and ZIP entry bodies are content-addressed so repeated original brand
assets are stored once. The original byte sequence and SHA-256 are verified for
every packed file. This is lossless storage, not logo alteration.
"""
from pathlib import Path
import json,re,hashlib,base64,zipfile,struct,gzip,shutil
import fitz
from pypdf import PdfReader
from build_math import ROOT,OUT,TMP
from math_content import PROFILES,SOURCE,SPECS

COLLECTIONS=['EOG & State Test Prep','Task Cards','Warm-Ups','PowerPoints','Sub Plans','Emergency Sub Plans','Fall Packets','Winter Packets','Spring Break Packets','Summer Packets','Lesson Plan Templates']
TEACHER_COLLECTIONS=['Classroom Management','Classroom Décor','Classroom Ideas','Teacher Behavior Supports','Parent Behavior Supports','New Teacher Tips']
GRADES=['Pre-K','Kindergarten']+[f'Grade {n}' for n in range(1,13)]
pool=[];lookup={};files={};productFiles={}
def intern(data):
 h=hashlib.sha256(data).hexdigest()
 if h not in lookup:lookup[h]=len(pool);pool.append(base64.b64encode(data).decode())
 return lookup[h]
def split(data,kind):
 if kind=='pdf':
  pos=0
  for m in re.finditer(rb'\bstream\r?\n(.*?)endstream',data,re.S):
   yield data[pos:m.start(1)];yield m.group(1);pos=m.end(1)
  yield data[pos:]
 elif kind in ['zip','pptx']:
  import io
  z=zipfile.ZipFile(io.BytesIO(data));pos=0
  for info in sorted(z.infolist(),key=lambda x:x.header_offset):
   off=info.header_offset;nlen,elen=struct.unpack_from('<HH',data,off+26);start=off+30+nlen+elen;end=start+info.compress_size
   yield data[pos:start]
   if info.compress_type==zipfile.ZIP_STORED and info.filename.rsplit('.',1)[-1] in ['pdf','pptx']:
    yield from split(data[start:end],info.filename.rsplit('.',1)[-1])
   else:yield data[start:end]
   pos=end
  yield data[pos:]
 else:yield data
def pack(path):
 raw=path.read_bytes();ids=[intern(x) for x in split(raw,path.suffix[1:]) if x]
 rebuilt=b''.join(base64.b64decode(pool[i]) for i in ids)
 assert rebuilt==raw,path
 ext=path.suffix[1:];ct={'pdf':'application/pdf','pptx':'application/vnd.openxmlformats-officedocument.presentationml.presentation','zip':'application/zip'}[ext]
 files[path.name]={'chunks':ids,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'contentType':ct}
 return path.name
def previews(id,pdf,pages):
 doc=fitz.open(pdf)
 thumb=ROOT/'public/product-thumbnails'/f'{id}.png';thumb.parent.mkdir(exist_ok=True)
 doc[0].get_pixmap(matrix=fitz.Matrix(.85,.85),alpha=False).save(thumb)
 results=[]
 for i,page in enumerate(pages):
  name=id+('' if i==0 else '-'+str(i+1))+'.png';dest=ROOT/'public/product-previews'/name
  pix=doc[page-1].get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False);pix.save(dest)
  results.append({'src':'/product-previews/'+name,'page':page,'alt':f'Actual page {page} from {id.replace("-"," ")}; sample only.'})
 return results
common={
 'approved':True,'publicationStatus':'Approved public preview; purchase not enabled for this resource',
 'license':'Single-teacher classroom use with the teacher’s own learners and their families in a private classroom or LMS. No resale, public posting, or redistribution of the complete files.',
 'originality':'Original questions, scripts, explanations, and layouts. No official released-test items or branded curriculum reproduced.',
 'accessedAt':'2026-09-15',
 'digitalNotes':'Print US Letter at actual size. Separate teacher keys from student pages. PDF annotation in a private LMS is optional; the forms are not digitally fillable.',
 'accessibility':{'AIG':'Second methods, counterexamples, transfer, or student-designed improvements.','504':'Follow the individual plan for time, breaks, copying, format, and environment.','EC':'Use the IEP and relevant team guidance; model one step and offer suitable representations or alternate responses.','ESL':'Preview vocabulary, demonstrate, offer home-language rehearsal, and use short sentence frames.'}
}
rows=[]
math_report=json.loads((TMP/'math-build-report.json').read_text())
for record in math_report:
 id=record['id'];d=json.loads((TMP/(id+'.json')).read_text());p=d['profile'];grade,key,title,code,obj,strategy=p
 slide_source=TMP/'slide-pdfs'/f'{id}.pdf';assert len(PdfReader(slide_source).pages)==10
 slide_pdf=OUT/f'{id}-slides.pdf';shutil.copyfile(slide_source,slide_pdf)
 pdf=OUT/f'{id}.pdf';ppt=OUT/f'{id}.pptx';assert ppt.exists()
 zpath=OUT/f'{id}.zip'
 with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_STORED) as z:
  for f in [pdf,ppt,slide_pdf]:
   info=zipfile.ZipInfo(f.name,date_time=(2026,9,15,0,0,0));info.compress_type=zipfile.ZIP_STORED;z.writestr(info,f.read_bytes())
 productFiles[id]={'default':pack(zpath),'pdf':pack(pdf),'pptx':pack(ppt),'slides':pack(slide_pdf)}
 row={**common,'id':id,'title':record['title'],'level':f'Grade {grade} • North Carolina','grades':[f'Grade {grade}'],'states':['North Carolina'],'state':'North Carolina','audience':'Students and educators','subject':'Mathematics','standard':code,'objective':obj,'resourceType':'Complete mathematics teaching bundle','collections':COLLECTIONS+['Classwork','Homework','Independent Work','Small-Group Work','Exit Tickets','Worksheets'],'formats':['PDF','PPTX'],'distributionFormat':'ZIP','pages':record['pages'],'additionalPdfPages':10,'slides':10,'priceCents':1200,
 'description':f'{obj} A Grade {grade} bundle with 48 printable teaching pages, a 10-slide editable mini-lesson, and a 10-page slide handout. Includes original skill practice, worked keys, seasonal revisits, and substitute lessons.',
 'summary':f'One focused skill across task cards, warm-ups, seasonal review, substitute plans, and slides.',
 'detailedDescription':f'Teach {title.lower()} through models, partner practice, independent work, and later review. The printable sections focus on {code}; they support a selected skill within the standard and do not claim to cover an entire grade curriculum or simulate a full EOG. The seasonal sets use fresh quantities and contexts. The mini-lesson shares selected examples and practice from the PDF so teachers can project the same teaching sequence.',
 'included':['1 ZIP containing the 48-page teaching PDF, 10-slide editable PPTX, and 10-page PDF slide handout','2 worked models','16 cut-apart task cards plus 1 response record','5 two-question warm-ups (10 items)','6 classwork questions','1 four-question exit ticket with local scoring guidance','4 seasonal sets: fall, winter, spring break, and summer (8 questions each; 32 total)','1 planned-absence substitute lesson plus 4 practice questions','1 emergency substitute lesson plus 4 practice questions and a no-copier option','1 completed lesson-plan example and 1 reusable blank planning page','Worked solutions for all 76 student practice and assessment items','AIG, 504, EC, and ESL support guidance; source and license notes'],
 'minutes':'Two to three teaching sessions, five 5-minute warm-ups, and separate 15–20-minute seasonal practice sittings; substitute lessons are 45 minutes.',
 'studentDirections':'Read the quantities, represent the situation, solve, and explain a check. Record task-card reasoning on the response page or separate paper. Complete the exit ticket independently.',
 'teacherUse':'Model first, use cards in pairs, assign classwork independently, and use the exit explanation to choose a reteaching step. Keep the teacher-review slide hidden during independent work.',
 'answerKey':'Worked solutions for all 76 printable student items, two worked models, slide speaker-note solutions, and a local 0–2 item rubric. No standardized score prediction.',
 'preparation':'Print selected pages and separate keys. Prepare pencils, paper, and useful counters or graph paper. A presentation viewer is needed only for the optional slides; no internet or paid app is needed for print activities.',
 'source':f'NCDPI mathematics standards, {SOURCE}; EOG mathematics specifications, {SPECS}. Accessed September 15, 2026.',
 'sources':[{'title':'NCDPI mathematics standards','url':SOURCE},{'title':'NCDPI EOG mathematics specifications','url':SPECS}],
 'tags':[f'Grade {grade}','North Carolina',code,'math','task cards','warm-ups','PowerPoint','seasonal review','substitute lesson','worked solutions'],
 'thumbnailAlt':f'Official KSP logo on the cover of {record["title"]}.',
 'previews':previews(id,pdf,[4,14]),'previewDescription':'Actual task-card and classwork pages from the printable bundle. Full answer keys and files are protected.'}
 rows.append(row)

for record in json.loads((TMP/'teacher-build-report.json').read_text()):
 id=record['id'];pdf=OUT/f'{id}.pdf';productFiles[id]={'default':pack(pdf),'pdf':pdf.name}
 rows.append({**common,'id':id,'title':record['title'],'level':'Pre-K–Grade 12 • Educator and family planning','grades':GRADES,'states':[],'state':'State-neutral','audience':'Educators and families','subject':'Classroom Practice','standard':'Professional objective: '+record['objective'],'objective':record['objective'],'resourceType':'Classroom and family routine toolkit','collections':TEACHER_COLLECTIONS,'formats':['PDF'],'distributionFormat':'PDF','pages':23,'slides':0,'priceCents':700,
 'summary':record['objective']+'. Practical scripts, displays, rehearsal tasks, and planning forms.',
 'description':record['objective']+'. A 23-page professional toolkit with age-band adaptations, a five-step routine, two printable displays, a functional room-layout diagram, classroom activities, family pages, and response guidance.',
 'detailedDescription':'Use this toolkit to teach and review one classroom routine. It provides concrete language, original decision cases, and tools for recording observations without public ranking. The Pre-K–Grade 12 tags identify the adults’ planning audience; age-band adaptations are on page 2. This is not a grade-specific academic worksheet, a state-standard alignment claim, an individualized intervention, or a crisis plan.',
 'included':['1 complete 23-page PDF','1 professional guide with adaptations for Pre-K/K, Grades 1–2, 3–5, 6–8, and 9–12','1 five-step classroom routine and an adult-script rehearsal page','3 decision cases with a complete facilitator response guide','2 printable typographic displays and 1 original functional room-layout diagram','1 display implementation and visual-rights guide','2 classroom activity plans plus 1 learner-response page and 1 reflection page','1 teacher response plan, 1 private observation form, and 1 neutral-observation response guide','1 caregiver guide, 1 home-practice card, and 1 five-day family check-in form','1 first-week run sheet for new teachers','1 five-question professional exit ticket and complete response guide','Accessibility, preparation, background source, and single-teacher license notes'],
 'minutes':'20–30 minutes of adult preparation; two 15–20-minute rehearsal activities; brief reviews across one week.',
 'studentDirections':'Practice the demonstrated routine, show or explain the next step, and suggest a helpful cue. Adults may scribe the response page for younger learners or those needing an alternate response method.',
 'teacherUse':'Select one routine, teach it explicitly, rehearse with supports, and review a concrete observation. Use family pages when relevant and keep completed observations private.',
 'answerKey':'Facilitator responses for 3 decision cases, a neutral-observation practice guide, and responses or criteria for all 5 professional exit-ticket prompts. Open planning forms intentionally have no single fixed answer.',
 'preparation':'Print the cue and selected forms. Check school procedures and individual learner plans. Demonstrate cues to nonreaders. Adapt the conceptual room diagram to actual access and space requirements.',
 'source':'Background: IRIS Center, Classroom Behavior Management (Part 1), https://iris.peabody.vanderbilt.edu/module/beh1/. Accessed September 15, 2026. All toolkit text and visuals are independently authored.',
 'sources':[{'title':'IRIS classroom behavior management background','url':'https://iris.peabody.vanderbilt.edu/module/beh1/'}],
 'tags':['teacher toolkit','classroom routines','parent guide','printable poster','classroom planning','new teacher','state-neutral'],
 'thumbnailAlt':f'Official KSP logo on the cover of {record["title"]}.','previews':previews(id,pdf,[7,9,14]),'previewDescription':'Actual routine display, conceptual room-layout diagram, and teacher-support page. This product contains original typography and diagrams, not classroom photographs.'})

for record in json.loads((TMP/'exam-build-report.json').read_text()):
 id=record['id'];pdf=OUT/f'{id}.pdf';productFiles[id]={'default':pack(pdf),'pdf':pdf.name}
 rows.append({**common,'id':id,'title':record['title'],'level':'Grades 9–12 • College-entrance math preparation','grades':[f'Grade {i}' for i in range(9,13)],'states':[],'state':'Exam preparation; no state alignment claim','audience':'Students and tutors','subject':'Mathematics','standard':'Exam skill objective: '+record['objective'],'objective':record['objective'],'resourceType':'Focused SAT / ACT mathematics skill packet','collections':['SAT Preparation','ACT Preparation','Independent Work','Worksheets'],'formats':['PDF'],'distributionFormat':'PDF','pages':record['pages'],'slides':0,'priceCents':600,
 'summary':record['objective']+' Focused original mathematics practice with worked solutions.',
 'description':record['objective']+' A 23-page SAT / ACT mathematics skill packet with two models, 16 practice questions, six explain-and-check tasks, a four-item exit ticket, and complete worked solutions.',
 'detailedDescription':f'Build the named mathematics skill within {record["domain"]}. Use the models to establish a method, then work independently and review the first step that caused an error. This shared mathematics foundation is relevant to both exams; it is not a full practice test, does not cover every tested subject, and does not reproduce either exam’s timing or scoring. Grade placement depends on prior coursework.',
 'included':['1 complete 23-page PDF','1 teacher/tutor session guide','2 worked models','16 original practice questions','6 explain-and-check transfer tasks','1 four-question independent exit ticket','Worked solutions for all 26 student items','1 error-review guide and local 0–2 item rubric','AIG, 504, EC, and ESL supports','Official exam-scope source links, printing guidance, and license notes'],
 'minutes':'Two 35–50-minute study sessions plus a 15–20-minute independent check; adapt to readiness.',
 'studentDirections':'Read the full task, define quantities, show a method, and check the result or restriction. Review worked solutions only after attempting the questions.',
 'teacherUse':'Use after the relevant prerequisite instruction. Diagnose the first misunderstanding, reteach a smaller example, and return to the original task. No scaled-score conversion is provided.',
 'answerKey':'Two complete worked models and worked solutions for all 26 practice, transfer, and assessment items. Written-judgment tasks include response criteria. Local rubric is not standardized exam scoring.',
 'preparation':'Prepare paper and a pencil. A calculator may be used for checking when useful. Review actual exam policies separately; this packet does not grant testing accommodations.',
 'source':'College Board SAT mathematics scope and ACT mathematics test description, accessed September 15, 2026.',
 'sources':[{'title':'College Board: types of SAT mathematics','url':'https://satsuite.collegeboard.org/sat/whats-on-the-test/math/types'},{'title':'ACT mathematics test description','url':'https://www.act.org/content/act/en/products-and-services/the-act/test-preparation/description-of-math-test.html'}],
 'tags':['SAT math','ACT math',record['domain'],'college entrance','worked solutions','exam skill practice'],
 'thumbnailAlt':f'Official KSP logo on the cover of {record["title"]}.','previews':previews(id,pdf,[4,10]),'previewDescription':'Actual practice and transfer pages. This is a focused mathematics packet, not a complete SAT or ACT practice exam.'})

assert len(rows)==90 and len({p['id'] for p in rows})==90
(ROOT/'data/catalog-expansion-2026-09-15.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
payload={'chunks':pool,'files':files,'products':productFiles}
dest=ROOT/'server/resource-payload.json';dest.write_text(json.dumps(payload,separators=(',',':')))
counts={name:sum(name in p['collections'] for p in rows) for name in COLLECTIONS+TEACHER_COLLECTIONS+['SAT Preparation','ACT Preparation']}
assert all(n==30 for n in counts.values()),counts
stats={'products':90,'pdfFiles':120,'pptxFiles':30,'printablePages':sum(p['pages']+p.get('additionalPdfPages',0) for p in rows),'slides':300,'uniqueChunks':len(pool),'privatePayloadBytes':dest.stat().st_size,'privatePayloadGzipBytes':len(gzip.compress(dest.read_bytes())),'collectionCounts':counts}
(ROOT/'data/resource-release-manifest.json').write_text(json.dumps({'date':'2026-09-15','stats':stats,'files':{k:{x:v[x] for x in ['bytes','sha256','contentType']} for k,v in files.items()},'products':productFiles},indent=2))
print(json.dumps(stats,indent=2))
