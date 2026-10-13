/* Preview enhancement. Native Cafe24 options must be mapped during migration. */
(() => {
 'use strict';
 const menu=document.querySelector('.ux-links'),toggle=document.querySelector('.ux-menu-toggle');
 const close=()=>{menu?.classList.remove('is-open');toggle?.setAttribute('aria-expanded','false');};
 toggle?.addEventListener('click',()=>{const open=menu.classList.toggle('is-open');toggle.setAttribute('aria-expanded',String(open));});
 menu?.addEventListener('click',e=>{if(e.target.closest('a'))close();});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.classList.contains('is-open')){close();toggle.focus();}});
 document.addEventListener('pointerdown',e=>{if(!e.target.closest('.ux-header'))close();});
 matchMedia('(min-width:901px)').addEventListener('change',close);
 const file=location.pathname.split('/').pop();
 document.querySelectorAll('.ux-links a').forEach(a=>{if(a.getAttribute('href')===file)a.setAttribute('aria-current','page');});
 const options=document.querySelector('[data-preview-product]');
 if(options){
  const select=options.querySelector('select'),qty=options.querySelector('input[type=number]');
  const product=(window.TAM_CATALOG||[]).find(p=>p.id===Number(options.dataset.previewProduct));
  const buttons=[...document.querySelectorAll('.ux-shade-button')];
  const selected=document.querySelector('.ux-shade-selected');
  buttons.forEach(button=>button.addEventListener('click',()=>{
   const option=select.options[Number(button.dataset.optionIndex)];
   if(!option||option.disabled)return;
   select.value=option.value;select.dispatchEvent(new Event('change',{bubbles:true}));
  }));
  const bar=document.createElement('aside');bar.className='ux-buybar';bar.setAttribute('aria-label','선택 상품 구매');
  const info=document.createElement('div');info.className='ux-buybar-info';
  const label=document.createElement('span'),price=document.createElement('strong');info.append(label,price);
  const buy=document.createElement('button');buy.type='button';bar.append(info,buy);document.body.append(bar);document.body.classList.add('ux-has-buybar');
  const update=()=>{
   const choice=select.selectedOptions[0];
   buttons.forEach(b=>b.setAttribute('aria-pressed',String(select.selectedIndex===Number(b.dataset.optionIndex))));
   if(selected)selected.textContent=select.value?(choice.dataset.description||choice.textContent.trim()):'컬러를 눌러 선택해 주세요.';
   label.textContent=select.value?choice.textContent.trim():'색상을 선택해 주세요';
   const n=Number(qty.value);price.textContent=product?((Number.isInteger(n)&&n>=1&&n<=99?n:1)*product.price).toLocaleString('ko-KR')+'원':'';
   buy.textContent=select.value?'바로 구매':'옵션 선택';
  };
  buy.addEventListener('click',()=>{
   if(!select.value||!qty.checkValidity()){
    options.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'auto':'smooth',block:'center'});
    (select.value?qty:select).focus({preventScroll:true});return;
   }
   options.querySelector('[data-buy]').click();
  });
  options.addEventListener('change',update);options.addEventListener('input',update);update();
  if('IntersectionObserver' in window){
   const observer=new IntersectionObserver(([entry])=>{bar.hidden=entry.isIntersecting;},{threshold:0.1});observer.observe(options);
  }
 }
 document.querySelectorAll('.ux-detail-nav a[href^="#"]').forEach(a=>a.addEventListener('click',()=>{
  const target=document.getElementById(a.hash.slice(1));if(target?.tagName==='DETAILS')target.open=true;
 }));
 const motion=matchMedia('(prefers-reduced-motion:reduce)');
 document.querySelectorAll('.ux-detail-media').forEach(figure=>{
  const video=figure.querySelector('video'),button=figure.querySelector('button'),status=figure.querySelector('.ux-media-status');
  let manuallyPaused=false;
  const sync=()=>{button.textContent=video.paused?'사용 장면 재생':'사용 장면 멈춤';button.setAttribute('aria-pressed',String(!video.paused));};
  button.addEventListener('click',()=>{if(video.paused){manuallyPaused=false;video.play().catch(()=>{status.textContent='재생할 수 없습니다. 아래 원본 보기로 확인해 주세요.';});}else{manuallyPaused=true;video.pause();}});
  video.addEventListener('play',sync);video.addEventListener('pause',sync);
  motion.addEventListener('change',()=>{if(motion.matches)video.pause();});
  if('IntersectionObserver' in window){new IntersectionObserver(([entry])=>{
   if(entry.isIntersecting&&!motion.matches&&!manuallyPaused)video.play().catch(()=>{});else video.pause();
  },{threshold:.2}).observe(video);}
  sync();
 });
})();
