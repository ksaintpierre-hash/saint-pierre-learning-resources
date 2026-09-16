// Run a scratch copy beside the runtime node_modules link. Original native slide content.
import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
import { finalizePresentation } from '/root/.codex/skills/builtins/presentations/container_tools/artifact_tool_utils.mjs';
process.env.RUNTIME_NODE_MODULES=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
process.env.RUNTIME_NODE=process.env.CODEX_PRIMARY_RUNTIME_NODE;
process.env.RUNTIME_PYTHON=process.env.CODEX_PRIMARY_RUNTIME_PYTHON;
process.env.RUNTIME_BIN_DIR=process.env.CODEX_PRIMARY_RUNTIME+'/dependencies/bin/override';

const root='/workspace/sites/saint-pierre-learning-resources';
const tmp=path.join(root,'tmp/resource-build');
const output=path.join(root,'resources/2026-09-15');
const skill='/root/.codex/skills/builtins/presentations';
const logo=new Uint8Array(await fs.readFile(path.join(root,'public/brand/saint-pierre-logo.png')));
const candidates=(await fs.readdir(tmp)).filter(n=>/^nc-g.*-teaching-bundle\.json$/.test(n)&&(!process.env.RESOURCE_ONLY||n.includes(process.env.RESOURCE_ONLY))).sort();
const limit=Number(process.argv[2]||candidates.length);
const font='DejaVu Sans';
function text(slide,value,x,y,w,h,size=32,bold=false,color='#172D46'){
 const shape=slide.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 shape.text=value;shape.text.style={typeface:font,fontSize:size,bold,color,autoFit:'none'};return shape;
}
function image(slide,x,y,w,h){slide.images.add({blob:logo,contentType:'image/png',alt:'Official Saint Pierre Learning Resources KSP Haitian-flag logo',fit:'contain',position:{left:x,top:y,width:w,height:h}})}
function makeSlide(p,title,kicker='LEARN • EXPLAIN • CHECK'){
 const s=p.slides.add();s.background.fill='#FFFFFF';
 text(s,kicker,60,26,1100,28,18,true,'#246A70');
 text(s,title,60,76,1150,118,43,true);
 image(s,60,631,62,69);
 text(s,'© 2026 Saint Pierre Learning Resources',137,658,950,25,16,false,'#536574');
 text(s,String(p.slides.items.length),1180,657,50,25,16,false,'#536574');
 return s;
}
for(const name of candidates.slice(0,limit)){
 const data=JSON.parse(await fs.readFile(path.join(tmp,name),'utf8'));
 const [grade,key,title,code,objective,strategy]=data.profile;
 const presentation=Presentation.create({slideSize:{width:1280,height:720}});
 let s=makeSlide(presentation,title,'SAINT PIERRE LEARNING RESOURCES');
 image(s,60,246,210,232);
 text(s,`Grade ${grade} • Mathematics\n${code}`,320,268,830,100,30,true,'#246A70');
 text(s,objective,320,393,835,148,32);
 s.speakerNotes.textFrame.setText('Original focused mini-lesson. Use with the complete teaching-bundle PDF. Objective: '+objective+' Standard: '+code+'. Official source accessed September 15, 2026: https://www.dpi.nc.gov/documents/publications/catalog/ma196-vertical-progression-math/open');
 s=makeSlide(presentation,'What will a strong explanation show?');
 text(s,'1. A model or equation that fits the quantities.\n\n2. Accurate calculation with appropriate units.\n\n3. A check that makes the answer reasonable.',65,235,1140,355,32);
 s.speakerNotes.textFrame.setText('Invite a simpler prior-knowledge example. Use counters, diagrams, home-language rehearsal, or documented supports. Read the full teacher guide before presenting.');
 s=makeSlide(presentation,'Watch the reasoning');
 text(s,data.models[0].q,65,224,1140,175,29,true);
 text(s,data.models[0].work,65,437,1140,142,29,false,'#246A70');
 s.speakerNotes.textFrame.setText(strategy);
 s=makeSlide(presentation,'Build a second model together');
 text(s,data.models[1].q,65,218,1140,220,30);
 text(s,'Discuss: What should the first step find?',65,510,1140,70,28,true,'#246A70');
 s.speakerNotes.textFrame.setText('Worked answer: '+data.models[1].work+' Ask students to connect the model with symbols before revealing the answer.');
 for(let i=0;i<4;i++){
  s=makeSlide(presentation,'Your turn • '+(i+1));
  text(s,data.cards[i].q,65,227,1135,252,33);
  text(s,'Represent → solve → explain → check',65,543,1110,50,27,true,'#246A70');
  s.speakerNotes.textFrame.setText('Student direction: write or draw your reasoning on paper. Worked solution: '+data.cards[i].work+' Access: allow oral rehearsal, manipulatives, or reduced copying according to individual plans. Extension: invent a new problem with the same structure and verify it.');
 }
 s=makeSlide(presentation,'Exit question • Explain independently');
 text(s,data.exit[0].q,65,222,1140,275,32);
 text(s,'Include a check. What would you teach someone else?',65,547,1135,60,26,true,'#246A70');
 s.speakerNotes.textFrame.setText('Answer: '+data.exit[0].work+' Score 2 for correct result with coherent reasoning, 1 for a correct method with a minor error or an unexplained correct result, 0 for unsupported reasoning. This is a local instructional rubric, not a standardized score.');
 s=makeSlide(presentation,'Teacher review and next steps','TEACHER KEY • HIDE DURING INDEPENDENT WORK');
 text(s,data.cards.slice(0,4).map((t,i)=>`${i+1}. ${t.answer}`).join('\n\n'),65,217,540,286,27,true);
 text(s,'Exit: '+data.exit[0].answer+'\n\nUse the worked PDF key and slide notes to discuss methods. Revisit the earliest unclear step before adding more practice.',663,217,540,330,27);
 s.speakerNotes.textFrame.setText(data.cards.slice(0,4).map((t,i)=>`${i+1}. ${t.work}`).join('\n')+'\nExit: '+data.exit[0].work+'\nAIG: second methods and counterexamples. 504: follow documented pacing and format supports. EC: model a step and provide concrete representations in line with the IEP. ESL: preview vocabulary and use partner or home-language rehearsal. Single-teacher classroom license. No public redistribution.');
 const stage=path.join(tmp,data.id+'-slides');await fs.mkdir(stage,{recursive:true});
 const revision=process.env.RESOURCE_REVISION||'initial';
 const candidatePath=path.join(stage,revision==='initial'?'candidate.pptx':`candidate-${revision}.pptx`);
 await (await PresentationFile.exportPptx(presentation)).save(candidatePath);
 const finalPath=revision==='initial'?path.join(output,data.id+'.pptx'):path.join(stage,'finalized',`final-${revision}.pptx`);
 await fs.mkdir(path.dirname(finalPath),{recursive:true});
 await finalizePresentation({workspaceDir:root,candidatePath,finalPath,pythonExecutable:'/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],fontPolicy:{basis:'design',families:[font]},explicitTotalSlideCount:10,verifyArtifactToolImport:true,receiptPath:path.join(stage,revision==='initial'?'validation.json':`validation-${revision}.json`)});
 if(revision!=='initial')await fs.copyFile(finalPath,path.join(output,data.id+'.pptx'));
 for(let i=0;i<presentation.slides.items.length;i++){
  const slide=presentation.slides.items[i];const png=await presentation.export({slide,format:'png',scale:1});
  await fs.writeFile(path.join(stage,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 }
 console.log(data.id+' • 10 editable slides finalized and rendered');
}
