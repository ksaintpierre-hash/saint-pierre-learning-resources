"""Render every paid PDF for visual QA; publish only cover and student sample."""
from pathlib import Path
from pypdf import PdfReader
from PIL import Image, ImageDraw
import subprocess,json,base64,os
r=Path(__file__).resolve().parents[1]; q=r/'output/catalog-qa';q.mkdir(parents=True,exist_ok=True)
renderer=os.environ.get('PDFTOPPM','pdftoppm')
cat=json.loads((r/'data/catalog.json').read_text()); assets={}
for p in cat:
 slug=p['id'];f=r/'output/pdf'/f'{slug}.pdf';reader=PdfReader(f);p['pages']=len(reader.pages)
 subprocess.run([renderer,'-scale-to','1500','-png',str(f),str(q/slug)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 pages=sorted(q.glob(slug+'-[0-9]*.png'))
 assert len(pages)==len(reader.pages)
 (r/'public/product-thumbnails'/f'{slug}.png').write_bytes(pages[0].read_bytes())
 sample=3 if slug=='fl-grade5-theme' else 2
 assert 'Student Directions' in reader.pages[sample].extract_text()
 (r/'public/product-previews'/f'{slug}.png').write_bytes(pages[sample].read_bytes())
 assets[slug]=base64.b64encode(f.read_bytes()).decode()
 sheet=Image.new('RGB',(1200,((len(pages)+2)//3)*550),'#dbe2e8');d=ImageDraw.Draw(sheet)
 for i,page in enumerate(pages):
  im=Image.open(page);im.thumbnail((390,510));x=i%3*400;y=i//3*550;sheet.paste(im,(x,y+24));d.text((x+10,y+5),f'{slug} / page {i+1}',fill='black')
 sheet.save(q/f'{slug}-sheet.jpg')
 print(slug,len(pages))
(r/'data/catalog.json').write_text(json.dumps(cat,indent=2)+'\n')
(r/'server/private-products.ts').write_text('// Server-only migration payload. Never import from client components.\nexport const privateProducts: Record<string,string> = '+json.dumps(assets)+';\n')
import subprocess, sys
subprocess.run([sys.executable, str(r/'scripts/package_legacy_resources.py')], check=True)
