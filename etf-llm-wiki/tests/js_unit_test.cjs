// Fast interaction unit tests using a minimal DOM event simulator, no browser network needed.
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const root=path.resolve(__dirname,'..');
function element(attrs={}){
  const handlers={};
  return {
    ...attrs,hidden: attrs.hidden??false,disabled:attrs.disabled??false,
    style:{},dataset:attrs.dataset||{},innerHTML:'',textContent:'',value: attrs.value||'',
    addEventListener(type,cb){handlers[type]=cb},click(){handlers.click?.()},
    fire(type,event={}){handlers[type]?.(event)},
    setAttribute(key,val){this[key]=val},
    isVisible(){return !this.hidden}
  };
}
const slides=Array.from({length:10},(_,i)=>element({hidden:i>0}));
const prev=element(),next=element(),fill=element(),counter=element();
const reveal=element(),explain=element({hidden:true}),quizCheck=element(),quizResult=element();
const q=[element({dataset:{answer:'B'}}),element({dataset:{answer:'A'}}),element({dataset:{answer:'B'}})];
let responses=[null,null,null];
q.forEach((x,i)=>x.querySelector=()=>responses[i]?element({value:responses[i]}):null);
const els={'prevBtn':prev,'nextBtn':next,'progressFill':fill,'progressText':counter,'dividendReveal':reveal,'dividendExplanation':explain,'quizCheck':quizCheck,'quizResult':quizResult};
const location={hash:''};const history={replaceState:(_,__,hash)=>{location.hash=hash}};
const document={
  querySelectorAll(qs){if(qs==='.slide')return slides;if(qs==='.quiz-question')return q;throw Error('unexpected '+qs)},
  getElementById(id){if(!els[id])throw Error(id);return els[id]},
  addEventListener(type,fn){this[type]=fn},activeElement:{tagName:'BODY'}
};
const window={addEventListener(){}};
const ctx={document,history,location,window,console};
vm.runInNewContext(fs.readFileSync(path.join(root,'slides/script.js'),'utf8'),ctx);
assert.equal(slides[0].hidden,false);assert.equal(next.disabled,false);assert.equal(prev.disabled,true);
next.click();assert.equal(slides[1].hidden,false);assert.equal(location.hash,'#slide-2');
document.keydown({key:'ArrowRight',preventDefault(){}});assert.equal(slides[2].hidden,false);
document.keydown({key:'End',preventDefault(){}});assert.equal(slides[9].hidden,false);assert.equal(next.disabled,true);
quizCheck.click();assert(quizResult.textContent.includes('請先完成'));
responses=['B','A','B'];quizCheck.click();assert(quizResult.textContent.includes('3 / 3'));
reveal.click();assert.equal(explain.hidden,false);assert.equal(reveal['aria-expanded'],'true');
reveal.click();assert.equal(explain.hidden,true);assert.equal(reveal['aria-expanded'],'false');
document.keydown({key:'Home',preventDefault(){}});assert.equal(slides[0].hidden,false);
console.log('PASS JS controls: page navigation, keyboard, bounds, 3-question quiz, reveal toggle (9 assertions)');
