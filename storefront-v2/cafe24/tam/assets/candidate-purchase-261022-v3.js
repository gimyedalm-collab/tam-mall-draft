/* Presentation/accessibility only: native options, prices and commerce handlers remain. */
(() => {
  'use strict';
  if (!/^\/skin-skin21(?:\/|$)/.test(location.pathname)) return;
  const layer=document.querySelector('.infoArea .jsMobileLayer');
  const bar=document.querySelector('.infoArea .mobile-fix-footer');
  if (!layer || !bar || layer.dataset.tamPurchaseReady) return;
  layer.dataset.tamPurchaseReady='true';
  const heading=document.createElement('div');heading.className='tam-purchase-heading';
  const title=document.createElement('strong');title.id='tam-purchase-title';
  title.textContent=document.querySelector('.infoArea h1')?.textContent.trim() || '옵션 선택';
  const close=document.createElement('button');close.type='button';close.className='tam-purchase-close';close.textContent='닫기';
  heading.append(title,close);layer.prepend(heading);
  close.addEventListener('click',()=>layer.querySelector('.jsFixClose')?.click());
  for(const control of bar.querySelectorAll('.jsLayerBtn,.yCartBtn,.jsGoReview')){
    control.setAttribute('role','button');control.tabIndex=0;
    if(control.matches('.jsGoReview')) control.setAttribute('aria-label','리뷰 보기');
    control.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();control.click();}});
  }
  const opener=bar.querySelector('.jsLayerBtn');
  layer.id ||= 'tam-native-options';
  opener?.setAttribute('aria-controls',layer.id);
  let wasOpen=false,returnFocus=null;
  const focusables=()=>[...layer.querySelectorAll('button,a[href],input,select,textarea,[tabindex]')].filter(e=>!e.disabled&&e.tabIndex>=0&&e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden');
  function sync(){
    const fixed=layer.classList.contains('fixed'),open=fixed&&layer.classList.contains('on');
    document.documentElement.classList.toggle('tam-purchase-open',open);
    layer.inert=fixed&&!open;
    if(fixed&&!open) layer.setAttribute('aria-hidden','true');else layer.removeAttribute('aria-hidden');
    bar.inert=!fixed||open;
    opener?.setAttribute('aria-expanded',String(open));
    if(open){
      layer.setAttribute('role','dialog');layer.setAttribute('aria-modal','true');layer.setAttribute('aria-labelledby',title.id);
      if(!wasOpen){
        returnFocus=bar.contains(document.activeElement)?document.activeElement:opener;
        // Native visibility transitions can reject focus in the first frame.
        setTimeout(()=>{if(layer.classList.contains('on')&&layer.classList.contains('fixed'))close.focus({preventScroll:true});},250);
      }
    }else{
      layer.removeAttribute('role');layer.removeAttribute('aria-modal');layer.removeAttribute('aria-labelledby');
      if(wasOpen){
        const destination=returnFocus;
        // Wait for the native bar's visibility transition before restoring focus.
        setTimeout(()=>{
          if(!layer.classList.contains('on')&&layer.classList.contains('fixed')&&destination?.isConnected&&!destination.closest('[inert]')) destination.focus({preventScroll:true});
        },320);
      }
    }
    wasOpen=open;
  }
  document.addEventListener('keydown',e=>{
    if(!wasOpen)return;
    if(e.key==='Escape'){e.preventDefault();close.click();}
    if(e.key==='Tab'){
      const items=focusables(),first=items[0],last=items.at(-1);
      if(!items.length){e.preventDefault();close.focus();return;}
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
    }
  });
  new MutationObserver(sync).observe(layer,{attributes:true,attributeFilter:['class']});
  sync();
})();
