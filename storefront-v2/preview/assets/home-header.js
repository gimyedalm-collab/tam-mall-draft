/* Only the homepage opts in; commerce pages retain their existing navigation. */
(() => {
  const header=document.querySelector('.home-film .ux-header');
  if(!header)return;
  const menu=header.querySelector('.ux-links');
  const toggle=header.querySelector('.ux-menu-toggle');
  const sync=()=>header.classList.toggle('is-solid',window.scrollY>16||toggle?.getAttribute('aria-expanded')==='true');
  sync();
  header.setAttribute('data-home-header-ready','');
  let scheduled=false;
  window.addEventListener('scroll',()=>{
    if(scheduled)return;
    scheduled=true;
    requestAnimationFrame(()=>{scheduled=false;sync();});
  },{passive:true});
  window.addEventListener('pageshow',sync);
  if(toggle)new MutationObserver(sync).observe(toggle,{attributes:true,attributeFilter:['aria-expanded']});
  if(menu)new MutationObserver(sync).observe(menu,{attributes:true,attributeFilter:['class']});
})();
