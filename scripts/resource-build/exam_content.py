from fractions import Fraction as F
import random,math
from math_content import fmt

EXAM=[
('linear-solve','Linear Equations with Structure','Algebra','Solve a linear equation and verify the solution.'),
('linear-context','Translate a Cost Story','Algebra','Represent fixed and variable costs with an equation.'),
('systems','Two Constraints, One Solution','Algebra','Solve and interpret a two-equation system.'),
('inequalities','Inequalities and Feasible Choices','Algebra','Represent a constraint and identify feasible values.'),
('literal','Rearrange a Formula','Algebra','Isolate a variable while preserving equivalence.'),
('slope','Slope from Different Representations','Algebra','Calculate and interpret a constant rate of change.'),
('line-relations','Parallel and Perpendicular Lines','Algebra','Use slopes to relate lines in a coordinate plane.'),
('break-even','Compare Two Linear Plans','Algebra','Find and interpret a break-even point.'),
('factoring','Factor to Reveal Structure','Advanced Math','Rewrite a quadratic expression as a product.'),
('quadratic-roots','Quadratic Solutions and Constraints','Advanced Math','Solve a factored quadratic and check its roots.'),
('vertex','Read a Quadratic Vertex','Advanced Math','Interpret a vertex-form quadratic and its extreme value.'),
('exponents','Equivalent Exponential Expressions','Advanced Math','Use exponent properties to simplify expressions.'),
('radicals','Radical Equations and Checks','Advanced Math','Solve a square-root equation and verify its domain.'),
('growth','Repeated Percent Growth','Advanced Math','Model repeated multiplicative change.'),
('rational','Rational Equations with Restrictions','Advanced Math','Solve a rational equation while excluding undefined values.'),
('functions','Function Notation and Inputs','Advanced Math','Evaluate functions and interpret a requested input.'),
('percent-change','Percent Change in Two Stages','Problem-Solving and Data Analysis','Distinguish additive and multiplicative percent changes.'),
('units','Units That Cancel','Problem-Solving and Data Analysis','Use dimensional reasoning to convert a rate.'),
('weighted-mean','Averages with Unequal Group Sizes','Problem-Solving and Data Analysis','Compute a combined mean using group sizes.'),
('outliers','Center and the Effect of an Outlier','Problem-Solving and Data Analysis','Compare how one changed value affects center and spread.'),
('probability','Probability with a Defined Sample Space','Problem-Solving and Data Analysis','Compute probabilities from equally likely outcomes.'),
('conditional','Read a Two-Way Count Table','Problem-Solving and Data Analysis','Identify the correct denominator for a conditional probability.'),
('prediction','Use a Linear Prediction Model','Problem-Solving and Data Analysis','Interpret a model prediction and residual.'),
('sampling','What a Sample Can Support','Problem-Solving and Data Analysis','Evaluate a sampling method and the limits of a claim.'),
('angles','Triangle Angles with Algebra','Geometry and Trigonometry','Use angle relationships to determine an unknown.'),
('trigonometry','Right-Triangle Ratios','Geometry and Trigonometry','Use sine, cosine, and tangent in a right triangle.'),
('circles','Circle Measures from a Constraint','Geometry and Trigonometry','Connect radius, circumference, area, and arc measures.'),
('similarity','Scale Factors and Similar Figures','Geometry and Trigonometry','Distinguish length and area scale factors.'),
('volume','Volume and Dimensional Scaling','Geometry and Trigonometry','Use volume formulas and cubic scale factors.'),
('distance','Coordinate Distance and Midpoints','Geometry and Trigonometry','Use coordinates to calculate distance and midpoint.'),
]

def exam_task(profile,seed):
 key,title,domain,obj=profile;r=random.Random(seed);a=r.randint(2,9);b=r.randint(2,9);c=r.randint(2,8);mode=seed%3
 def t(q,ans,work,value=None,contract=None):return {'q':q,'answer':str(ans),'work':work,'value':value,'contract':contract,'diagram':None,'skill':key}
 if key=='linear-solve':
  x=r.randint(-8,14);v=a*(x+b)-c*x
  if a==c:c+=1;v=a*(x+b)-c*x
  return t(f'Solve {a}(x + {b}) − {c}x = {v}. Give the value of x and verify it.',x,f'Expand: {a-c}x + {a*b} = {v}. Thus {a-c}x = {v-a*b}, so x = {x}. Substitution gives {v} on both sides.',x,{'kind':'linear','a':a-c,'b':a*b,'rhs':v,'x':x})
 if key=='linear-context':
  rate=a+4;fee=b*5;n=c+7;budget=fee+rate*n
  return t(f'A workshop charges a ${fee} booking fee and ${rate} per participant. A group pays ${budget}. How many participants are included?',n,f'{fee} + {rate}n = {budget}. Subtract {fee}, then divide by {rate}: n = {n}.',n,{'kind':'linear','a':rate,'b':fee,'rhs':budget,'x':n})
 if key=='systems':
  x=a;y=b;u=x+y;v=3*x+2*y
  if mode==0:q=f'The system is x + y = {u} and 3x + 2y = {v}. Find x and y.'
  else:q=f'A club sells {u} tickets. Adult tickets cost $3 and student tickets cost $2. Revenue is ${v}. How many of each type were sold?'
  return t(q,f'x = {x}, y = {y}' if mode==0 else f'{x} adult; {y} student',f'Double the first equation: 2x + 2y = {2*u}. Subtract it from the second: x = {v-2*u}. Then y = {u} − {x} = {y}. Check both totals.',x,{'kind':'system','x':x,'y':y,'sum':u,'weighted':v})
 if key=='inequalities':
  fee=b*5;rate=a;limit=fee+rate*(c+5)+rate-1;mx=(limit-fee)//rate
  return t(f'A club has at most ${limit} to spend. Supplies cost ${fee} plus ${rate} per participant. What is the greatest whole number of participants it can support?',mx,f'{fee}+{rate}n ≤ {limit}; n ≤ {fmt(F(limit-fee,rate))}. The greatest whole number is {mx}. {mx+1} participants would cost ${fee+rate*(mx+1)}, over the limit.',mx,{'kind':'budget','fee':fee,'rate':rate,'limit':limit,'n':mx})
 if key=='literal':
  return t(f'The formula T = {a}p + {b}q relates T, p, and q. Write p in terms of T and q. Then find p when T = {a*c+b*4} and q = 4.',f'p = (T − {b}q)/{a}; p = {c}',f'Subtract {b}q: T − {b}q = {a}p. Divide by nonzero {a}. Substitute: ({a*c+b*4} − {b}×4)/{a} = {c}.',c,{'kind':'linear','a':a,'b':b*4,'rhs':a*c+b*4,'x':c})
 if key=='slope':
  x1=b;x2=b+c;m=a if mode else -a;start=15;y1=m*x1+start;y2=m*x2+start
  return t(f'A linear function passes through ({x1}, {y1}) and ({x2}, {y2}). Find its slope and y-intercept, then write the function.',f'y = {m}x + {start}',f'Slope = ({y2}−({y1}))/({x2}−{x1}) = {m}. Intercept = {y1}−({m})({x1}) = {start}.',m,{'kind':'slope','x1':x1,'x2':x2,'y1':y1,'y2':y2,'m':m})
 if key=='line-relations':
  m=F(a,b);x=c;y=a+4;per=-1/m
  return t(f'A line has slope {fmt(m)}. Write equations for a parallel line and a perpendicular line through ({x}, {y}).',f'Parallel: y − {y} = {fmt(m)}(x − {x}); perpendicular: y − {y} = {fmt(per)}(x − {x})',f'Parallel slopes are equal. Perpendicular slopes are negative reciprocals: {fmt(m)} × ({fmt(per)}) = −1. Point-slope form ensures each line passes through ({x},{y}).')
 if key=='break-even':
  n=c+5;m1=a+5;m2=a;f1=b*3;f2=f1+(m1-m2)*n
  return t(f'Plan A costs ${f1} plus ${m1} per session. Plan B costs ${f2} plus ${m2} per session. After how many sessions do they cost the same, and which is cheaper after that?',f'{n} sessions; Plan B after that',f'{f1}+{m1}x = {f2}+{m2}x gives {m1-m2}x = {f2-f1}, so x = {n}. B has the lower per-session cost and is cheaper for x > {n}.',n,{'kind':'linear','a':m1-m2,'b':f1,'rhs':f2,'x':n})
 if key=='factoring':
  u=a;v=-b if mode%2 else b;sm=u+v;prod=u*v
  return t(f'Factor x² + ({sm})x + ({prod}) over the integers. Check by expanding.',f'(x + ({u}))(x + ({v}))',f'The constants must add to {sm} and multiply to {prod}. {u}+({v}) = {sm}, and {u}×({v}) = {prod}.',None,{'kind':'factor','u':u,'v':v,'sum':sm,'product':prod})
 if key=='quadratic-roots':
  u=a;v=-b;sm=u+v;prod=u*v
  return t(f'Solve x² − ({sm})x + ({prod}) = 0. Give all real solutions and check them.',f'x = {u} or x = {v}',f'Factor as (x − ({u}))(x − ({v})) = 0. A zero product requires x = {u} or {v}. Each makes one factor zero.',None,{'kind':'roots','u':u,'v':v,'sum':sm,'product':prod})
 if key=='vertex':
  h=b;k=c+5;coef=-a if mode==0 else a
  return t(f'f(x) = {coef}(x − {h})² + {k}. State the vertex and whether the function has a maximum or minimum. Find f({h+2}).',f'({h},{k}); {"maximum" if coef<0 else "minimum"}; f({h+2}) = {coef*4+k}',f'The square is zero at x = {h}. The sign of {coef} determines the opening direction. At x = {h+2}, the square equals 4, so f = {coef}×4+{k} = {coef*4+k}.',coef*4+k)
 if key=='exponents':
  base=r.randint(2,4);m=r.randint(2,5);n=r.randint(1,3)
  return t(f'Simplify ({base}^{m} × {base}^{n}) / {base}^{n+1} as one power and evaluate.',f'{base}^{m-1} = {base**(m-1)}',f'Combine exponents: {m}+{n}−({n+1}) = {m-1}. The nonzero base is {base}, so the result is {base**(m-1)}.',base**(m-1))
 if key=='radicals':
  rhs=a+1;offset=b;x=rhs*rhs-offset
  return t(f'Solve √(x + {offset}) = {rhs}. State the domain restriction and verify the solution.',f'x = {x}; x ≥ −{offset}',f'Squaring gives x+{offset} = {rhs*rhs}, so x = {x}. This meets x ≥ −{offset}; √({x}+{offset}) = √{rhs*rhs} = {rhs}.',x,{'kind':'radical','x':x,'offset':offset,'rhs':rhs})
 if key=='growth':
  initial=r.choice([400,800,1200,2000]);pct=r.choice([5,10,20]);factor=F(100+pct,100);ans=initial*factor**2
  return t(f'A hypothetical fund starts with ${initial} and increases by {pct}% at the end of each of two years. No money is added or removed. Write a model and find its value after two years.',f'A(t) = {initial}({float(factor):g})^t; ${float(ans):.2f}',f'Each year multiplies the previous value by {float(factor):g}. Two years give {initial}×{float(factor):g}² = {float(ans):.2f}. This is a fictional math model, not an investment forecast.',float(ans))
 if key=='rational':
  offset=b;numer=a*c;rhs=a;x=c+offset
  return t(f'Solve {numer}/(x − {offset}) = {rhs}. State the excluded value and check the solution.',f'x = {x}; exclude x = {offset}',f'The denominator cannot be zero. Multiply by x−{offset}: {numer} = {rhs}(x−{offset}); x−{offset} = {c}; x = {x}. Check: {numer}/{c} = {rhs}.',x,{'kind':'rational','x':x,'offset':offset,'num':numer,'rhs':rhs})
 if key=='functions':
  x=c-4;value=a*x*x+b
  return t(f'f(t) = {a}t² + {b}. Find f({x}). Then solve f(t) = {a*9+b} for real t.',f'f({x}) = {value}; t = −3 or 3',f'Substitute the entire input: {a}({x})²+{b} = {value}. For the second part, {a}t² = {a*9}, so t² = 9 and t = ±3.',value)
 if key=='percent-change':
  price=r.choice([80,120,160,240]);up=r.choice([10,20,25]);down=r.choice([10,20,25]);final=F(price*(100+up)*(100-down),10000);net=(final/price-1)*100
  return t(f'A price of ${price} rises {up}% and then falls {down}% from the increased price. Find the final price and the net percent change from the original.',f'${float(final):.2f}; {fmt(net)}%',f'Multiply successive factors: {price}×{(100+up)/100:g}×{(100-down)/100:g} = {float(final):.2f}. Net change = ({fmt(final)}/{price}−1)×100% = {fmt(net)}%.',float(final))
 if key=='units':
  speed=r.choice([3,5,8,12]);minutes=a+4;meters=speed*minutes*60
  return t(f'A cart moves at {speed} meters per second for {minutes} minutes at a constant speed. How many kilometers does it travel? Show units canceling.',fmt(F(meters,1000))+' km',f'{speed} m/s × {minutes} min × 60 s/min × 1 km/1000 m = {fmt(F(meters,1000))} km.',float(F(meters,1000)))
 if key=='weighted-mean':
  n1=a*2;n2=b*3;m1=60+c;m2=80+c;ans=F(n1*m1+n2*m2,n1+n2)
  return t(f'Group A has {n1} scores with mean {m1}. Group B has {n2} scores with mean {m2}. Find the combined mean. Explain why simply averaging the two means can fail.',fmt(ans),f'Total score = {n1}×{m1}+{n2}×{m2} = {n1*m1+n2*m2}. Divide by {n1+n2} scores: {fmt(ans)}. The group sizes determine each mean’s weight.',float(ans))
 if key=='outliers':
  vals=[a,a+2,a+4,a+6,a+8];delta=b*5;new=vals[:-1]+[vals[-1]+delta]
  return t(f'Data: {vals}. Replace the greatest value with {new[-1]}. How do the mean, median, and range change?',f'Mean +{fmt(F(delta,5))}; median unchanged; range +{delta}',f'Only the total changes by {delta}, so mean increases by {delta}/5 = {fmt(F(delta,5))}. The third ordered value remains {a+4}. The maximum, and therefore range, increases by {delta}.',float(F(delta,5)))
 if key=='probability':
  red=a;blue=b;total=a+b;ans=F(red,total)*F(blue,total-1)
  return t(f'A bag contains {red} red and {blue} blue identical-size counters. Two are drawn without replacement. Find the probability of red first and blue second.',fmt(ans),f'P(red first) = {red}/{total}. Then {blue} blue remain among {total-1} counters. Multiply: {red}/{total}×{blue}/{total-1} = {fmt(ans)}.',float(ans))
 if key=='conditional':
  ay=a*3;an=b*2;by=c*4;bn=a+7;ans=F(ay,ay+by)
  return t(f'A survey count table has: Group A, Yes {ay}, No {an}; Group B, Yes {by}, No {bn}. Among respondents who answered Yes, what fraction belong to Group A?',fmt(ans),f'The condition limits the denominator to Yes responses: {ay}+{by} = {ay+by}. Group A contributes {ay} of those, so the fraction is {fmt(ans)}.',float(ans))
 if key=='prediction':
  m=F(a,2);inter=b+10;x=c+5;pred=m*x+inter;observed=pred+3
  return t(f'A fitted model is ŷ = {fmt(m)}x + {inter}. At x = {x}, an observed y is {fmt(observed)}. Find the prediction and residual (observed minus predicted). Does a residual of zero prove a causal relationship?',f'Prediction {fmt(pred)}; residual 3; no',f'Prediction = {fmt(m)}×{x}+{inter} = {fmt(pred)}. Residual = {fmt(observed)}−{fmt(pred)} = 3. Even a perfect fit does not establish cause.',float(pred))
 if key=='sampling':
  contexts=[('all students at a school','volunteers from its debate club','a random selection from the full enrollment list'),('all library members','people attending a poetry event','a random selection from the membership list'),('all residents of a town','visitors to one sports field','a random sample from an appropriate town-wide address frame')]
  pop,sample,better=contexts[mode];n=20+a*5;favor=(2*n)//3;pct=round(100*favor/n)
  return t(f'A survey of {n} {sample} finds that {favor} favor a proposal. A report claims about {pct}% of {pop} favor it. Evaluate the claim and suggest a better sampling plan.','The sample may not represent the target population.',f'Participation or location selects a particular group. The reported sample percentage does not justify the same population percentage. Use {better}, plan for nonresponse, and state remaining uncertainty.')
 if key=='angles':
  x=c+6;a1=2*x;a2=3*x;a3=180-5*x
  return t(f'A triangle has angles 2x°, 3x°, and {a3}°. Find x and all three angles.',f'x = {x}; {a1}°, {a2}°, {a3}°',f'2x+3x+{a3} = 180; 5x = {180-a3}; x = {x}. The positive angles total 180°.',x,{'kind':'angles','values':[a1,a2,a3]})
 if key=='trigonometry':
  opp,adj,hyp=r.choice([(3,4,5),(5,12,13),(8,15,17)]);scale=r.randint(1,3)
  return t(f'In a right triangle, relative to angle θ, the opposite leg is {opp*scale} and adjacent leg is {adj*scale}. Find the hypotenuse and exact sin θ, cos θ, and tan θ.',f'{hyp*scale}; sin θ = {fmt(F(opp,hyp))}; cos θ = {fmt(F(adj,hyp))}; tan θ = {fmt(F(opp,adj))}',f'Hypotenuse = √({opp*scale}²+{adj*scale}²) = {hyp*scale}. Use opposite/hypotenuse, adjacent/hypotenuse, and opposite/adjacent.',hyp*scale)
 if key=='circles':
  rad=a;angle=r.choice([60,90,120,180]);arc=F(angle*2*rad,360);sector=F(angle*rad*rad,360)
  return t(f'A circle has radius {rad} cm. A sector has central angle {angle}°. Find the sector’s arc length and area in exact form using π.',f'Arc ({fmt(arc)})π cm; area ({fmt(sector)})π cm²',f'The sector is {angle}/360 of the whole. Arc = ({angle}/360)×2π({rad}) = ({fmt(arc)})π. Area = ({angle}/360)×π({rad})² = ({fmt(sector)})π.')
 if key=='similarity':
  small=a;large=small*F(3,2);area=b*8;ans=F(area*9,4)
  return t(f'Two similar figures have corresponding side lengths {small} cm and {fmt(large)} cm. The smaller area is {area} cm². Find the larger area and justify the scale factor.',fmt(ans)+' cm²',f'Length factor = {fmt(large)}/{small} = 3/2. Area factor = (3/2)² = 9/4. Larger area = {area}×9/4 = {fmt(ans)} cm².',float(ans))
 if key=='volume':
  vol=a*b*c;scale=r.choice([2,3]);ans=vol*scale**3
  return t(f'A rectangular prism measures {a} cm by {b} cm by {c} cm. Every dimension is multiplied by {scale}. Find the new volume and compare it with the original.',f'{ans} cm³; {scale**3} times as large',f'Original volume = {a}×{b}×{c} = {vol}. Three dimensions each scale by {scale}, so volume scales by {scale}³ = {scale**3}; new volume = {ans} cm³.',ans)
 if key=='distance':
  x1=-a;y1=b;dx,dy,hyp=r.choice([(3,4,5),(5,12,13),(8,15,17)]);x2=x1+dx;y2=y1+dy;mx=F(x1+x2,2);my=F(y1+y2,2)
  return t(f'Points A({x1},{y1}) and B({x2},{y2}) are endpoints of a segment. Find its length and midpoint.',f'Length {hyp}; midpoint ({fmt(mx)},{fmt(my)})',f'Distance = √(({x2}−({x1}))²+({y2}−({y1}))²) = √({dx}²+{dy}²) = {hyp}. Average each coordinate for the midpoint.',hyp)
 raise ValueError(key)

def verify(t):
 c=t.get('contract')
 if not c:return
 k=c['kind']
 if k=='linear':assert c['a']*c['x']+c['b']==c['rhs']
 elif k=='system':assert c['x']+c['y']==c['sum'] and 3*c['x']+2*c['y']==c['weighted']
 elif k=='budget':assert c['fee']+c['rate']*c['n']<=c['limit']<c['fee']+c['rate']*(c['n']+1)
 elif k=='slope':assert F(c['y2']-c['y1'],c['x2']-c['x1'])==c['m']
 elif k in ['factor','roots']:assert c['u']+c['v']==c['sum'] and c['u']*c['v']==c['product']
 elif k=='radical':assert c['x']+c['offset']>=0 and math.isclose(math.sqrt(c['x']+c['offset']),c['rhs'])
 elif k=='rational':assert c['x']!=c['offset'] and F(c['num'],c['x']-c['offset'])==c['rhs']
 elif k=='angles':assert sum(c['values'])==180 and min(c['values'])>0

if __name__=='__main__':
 for p in EXAM:
  for seed in range(100):verify(exam_task(p,seed))
 print('30 exam skill generators checked across 3,000 cases.')
