import { safe, json } from '../../../../server/commerce';
import { editorGet,editorSave,editorPublish,editorUpload,editorMedia,siteContent } from '../../../../server/editor';
export const dynamic='force-dynamic';
export async function GET(request:Request,{params}:{params:Promise<{action:string}>}){return safe(async()=>{const {action}=await params;if(action==='state')return editorGet(request);if(action==='site')return json(await siteContent());if(action==='media')return editorMedia(request);return json({error:'Not found'},404);});}
export async function POST(request:Request,{params}:{params:Promise<{action:string}>}){return safe(async()=>{const {action}=await params;if(action==='save')return editorSave(request);if(action==='publish')return editorPublish(request);if(action==='upload')return editorUpload(request);return json({error:'Not found'},404);});}
