import json,random
from build_math import Book,ROOT,OUT,TMP,TEAL
from exam_content import EXAM,exam_task,verify
from math_content import fmt

def build(p,index):
 key,title,domain,obj=p;slug='sat-act-'+key+'-math-skill-builder';b=Book(OUT/(slug+'.pdf'),title,'Grades 9–12 • SAT / ACT mathematics foundations')
 seed=500000+index*1000;models=[exam_task(p,seed+i) for i in range(2)];practice=[exam_task(p,seed+20+i) for i in range(16)];transfer=[exam_task(p,seed+50+i) for i in range(6)];exit_items=[exam_task(p,seed+80+i) for i in range(4)]
 for t in models+practice+transfer+exit_items:verify(t)
 b.cover(domain+' • '+obj,'Original focused skill practice for learners preparing for college-entrance mathematics. Includes models, 16 practice tasks, six explain-and-check tasks, a four-item exit ticket, and worked solutions. Not a full practice exam.')
 b.page('Plan a focused study session','TEACHER / TUTOR GUIDE');y=680
 for h,t in [('Learning objective',obj),('Readiness','Use after learners have studied the relevant algebra, geometry, or data concepts. Grade tags describe a typical preparation audience; readiness depends on prior coursework.'),('Suggested use','Session 1: 10 minutes on worked examples and 20–30 minutes on practice. Session 2: review errors, then use explain-and-check tasks. Finish with the independent exit ticket. Pause and reteach a prerequisite when the model is not yet understood.'),('What this resource covers','The named mathematics skill is useful within SAT and ACT preparation. The packet does not cover every exam domain, reproduce an official section, provide standardized timing, or predict a score.'),('Materials','Pencil, paper, and a calculator for checking when useful. Practice both symbolic reasoning and calculator verification. Follow each exam publisher’s current policies for an actual test.'),('Student directions','Read the entire question, define quantities, show a method, and check the result. For a written explanation, cite the calculation or feature that supports your conclusion.')]:
  y=b.text(h,48,y,size=12,font='Bold',color=TEAL)-5;y=b.text(t,48,y,size=11.2)-17
 b.page('Two worked examples','MODEL THE REASONING');y=680
 for i,t in enumerate(models):
  y=b.text(f'Model {i+1}. '+t['q'],48,y,size=12,font='Bold')-10;y=b.text(t['work'],48,y,size=12)-34
 b.text('Pause before looking at a solution: which relationship, definition, or constraint determines the first step?',48,147,size=11,color=TEAL)
 b.questions('Practice • Show a complete method',practice,per=3)
 b.questions('Explain and check • Transfer practice',transfer,per=2,directions='Solve the task, then explain a check or limitation. Compare your reasoning with the worked key only after making your own attempt.')
 b.questions('Exit ticket • Independent check',exit_items,per=2,directions='Complete independently. Show reasoning and any relevant restriction. This is a classroom learning check, not a standardized test score.')
 for label,items in [('Practice worked solutions',practice),('Transfer worked solutions',transfer),('Exit-ticket worked solutions',exit_items)]:b.key(label,items,per=4)
 b.page('Use errors to choose the next step','TEACHER REVIEW');y=680
 for h,t in [('Identify the first mismatch','Compare the student’s representation with the quantities or stated condition. Separate reading the situation, choosing a method, calculation, and interpretation.'),('Respond precisely','If the model is wrong, use a simpler example before repeating the procedure. If the method is sound and arithmetic is wrong, correct that step and verify the original result.'),('Review the exit ticket','For each item: 2 points for an accurate result with coherent reasoning; 1 for a sound method with a minor error or an unexplained correct answer; 0 for unsupported or missing reasoning. Use comments to select a next action. These are local instructional criteria.'),('AIG','Compare two methods, construct a counterexample, or create a new problem with a prescribed solution and justify its restrictions.'),('504 / EC','Follow the individual plan. Offer manageable item groups, documented time or format supports, a worked step, or an alternate response method while retaining the mathematical objective.'),('ESL','Preview terms and symbols in the questions. Use home-language rehearsal or a bilingual glossary, then ask for a concise explanation such as “The condition means ___, so I used ___.”')]:
  y=b.text(h,48,y,size=11.5,font='Bold',color=TEAL)-5;y=b.text(t,48,y,size=10.9)-17
 b.page('Sources, preparation, and license','TEACHER NOTES');y=680
 paragraphs=[
  'Objective: '+obj+' State alignment: not claimed. This is a focused college-entrance preparation resource, not a state course or a claim of course equivalency.',
  'Official exam scope consulted September 15, 2026: College Board, Types of Math Tested, https://satsuite.collegeboard.org/sat/whats-on-the-test/math/types ; ACT, Mathematics Test Description, https://www.act.org/content/act/en/products-and-services/the-act/test-preparation/description-of-math-test.html .',
  'The questions, contexts, explanations, and practice sequence are independently authored. No official test items, passages, answer choices, logos, or branded curriculum are reproduced. SAT is a College Board trademark; ACT is an ACT trademark. This resource is not affiliated with or endorsed by either organization.',
  'Print US Letter at actual size. Separate student practice from the teacher keys. The PDF can be annotated in a private learning platform but does not contain fillable form fields. No paid software or device is required for print use.',
  'Single-teacher classroom license: use copies with your own learners in a private classroom or LMS. Do not resell, share the complete file publicly, or redistribute it to other teachers. Suggested time and scoring guidance are instructional choices, not official exam timing, accommodations approval, or score prediction.'
 ]
 for t in paragraphs:y=b.text(t,48,y,size=11.2)-25
 pages=b.finish();data={'id':slug,'title':title+' • SAT / ACT Math Skill Builder','pdf':str(b.path.relative_to(ROOT)),'pages':pages,'objective':obj,'domain':domain,'models':models,'practice':practice,'transfer':transfer,'exit':exit_items};(TMP/(slug+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2));return {k:data[k] for k in ['id','title','pdf','pages','objective','domain']}

if __name__=='__main__':
 rows=[]
 for i,p in enumerate(EXAM):
  row=build(p,i);rows.append(row);print(row['id'],row['pages'],flush=True)
 (TMP/'exam-build-report.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
