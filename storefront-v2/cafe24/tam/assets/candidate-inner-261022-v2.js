/* Candidate skin only. Native commerce modules remain the source of prices/actions. */
(() => {
  'use strict';
  if (!location.pathname.startsWith('/skin-skin21/')) return;
  const base='/skin-skin21', media='https://awiz.cafe24.com/tam-detail-20261022/inner-';
  const catalog={23:['jelly','base'],111:['cloud','base'],102:['jelly','cheek'],110:['cloud','cheek'],24:['jelly','cheek'],109:['cloud','cheek'],18:['jelly','lip'],112:['cloud','lip'],101:['jelly','lip'],118:['cloud','lip'],25:['jelly','lip'],114:['cloud','base'],115:['cloud','brow'],121:['cloud','brow']};
  function init(){
    const header=document.querySelector('body.tam-native > .tam-nav-header');
    if(header){
      const button=header.querySelector('.tam-nav-menu-toggle'),nav=header.querySelector('.tam-nav-links');
      const close=()=>{nav.classList.remove('is-open');button.setAttribute('aria-expanded','false');};
      button.addEventListener('click',()=>{const open=button.getAttribute('aria-expanded')!=='true';button.setAttribute('aria-expanded',String(open));nav.classList.toggle('is-open',open);});
      header.addEventListener('keydown',e=>{if(e.key==='Escape'){close();button.focus();}});
      document.addEventListener('click',e=>{if(!header.contains(e.target))close();});
      matchMedia('(min-width:901px)').addEventListener('change',close);
      for(const a of nav.querySelectorAll('a'))if(new URL(a.href).pathname===location.pathname&&!new URL(a.href).searchParams.has('tam_collection'))a.setAttribute('aria-current','page');
    }
    function decorate(card){
      const id=Number(card.id.replace('anchorBoxId_','')),info=catalog[id];if(!info)return;
      card.dataset.tamLine=info[0];card.dataset.tamCategory=info[1];
      const img=card.querySelector('.thumbnail>a>img');
      if(img&&!img.dataset.tamPackshot){
        img.dataset.tamPackshot='true';img.removeAttribute('data-src');img.classList.remove('asyncImage');
        img.src=media+(id===23?'cushion-pink-original-2.png':`packshot-${id}.png`);img.loading='lazy';img.decoding='async';
      }
      const desc=card.querySelector('.description');
      if(desc&&!desc.querySelector('.tam-line-tag')){const tag=document.createElement('span');tag.className='tam-line-tag';tag.textContent=`THE ${info[0].toUpperCase()} LINE`;desc.prepend(tag);}
    }
    const shop=document.querySelector('[data-tam-catalog]');
    if(shop){
      const params=new URLSearchParams(location.search), requested=params.get('tam_collection');
      let line=['jelly','cloud'].includes(requested)?requested:'all',category='all';
      const title=document.querySelector('[data-tam-shop-title]');
      const update=()=>{
        document.body.dataset.tamCollection=line;
        const cards=[...shop.querySelectorAll('.prdList>li[id^="anchorBoxId_"]')];
        cards.forEach(card=>{decorate(card);card.hidden=!((line==='all'||card.dataset.tamLine===line)&&(category==='all'||card.dataset.tamCategory===category));});
        shop.querySelectorAll('[data-tam-line]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.tamLine===line)));
        shop.querySelectorAll('[data-tam-category]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.tamCategory===category)));
        const count=cards.filter(c=>!c.hidden).length;shop.querySelector('.tam-count').textContent=`${count} products`;
        shop.querySelector('.tam-empty').hidden=count>0;
        if(title)title.textContent=line==='all'?'Shop all':line==='jelly'?'The Jelly':'The Cloud';
        const select=shop.querySelector('#selArray');if(select)for(const o of select.options){if(!o.value)continue;const url=new URL(o.value,location.href);line==='all'?url.searchParams.delete('tam_collection'):url.searchParams.set('tam_collection',line);o.value=url.pathname+url.search;}
      };
      shop.querySelector('.tam-filters').addEventListener('click',e=>{
        const b=e.target.closest('button');if(!b)return;
        if(b.dataset.tamLine){line=b.dataset.tamLine;const url=new URL(location.href);line==='all'?url.searchParams.delete('tam_collection'):url.searchParams.set('tam_collection',line);history.replaceState(null,'',url);}
        if(b.dataset.tamCategory)category=b.dataset.tamCategory;update();
      });
      update();const grid=shop.querySelector('.prdList');if(grid)new MutationObserver(update).observe(grid,{childList:true});
    }
    const explore=document.querySelector('[data-tam-explore]');
    if(explore){
      fetch(base+'/product/list.html?cate_no=74',{credentials:'same-origin'}).then(r=>{if(!r.ok)throw Error('catalog');return r.text();}).then(html=>{
        const doc=new DOMParser().parseFromString(html,'text/html'),grid=document.createElement('ul');grid.className='tam-explore-grid';
        for(const card of doc.querySelectorAll('.prdList>li[id^="anchorBoxId_"]')){
          const id=Number(card.id.replace('anchorBoxId_',''));if(!catalog[id])continue;
          const nativeLink=card.querySelector('.thumbnail>a'),name=card.querySelector('.name'),price=card.querySelector('.spec');if(!nativeLink||!name||!price)continue;
          const item=document.createElement('li'),link=document.createElement('a'),img=document.createElement('img'),label=document.createElement('span'),heading=document.createElement('h3');
          const cleanName=name.cloneNode(true);cleanName.querySelectorAll('.title').forEach(e=>e.remove());
          link.href=nativeLink.getAttribute('href');img.src=media+(id===23?'cushion-pink-original-2.png':`packshot-${id}.png`);img.alt=cleanName.textContent.trim();img.loading='lazy';img.width=800;img.height=800;
          label.className='tam-line-tag';label.textContent=`THE ${catalog[id][0].toUpperCase()} LINE`;heading.textContent=img.alt;
          const prices=price.cloneNode(true);prices.querySelectorAll('.title,script').forEach(n=>n.remove());prices.querySelectorAll('[id]').forEach(n=>n.removeAttribute('id'));
          link.append(img,label,heading,prices);item.append(link);const icons=card.querySelector('.icon');if(icons)item.append(icons.cloneNode(true));grid.append(item);
        }
        if(grid.children.length)explore.replaceChildren(grid);
      }).catch(()=>{/* Visible native catalog link remains available. */});
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
