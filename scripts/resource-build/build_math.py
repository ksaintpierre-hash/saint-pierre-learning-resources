from pathlib import Path
import json,hashlib,math,sys,re
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader
from PIL import Image
from math_content import PROFILES,SOURCE,SPECS,task,validate_profiles

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'resources/2026-09-15';OUT.mkdir(parents=True,exist_ok=True)
TMP=ROOT/'tmp/resource-build';TMP.mkdir(parents=True,exist_ok=True)
LOGO=ROOT/'public/brand/saint-pierre-logo.png'
NAVY='#172D46';TEAL='#246A70';GOLD='#B08838';INK='#233547';GRAY='#536574'
for name,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Title','DejaVuSerif.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFont(TTFont('CJK','/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',subfontIndex=0))
W,H=612,792
class Book:
 def __init__(self,path,title,level):
  self.path=path;self.title=title;self.level=level;self.n=0;self.layouts=[]
  self.c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1,invariant=1)
  self.c.setTitle(title);self.c.setAuthor('Saint Pierre Learning Resources');self.c.setSubject(level)
  # Reserve the same used character repertoire in each document. This makes
  # embedded font subsets reusable in lossless private storage, without adding
  # hidden page content or changing typography.
  repertoire=''.join(sorted({ch for f in (ROOT/'scripts/resource-build').glob('*.py') for ch in f.read_text() if ord(ch)>=32}|set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')))
  for family in ['Body','Bold','Title']:pdfmetrics.getFont(family).splitString(repertoire,self.c._doc)
 def logo(self,x,y,w):
  im=Image.open(LOGO);h=w*im.height/im.width
  self.c.drawImage(str(LOGO),x,y,width=w,height=h,mask='auto',preserveAspectRatio=True)
  return h
 def text(self,txt,x=48,y=680,w=516,size=11.5,font='Body',color=INK,leading=None):
  s=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.4,textColor=HexColor(color),spaceAfter=0,wordWrap='CJK' if font=='CJK' else None)
  p=Paragraph(escape(str(txt)).replace('\n','<br/>'),s);pw,ph=p.wrap(w,700)
  if (y>60 and y-ph<59) or y-ph<0:raise ValueError(f'Overflow {self.title} page {self.n}: {txt[:50]} bottom {y-ph}')
  p.drawOn(self.c,x,y-ph);self.layouts.append({'page':self.n,'x':x,'y':y-ph,'w':w,'h':ph,'text':txt})
  return y-ph
 def lines(self,y,count=3,x=48,w=516,gap=25):
  self.c.setStrokeColor(HexColor('#C7D0D6'));self.c.setLineWidth(.5)
  for i in range(count):self.c.line(x,y-i*gap,x+w,y-i*gap)
 def page(self,title,kicker='STUDENT PRACTICE',title_font='Title'):
  if self.n:self.c.showPage()
  self.n+=1;self.c.setFillColor(HexColor(TEAL));self.c.rect(0,H-8,W,8,fill=1,stroke=0)
  self.text(kicker,48,754,size=8.5,font='Bold',color=TEAL)
  self.text(title,48,732,w=516,size=23,font=title_font,color=NAVY,leading=24)
  self.c.setStrokeColor(HexColor('#D6DEE1'));self.c.line(48,60,564,60)
  self.logo(48,14,42);self.text('© 2026 Saint Pierre Learning Resources',98,42,w=365,size=7.4,color=GRAY)
  self.c.setFont('Body',8);self.c.setFillColor(HexColor(GRAY));self.c.drawRightString(564,29,str(self.n))
 def cover(self,subtitle,description,title_font='Title'):
  self.page('', 'SAINT PIERRE LEARNING RESOURCES')
  self.logo(48,574,175)
  y=self.text(self.title,48,540,w=506,size=33,font=title_font,color=NAVY,leading=41)
  y=self.text(self.level,48,y-28,size=15,font='Bold',color=TEAL)
  y=self.text(subtitle,48,y-26,size=15)
  self.text(description,48,y-30,size=12,w=485)
  self.text('PRINT • TEACH • REVISIT',48,120,size=10,font='Bold',color=GOLD)
 def diagram(self,d,x,y,w=210,h=85):
  if not d:return
  c=self.c;c.setStrokeColor(HexColor(TEAL));c.setLineWidth(1);c.setFont('Body',8);c.setFillColor(HexColor(TEAL))
  typ=d['type']
  if typ=='fraction':
   bw=min(w,200)/d['d'];bh=25
   for i in range(d['d']):
    c.setFillColor(HexColor('#B7DADC') if i<d['n'] else HexColor('#FFFFFF'));c.rect(x+i*bw,y+20,bw,bh,stroke=1,fill=1)
  elif typ in ['rectangle','triangle','righttriangle']:
   dw=min(140,w-35);dh=min(52,h-23)
   if typ=='rectangle':c.rect(x+20,y+15,dw,dh)
   else:
    p=c.beginPath();p.moveTo(x+20,y+15);p.lineTo(x+20+dw,y+15);p.lineTo(x+20,y+15+dh);p.close();c.drawPath(p)
   c.drawString(x+dw/2,y+3,str(d['w']));c.drawString(x+2,y+35,str(d['h']))
  elif typ=='circle':
   c.circle(x+55,y+40,30);c.line(x+55,y+40,x+85,y+40);c.drawString(x+62,y+45,'r = '+str(d['r']))
  elif typ=='prism':
   c.rect(x+25,y+15,100,40);c.lines([(x+25,y+55,x+45,y+75),(x+125,y+55,x+145,y+75),(x+145,y+75,x+145,y+35),(x+125,y+15,x+145,y+35),(x+45,y+75,x+145,y+75)])
   c.drawString(x+55,y+3,str(d['w']));c.drawString(x+4,y+35,str(d['h']));c.drawString(x+140,y+62,str(d['d']))
  elif typ=='scatter':
   pairs=d['pairs'];maxy=max(v for _,v in pairs)+3
   c.lines([(x+20,y+10,x+190,y+10),(x+20,y+10,x+20,y+78)])
   for px,py in pairs:c.circle(x+20+px*23,y+10+py/maxy*65,2,fill=1)
   c.drawString(x+185,y,'x');c.drawString(x+5,y+75,'y')
 def questions(self,title,items,start=1,per=4,kicker='STUDENT PRACTICE',directions='Show your thinking with a drawing, equation, or explanation. Use the space under each question.',font='Body'):
  for offset in range(0,len(items),per):
   chunk=items[offset:offset+per];self.page(title,kicker)
   self.text(directions,48,681,size=10,color=GRAY)
   top=637;space=554/per
   for j,t in enumerate(chunk):
    y=top-j*space;bottom=self.text(f'{start+offset+j}. '+t['q'],48,y,size=11.2,font=font)
    if t.get('diagram') and space>=175:self.diagram(t['diagram'],62,bottom-90)
    self.lines(max(y-space+28,82),1)
 def key(self,title,items,labels=None,per=6,font='Body'):
  for offset in range(0,len(items),per):
   self.page(title,'TEACHER ANSWER KEY');y=678
   for j,t in enumerate(items[offset:offset+per]):
    label=labels[offset+j] if labels else str(offset+j+1)
    y=self.text(f'{label}. {t["answer"]}',48,y,size=11,font='Bold',color=TEAL)
    y=self.text(t['work'],48,y-4,size=10.2,font=font)-14
 def finish(self):
  self.c.save();assert len(PdfReader(self.path).pages)==self.n
  (TMP/(self.path.stem+'-layout.json')).write_text(json.dumps(self.layouts,ensure_ascii=False))
  return self.n

def math_bundle(p,index):
 grade,key,title,code,obj,strategy=p;slug='nc-g'+str(grade)+'-'+key+'-teaching-bundle'
 book=Book(OUT/(slug+'.pdf'),title+' Teaching Bundle',f'Grade {grade} • North Carolina • Mathematics')
 seed=100000+index*1000
 cards=[task(p,seed+i) for i in range(16)]
 warms=[task(p,seed+30+i) for i in range(10)]
 practice=[task(p,seed+50+i) for i in range(6)]
 exit_items=[task(p,seed+70+i) for i in range(4)]
 model=[task(p,seed+90+i) for i in range(2)]
 book.cover(code+' • '+obj,'A focused classroom collection: task cards, five warm-ups, classwork, an exit ticket, four seasonal practice sets, substitute lessons, and planning pages. Each section has worked answers.')
 book.page('Your teaching route','TEACHER GUIDE');y=678
 for h,t in [('Focus',obj+' This bundle practices a focused part of '+code+'; it is not a complete grade curriculum or a simulated EOG.'),('Before teaching','Learners should explain a simpler example using a model. Read the two worked examples, then use the first task card to check readiness.'),('Suggested sequence','Day 1: model for 10 minutes, then guided task cards for 15 minutes. Day 2: a 5-minute warm-up and 20 minutes of practice. Use the exit ticket to choose a small-group reteaching focus. Seasonal sets revisit the same skill using different quantities.'),('Materials','Pencils, blank paper, and graph paper or counters as useful. No paid app or internet is needed for student work. A calculator may check finished calculations; these are instructional choices, not official testing accommodation rules.')]:
  y=book.text(h,48,y,size=12,font='Bold',color=TEAL);y=book.text(t,48,y-6,size=11.2)-18
 book.page('Make the reasoning visible','WORKED EXAMPLES');y=680
 y=book.text(strategy,48,y,size=12)-25
 for j,t in enumerate(model):
  y=book.text(f'Example {j+1}: '+t['q'],48,y,size=11.5,font='Bold')-8
  y=book.text(t['work'],48,y,size=11.5)-25
 book.text('Ask: What does each number represent? How could a model or inverse operation check the result?',48,160,size=11,color=TEAL)
 # Four cut-apart task cards on each page, each with full directions and ample response space.
 for offset in range(0,16,4):
  book.page(f'Task cards {offset+1}–{offset+4}','CUT APART • WORK WITH A PARTNER')
  book.text('Read, represent, solve, and explain. Record full reasoning on the response page or separate paper.',48,679,size=10,color=GRAY)
  for j,t in enumerate(cards[offset:offset+4]):
   x=48+(j%2)*264;y=645-(j//2)*270
   book.c.setStrokeColor(HexColor('#A3B3BE'));book.c.rect(x,y-251,252,251)
   book.text(f'CARD {offset+j+1:02d}',x+12,y-13,w=228,size=9,font='Bold',color=TEAL)
   bottom=book.text(t['q'],x+12,y-38,w=228,size=10.6)
   if t.get('diagram') and bottom-(y-241)>92:book.diagram(t['diagram'],x+14,y-229,w=205,h=80)
   book.text('Explain your method.',x+12,y-226,w=228,size=9,color=GRAY)
 book.page('Task-card response record');book.text('Use this page for final answers; attach drawings or full worked solutions on separate paper.',48,680,size=10.5)
 for i in range(16):
  y=625-i*31;book.text(str(i+1)+'.',48,y,size=11);book.lines(y-17,1,x=76,w=480)
 for day in range(5):
  book.questions(f'Warm-up • Day {day+1}',warms[2*day:2*day+2],start=2*day+1,per=2,directions='Work for about five minutes. Compare one method with a partner. Complete unfinished reasoning during review.')
 book.questions('Classwork • Represent and explain',practice,per=3)
 book.questions('Exit ticket • Try independently',exit_items,per=4,directions='Complete the four questions independently. Show enough reasoning for your teacher to see your method. This is a classroom check, not a standardized score.')
 for heading,items in [('Task-card worked solutions',cards),('Warm-up worked solutions',warms),('Classwork worked solutions',practice),('Exit-ticket worked solutions',exit_items)]:book.key(heading,items,per=6)
 season_sets={}
 for season,display in [('fall','Fall'),('winter','Winter'),('spring','Spring break'),('summer','Summer')]:
  offset={'fall':120,'winter':150,'spring':180,'summer':210}[season]
  items=[task(p,seed+offset+i,season) for i in range(8)];season_sets[season]=items
  book.questions(display+' • Skill revisit',items,per=4,kicker=display.upper()+' PRACTICE PACKET',directions='Complete four questions per sitting, about 15–20 minutes. Review the worked examples if needed. Explain one answer to a classmate or adult.')
  book.key(display+' • Worked solutions',items,per=4)
 sub_sets={}
 for section,label,offset in [('sub','Substitute lesson',240),('emergency','Emergency substitute lesson',260)]:
  items=[task(p,seed+offset+i,section) for i in range(4)];sub_sets[section]=items
  book.page(label,'TEACHER RUN SHEET');y=680
  blocks=[('Before students arrive','Locate the class schedule, seating plan, emergency procedures, and approved learner supports from the school. This academic packet does not replace those school-specific instructions.'),('0–5 minutes: settle','Read the goal aloud: '+obj+' Let students explain a familiar strategy to a partner.'),('5–15 minutes: model',('Use the worked-example page. ' if section=='sub' else 'No copies or devices? Write the first worked example on the board; students use blank paper. ')+strategy),('15–30 minutes: practice','Distribute the next practice page. Students solve independently first, then compare one explanation in pairs. If copying is unavailable, read one question at a time and allow drawings or oral responses.'),('30–40 minutes: discuss','Use the following key. Ask students to locate the first step where methods diverged; invite a correction supported by a model.'),('40–45 minutes: handover','Collect one explanation from each student. On the planning page, record which step needs reteaching, who requested help, and what was completed. Use neutral observations, not diagnostic labels.')]
  for h,t in blocks:
   y=book.text(h,48,y,size=11.5,font='Bold',color=TEAL);y=book.text(t,48,y-4,size=10.6)-13
  book.questions(label+' • Practice',items,per=4);book.key(label+' • Worked solutions',items,per=4)
 book.page('A completed lesson-plan example','TEACHER PLANNING');y=680
 for h,t in [('Level and focus',f'Grade {grade}; '+code+'; '+obj),('Evidence of learning','Student represents the quantities, selects a valid method, calculates accurately, and explains the result with appropriate units.'),('Launch / model','Use worked example 1. Ask students to annotate the role of every quantity. Demonstrate the model before moving to symbols.'),('Guided / independent practice','Use cards 1–4 in pairs; assign classwork independently. Change grouping according to the explanation you hear rather than speed alone.'),('Formative check','Use the four-question exit ticket. Score each item 0–2: 2 for an accurate result with coherent reasoning, 1 for a sound method with a minor error or an unexplained correct result, 0 for missing or unsupported reasoning.'),('Next teaching decision','0–3 points: reteach with a concrete model. 4–6: correct the specific misconception with a short example. 7–8: invite a second representation or a student-created problem. These are local instructional decisions, not mastery cutoffs validated by a test publisher.')]:
  y=book.text(h,48,y,size=11.5,font='Bold',color=TEAL);y=book.text(t,48,y-5,size=11)-15
 book.page('Plan your next lesson','REUSABLE PLANNING TEMPLATE');y=675
 for prompt in ['Date, class, and focus / exact local standard:','What will students do to show understanding?','Launch and worked example:','Guided practice and independent task:','Access supports and extension:','Exit evidence and next lesson decision:']:
  book.text(prompt,48,y,size=11,font='Bold');book.lines(y-32,2,gap=23);y-=94
 book.page('Access, sources, and classroom license','TEACHER NOTES');y=680
 support=[('AIG','Invite two methods, a counterexample, or a new task with a specified solution. Ask students to explain limits of a shortcut.'),('504','Apply the student’s plan: breaks, extra time, enlarged print, reduced copying, or alternate response methods as documented.'),('EC','Use the IEP to select supports. Model one step, offer counters or a diagram, reduce the visible item set, and accept an oral explanation when appropriate.'),('ESL','Preview quantity, difference, factor, or other relevant terms. Let students rehearse in a home language, then use “I chose ___ because ___.” Maintain the mathematical goal.')]
 for h,t in support:
  y=book.text(h+': '+t,48,y,size=10.5)-13
 y=book.text('Official alignment sources • accessed September 15, 2026',48,y,size=11,font='Bold',color=TEAL)-6
 y=book.text(code+' is verified in the NCDPI mathematics progression. The activity objective is original wording; it describes the skill focus, not the full standard text.',48,y,size=10)-8
 for label,url in [('NCDPI mathematics standards',SOURCE),('NCDPI EOG mathematics specifications',SPECS)]:
  y=book.text(label+': '+url,48,y,size=8.8)-10
 y=book.text('Independent original practice. Not endorsed by NCDPI. No released questions, passages, or answer choices are reproduced. Classroom practice supports may differ from permitted test accommodations.',48,y,size=9.7)-12
 book.text('Print US Letter at actual size. Keep keys separate from student pages. Digital annotation is optional; this PDF is not a fillable form. One teacher may use copies with their own students in a private classroom or LMS. No resale, public posting, or redistribution of the complete files.',48,y,size=9.7)
 pages=book.finish()
 data={'profile':list(p),'id':slug,'title':title+' Teaching Bundle','pdf':str(book.path.relative_to(ROOT)),'pages':pages,'models':model,'cards':cards,'warmups':warms,'classwork':practice,'exit':exit_items,'seasonal':season_sets,'sub':sub_sets}
 (TMP/(slug+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2))
 return data

if __name__=='__main__':
 validate_profiles((ROOT/'tmp/research/nc-math.txt').read_text())
 which=sys.argv[1:];rows=[]
 for i,p in enumerate(PROFILES):
  if which and str(i) not in which:continue
  result=math_bundle(p,i);rows.append({k:result[k] for k in ['id','title','pdf','pages']});print(result['id'],result['pages'],flush=True)
 (TMP/'math-build-report.json').write_text(json.dumps(rows,indent=2))
