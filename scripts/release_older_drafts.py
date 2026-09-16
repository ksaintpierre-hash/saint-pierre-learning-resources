"""Release copies of the ten September 14 drafts; preserve their historical originals."""
from pathlib import Path
import ast, json, re, html
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'resources/released-2026-09-15'; OUT.mkdir(parents=True,exist_ok=True)
tree=ast.parse((ROOT/'scripts/generate_daily_products_2026_09_14.py').read_text())
scope={}
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['NC_SOURCE','P'] for t in node.targets):
        exec(compile(ast.Module(body=[node],type_ignores=[]),'<draft-content>','exec'),scope)
products=scope['P']
pdfmetrics.registerFont(TTFont('Release','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('ReleaseBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('Release',normal='Release',bold='ReleaseBold')
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
ink=colors.HexColor('#1b2f49');teal=colors.HexColor('#30666c');pale=colors.HexColor('#edf4f5')
body=ParagraphStyle('Body',fontName='Release',fontSize=11,leading=15,spaceAfter=8,textColor=ink)
small=ParagraphStyle('Small',parent=body,fontSize=9,leading=12)
heading=ParagraphStyle('Heading',parent=body,fontName='ReleaseBold',fontSize=20,leading=25,spaceAfter=18)
title=ParagraphStyle('Title',parent=heading,fontSize=29,leading=35,spaceAfter=22)
LOGO=ROOT/'public/brand/saint-pierre-logo.png'
def markup(text):
    return re.sub(r'[\u3400-\u9fff]+',lambda m:'<font name="STSong-Light">'+m[0]+'</font>',html.escape(text))
def para(text,style=body):return Paragraph(markup(text),style)
def brand(c,d):
    c.saveState();c.drawImage(ImageReader(str(LOGO)),42,736,48,34,preserveAspectRatio=True,mask='auto')
    c.setFont('ReleaseBold',8);c.setFillColor(ink);c.drawString(100,751,'SAINT PIERRE LEARNING RESOURCES')
    c.setStrokeColor(teal);c.line(42,42,570,42);c.setFont('Release',8)
    c.drawString(42,28,'© 2026 Saint Pierre Learning Resources | Single-teacher license');c.drawRightString(570,28,str(d.page));c.restoreState()

for p in products:
    if p['slug']=='nc-g3-two-step-task-cards':
        p['qs'][3]=('A garden has 7 rows with 9 plants each. Three plants in each row do not bloom. How many plants bloom?','7 × (9 − 3) = 42 blooming plants.')
        p['qs'][9]=('A baker makes 72 rolls and sells 4 trays with 8 rolls each. How many rolls remain?','72 − 4 × 8 = 40 rolls remain.')
    if p['slug']=='nc-g5-multiplication-warmups':
        p['qs'][7]=('Check this answer: 63 × 27 = 1,071. Show correct partial products.','63 × 20 = 1,260; 63 × 7 = 441; total 1,701. The final answer alone does not show which step was mistaken.')
    if p['slug']=='college-french101-cafe':
        p['title']='French 101 Café Conversations'
        p['qs'][1]=('Complete: Je ___ étudiante.','suis')
        p['qs'][2]=('Complete with avoir: Nous ___ deux cafés.','avons')
        p['qs'][3]=('Say: I would like a tea, please.','Je voudrais un thé, s’il vous plaît.')
        p['qs'][7]=('Translate: The bill, please.','L’addition, s’il vous plaît.')
        p['qs'][9]=('Write an indefinite plural: un café.','des cafés')
        p['qs'][10]=('Put in order: voudrais / je / de l’eau.','Je voudrais de l’eau.')
        p['qs'][14]=('Translate: We have a reservation.','Nous avons une réservation.')
        p['standard']=p['standard'].replace('etre','être');p['source']='Course objective; grammar reference: https://www.laits.utexas.edu/tex/index.html. Original practice; no affiliation.'
    if p['slug']=='college-german101-introductions':
        p['qs'][1]=('Complete with heißen: Ich ___ Katia.','heiße (heisse is the Swiss spelling).')
        p['qs'][3]=('Ask informally: What is your name?','Wie heißt du?')
        p['qs'][13]=('Say you are learning English.','Ich lerne Englisch.')
        p['standard']=p['standard'].replace('heissen','heißen')
    if p['slug']=='college-mandarin101-campus':
        p['rtype']='Language practice cards'
        p['qs'][0]=('你好 (nǐ hǎo) means?','Hello. In speech, the first third tone changes before another third tone.')
        p['qs'][1]=('谢谢 (xièxie) means?','Thank you; the second syllable is neutral tone.')
        p['qs'][2]=('你叫什么名字？(Nǐ jiào shénme míngzi?) asks what?','What is your name?')
        p['qs'][3]=('Translate: 我叫 Katia。(Wǒ jiào Katia.)','My name is Katia.')
        p['qs'][4]=('Write tone-marked pinyin for 再见.','zàijiàn')
        p['qs'][7]=('Translate: 我是学生。(Wǒ shì xuésheng.)','I am a student.')
        p['qs'][8]=('Which pronoun means I/me: 我 (wǒ) or 你 (nǐ)?','我 (wǒ)')
        p['qs'][9]=('Which pronoun means you?','你 (nǐ)')
        p['qs'][11]=('Write: Nice to meet you. Include tone-marked pinyin.','很高兴认识你。Hěn gāoxìng rènshi nǐ.')
        p['qs'][12]=('Count 1–5 in tone-marked pinyin.','yī, èr, sān, sì, wǔ')
        p['qs'][13]=('What does 是 (shì) do in the model 我是学生?','Links the subject to a noun identifying them. Do not insert 是 before every adjective.')
        p['standard']='Course objective - Interpret basic greetings, name questions, identity sentences, and selected numbers using characters and tone-marked pinyin.'
    if p['slug']=='college-asl101-classroom':
        p['title']='ASL 101 Classroom Communication Reflection Guide';p['rtype']='Reflection and discussion guide'
        p['standard']='Course objective - Explain visual-attention norms and reflect on fingerspelling and classroom exchanges after qualified live or video instruction.'
        p['focus']='Reflect on visual communication, fingerspelling habits, and classroom interaction after an ASL lesson. This is a text-based companion, not an illustrated sign dictionary or standalone signing course.'
        p['source']='Instructor-led prerequisite. ASL University reference: https://www.lifeprint.com/asl101/topics/parameters-asl.htm. No affiliation or endorsement.'
    if p['slug']=='college-art-composition':
        p['source']='Original discussion and drawing prompts. Learners create two abstract sketches on separate paper; no artwork reproductions or ready-made composition studies are included.'
        p['focus']='Use art vocabulary to compare and revise two abstract sketches you create: one calm composition and one crowded or tense composition.'
    if p['slug']=='college-engineering-design':
        p['focus']='Design a paper structure using at most 10 sheets, supporting 500 g for 10 seconds on a low tabletop. Record three trials, inspect failures, and justify one redesign. Use small classroom-safe weights under instructor supervision.'
    s=[Spacer(1,45),para(p['subject'].upper(),small),para(p['title'],title),para(p['level']+' | '+p['rtype']),Spacer(1,20),para(p['focus']),Spacer(1,35),para('INSIDE THIS RESOURCE',heading),para('Teacher guidance • 16 practice prompts • Reflection exit ticket • Complete answer guidance'),Spacer(1,20),para('Print the practice pages separately from the teacher key. Provide extra paper for extended work.'),PageBreak()]
    s += [para('Teacher guide',heading),para(p['standard']),para('Suggested time: '+p['time']),para('Learning focus: '+p['focus']),para('Teaching sequence: Review prior instruction and model the first prompt with its answer. Assign one four-prompt page at a time. Ask for a check, a reason, or a specific example. Use the reflection ticket to plan the next lesson; it is not a standardized mastery score.')]
    if p['slug']=='nc-g5-multiplication-warmups':s.append(para('Five-day schedule: prompts 1–3, 4–6, 7–9, 10–12, then 13–16. Use separate paper for algorithms.'))
    s += [para('Model prompt: '+p['qs'][0][0]),para('Model answer: '+p['qs'][0][1]),para('Support options',heading),para('AIG: justify a second method or create a transfer example. 504: follow the learner’s plan for time, breaks, format, and reduced copying. EC: model steps and accept aligned oral, drawn, or written responses. ESL: preview vocabulary, use bilingual references, and rehearse before writing.'),para('Source and scope: '+p['source'],small),PageBreak()]
    for start in range(0,16,4):
        s += [para('Practice '+str(start+1)+'–'+str(start+4),heading),para('Show work or explain your response. Use additional paper when needed. Teachers may cut apart the four bordered prompts.')]
        for i,(q,a) in enumerate(p['qs'][start:start+4],start+1):
            card=Table([[para(str(i)+'. '+q)]],colWidths=[510],rowHeights=[115]);card.setStyle(TableStyle([('BOX',(0,0),(-1,-1),.6,teal),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),10)]));s += [card,Spacer(1,10)]
        s.append(PageBreak())
    s += [para('Reflection exit ticket',heading),para('Complete independently. Refer to your completed practice, but explain in your own words. This checks reflection and application, not a test score prediction.')]
    exits=['State the focus of this resource in your own words.','Create one accurate example connected to the practice.','Explain how you checked that example.','Identify one possible error and show a correction.','Name one specific next practice step and explain why it will help.']
    for i,q in enumerate(exits,1):s += [para(str(i)+'. '+q),Spacer(1,57)]
    s += [PageBreak(),para('Teacher answer guidance',heading)]
    for i,(q,a) in enumerate(p['qs'],1):s.append(para(str(i)+'. '+a,small))
    s += [para('Reflection criteria',body),para('Items 1–4: 2 points for an accurate, specific response; 1 for a partly correct response; 0 for a missing or unrelated response. Accept justified alternatives. Item 5 is an unscored planning reflection. Feedback should identify a next teaching move, not label a learner.',small),para('Single-teacher license: use with your own learners in class or a restricted LMS. Do not resell, redistribute complete files, or post them publicly. All questions and explanations are original.',small)]
    SimpleDocTemplate(str(OUT/(p['slug']+'.pdf')),pagesize=(612,792),leftMargin=48,rightMargin=48,topMargin=80,bottomMargin=58).build(s,onFirstPage=brand,onLaterPages=brand)
(OUT/'metadata.json').write_text(json.dumps(products,ensure_ascii=False,indent=2))
print('Prepared ten corrected release PDFs; historical drafts unchanged.')
