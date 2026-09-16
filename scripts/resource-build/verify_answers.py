"""Recompute arithmetic from authored question strings, independently of answer construction."""
from pathlib import Path
from fractions import Fraction as F
import re,json,ast,math,statistics
from exam_content import verify

ROOT=Path(__file__).resolve().parents[2];TMP=ROOT/'tmp/resource-build'
def nums(s):return [F(x.replace(',','')) for x in re.findall(r'(?<![A-Za-z])[-−]?\d[\d,]*(?:\.\d+)?',s.replace('−','-'))]
def number(s):return F(s.strip().replace(',','').replace('−','-'))
def check(t):
 q=t['q'];a=t['answer'];k=t['skill'];n=nums(q);expected=None
 if k=='equal-groups':expected=n[0]/n[1] if 'places' in q else n[0]*n[1]
 elif k=='two-step':expected=n[0]*n[1]+(n[2] if 'receives' in q else -n[2])
 elif k in ['place-add','multi-add']:expected=n[0]+n[1] if '+' in q else n[0]-abs(n[1])
 elif k=='fraction-model':assert number(a)==n[1]/n[0];return
 elif k in ['tile-area','partial-products','standard-multiply']:expected=n[0]*n[1]
 elif k=='division-remainders':assert nums(a)==[n[0]//n[1],n[0]%n[1]];return
 elif k=='like-fractions':
  fs=[F(x) for x in re.findall(r'\d+/\d+',q)];expected=fs[0]+fs[1] if '+' in q else fs[0]-fs[1];assert F(a)==expected;return
 elif k=='area-perimeter':assert nums(a)==[n[0]*n[1],2*(n[0]+n[1])];return
 elif k=='decimal-money':expected=n[2]-n[0]-n[1];assert F(a.replace('$',''))==expected;return
 elif k=='unlike-fractions':assert F(a.split()[0])==sum(F(x) for x in re.findall(r'\d+/\d+',q));return
 elif k=='fraction-sharing':assert F(a.split()[0])==n[0]/n[1];return
 elif k=='prism-volume':expected=n[0]*n[1]*n[2]
 elif k=='ratio-tables':expected=n[0]/n[1]*n[2]
 elif k=='percent-benchmarks':expected=n[0]*n[1]/100
 elif k=='one-step-equations':
  equation=q.split('Solve ',1)[1].split('. Show')[0];left,right=equation.split(' = ')
  expected=F(right)-F(left.split(' + ')[1]) if ' + ' in left else F(right)/F(left.replace('x',''))
  assert F(a.split(' = ')[1])==expected;return
 elif k=='triangle-area':expected=n[0]*n[1]/2
 elif k=='center-spread':
  left,right=re.findall(r'Set [AB]: ([\d, ]+)\.',q);sets=[[int(x) for x in text.split(',')] for text in [left,right]]
  ex=[]
  for data in sets:ex += [F(sum(data),len(data)),F(statistics.median(data)),F(max(data)-min(data))]
  assert nums(a)==ex,(a,ex);return
 elif k=='proportion-models':
  pairs=ast.literal_eval(q[q.index('['):q.index(']')+1]);ratios=[F(y,x) for x,y in pairs]
  assert a.startswith('Yes')==(len(set(ratios))==1);return
 elif k=='signed-change':expected=n[0]+(n[1] if 'increases' in q else -n[1])
 elif k=='multi-step-equations':expected=(n[2]-n[0])/n[1]
 elif k=='circle-measures':assert nums(a)==[2*n[0],2*n[0],n[0]**2];return
 elif k=='chance-models':assert [F(x.strip()) for x in a.split(';')]==[n[0]/sum(n[:3]),(n[1]+n[2])/sum(n[:3])];return
 elif k=='both-sides':
  m=re.search(r'Solve (\d+)x \+ (\d+) = (\d+)x \+ \(?(-?\d+)\)?\.',q);aa,b,cc,d=map(int,m.groups())
  if aa==cc:assert a==('All real numbers' if b==d else 'No solution')
  else:assert F(a.split(' = ')[1])==F(d-b,aa-cc)
  return
 elif k=='linear-functions':
  pairs=[tuple(map(int,x)) for x in re.findall(r'\((\d+),(\d+)\)',q)];(x1,y1),(x2,y2)=pairs;m=F(y2-y1,x2-x1);inter=F(y1)-m*x1
  assert nums(a)==[m,inter];return
 elif k=='right-triangles':expected=F(math.isqrt(int(n[0]**2+n[1]**2)));assert expected**2==n[0]**2+n[1]**2
 elif k=='scatter-data':
  pairs=ast.literal_eval(q[q.index('['):q.index(']')+1]);xs,ys=zip(*pairs);xm=statistics.mean(xs);ym=statistics.mean(ys);cov=sum((x-xm)*(y-ym) for x,y in pairs)
  assert a.startswith('Positive' if cov>0 else 'Negative');return
 elif k=='integer-exponents':
  powers=[tuple(map(int,x)) for x in re.findall(r'(\d+)\^(\d+)',q)]
  (base,m),(other,n)=powers;assert base==other;expected=F(base)**(m+n if 'as one power and evaluate it. Explain using repeated factors' in q else m-n)
  assert F(a.split(' = ')[1])==expected;return
 else:raise ValueError(k)
 assert nums(a)[0]==expected,(k,q,a,expected)

counts={'mathItems':0,'examItems':0}
for path in sorted(TMP.glob('nc-g*-teaching-bundle.json')):
 d=json.loads(path.read_text());items=d['models']+d['cards']+d['warmups']+d['classwork']+d['exit']+sum(d['seasonal'].values(),[])+sum(d['sub'].values(),[])
 for t in items:
  try:check(t)
  except Exception as e:raise AssertionError((path.name,t)) from e
 counts['mathItems']+=len(items)
for path in sorted(TMP.glob('sat-act-*-math-skill-builder.json')):
 d=json.loads(path.read_text());items=d['models']+d['practice']+d['transfer']+d['exit']
 for t in items:verify(t)
 counts['examItems']+=len(items)
(TMP/'answer-check.json').write_text(json.dumps(counts,indent=2));print(json.dumps(counts))
