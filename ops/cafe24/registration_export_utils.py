"""Small, shared corrections for noninteractive Cafe24 image exports."""
CLOUD_INFO_ALT = '제품 정보 · 전성분'

def prepare_cloud_info(page):
    page.evaluate('''()=>{
      const info=document.querySelector('#cloud-blush .product-info');
      if(!info)return;
      info.open=true;
      info.querySelectorAll('a').forEach(a=>{
        const p=a.parentElement;
        if(p.tagName==='P' && p.textContent.trim()===a.textContent.trim())p.remove();
        else a.remove();
      });
      const walker=document.createTreeWalker(info,NodeFilter.SHOW_TEXT);
      while(walker.nextNode())walker.currentNode.textContent=walker.currentNode.textContent.replace(/\uFEFF/g,'');
    }''')
    page.add_style_tag(content='#cloud-blush .product-info summary{list-style:none;cursor:default}#cloud-blush .product-info summary::marker{content:""}#cloud-blush .product-info summary::-webkit-details-marker{display:none}')

def panel_alt(page,top,bottom,info=False):
    if info:return CLOUD_INFO_ALT
    text=page.evaluate('''([top,bottom])=>[...document.querySelectorAll('h1,h2,h3,p,summary,figcaption')].filter(e=>{
      const r=e.getBoundingClientRect();
      return r.top+scrollY>=top&&r.top+scrollY<bottom&&!e.querySelector('h1,h2,h3,p,summary,figcaption');
    }).map(e=>e.innerText).join(' ')''',[top,bottom])
    return ' '.join(text.replace('\ufeff','').split())[:1800]
