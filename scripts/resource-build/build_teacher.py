from pathlib import Path
import json,re
from reportlab.lib.colors import HexColor
from build_math import Book,OUT,TMP,ROOT,TEAL,GRAY,NAVY
from teacher_content import TOPICS

def build_topic(topic,index):
 title,goal,situation,steps,script,avoid,activity,home=topic
 slug='teacher-'+re.sub('[^a-z0-9]+','-',title.lower()).strip('-')+'-toolkit'
 b=Book(OUT/(slug+'.pdf'),title+' Toolkit','Pre-K–Grade 12 • Educator and family planning')
 b.cover(goal,'An original professional toolkit with a five-step routine, rehearsal activities, printable displays, a room-layout planning diagram, observation tools, family pages, and a new-teacher run sheet.')
 b.page('Choose the version your learners need','PROFESSIONAL LEARNING GUIDE');y=680
 blocks=[('Objective',goal+'. This is an adult planning resource; it is not a state-aligned academic worksheet, an individualized intervention, or a crisis plan.'),('Pre-K and Kindergarten','Use one spoken step, a real object or adult demonstration, and a brief supported rehearsal. An adult records observations; children do not need to read the planning forms.'),('Grades 1–2','Teach two steps at a time. Pair the printed cue with an example and let learners show or tell what comes next.'),('Grades 3–5','Let students explain the sequence, practice roles, and offer one suggestion. Use a short written or drawn reflection.'),('Grades 6–8','Offer private feedback and meaningful choices. Ask learners to identify barriers in the routine and help revise one step.'),('Grades 9–12','Connect the routine to increasing independence, collaborative projects, and self-advocacy. Invite students to assess whether the system is useful and respectful.')]
 for h,t in blocks:
  y=b.text(h,48,y,size=11.5,font='Bold',color=TEAL);y=b.text(t,48,y-4,size=10.7)-14
 b.page('Teach the routine explicitly','CLASSROOM MANAGEMENT');y=680
 y=b.text('Situation to plan for: '+situation,48,y,size=11.5)-22
 for i,step in enumerate(steps):
  y=b.text(f'{i+1}. '+step,48,y,size=13,font='Bold',color=TEAL)-7
  notes=[f'Describe what students should see or hear. Start with the actual situation: {situation}',f'Model the action instead of only naming it. Keep the cue short: “{step}.”',f'Invite a supported rehearsal. Offer a spoken, drawn, or demonstrated response so participation is not limited to writing.',f'Watch one learner or pair try the sequence. If the step is unclear, revise the cue or the environment before repeating it.',f'Ask what helped. Notice a concrete action, then decide whether to keep or adjust the routine.']
  y=b.text(notes[i],48,y,size=10.7)-17
 b.page('Language that teaches the next action','CLASSROOM MANAGEMENT');y=680
 y=b.text('A usable adult script',48,y,size=14,font='Bold',color=TEAL)-12
 y=b.text(script,48,y,size=16,leading=24)-32
 y=b.text('A response to avoid',48,y,size=14,font='Bold',color=TEAL)-10
 y=b.text(avoid,48,y,size=12)-26
 y=b.text('Rehearse with a colleague',48,y,size=14,font='Bold',color=TEAL)-10
 y=b.text('Read the situation. Person A uses the script; Person B responds as a learner who needs the first step clarified. Switch roles. Identify the exact words that made the action more understandable.',48,y,size=12)-26
 b.text('Your adapted script, using language natural to your classroom:',48,y,size=11,font='Bold');b.lines(y-35,4,gap=29)
 cases=[
  ('The first cue does not work',situation+' The adult repeats the same words louder. What information should the adult check, and what could change?',f'Check whether the learner can access the cue, understands the first action, and has the needed materials. Model “{steps[0]}” and invite a supported rehearsal. Increasing volume alone does not clarify the step.'),
  ('The routine works for some learners','Most students use the routine, but one learner needs a different response method. How can the goal stay consistent while access changes?',f'Keep the goal “{goal.lower()}.” Offer demonstration, oral response, reduced copying, or another documented support. Compare the actual learning or participation evidence, not whether every learner used an identical method.'),
  ('Students propose an improvement','A learner says one part of the routine is confusing and suggests a simpler cue. How should the adult respond?',f'Ask the learner to demonstrate the confusing point. Try a small change to “{steps[2]},” explain any non-negotiable school requirements, and review whether the revised cue helps participation.')]
 b.page('Three decision cases','PROFESSIONAL PRACTICE');y=680
 for i,(h,q,a) in enumerate(cases):
  y=b.text(f'{i+1}. {h}',48,y,size=12,font='Bold',color=TEAL)-6;y=b.text(q,48,y,size=11)-9;b.lines(y-8,2,gap=24);y-=78
 b.page('Decision-case response guide','FACILITATOR KEY');y=680
 for i,(h,q,a) in enumerate(cases):
  y=b.text(f'{i+1}. {h}',48,y,size=12,font='Bold',color=TEAL)-5;y=b.text(a,48,y,size=11.2)-24
 b.text('Other responses can be appropriate when they preserve dignity, teach a specific action, follow school procedures and individual plans, and include a way to review the result.',48,168,size=11)
 b.page(title,'PRINTABLE ROUTINE DISPLAY');y=660
 for i,step in enumerate(steps):
  b.text(f'{i+1:02d}',48,y,w=48,size=28,font='Bold',color=TEAL)
  b.text(step,112,y,w=446,size=21,leading=30);y-=100
 b.page('Pause. Find your next step.','PRINTABLE DESK OR HOME CUE');y=660
 for h,t in [('NOTICE','What is happening? What do I need to understand?'),('CHOOSE',steps[0]+'.'),('TRY',steps[2]+'.'),('CHECK',steps[4]+'.')]:
  b.text(h,48,y,size=16,font='Bold',color=TEAL);b.text(t,48,y-31,size=19,leading=27);y-=132
 b.page('A room layout you can adapt','CLASSROOM DÉCOR • FUNCTIONAL PLANNING DIAGRAM')
 b.text('Conceptual layout, not a measured floor plan. Preserve required exits, accessible routes, sight lines, and school rules. The display supports a routine; it does not replace teaching it.',48,681,size=10.5)
 c=b.c;c.setStrokeColor(HexColor(NAVY));c.setLineWidth(1.2);c.rect(72,231,468,366)
 zones=[(90,491,188,83,'VISIBLE ROUTINE CUE'),(333,491,185,83,'MATERIALS / RETURN'),(90,352,188,102,'PARTNER REHEARSAL'),(333,352,185,102,'INDEPENDENT TASK'),(90,248,188,76,'ADULT CHECK-IN'),(333,248,185,76,'FLEXIBLE RESPONSE')]
 for x,y,w,h,label in zones:
  c.setFillColor(HexColor('#F2F7F7'));c.rect(x,y,w,h,fill=1,stroke=1);b.text(label,x+10,y+h-20,w=w-20,size=9.4,font='Bold',color=TEAL)
 b.text('Clear route between zones',217,473,w=200,size=9.2,color=GRAY)
 b.text('Display focus: '+steps[0],48,200,size=11,font='Bold')
 b.text('Use a routine cue where the action begins. Locate materials so learners can find them. Provide a seated or alternative response route without isolating the learner.',48,170,size=10.8)
 b.page('Make the display earn its space','DÉCOR IMPLEMENTATION');y=680
 for h,t in [('Before posting','Print the routine display and the desk cue. Read both from the distance at which students will use them. Enlarge if needed; pair text with real demonstrations for nonreaders.'),('Introduce it','Point to the exact step during rehearsal. Ask learners where the cue would be most useful. A poster becomes instructional when students know how to use it.'),('Keep it usable','Reduce competing visual clutter near the cue. Keep copies reachable and avoid placing private observation records or student comparisons on display.'),('Review after a week','Ask learners to locate the cue and explain its next action. If they cannot use it, revise placement, wording, or instruction instead of adding more posters.'),('Visual rights','The typographic posters and functional layout diagram are original Saint Pierre Learning Resources designs. The unchanged KSP logo is the store’s supplied brand asset. No stock photography or third-party illustration is included.')]:
  y=b.text(h,48,y,size=12,font='Bold',color=TEAL)-5;y=b.text(t,48,y,size=11.2)-22
 b.page('Try the routine in a real activity','CLASSROOM IDEAS');y=680
 y=b.text('Activity 1 • Rehearse and revise (15–20 minutes)',48,y,size=13,font='Bold',color=TEAL)-10
 y=b.text(activity,48,y,size=12)-18
 y=b.text('Prepare blank paper and the printed cue. Model one turn, let partners rehearse, then ask each pair to name one useful step and one improvement. Collect a drawn, oral, or written response.',48,y,size=11.5)-27
 y=b.text('Activity 2 • Teach a new classmate (15 minutes)',48,y,size=13,font='Bold',color=TEAL)-10
 y=b.text(f'Partners make a short guide for a fictional learner joining the class. Include the purpose “{goal.lower()},” the first action, where help is available, and one example of success. Swap guides and test whether the next step is clear.',48,y,size=12)-25
 b.text('Success criteria: the guide names an observable action, is understandable to the intended learner, offers a help route, and avoids public judgment of classmates.',48,y,size=11.2,color=TEAL)
 b.page('My routine rehearsal','LEARNER RESPONSE • ADULT SCRIBE IF NEEDED');y=675
 for prompt in ['The routine helps us…','The first action I can show is…','A cue or material that would help me is…','If I am unsure, I can…','One change I would suggest is…']:
  b.text(prompt,48,y,size=13,font='Bold');b.lines(y-40,3,gap=24);y-=116
 b.page('Review what happened','CLASSROOM IDEAS • REFLECTION');y=680
 for prompt in ['What action did you observe? Write or draw a concrete example.','Which part was clear, and what evidence supports that view?','What barrier appeared? Consider directions, materials, time, space, or response method.','What one change will you try next, and how will you know whether it helped?']:
  b.text(prompt,48,y,size=11.5,font='Bold');b.lines(y-54,3,gap=24);y-=144
 b.page('A supportive response plan','TEACHER BEHAVIOR SUPPORTS');y=680
 for h,t in [('Describe, then inquire',situation+' Describe only what you observed. Ask a neutral question about the difficult step before deciding why it happened.'),('Teach the alternative',script+' Demonstrate the action and provide an opportunity to rehearse with support.'),('Adjust access','Check the learner’s existing plan, task demands, language access, and environment. Choose a support with the learner and relevant staff rather than inventing a diagnosis.'),('Notice progress','Record a concrete example of participation, such as beginning a step, requesting clarification, or using the cue. Avoid public ranking charts.'),('Review and refer appropriately','Use the observation form to decide whether the classroom routine needs adjustment. Persistent or safety-related concerns belong with the school’s designated support team and procedures.')]:
  y=b.text(h,48,y,size=12,font='Bold',color=TEAL)-6;y=b.text(t,48,y,size=11.2)-20
 b.page('Private observation record','TEACHER TOOL • KEEP CONFIDENTIAL');y=674
 for prompt in ['Date / setting / task (avoid unnecessary personal details):','What happened immediately before the observed action?','What did the learner actually say or do?','What cue, model, or access support was offered?','What happened next?','One next instructional adjustment and review date:']:
  b.text(prompt,48,y,size=11,font='Bold');b.lines(y-32,2,gap=23);y-=95
 b.page('Practice neutral observation','TEACHER ANSWER GUIDANCE');y=680
 y=b.text('Prompt: Replace “The student did not care” with an observation based on the scenario.',48,y,size=12,font='Bold')-10
 y=b.text('Possible response: '+situation+' This names visible actions and the setting without claiming to know the learner’s motives.',48,y,size=12)-30
 y=b.text('Prompt: What additional information would be useful?',48,y,size=12,font='Bold')-10
 y=b.text('Ask whether the learner understood the first step, could access the materials or response method, and had the needed support. Note what changes after one specific adjustment.',48,y,size=12)-30
 y=b.text('Prompt: What would count as improvement?',48,y,size=12,font='Bold')-10
 b.text('A reasonable example is a learner using one step of the routine with a support that works for them, then rejoining the task. Define the observation before collecting it; do not assume fewer visible movements or faster completion alone means better learning.',48,y,size=12)
 b.page('A home connection that stays manageable','PARENT AND CAREGIVER GUIDE');y=680
 for h,t in [('Shared purpose',goal+'. The family page supports a short conversation and one manageable routine; families do not need to reproduce the whole classroom system.'),('Try this',home),('Conversation opener','“What part feels clear? What part is difficult? Would it help to show me, draw it, or try the first step together?”'),('Keep school and home connected','Share a neutral observation and ask which support is already agreed at school. Use the child’s perspective and avoid comparing siblings or classmates.'),('If it is not helping','Stop and simplify the routine. Ask the teacher or relevant support professional to help review persistent barriers. This general guide does not replace an individual education, health, or support plan.')]:
  y=b.text(h,48,y,size=12,font='Bold',color=TEAL)-6;y=b.text(t,48,y,size=11.7)-22
 b.page('One small step at home','FAMILY PRACTICE CARD');y=675
 b.text(home,48,y,size=15,leading=23);y-=145
 for prompt in ['The one step we chose:','What the child said, showed, or asked:','What helped, and what we will adjust:']:
  b.text(prompt,48,y,size=12,font='Bold');b.lines(y-39,3,gap=24);y-=133
 b.page('A five-day family check-in','PARENT TOOL • OBSERVATIONS, NOT SCORES')
 b.text('Use a brief note or drawing. This is not a reward chart or a diagnostic measure. Skip a day if the routine is not relevant.',48,681,size=10.6)
 for i in range(5):
  y=628-i*104;b.text(f'Day {i+1} • What we tried / what helped / next adjustment',48,y,size=10.5,font='Bold');b.lines(y-34,2,gap=25)
 b.page('A new teacher’s first-week run sheet','NEW TEACHER TIPS');y=680
 for h,t in [('Before Day 1','Learn the school’s procedures and where individual supports are documented. Choose one routine, not a complete classroom overhaul.'),('Day 1: explain and model',f'Use the goal “{goal.lower()}.” Demonstrate “{steps[0]}” and allow a supported rehearsal.'),('Day 2: observe','Use the private record for one short period. Look for barriers in the task and environment as well as the learner’s response.'),('Day 3: ask and adjust',f'Invite feedback about “{steps[2]}.” Change one cue or material, then explain why.'),('Day 4: connect with home','Use the family page only when relevant. Explain the shared purpose and ask for perspective rather than assigning families a new enforcement role.'),('Day 5: review','Compare concrete observations. Keep the parts that help, revise a confusing step, and ask a mentor for support when needed.')]:
  y=b.text(h,48,y,size=11.8,font='Bold',color=TEAL)-5;y=b.text(t,48,y,size=11)-19
 b.page('Check your plan before using it','PROFESSIONAL EXIT TICKET');y=680
 prompts=['Name one observable action the routine teaches.','Write the first cue in language your learners can use.','Describe an access option that keeps the goal intact.','Identify one response to avoid and explain why.','Choose one observation and a date to review the routine.']
 for i,q in enumerate(prompts):
  b.text(f'{i+1}. '+q,48,y,size=11.5,font='Bold');b.lines(y-40,2,gap=24);y-=113
 b.page('Exit-ticket response guide','PROFESSIONAL ANSWER KEY');y=680
 answers=[steps[0]+'. Other concrete actions from the routine are acceptable.',script,'Examples include oral response, demonstration, a visible step cue, reduced copying, or a support in the learner’s existing plan. Explain how it still serves the goal.',avoid,'Choose a specific action in a defined setting, such as use of the first cue during the opening task. Name a realistic review date and the adjustment the observation will inform.']
 for i,a in enumerate(answers):
  y=b.text(f'{i+1}. '+a,48,y,size=11.5)-25
 b.text('Use this as a planning check. A response is useful when it is specific, respectful, feasible, and connected to evidence. There is no certified score or universal compliance claim.',48,160,size=11)
 b.page('Access and responsible use','TEACHER NOTES');y=680
 notes=[('AIG','Invite learners to evaluate and redesign a routine, compare alternatives, or lead a consent-based demonstration. Do not make advanced learners permanent peer supervisors.'),('504','Follow the individual plan for pacing, breaks, environment, and response methods. A posted routine does not replace documented accommodations.'),('EC','Use the IEP and relevant team guidance. Model one step, provide supported practice, and adapt communication and response options.'),('ESL','Use plain language, demonstrations, home-language discussion, and short sentence frames. Families may respond in their preferred language.'),('Preparation and printing','Print selected US Letter pages at actual size; enlarge display pages if useful. Forms are printable, not digitally fillable. Keep completed observation and family records private.'),('Sources and originality','Background reference, accessed September 15, 2026: IRIS Center, Classroom Behavior Management (Part 1), https://iris.peabody.vanderbilt.edu/module/beh1/. All scripts, cases, forms, posters, and the layout diagram here are original; no IRIS content or third-party visuals are reproduced.'),('License','Single-teacher use with that teacher’s learners and their families in a private classroom or LMS. No resale, public posting, or redistribution of the complete toolkit. This is general instructional planning, not individualized clinical, legal, or crisis guidance.')]
 for h,t in notes:
  y=b.text(h+': '+t,48,y,size=10.4)-15
 pages=b.finish();return {'id':slug,'title':title+' Toolkit','objective':goal,'pdf':str(b.path.relative_to(ROOT)),'pages':pages,'topicIndex':index}

if __name__=='__main__':
 rows=[]
 for i,t in enumerate(TOPICS):
  row=build_topic(t,i);rows.append(row);print(row['id'],row['pages'],flush=True)
 (TMP/'teacher-build-report.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
