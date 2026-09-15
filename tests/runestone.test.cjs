const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const files = ['JS/Runestone_V3.js', 'JS/Runestone_Charlie.js'].filter(fs.existsSync);
const nodes = names => names.map(name => ({name, type:'ss',server:'example.invalid',port:443,cipher:'aes-128-gcm',password:'test-only'}));
function run(file, config) {
 const sandbox = {input:config};
 vm.createContext(sandbox);
 vm.runInContext(fs.readFileSync(file,'utf8')+'\nresult = main(input);', sandbox, {timeout:2000});
 return JSON.parse(JSON.stringify(sandbox.result));
}
function validate(c) {
 const groups = new Map(c['proxy-groups'].map(g=>[g.name,g]));
 const known = new Set(['DIRECT','REJECT',...c.proxies.map(p=>p.name),...groups.keys()]);
 assert.equal(groups.size,c['proxy-groups'].length);
 for (const g of groups.values()) {
  assert.ok(g.proxies.length, g.name+' is empty');
  assert.equal(g.proxies.length,new Set(g.proxies).size);
  for(const n of g.proxies) assert.ok(known.has(n),`${g.name}: missing ${n}`);
 }
 const walk=(name,path=[])=>{
  assert.ok(!path.includes(name),'group cycle '+[...path,name]);
  if(groups.has(name)) groups.get(name).proxies.forEach(n=>walk(n,[...path,name]));
 };
 for(const name of groups.keys()) walk(name);
 for(const rule of c.rules){
  const parts=rule.split(',');
  const target=parts.at(-1)==='no-resolve'?parts.at(-2):parts.at(-1);
  assert.ok(known.has(target),'missing rule target '+target);
  if(parts[0]==='RULE-SET') assert.ok(c['rule-providers'][parts[1]],'missing provider');
 }
 assert.equal(c.rules.at(-1),'MATCH,PROXY-Gate');
 assert.equal(new Set(c.rules).size,c.rules.length);
}
for(const file of files){
 test(file+' preserves networking, nodes and input; deterministic/idempotent',()=>{
  const config={proxies:nodes(['日本 01','新加坡 01','马来西亚 01','澳洲 01','印度 01','unknown']),dns:{enable:true,nameserver:['1.1.1.1']},tun:{enable:false},'mixed-port':8888,'proxy-providers':{source:{type:'inline',payload:[]}},profile:{'store-fake-ip':false},rules:['MATCH,DIRECT']};
  const original=JSON.stringify(config); const c=run(file,config); validate(c);
  assert.equal(JSON.stringify(config),original);
  for(const key of ['proxies','dns','tun','mixed-port','proxy-providers']) assert.deepEqual(c[key],config[key]);
  assert.deepEqual(run(file,c),c); assert.deepEqual(run(file,config),c);
 });
 test(file+' empty, provider-only, invalid and duplicate nodes fail clearly',()=>{
  for(const config of [null,{}, {proxies:[]},{'proxy-providers':{p:{}}},{proxies:['JP']},{proxies:nodes(['JP','JP'])},{proxies:nodes(['DIRECT'])},{proxies:nodes(['YouTube'])},{proxies:nodes(['JP']), 'proxy-providers':{YouTube:{}}},{proxies:[{...nodes(['JP'])[0], 'dialer-proxy':'removed-source-group'}]}]) assert.throws(()=>run(file,config),/Runestone/);
 });
 test(file+' unidentified nodes remain usable without empty groups',()=>{
  const c=run(file,{proxies:nodes(['Unclassified 1'])}); validate(c);
  assert.deepEqual(c['proxy-groups'].find(g=>g.name==='APNs-Fallback').proxies,['Unclassified 1']);
 });
 test(file+' recognizes MY AU IN and avoids short-code substring collisions',()=>{
  const names=['🇲🇾 1','馬來西亞 2','Kuala Lumpur 3','MY01','AU01','澳大利亞 2','Melbourne 3','IN01','印度 2','Mumbai 3','Singapore 1','Premium 1','Main 1','AUSome 1','MYriad 1','INLINE 1'];
  const c=run(file,{proxies:nodes(names)}); validate(c);
  for(const [name,expected] of [['🇲🇾 MY-Auto',names.slice(0,4)],['🇦🇺 AU-Auto',names.slice(4,7)],['🇮🇳 IN-Auto',names.slice(7,10)]]) assert.deepEqual(c['proxy-groups'].find(g=>g.name===name).proxies,expected);
 });
 test(file+' explicit services precede final catch-all',()=>{
  const c=run(file,{proxies:nodes(['日本'])}); validate(c);
  for(const [domain,group] of [['pixiv.net','Pixiv'],['pximg.net','Pixiv'],['linkedin.com','LinkedIn'],['licdn.com','LinkedIn'],['threads.net','Threads'],['threads.com','Threads']]) assert.ok(c.rules.includes(`DOMAIN-SUFFIX,${domain},${group}`));
  assert.ok(!c.rules.some(r=>/DOMAIN-KEYWORD,(google|copilot|grok),/.test(r)));
 });
}
if(files.includes('JS/Runestone_Charlie.js')) test('personal preferences, shared Meta region and fork-only MRS',()=>{
 const c=run('JS/Runestone_Charlie.js',{proxies:nodes(['日本','新加坡','马来西亚','美国'])});
 const group=n=>c['proxy-groups'].find(g=>g.name===n);
 assert.equal(group('GPT').proxies[0],'🇯🇵 JP-Manual');
 assert.equal(group('YouTube').proxies[0],'🇯🇵 JP-Auto');
 assert.equal(group('Spotify').proxies[0],'🇲🇾 MY-Manual');
 assert.equal(group('Apple').proxies[0],'DIRECT');
 for(const n of ['Facebook','Instagram','Threads']) assert.equal(group(n).proxies[0],'Meta-Region');
 for(const p of Object.values(c['rule-providers']).filter(p=>p.url.includes('/Network-Profiles/'))) assert.ok(p.url.includes('charlienotcharles284-cyber/Network-Profiles'));
});
