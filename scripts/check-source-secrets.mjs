import {execFileSync} from 'node:child_process';
import {readFile} from 'node:fs/promises';
const files=execFileSync('git',['ls-files','-z'],{encoding:'utf8'}).split('\0').filter(Boolean);
const problems=[];
for(const name of files){
 if(/(^|\/)(\.env(?!\.example$)|\.dev\.vars(?!\.example$)|.*password.*|.*\.(pem|key|p12|pfx|sqlite|db)$)/i.test(name)){problems.push(name+' (sensitive filename)');continue;}
 if(!/\.(tsx?|m?js|cjs|json|md|ya?ml|txt|example)$/.test(name)||name.includes('resource-payload.json'))continue;
 const text=await readFile(name,'utf8');
 if(/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/.test(text)||/gh[pousr]_[A-Za-z0-9]{30,}/.test(text)||/github_pat_[A-Za-z0-9_]{40,}/.test(text)||/\bsk_(?:live|test)_[A-Za-z0-9]{20,}/.test(text))problems.push(name+' (credential pattern)');
}
if(problems.length)throw new Error('Remove credentials before upload:\n'+problems.join('\n'));
console.log(`Checked ${files.length} tracked paths for password files and credential patterns. Hosted secrets are not included.`);
