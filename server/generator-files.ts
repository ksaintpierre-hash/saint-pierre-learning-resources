// Server-only private bytes for the Practice Packet Generator's pre-built
// variant pool. Callers must check an active subscription first.
import payload from './generator-payload.json';
type StoredFile={chunks:number[];bytes:number;sha256:string;contentType:string};
const files=payload.files as Record<string,StoredFile>;
export function generatorFile(name:string){
 const file=Object.hasOwn(files,name)?files[name]:undefined;
 if(!file)return null;
 const stream=new ReadableStream<Uint8Array>({start(controller){
  for(const chunk of file.chunks)controller.enqueue(Uint8Array.from(atob(payload.chunks[chunk]),c=>c.charCodeAt(0)));
  controller.close();
 }});
 return {name,contentType:file.contentType,bytes:file.bytes,sha256:file.sha256,body:stream};
}
