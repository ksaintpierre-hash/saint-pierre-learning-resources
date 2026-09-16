from pathlib import Path
import json
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Flowable

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/pdf'; PUB=ROOT/'private-downloads'
OUT.mkdir(parents=True,exist_ok=True); PUB.mkdir(parents=True,exist_ok=True)

products=[
dict(slug='ca-grade4-multidigit',title='Multi-Digit Operations: Place-Value Strategies',level='Grade 4 • California',subject='Mathematics',standard='CA CCSS.MATH.CONTENT.4.NBT.B.4 — Fluently add and subtract multi-digit whole numbers using the standard algorithm.',source='California Department of Education: https://www2.cde.ca.gov/cacs/math?c2=4%2C1%2C1%2C2',price='$5.00',lesson='Use place value to estimate, add, subtract, and check multi-digit whole-number calculations.',items=['Estimate 38,472 + 16,905 to the nearest thousand.','46,728 + 9,563','80,004 − 27,856','A library had 48,736 books and added 6,895. How many now?','A stadium has 72,450 seats; 58,967 were filled. How many empty?','Find and correct: 63,210 − 18,475 = 45,835.','Write a four-digit addition problem with a sum greater than 12,000. Solve it.','Explain how addition can check subtraction.'],answers=['55,000','56,291','52,148','55,631','13,483','Correct answer: 44,735; the shown result is 1,100 too large.','Answers vary; example 7,250 + 5,100 = 12,350.','Add the difference to the subtrahend; the result should equal the minuend.']),
dict(slug='fl-grade5-theme',title='Theme Detectives: Evidence in Original Fiction',level='Grade 5 • Florida',subject='Reading',standard='ELA.5.R.1.2 — Explain the development of stated or implied theme(s) throughout a literary text.',source='Florida Department of Education B.E.S.T. ELA Standards: https://www.fldoe.org/core/fileparse.php/7539/urlt/elabeststandardsfinal.pdf',price='$5.00',lesson='Read an original story about a student repairing a community garden sign; trace how choices and consequences develop a theme.',items=['What challenge does Mina face?','Which action first suggests persistence?','State one possible theme.','Give two details that develop that theme.','How does the ending strengthen the theme?','Which detail would weaken the theme if removed? Explain.','Write a four-sentence objective summary.','Write a new ending that preserves the theme.'],answers=['The rain ruins Mina’s painted sign before the garden opening.','She dries the board and begins again instead of quitting.','Possible: steady effort and accepting help can overcome setbacks.','She restarts after the rain; she accepts neighbors’ spare paint and help.','The completed sign represents shared effort and resilience.','Reasoned responses using a relevant story detail.','Summary should include challenge, response, help, and outcome without opinion.','Answers vary but must show the same theme.']),
dict(slug='tx-grade7-elements-compounds',title='Elements & Compounds: Particle Evidence Lab',level='Grade 7 • Texas',subject='Science',standard='TEKS 7.6(A) — Compare and contrast elements and compounds in terms of atoms and molecules, chemical symbols, and chemical formulas.',source='Texas Education Agency TEKS Guide - Science 7.6A: https://teksguide.org/teks/s76a/overview',price='$6.00',lesson='Analyze particle models and formulas to distinguish elements from compounds.',items=['Classify O₂ as element or compound and explain.','Classify H₂O and name the kinds and number of atoms.','What does the 2 mean in CO₂?','Compare Na and NaCl.','A model has four identical N atoms. Element or compound?','A model has two molecules, each with two H and one O. Write the formula.','Explain why air is a mixture, not a compound.','Design a particle key for CO₂ and sketch three molecules.'],answers=['Element; it contains only oxygen atoms.','Compound; two hydrogen atoms and one oxygen atom.','Two oxygen atoms in each molecule.','Na is an element symbol; NaCl is a compound formula containing sodium and chlorine.','Element.','H₂O.','Its substances are physically combined in variable proportions.','Three groups, each with one carbon and two oxygen particles.']),
dict(slug='college-composition-claims',title='College Composition: Claims, Evidence & Reasoning',level='College • First-Year Writing',subject='English Composition',standard='Course objective — Develop a focused arguable thesis, evaluate evidence, and connect evidence to claims through explicit reasoning.',source='Course-level objective; no accreditation or universal equivalency claimed.',price='$7.00',lesson='Revise weak claims, evaluate source notes, and build an evidence-reasoning paragraph.',items=['Turn “School matters” into a focused arguable thesis.','Identify the claim in: Cities should extend library hours because evening access supports working learners.','Name one credibility question for a source.','Distinguish evidence from reasoning.','Write a counterclaim to the library-hours position.','Draft a concession sentence.','Order these paragraph moves: evidence, claim, analysis.','Write a 150-word argument using the provided fictional survey data: 68 of 100 evening students used the library after 6 p.m.'],answers=['Answers vary; must be specific, debatable, and supportable.','Cities should extend library hours.','Examples: author expertise, publication process, date, evidence, conflicts of interest.','Evidence supplies support; reasoning explains how support proves the claim.','A reasoned opposing position.','Acknowledges a valid limitation before reaffirming the claim.','Claim, evidence, analysis.','Rubric: clear thesis, accurate use of 68/100 data, reasoning, counterclaim, conventions.']),
dict(slug='college-algebra-linear',title='College Algebra: Linear Models in Context',level='College • Introductory Algebra',subject='Mathematics',standard='Course objective — Interpret slope and intercept, construct linear models, solve linear equations, and evaluate model limitations.',source='Course-level objective; no accreditation or universal equivalency claimed.',price='$7.00',lesson='Model constant-rate situations and interpret parameters with units.',items=['Find slope through (2,7) and (6,19).','Write the line with slope 4 and y-intercept −3.','Solve 5x−7=28.','A service costs $18 plus $6 per hour. Write C(h).','Interpret the intercept in C(h).','Find C(7).','At what h is C=72?','Why might a linear model fail for very large h?'],answers=['3','y=4x−3','x=7','C(h)=18+6h','$18 fixed starting fee.','$60','9 hours','Rates, capacity, discounts, or conditions may change outside the observed range.']),
dict(slug='college-biology-membranes',title='General Biology: Cell Membrane Transport',level='College • General Biology I',subject='Biology',standard='Course objective — Predict passive and active transport outcomes using concentration gradients, membrane properties, and energy requirements.',source='Course-level objective; no accreditation or universal equivalency claimed.',price='$7.00',lesson='Use concentration scenarios to compare diffusion, osmosis, facilitated diffusion, and active transport.',items=['Define concentration gradient.','Does simple diffusion require ATP?','Predict water movement: cell 2% solute, solution 8% solute.','Name transport through a channel protein down a gradient.','Why can ions not freely cross the lipid bilayer?','Which process moves solute against its gradient?','Predict a red blood cell in a strongly hypotonic solution.','Design a control for a dialysis-tubing investigation.'],answers=['A difference in concentration across space or a membrane.','No.','Water moves out of the cell toward the higher solute concentration.','Facilitated diffusion.','Their charge interacts poorly with the hydrophobic membrane interior.','Active transport; it requires energy.','Water enters; the cell swells and may lyse.','An identical setup with no concentration difference or without the tested solute.']),
dict(slug='college-psych-research',title='Intro Psychology: Research Methods & Ethics',level='College • Introductory Psychology',subject='Psychology',standard='Course objective — Distinguish research designs, identify variables and bias, interpret correlation cautiously, and apply core human-subject protections.',source='Course-level objective; no accreditation or universal equivalency claimed.',price='$6.00',lesson='Evaluate fictional studies without confusing correlation and causation.',items=['Define independent variable.','Define dependent variable.','What design best tests cause and effect?','A correlation is r=−0.78. Describe direction and strength.','Does correlation prove causation?','Identify bias in a voluntary online poll.','Why use random assignment?','Name two protections for human participants.'],answers=['The variable manipulated by the researcher.','The measured outcome.','A controlled experiment with appropriate assignment.','Strong negative association.','No; third variables and directionality remain possible.','Voluntary-response/self-selection bias.','To reduce systematic preexisting differences between groups.','Examples: informed consent, minimized risk, privacy, right to withdraw, debriefing.']),
dict(slug='spanish101-campus',title='Spanish 101: Campus Conversations',level='College • Spanish 101',subject='World Language',standard='Course objective — Exchange greetings and basic personal information and use common present-tense forms of ser, llamarse, and regular -ar verbs.',source='Course-level objective; no accreditation or universal equivalency claimed.',price='$6.00',lesson='Practice respectful greetings, introductions, and basic present-tense sentences.',items=['Translate: Good morning.','Complete: Yo ___ Katia. (llamarse)','Complete: Nosotros ___ estudiantes. (ser)','Conjugate estudiar for ella.','Ask “What is your name?” formally.','Respond: ¿De dónde eres?','Change to plural: Él estudia español.','Write a four-line introductory dialogue.'],answers=['Buenos días.','me llamo','somos','estudia','¿Cómo se llama usted?','Soy de…','Ellos estudian español.','Answers vary; should include greeting, name question/answer, and closing.']),
dict(slug='college-accounting-cycle',title='Financial Accounting: Transaction Analysis',level='College • Introductory Accounting',subject='Business',standard='Course objective — Analyze transactions using the accounting equation and explain changes in assets, liabilities, and equity.',source='Course-level objective; no accreditation or universal equivalency claimed.',price='$7.00',lesson='Track assets, liabilities, and equity through original small-business scenarios.',items=['Owner invests $8,000 cash. State equation effect.','Buy $1,200 equipment for cash.','Purchase $500 supplies on account.','Earn $900 cash revenue.','Pay $200 of accounts payable.','Pay $300 rent.','Compute ending assets after all six transactions.','Compute ending liabilities and equity.'],answers=['Assets +8,000; equity +8,000.','Cash −1,200; equipment +1,200; total assets unchanged.','Assets +500; liabilities +500.','Assets +900; equity +900.','Assets −200; liabilities −200.','Assets −300; equity −300.','Assets $8,900.','Liabilities $300; equity $8,600.']),
dict(slug='college-programming-python',title='Introduction to Programming: Python Decisions',level='College • Introductory Computer Science',subject='Computer Science',standard='Course objective — Trace variables and conditionals, write Boolean expressions, and create small input-process-output programs in Python.',source='Course-level objective; no accreditation or universal equivalency claimed.',price='$7.00',lesson='Trace and write short Python programs using if, elif, else, comparison, and Boolean operators.',items=['What prints? x=7; print(x+3)','Evaluate: 5 < 8 and 2 == 2','Write a condition for age at least 18.','What prints? n=4; print("even" if n%2==0 else "odd")','Find the bug: if score = 90:','Write code that prints “warm” when temp>75.','Why should input converted with int() be validated?','Trace: x=3; if x>5: x+=2; else: x*=2. What is x?'],answers=['10','True','age >= 18','even','Use == for comparison.','if temp > 75: print("warm")','Non-numeric input can raise an error; validation improves reliability.','6']),
]

pdfmetrics.registerFont(TTFont('DejaVu',str(ROOT/'scripts/fonts/DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVu-Bold',str(ROOT/'scripts/fonts/DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu',boldItalic='DejaVu-Bold')
styles=getSampleStyleSheet();
for style in styles.byName.values(): style.fontName='DejaVu'
navy=colors.HexColor('#17324D'); coral=colors.HexColor('#E97451'); gold=colors.HexColor('#E7B34B')
styles.add(ParagraphStyle(name='Cover',fontName='DejaVu-Bold',fontSize=34,leading=41,textColor=navy,spaceAfter=18))
styles.add(ParagraphStyle(name='H',fontName='DejaVu-Bold',fontSize=18,leading=23,textColor=navy,spaceAfter=12))
styles.add(ParagraphStyle(name='Body2',fontName='DejaVu',fontSize=10.5,leading=15,spaceAfter=8))

class ResourceCover(Flowable):
    width=528
    height=688
    def __init__(self,p):
        Flowable.__init__(self)
        self.width=528
        self.height=688
        self.p=p
    def draw(self):
        c=self.canv; p=self.p
        c.setFillColor(colors.HexColor('#137C82')); c.rect(0,675,528,7,fill=1,stroke=0)
        c.drawImage(str(ROOT/'public/brand/saint-pierre-logo.png'),0,592,width=72,height=72,preserveAspectRatio=True,mask='auto')
        c.setFillColor(navy); c.setFont('DejaVu-Bold',14)
        c.drawString(88,636,'SAINT PIERRE')
        c.setFont('DejaVu',11); c.drawString(88,616,'LEARNING RESOURCES')
        c.setFillColor(colors.HexColor('#137C82')); c.setFont('DejaVu-Bold',13)
        c.drawString(0,553,p['subject'].upper())
        title=p['title'].split(': ',1)
        main=Paragraph(escape(title[0]),styles['Cover']); _,h=main.wrap(510,200); main.drawOn(c,0,505-h)
        y=480-h
        if len(title)>1:
            sub=Paragraph(escape(title[1]),ParagraphStyle('subtitle',fontName='DejaVu',fontSize=22,leading=29,textColor=navy))
            _,sh=sub.wrap(510,120); sub.drawOn(c,0,y-sh); y-=sh+35
        c.setFillColor(colors.HexColor('#EAF3F4')); c.roundRect(0,225,528,62,8,fill=1,stroke=0)
        level=Paragraph(escape(p['level']),ParagraphStyle('level',fontName='DejaVu-Bold',fontSize=15,leading=20,textColor=navy))
        _,lh=level.wrap(484,48); level.drawOn(c,22,256-lh/2)
        c.setFillColor(navy); c.setFont('DejaVu-Bold',13); c.drawString(0,188,'INSIDE THIS RESOURCE')
        c.setFont('DejaVu',12)
        for i,line in enumerate(['Teacher guide and student practice','Assessment and answer key','Differentiation and accessibility supports']):
            c.drawString(0,158-i*23,line)
        c.setStrokeColor(colors.HexColor('#CAD8DF')); c.line(0,54,528,54)
        c.setFont('DejaVu-Bold',10); c.drawString(0,29,'PRINTABLE PDF  |  SINGLE-TEACHER LICENSE')
        c.setFont('DejaVu',10); c.drawString(0,9,'saintpierreresources.com')

def footer(canvas,doc):
    canvas.saveState(); canvas.setFont('Helvetica',8); canvas.setFillColor(colors.grey)
    canvas.drawString(40,25,'Saint Pierre Learning Resources | Single-teacher license | Original material')
    if doc.page > 1: canvas.drawImage(str(ROOT/'public/brand/saint-pierre-logo.png'),540,750,width=30,height=30,preserveAspectRatio=True,mask='auto')
    canvas.drawRightString(572,25,f'Page {doc.page}'); canvas.restoreState()

pedagogy=json.loads((ROOT/'data/pedagogy.json').read_text())
for p in products:
    guide=pedagogy[p['slug']]
    if p['slug']=='college-biology-membranes':
        p['items'][2]='Water can cross the membrane, but the solute cannot. Predict net water movement: cell 2% solute, solution 8% solute.'
    if p['slug']=='college-programming-python':
        p['items'][7]='Trace this rule: start with x=3; if x is greater than 5, add 2; otherwise multiply x by 2. What is x?'
    path=OUT/(p['slug']+'.pdf')
    doc=SimpleDocTemplate(str(path),pagesize=letter,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=42)
    story=[]
    story += [ResourceCover(p),PageBreak()]
    story += [Paragraph('Teacher Guide',styles['H'])]
    for label,value in [('Level',p['level']),('Standard / objective',p['standard']),('Source / course note',p['source']),('Before this lesson',guide['prerequisites']),('Model and discuss',guide['model']),('Watch for',guide['misconception'])]:
        story.append(Paragraph('<b>'+label+':</b> '+escape(value),styles['Body2']))
    story.append(Paragraph('<b>Suggested sequence:</b> 5-minute launch, 10-minute model, 20-30 minutes of practice, then a 5-minute exit ticket. Use separate paper for extended writing.',styles['Body2']))
    story.append(Paragraph('Learning supports',styles['H']))
    for label,value in guide['supports'].items():
        story.append(Paragraph('<b>'+label+':</b> '+escape(value),styles['Body2']))
    story.append(Paragraph('Adapt these suggestions to the current learning plan. Print on US Letter paper at actual size; keep the key separate. One teacher may use the resource with their own students; no public posting or resale.',styles['Body2']))
    story.append(PageBreak())
    if p['slug']=='fl-grade5-theme':
        story += [Paragraph('The Garden Sign',styles['H'])]
        for paragraph in [
            'Mina had promised to paint the welcome sign for the community garden. On Friday afternoon, she brushed green letters across a smooth board: EVERYONE CAN GROW HERE. She added tiny yellow flowers around the edge. The garden would open the next morning, and Mina wanted her sign to be the first thing visitors saw.',
            'She left the board outside while she went in to wash her brushes. A sudden shower rattled the windows. By the time she reached the porch, rain had dragged green paint down the board. The letters looked like tall weeds. Mina pressed her lips together. She had used nearly all her paint.',
            'For a moment, she imagined telling the neighbors that the sign was impossible. Instead, she carried the board inside, dried it with an old towel, and set it near the open window. When the wood was dry, she sanded the smeared letters and drew new pencil lines. Starting again did not feel exciting. It felt slow.',
            'Mr. Ortiz stopped by with garden stakes and noticed the board. He offered blue paint left from his fence. Mina almost refused. She wanted to finish the sign herself. Then she looked at her nearly empty jars and asked whether they could use his paint for the background.',
            'Soon Leila brought white paint, and two younger neighbors offered to fill in the flowers. Mina showed them how to wipe extra paint from their brushes. One flower turned into a large, uneven circle. Instead of covering it, Mina added a stem and made it the tallest blossom. The neighbors laughed and kept working.',
            'On Saturday morning, they carried the dry sign to the gate together. Its flowers were different sizes, and its blue background was not what Mina had planned. But the words were clear. When the first family arrived, a little boy read them aloud. Mina smiled at her neighbors. The sign did more than welcome people to the garden. It showed how the garden had begun.'
        ]: story += [Paragraph(paragraph,styles['Body2'])]
        story += [Paragraph('Original fiction written for this resource. Use details from the beginning, middle, and ending to explain how a theme develops.',styles['Body2']),PageBreak()]
    story += [Paragraph('Student Directions & Practice',styles['H']),Paragraph(p['lesson'],styles['Body2']),Paragraph('Directions: Complete every item. Show work or cite evidence. For open responses, answer in complete sentences.',styles['Body2'])]
    for i,q in enumerate(p['items'],1): story += [Paragraph(f'<b>{i}.</b> {escape(q)}',styles['Body2']),Spacer(1,18)]
    story += [PageBreak(),Paragraph('Assessment / Exit Ticket',styles['H']),Paragraph('Work independently. Show your reasoning. Use extra paper if needed.',styles['Body2'])]
    for i,q in enumerate(guide['exitItems'],1):
        story += [Paragraph(f'<b>{i}.</b> '+escape(q),styles['Body2']),Spacer(1,80)]
    story += [Paragraph('<b>Reflection:</b> What helped you decide? What do you want to practice next?',styles['Body2']),Spacer(1,45),Paragraph('Score each task: 2 = accurate with clear reasoning; 1 = partly correct or missing reasoning; 0 = incorrect or no evidence. The reflection is not scored.',styles['Body2']),PageBreak(),Paragraph('Answer Key & Teaching Guidance',styles['H'])]
    for i,a in enumerate(p['answers'],1): story += [Paragraph(f'<b>{i}.</b> {escape(a)}',styles['Body2'])]
    story += [Spacer(1,12),Paragraph('Exit ticket guidance',styles['H'])]
    for i,a in enumerate(guide['exitAnswers'],1):
        story.append(Paragraph(f'<b>{i}.</b> '+escape(a),styles['Body2']))
    story.append(Paragraph('<b>Next teaching move:</b> Use the worked model again if the concept is unclear. If the answer is correct but reasoning is incomplete, ask for an explanation. Offer the extension once both tasks are secure. Scores guide instruction; they are not standardized mastery cutoffs.',styles['Body2']))
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    (PUB/path.name).write_bytes(path.read_bytes())
print(f'created {len(products)} PDFs')
