"""Original, deterministic mathematics content. No released assessment items.

Generators return worked reasoning plus independently checkable contracts.
Seeded variation changes contexts and quantities; each product has a distinct
instructional focus. These are teaching bundles, never full EOG replicas.
"""
from fractions import Fraction as F
import random, math

SOURCE='https://www.dpi.nc.gov/documents/publications/catalog/ma196-vertical-progression-math/open'
SPECS='https://www.dpi.nc.gov/documents/accountability/testing/eog/eog-mathematics-grades-3-8-test-specifications'
PROFILES=[
 (3,'equal-groups','Equal Groups and Fair Shares','NC.3.OA.3','Connect equal groups, multiplication, and division.','Draw one box for each group. Put the same number of marks in every box. Count all marks to check the product.'),
 (3,'two-step','Two Decisions, One Story','NC.3.OA.8','Represent and solve two-step stories.','Name what each operation finds. Solve the first question before using its answer in the second step.'),
 (3,'place-add','Build and Regroup to 1,000','NC.3.NBT.2','Explain addition and subtraction with place value.','Decompose hundreds, tens, and ones. Trade one ten for ten ones when needed. Check subtraction with addition.'),
 (3,'fraction-model','Fractions on Strips and Number Lines','NC.3.NF.2','Connect equal parts with fraction notation.','Choose a whole and partition it equally. The denominator counts all equal parts; the numerator counts selected parts.'),
 (3,'tile-area','Tile It, Split It, Find the Area','NC.3.MD.7','Connect tiled rectangles with multiplication.','Draw equal rows of unit squares. Multiply row count by squares in each row. Split a rectangle to check by addition.'),
 (4,'multi-add','Regrouping with Large Numbers','NC.4.NBT.4','Explain multi-digit addition and subtraction.','Align equal place values, record each regroup, and use an estimate and inverse operation to check the result.'),
 (4,'partial-products','Partial Products, Clear Thinking','NC.4.NBT.5','Connect area models with partial products.','Split a factor by place value. Multiply each part and combine partial products. Label the pieces in an area model.'),
 (4,'division-remainders','Division with Meaningful Remainders','NC.4.NBT.6','Explain whole-number division and remainders.','Build useful multiples of the divisor. Subtract partial groups. Check dividend = divisor × quotient + remainder.'),
 (4,'like-fractions','Join and Separate Fraction Parts','NC.4.NF.3','Add and subtract like-denominator fractions.','Use parts of the same size and the same whole. Join or remove parts, keeping the denominator unchanged.'),
 (4,'area-perimeter','Same Area, Different Borders','NC.4.MD.3','Distinguish area from perimeter.','Area counts square units inside; perimeter measures distance around. Draw and label a rectangle before calculating.'),
 (5,'standard-multiply','Multiplication with a Reasonableness Check','NC.5.NBT.5','Use multi-digit multiplication accurately.','Multiply by the ones and tens separately. Shift the tens product by one place. Add and compare with an estimate.'),
 (5,'decimal-money','Decimal Decisions at the Supply Desk','NC.5.NBT.7','Use decimal place value in contextual operations.','Align decimal places when combining amounts. Estimate with whole dollars, then check the exact cents.'),
 (5,'unlike-fractions','Related Denominators, Shared Units','NC.5.NF.1','Use equivalent fractions to combine unlike parts.','Rename fractions with related denominators using equal-sized parts. Combine numerators and simplify.'),
 (5,'fraction-sharing','Sharing Quantities Fairly','NC.5.NF.3','Interpret division as a fraction.','Draw the amount being shared. Divide each whole into equal shares; combine each person’s parts.'),
 (5,'prism-volume','Pack the Prism','NC.5.MD.5','Connect layers of cubes with volume.','Count cubes in a base layer, then multiply by the number of layers. State volume in cubic units.'),
 (6,'ratio-tables','Ratio Tables That Tell a Story','NC.6.RP.3','Use unit rates and equivalent ratios.','Find the amount per one unit. Multiply both quantities by the same scale factor and label units.'),
 (6,'percent-benchmarks','Percent Benchmarks in Action','NC.6.RP.4','Find parts using percent benchmarks.','Think of percent as parts per hundred. Build useful amounts from 10%, 25%, or 50%, then check against the whole.'),
 (6,'one-step-equations','Balance a One-Step Equation','NC.6.EE.7','Write and solve one-step equations.','Undo the operation on the unknown by applying the same inverse operation to both sides. Substitute to verify.'),
 (6,'triangle-area','Triangles from Rectangles','NC.6.G.1','Use decomposition to find triangle area.','Pair two congruent triangles to form a rectangle. A triangle has half the area of that base-height rectangle.'),
 (6,'center-spread','Center and Spread Data Lab','NC.6.SP.3','Compare center and variability in data.','Order the data. Find the median and mean, then describe spread so the typical value has context.'),
 (7,'proportion-models','Proportional or Not?','NC.7.RP.2','Identify and represent proportional relationships.','Compare y/x at nonzero x values. A constant ratio gives y = kx and a graph through the origin.'),
 (7,'signed-change','Signed Numbers, Real Changes','NC.7.NS.1','Interpret rational-number sums and differences.','Choose zero and a positive direction. Represent gains and losses with signs. Subtracting a negative reverses its direction.'),
 (7,'multi-step-equations','Equations from Quantities','NC.7.EE.4','Model and solve multi-step equations.','Define the unknown with units. Undo addition before multiplication, or expand first. Substitute the answer into the original equation.'),
 (7,'circle-measures','Radius, Border, and Circle Area','NC.7.G.4','Distinguish circumference and circle area.','Label radius and diameter first. Use C = 2πr for the border and A = πr² for the interior.'),
 (7,'chance-models','Build a Fair Probability Model','NC.7.SP.7','Use equally likely outcomes to model chance.','List the equally likely outcomes. Probability is favorable outcomes divided by all outcomes. Check that probabilities total one.'),
 (8,'both-sides','Variables on Both Sides','NC.8.EE.7','Solve and classify linear equations.','Collect variable terms on one side and constants on the other. An always-true statement has infinitely many solutions; a contradiction has none.'),
 (8,'linear-functions','A Rate and a Starting Value','NC.8.F.4','Build and interpret linear models.','Find change in y divided by change in x. Use a point to find the starting value in y = mx + b.'),
 (8,'right-triangles','Right-Triangle Route Planner','NC.8.G.7','Use the Pythagorean theorem and its converse.','Identify the hypotenuse opposite the right angle. Square the legs, add, and take the square root to find the hypotenuse.'),
 (8,'scatter-data','Patterns in Paired Data','NC.8.SP.1','Represent and describe bivariate associations.','Plot one point for each pair. Describe direction, shape, and unusual points. Association alone does not establish cause.'),
 (8,'integer-exponents','Exponent Rules with Reasons','NC.8.EE.1','Generate equivalent exponential expressions.','Write small powers as repeated factors. Multiplying like bases adds exponents; dividing subtracts them when the base is nonzero.'),
]

CONTEXTS={
 'core':['art club','school garden','library team','music club','community center','science club','reading group','design team'],
 'fall':['autumn reading fair','fall garden club','September art display','leaf observation team','October book drive'],
 'winter':['winter reading club','indoor garden project','December art display','January puzzle club','winter supply drive'],
 'spring':['spring reading fair','seedling club','March art display','April science team','spring book swap'],
 'summer':['summer library club','community garden','June art workshop','July puzzle camp','summer supply team'],
 'sub':['classroom supply team','library helpers','school art team','student design group'],
 'emergency':['paper puzzle team','classroom book group','desk-supply team','quiet design team'],
}

def fmt(v):
 if isinstance(v,F): return str(v.numerator) if v.denominator==1 else f'{v.numerator}/{v.denominator}'
 if isinstance(v,float): return f'{v:.2f}'.rstrip('0').rstrip('.')
 return str(v)

def task(p,seed,section='core'):
 g,k,title,code,obj,strategy=p;r=random.Random(seed); a=r.randint(2,9);b=r.randint(2,8);c=r.randint(2,7);mode=seed%4
 context=r.choice(CONTEXTS.get(section,CONTEXTS['core'])); diagram=None;numeric=None
 def item(q,answer,work,diagram=None,numeric=None):
  return {'q':q,'answer':str(answer),'work':work,'diagram':diagram,'numeric':numeric,'skill':k}
 if k=='equal-groups':
  n=a*b
  if mode%2: return item(f'The {context} places {n} cards equally into {a} folders. How many cards go in each folder? Draw a model and write an equation.',b,f'{n} ÷ {a} = {b}; {a} groups of {b} make {n}.',numeric=n/a)
  return item(f'The {context} fills {a} folders with {b} cards each. How many cards are there altogether? Draw equal groups and write an equation.',n,f'{a} × {b} = {n}; add {b} a total of {a} times.',numeric=a*b)
 if k=='two-step':
  n=a*b+c if mode%2 else a*b-c
  verb=f'receives {c} more' if mode%2 else f'uses {c}'
  return item(f'The {context} has {a} packs of {b} cards and then {verb} cards. How many cards are there now? Label both steps.',n,f'First {a} × {b} = {a*b}. Then {a*b} {"+" if mode%2 else "−"} {c} = {n}.',numeric=n)
 if k in ['place-add','multi-add']:
  limit=450 if g==3 else 45000;x=r.randint(limit//3,limit);y=r.randint(limit//3,limit)
  if mode%2:q=f'{x+y:,} − {x:,}';ans=y;work=f'Subtract by place value: {x+y:,} − {x:,} = {y:,}. Inverse check: {y:,} + {x:,} = {x+y:,}.'
  else:q=f'{x:,} + {y:,}';ans=x+y;work=f'Combine equal place values and regroup: {x:,} + {y:,} = {x+y:,}. Check by subtracting {x:,}.'
  return item(f'Find {q}. Show a place-value method and a different check.',f'{ans:,}',work,numeric=ans)
 if k=='fraction-model':
  den=r.choice([2,3,4,6,8]);num=r.randint(1,den)
  return item(f'A strip is divided into {den} equal parts. {num} {"part is" if num==1 else "parts are"} shaded. Write the shaded fraction. Mark the same quantity on a number line from 0 to 1.',f'{num}/{den}',f'Each part is 1/{den}. {num} {"copy makes" if num==1 else "copies make"} {num}/{den}. The point is {num} equal {"step" if num==1 else "steps"} of size 1/{den} from zero.',{'type':'fraction','n':num,'d':den})
 if k=='tile-area':
  return item(f'A rectangular display for the {context} measures {a} units by {b} units. Draw unit-square rows, find the area, and show a split-and-add check.',f'{a*b} square units',f'{a} × {b} = {a*b}. One split gives ({a-1} × {b}) + (1 × {b}) = {(a-1)*b} + {b} = {a*b}.',{'type':'rectangle','w':a,'h':b},a*b)
 if k in ['partial-products','standard-multiply']:
  x=r.randint(12,98) if mode<2 else r.randint(102,398);y=r.randint(2,9) if g==4 and x>99 else r.randint(12,29)
  parts=f'{x} × {y//10*10} + {x} × {y%10} = {x*(y//10*10)} + {x*(y%10)}' if y>=10 else f'({x//10*10} × {y}) + ({x%10} × {y}) = {x//10*10*y} + {x%10*y}'
  return item(f'The {context} packs {x} cards in each of {y} boxes. Find the total. Show partial products and explain why they can be added.',x*y,f'{parts} = {x*y}. The parts account for every box or card exactly once.',numeric=x*y)
 if k=='division-remainders':
  divisor=b;quo=r.randint(12,79);rem=r.randint(1,b-1);n=divisor*quo+rem
  return item(f'{n} counters are shared equally among {divisor} groups. Each group must get a whole number. How many per group and how many left? Show a partial-quotient strategy.',f'{quo} each; {rem} left',f'{n} = {divisor} × {quo} + {rem}; {rem} is smaller than {divisor}. Use {quo//10*10} groups, then {quo%10} more.',numeric=quo)
 if k=='like-fractions':
  d=r.choice([4,5,6,8,10,12]);u=r.randint(1,d-1);v=r.randint(1,d-1);sign='+' if mode%2 else '−';num=u+v if mode%2 else abs(u-v);hi=max(u,v);lo=min(u,v);q=f'{u}/{d} + {v}/{d}' if mode%2 else f'{hi}/{d} − {lo}/{d}'
  return item(f'Find {q}. Use equal-sized parts of the same whole and draw a fraction model.',fmt(F(num,d)),f'{q} = {num}/{d} = {fmt(F(num,d))}. Only the number of parts changes; the size stays 1/{d}.')
 if k=='area-perimeter':
  w=a+3;h=b+2
  return item(f'A rectangular reading space is {w} m long and {h} m wide. Find its area and perimeter. Which answer measures floor covering, and which measures a border?',f'{w*h} m²; {2*(w+h)} m',f'Area = {w} × {h} = {w*h} m² for covering. Perimeter = 2({w}+{h}) = {2*(w+h)} m for the border.',{'type':'rectangle','w':w,'h':h})
 if k=='decimal-money':
  x=r.randint(115,985);y=r.randint(110,990);cash=((x+y)//100+3)*100;ans=F(cash-x-y,100)
  return item(f'The {context} buys supplies costing ${x/100:.2f} and ${y/100:.2f}. It pays ${cash/100:.2f}. Find the change and show a decimal-place check.',f'${float(ans):.2f}',f'Total: ${x/100:.2f} + ${y/100:.2f} = ${(x+y)/100:.2f}. Change: ${cash/100:.2f} − ${(x+y)/100:.2f} = ${float(ans):.2f}.',numeric=float(ans))
 if k=='unlike-fractions':
  d,D=r.choice([(2,4),(4,8),(3,6),(6,12),(5,10)]);u=r.randint(1,d-1);v=r.randint(1,D-1);ans=F(u,d)+F(v,D)
  return item(f'A project uses {u}/{d} m of ribbon and then {v}/{D} m more. How much ribbon is used? Draw a length model with equal-size parts.',fmt(ans)+' m',f'{u}/{d} = {u*(D//d)}/{D}. Add: ({u*(D//d)}+{v})/{D} = {fmt(ans)} m.')
 if k=='fraction-sharing':
  return item(f'{a} identical paper strips are shared equally among {b} students. How much of one strip does each student receive? Draw and label a sharing model.',fmt(F(a,b))+' of a strip',f'{a} ÷ {b} = {a}/{b} = {fmt(F(a,b))}. Split each strip into {b} equal parts; each student gets {a} such parts.')
 if k=='prism-volume':
  return item(f'A storage prism for the {context} measures {a} cm by {b} cm by {c} cm. Find its volume. Explain the number of unit cubes in one layer and the number of layers.',f'{a*b*c} cm³',f'One layer has {a} × {b} = {a*b} cubes. {c} layers give {a*b} × {c} = {a*b*c} cm³.',{'type':'prism','w':a,'h':b,'d':c},a*b*c)
 if k=='ratio-tables':
  total=a*b;target=c+5
  return item(f'The {context} uses {total} labels for {a} equal kits. At the same rate, how many labels are needed for {target} kits? Make a ratio table including one kit.',f'{b*target} labels',f'Unit rate: {total} ÷ {a} = {b} labels/kit. Table pairs: (1,{b}), ({a},{total}), ({target},{b*target}).',numeric=b*target)
 if k=='percent-benchmarks':
  whole=r.choice([40,60,80,120,160,200]);pct=r.choice([5,10,15,20,25,30,50,75]);part=F(whole*pct,100)
  return item(f'Of {whole} supplies, {pct}% are set aside for a class project. How many are set aside? Show a benchmark-percent strategy.',fmt(part),f'{pct}% = {pct}/100. {whole} × {pct}/100 = {fmt(part)}. For example, 10% of {whole} is {whole/10:g}; combine convenient benchmark parts.',numeric=float(part))
 if k=='one-step-equations':
  x=F(r.randint(4,24),2);pval=F(r.randint(2,16),2)
  if mode%2:q=f'x + {fmt(pval)} = {fmt(x+pval)}';work=f'Subtract {fmt(pval)} on both sides: x = {fmt(x)}. Check: {fmt(x)} + {fmt(pval)} = {fmt(x+pval)}.'
  else:q=f'{a}x = {fmt(a*x)}';work=f'Divide both sides by {a}: x = {fmt(x)}. Check: {a} × {fmt(x)} = {fmt(a*x)}.'
  return item(f'Solve {q}. Show the same operation on both sides, then substitute to check.',f'x = {fmt(x)}',work,numeric=float(x))
 if k=='triangle-area':
  return item(f'A triangular display has base {2*a} cm and perpendicular height {b} cm. Find the area. Explain why multiplying base by height alone is too large.',f'{a*b} cm²',f'A = ½ × {2*a} × {b} = {a*b} cm². The base-height rectangle contains two congruent triangles.',{'type':'triangle','w':2*a,'h':b},a*b)
 if k=='center-spread':
  data=sorted([a,a+2,a+4,a+6,a+8]);data2=[a,a+2,a+4,a+6,a+18];mean2=sum(data2)/5
  return item(f'Set A: {", ".join(map(str,data))}. Set B: {", ".join(map(str,data2))}. Find the mean, median, and range of both sets. Explain what changed.',f'A: {a+4}, {a+4}, 8. B: {fmt(mean2)}, {a+4}, 18.',f'A mean = {sum(data)}/5 = {a+4}; B mean = {sum(data2)}/5 = {fmt(mean2)}. The third value is the median in each ordered set. Increasing the greatest value raises mean and range, not median.')
 if k=='proportion-models':
  offset=0 if mode%2 else c;pairs=[(x,a*x+offset) for x in [1,2,4]]
  return item(f'A table has (x,y) pairs {pairs}. Is the relationship proportional? Explain using ratios and write a rule.',('Yes; '+f'y = {a}x') if offset==0 else f'No; y = {a}x + {offset}',f'Ratios y/x are {", ".join(fmt(F(y,x)) for x,y in pairs)}. '+('They are equal, so the constant of proportionality is '+str(a)+'.' if offset==0 else 'They differ. The starting value is not zero.'))
 if k=='signed-change':
  start=-a;change=b if mode%2 else -b;ans=start+change
  return item(f'A game score starts at {start}. It then {"increases" if change>0 else "decreases"} by {abs(change)} points. Find the new score. Represent the change on a number line.',ans,f'{start} + ({change}) = {ans}. Start at {start}; move {abs(change)} units {"right" if change>0 else "left"}.',numeric=ans)
 if k=='multi-step-equations':
  x=r.randint(3,20);total=a*x+b
  return item(f'The {context} pays a ${b} setup fee plus ${a} for each kit. The total is ${total}. Write and solve an equation for the number of kits.',f'{x} kits',f'Let x count kits. {a}x + {b} = {total}; {a}x = {total-b}; x = {x}. Check: {a}({x}) + {b} = {total}.',numeric=x)
 if k=='circle-measures':
  return item(f'A circular sign has radius {a} cm. Find its diameter, circumference, and area. Give exact answers using π, then approximate with π = 3.14.',f'{2*a} cm; {2*a}π cm; {a*a}π cm²',f'd = 2({a}) = {2*a}. C = 2π({a}) = {2*a}π ≈ {2*a*3.14:.2f} cm. A = π({a})² = {a*a}π ≈ {a*a*3.14:.2f} cm².',{'type':'circle','r':a})
 if k=='chance-models':
  red=a;blue=b;green=c;tot=a+b+c
  return item(f'A bag holds {red} red, {blue} blue, and {green} green counters, identical except for color. One is drawn at random. Find P(red), P(not red), and explain why their sum is 1.',f'{fmt(F(red,tot))}; {fmt(F(blue+green,tot))}',f'There are {tot} equally likely counters. Red: {red}/{tot}; not red: {blue+green}/{tot}. These disjoint events cover all {tot} counters.')
 if k=='both-sides':
  x=r.randint(-5,10);d=a+c;right=(d-a)*x+b
  if mode==0:return item(f'Solve {a}x + {b} = {a}x + {b}. Classify the solution set and justify it.','All real numbers',f'Subtract {a}x from each side to obtain {b} = {b}, true for every real x.')
  if mode==1:return item(f'Solve {a}x + {b} = {a}x + {b+c}. Classify the solution set and justify it.','No solution',f'Subtract {a}x to obtain {b} = {b+c}, a contradiction.')
  return item(f'Solve {d}x + {b} = {a}x + ({right}). Show your work and check.',f'x = {x}',f'Subtract {a}x and {b}: {d-a}x = {right-b}. Divide by {d-a}: x = {x}. Both original sides equal {d*x+b}.',numeric=x)
 if k=='linear-functions':
  m=a;inter=b;x1=c;x2=c+3;y1=m*x1+inter;y2=m*x2+inter
  return item(f'A club’s total cost y dollars depends linearly on x kits. Two records are ({x1},{y1}) and ({x2},{y2}). Find y = mx + b and interpret m and b.',f'y = {m}x + {inter}',f'm = ({y2}−{y1})/({x2}−{x1}) = {m} dollars/kit. b = {y1}−{m}({x1}) = {inter} dollars before any kits. Plot (0,{inter}) and the two records.')
 if k=='right-triangles':
  u,v,hyp=r.choice([(3,4,5),(5,12,13),(8,15,17),(7,24,25)]);scale=r.randint(1,3);u*=scale;v*=scale;hyp*=scale
  return item(f'A route goes {u} m east, then {v} m north. Find the direct straight-line distance from start to finish. Explain why the theorem applies.',f'{hyp} m',f'The directions form a right angle. d² = {u}² + {v}² = {u*u}+{v*v} = {hyp*hyp}; d = {hyp} m.',{'type':'righttriangle','w':u,'h':v},hyp)
 if k=='scatter-data':
  sign=1 if mode%2 else -1;pairs=[(x, a+12+sign*2*x+(x%2)) for x in range(1,7)]
  return item(f'An invented study records practice sessions x and task scores y: {pairs}. Plot every pair. Describe the association and explain why these data alone do not prove cause.',('Positive' if sign>0 else 'Negative')+' approximately linear association',f'As x increases, y generally {"increases" if sign>0 else "decreases"}. Points follow an approximate line. Other factors or selection of participants could explain the relationship.',{'type':'scatter','pairs':pairs})
 if k=='integer-exponents':
  base=r.randint(2,5);m=r.randint(2,5);n=r.randint(1,4)
  if mode%2:return item(f'Simplify ({base}^{m})({base}^{n}) as one power and evaluate it. Explain using repeated factors.',f'{base}^{m+n} = {base**(m+n)}',f'There are {m}+{n} = {m+n} factors of {base}. Their product is {base**(m+n)}.',numeric=base**(m+n))
  return item(f'Simplify {base}^{m+n} ÷ {base}^{m} as one power and evaluate it. Explain by canceling equal factors.',f'{base}^{n} = {base**n}',f'Cancel {m} nonzero factors from numerator and denominator. {m+n}−{m} = {n} factors remain.',numeric=base**n)
 raise ValueError(k)

def validate_profiles(text):
 for p in PROFILES:
  assert p[3] in text,p[3]
  for seed in range(200):
   t=task(p,seed)
   assert t['q'] and t['work'] and t['answer']
   if t['numeric'] is not None: assert math.isfinite(float(t['numeric']))

if __name__=='__main__':
 from pathlib import Path
 validate_profiles(Path('tmp/research/nc-math.txt').read_text())
 print('30 verified code references; 6,000 generator cases constructed without missing answers.')
