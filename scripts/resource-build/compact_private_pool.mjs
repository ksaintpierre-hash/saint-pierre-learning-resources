// Losslessly share identical embedded brand/font bytes across old and new PDFs.
import fs from 'node:fs';
import {createHash} from 'node:crypto';
const mainPath='server/resource-payload.json';
const main=JSON.parse(fs.readFileSync(mainPath)),legacy=JSON.parse(fs.readFileSync('server/legacy-resource-payload.json'));
const byValue=new Map(main.chunks.map((value,index)=>[value,index]));
const remap=legacy.chunks.map(value=>{if(!byValue.has(value)){byValue.set(value,main.chunks.length);main.chunks.push(value);}return byValue.get(value);});
const files=Object.fromEntries(Object.entries(legacy.files).map(([id,file])=>[id,{...file,chunks:file.chunks.map(i=>remap[i])}]));
for(const [id,file] of Object.entries(files)){
 const bytes=Buffer.concat(file.chunks.map(i=>Buffer.from(main.chunks[i],'base64')));
 if(bytes.length!==file.bytes||createHash('sha256').update(bytes).digest('hex')!==file.sha256)throw new Error('Changed legacy bytes: '+id);
}
fs.writeFileSync(mainPath,JSON.stringify(main));
fs.writeFileSync('server/legacy-file-index.json',JSON.stringify({files}));
console.log('Verified ten legacy PDFs; embedded resources now share exact chunks.');
