// Server-only private bytes. Callers must authenticate and check ownership or a paid entitlement first.
import payload from './resource-payload.json';
type StoredFile={chunks:number[];bytes:number;sha256:string;contentType:string};
const files=payload.files as Record<string,StoredFile>;
const products=payload.products as Record<string,Record<string,string>>;
export const hasResourceFile=(id:string)=>Object.hasOwn(products,id)&&!!products[id]?.default;
export function resourceMetadata(id:string){
 const name=Object.hasOwn(products,id)?products[id]?.default:undefined;
 const file=name&&Object.hasOwn(files,name)?files[name]:undefined;
 return name&&file?{name,bytes:file.bytes,sha256:file.sha256,contentType:file.contentType}:null;
}
export function resourceFile(id:string,format='default'){
 if(!Object.hasOwn(products,id)||!['default','pdf','pptx','slides','thumbnail'].includes(format))return null;
 const name=products[id]?.[format];const file=name&&Object.hasOwn(files,name)?files[name]:undefined;
 if(!name||!file)return null;
 // Stream exact immutable chunks; never build a public asset URL for a full resource.
 const stream=new ReadableStream<Uint8Array>({start(controller){
  for(const chunk of file.chunks)controller.enqueue(Uint8Array.from(atob(payload.chunks[chunk]),c=>c.charCodeAt(0)));
  controller.close();
 }});
 return {name,contentType:file.contentType,bytes:file.bytes,sha256:file.sha256,body:stream};
}
