// Server-only exact original catalog files. Decoded only when provisioning.
import payload from './resource-payload.json';
import index from './legacy-file-index.json';
export const privateProducts = Object.create(null) as Record<string,string>;
for (const [id,file] of Object.entries(index.files)) {
 Object.defineProperty(privateProducts,id,{enumerable:true,get:()=>btoa(file.chunks.map(index=>atob(payload.chunks[index])).join(''))});
}
