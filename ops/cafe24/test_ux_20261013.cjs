/* DOM integration checks, without a browser or customer data. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {JSDOM}=require(process.env.TAM_JSDOM_PATH || 'jsdom');
const root=path.resolve(__dirname,'../..'),base=path.join(root,'storefront-v2/preview');
let passed=0;const results=[];
function check(name,fn){fn();passed++;results.push(name);}
function load(name){
 const dom=new JSDOM(fs.readFileSync(path.join(base,name),'utf8'),{url:'https://example.test/'+name,runScripts:'outside-only',pretendToBeVisual:true});
 const w=dom.window;w.matchMedia=()=>({matches:false,addEventListener(){},removeEventListener(){}});
 w.HTMLElement.prototype.scrollIntoView=function(){};
 w.HTMLMediaElement.prototype.pause=function(){};w.HTMLMediaElement.prototype.play=function(){return Promise.resolve();};
 w.IntersectionObserver=class{observe(){}disconnect(){}};
 // Execute scripts as deferred HTML does, in document order; no third-party fetches.
 for(const script of [...w.document.querySelectorAll('script[src]')]){
  const src=script.getAttribute('src').split('?')[0];if(!src.startsWith('assets/'))continue;
  w.eval(fs.readFileSync(path.join(base,src),'utf8'));
 }
 w.document.dispatchEvent(new w.Event('DOMContentLoaded'));
 return dom;
}
const pages=fs.readdirSync(base).filter(n=>n.endsWith('.html')&&fs.readFileSync(path.join(base,n),'utf8').includes('class="ux-header"'));
for(const name of pages){
 const dom=load(name),w=dom.window,d=w.document;
 check(name+' common navigation',()=>{assert.equal(d.querySelectorAll('.ux-header').length,1);assert.equal(d.querySelectorAll('.ux-footer').length,1);assert(d.querySelector('.ux-utilities a[href="search.html"]'));});
 check(name+' menu closes and updates aria',()=>{const b=d.querySelector('.ux-menu-toggle');b.click();assert.equal(b.getAttribute('aria-expanded'),'true');d.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape'}));assert.equal(b.getAttribute('aria-expanded'),'false');});
 const opts=d.querySelector('[data-preview-product]');
 if(opts){
  const select=opts.querySelector('select'),qty=opts.querySelector('input[type=number]');
  check(name+' purchase bar follows option and quantity',()=>{select.selectedIndex=1;select.dispatchEvent(new w.Event('change',{bubbles:true}));qty.value='2';qty.dispatchEvent(new w.Event('input',{bubbles:true}));const p=w.TAM_CATALOG.find(p=>p.id===Number(opts.dataset.previewProduct));assert.equal(d.querySelector('.ux-buybar strong').textContent,(p.price*2).toLocaleString('ko-KR')+'원');assert.equal(d.querySelector('.ux-buybar button').textContent,'바로 구매');});
  check(name+' cart retains exact option value',()=>{opts.querySelector('[data-add]').click();const cart=JSON.parse(w.sessionStorage.getItem('tam-preview-cart-v2'));assert.equal(cart[0].option,select.value);assert.equal(cart[0].qty,2);});
  check(name+' bottom buy uses existing handler',()=>{let clicks=0;opts.querySelector('[data-buy]').onclick=()=>clicks++;d.querySelector('.ux-buybar button').click();assert.equal(clicks,1);});
  check(name+' invalid quantity does not buy',()=>{let clicks=0;opts.querySelector('[data-buy]').onclick=()=>clicks++;qty.value='0';d.querySelector('.ux-buybar button').click();assert.equal(clicks,0);});
  check(name+' details and review anchors resolve',()=>{for(const a of d.querySelectorAll('.ux-detail-nav a[href^="#"]'))assert(d.querySelector(a.getAttribute('href')));});
  const shades=[...d.querySelectorAll('.ux-shade-button')];
  if(shades.length)check(name+' all photographic shades map to actual options',()=>{for(const [i,b] of shades.entries()){b.click();assert.equal(select.selectedIndex,i+1);assert.equal(b.getAttribute('aria-pressed'),'true');assert(d.querySelector('.ux-shade-selected').textContent.includes(select.selectedOptions[0].textContent.split('.')[1].trim()));}});
 }
 if(name==='design-only.html'){
  check('hero v16 retained',()=>{const v=d.querySelector('.do-hero video');assert(v.loop&&v.autoplay&&v.hasAttribute('muted'));assert(v.querySelector('source').src.includes('v16-261013'));});
  check('logo overlay and loop reset timing retained',()=>{const v=d.querySelector('.do-hero video');v.currentTime=6.2;v.dispatchEvent(new w.Event('timeupdate'));assert(d.querySelector('.do-hero').hasAttribute('data-film-ending'));v.currentTime=.1;v.dispatchEvent(new w.Event('timeupdate'));assert(!d.querySelector('.do-hero').hasAttribute('data-film-ending'));});
  check('four products have prices',()=>assert.equal(d.querySelectorAll('.ux-product-price').length,4));
  check('repeated brand panel removed',()=>assert.equal(d.querySelectorAll('.brand-note').length,0));
 }
 check(name+' automatic coupon solicitation disabled',()=>{assert.equal(d.querySelectorAll('footer .tam-channel-trigger').length,0);const panel=d.querySelector('.tam-channel-panel');if(panel)assert(panel.hidden);});
 dom.window.close();
}
const report={kind:'jsdom integration, not rendered browser QA',pages:pages.length,passed,checks:results};
fs.writeFileSync(path.join(root,'ops/cafe24/ux-dom-20261013.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({pages:pages.length,passed}));
