// Lightweight DOM stand-in: checks behavior, not browser layout. Run: node tests/ui_smoke.cjs
const fs=require('fs'),vm=require('vm'),assert=require('assert');
class Element{constructor(){this.value='';this.children=[];this.style={};this.dataset={};this.textContent='';this.disabled=false;this.checked=false}setAttribute(k,v){this[k]=v}append(...nodes){this.children.push(...nodes)}replaceChildren(...nodes){this.children=nodes}click(){} }
const elements=new Map();const get=id=>{if(!elements.has(id))elements.set(id,new Element());return elements.get(id)};get('view').value='colors';
const rgb=new Element();rgb.dataset.rgb='10,20,30';const start=new Element();start.dataset.start='15';
const snapshot={mode:'ДАДЛАГЫН ЗАГВАРЧЛАЛ',colors:{found:0,head:{next:1,prev:1},nodes:[{id:1,r:255,g:0,b:0,prev:0,next:0}]},collatz:{head:{next:1,prev:1},nodes:[{id:1,value:'1',next:0,prev:0}]}};
let calls=0,interval;const context={document:{getElementById:get,createElement:()=>new Element(),createElementNS:()=>new Element(),querySelectorAll:q=>q==='[data-rgb]'?[rgb]:[start],hidden:false},fetch:async()=>{calls++;return {ok:true,json:async()=>snapshot}},setInterval:f=>interval=f,setTimeout,URL,Blob,Date,console};
vm.createContext(context);vm.runInContext(fs.readFileSync(require('path').join(__dirname,'../src/ui/index.html'),'utf8').match(/<script>([\s\S]*)<\/script>/)[1],context);
(async()=>{await new Promise(setImmediate);assert.equal(get('count').textContent,1);rgb.onclick();assert.equal(get('r').value,'10');assert.equal(calls,1,'preset must not mutate backend');
let graph=get('graph').children[0];let node=graph.children.find(n=>n['data-id']===1);assert(node);node.onclick();assert.equal(get('id').value,1);assert.equal(get('r').value,255);
get('auto').checked=true;interval();interval();await new Promise(setImmediate);assert.equal(calls,2,'poll requests must not overlap');
context.fetch=async()=>({ok:false,json:async()=>({error:'Тестийн алдаа'})});get('add').onclick();await new Promise(setImmediate);assert(get('history').children[0].textContent.includes('Тестийн алдаа'));assert.equal(get('add').disabled,false);
console.log('PASS: rendering, non-mutating presets, graph selection, poll concurrency and failed-operation history');})().catch(e=>{console.error(e);process.exitCode=1});
