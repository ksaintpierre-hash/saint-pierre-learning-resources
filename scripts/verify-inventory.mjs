import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const files=JSON.parse(await readFile(new URL('../snapshots/product-files-manifest.json',import.meta.url),'utf8'));
const catalog=JSON.parse(await readFile(new URL('../snapshots/catalog-2026-09-16.json',import.meta.url),'utf8')).products;
for(const p of catalog){if(!files.some(f=>f.productId===p.id))throw new Error('Missing product: '+p.id);}
for(const f of files){const b=await readFile(new URL('../'+f.file,import.meta.url));if(b.length!==f.bytes||createHash('sha256').update(b).digest('hex')!==f.sha256)throw new Error('Product file changed: '+f.file);}
console.log(`${files.length} current customer downloads verified against exact SHA-256 fingerprints.`);
