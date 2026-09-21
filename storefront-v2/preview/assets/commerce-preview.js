/* Preview only. Never included in the Cafe24 skin or used for payment. */
(()=>{const KEY='tam-preview-cart-v2';
 const money=n=>Number(n).toLocaleString('ko-KR')+'원';
 const products=window.TAM_CATALOG||[];
 const find=id=>products.find(p=>p.id===Number(id));
 const read=()=>{try{return JSON.parse(sessionStorage.getItem(KEY)||'[]').filter(x=>find(x.id)&&Number.isInteger(x.qty)&&x.qty>0&&x.qty<=99&&find(x.id).options.some(o=>o.values.includes(x.option)))}catch{return []}};
 const save=cart=>sessionStorage.setItem(KEY,JSON.stringify(cart));
 const status=document.querySelector('[data-status]');
 const say=text=>{if(status)status.textContent=text};
 const detail=document.querySelector('[data-preview-product]');
 if(detail){const id=Number(detail.dataset.previewProduct),select=detail.querySelector('select'),qty=detail.querySelector('input[type=number]');
 const add=()=>{const n=Number(qty.value);if(!select.value){select.reportValidity();say('색상을 선택해 주세요.');return false}if(!Number.isInteger(n)||n<1||n>99){qty.reportValidity();say('수량은 1개부터 99개까지 선택할 수 있습니다.');return false}const cart=read(),old=cart.find(p=>p.id===id&&p.option===select.value);if(old)old.qty=Math.min(99,old.qty+n);else cart.push({id,option:select.value,qty:n});save(cart);return true};
 detail.querySelector('[data-add]').onclick=()=>{if(!add())return;say('장바구니에 담았습니다.');detail.querySelector('[data-basket-link]').hidden=false};
 /* 바로 구매: 같은 확인을 거쳐 담은 뒤 주문서 화면으로. 카페24에서는 기본 구매 모듈(product_submit)이 이 자리를 맡는다. */
 const buy=detail.querySelector('[data-buy]');if(buy)buy.onclick=()=>{if(add())location.href='checkout.html'};
 }
 const basket=document.querySelector('[data-basket-items]');
 const summary=document.querySelector('[data-subtotal]');
 const render=()=>{const cart=read();if(summary)summary.textContent=money(cart.reduce((sum,x)=>sum+find(x.id).price*x.qty,0));if(!basket)return;basket.replaceChildren();
 cart.forEach((item,index)=>{const p=find(item.id),row=document.createElement('article');row.className='cart-row';const img=document.createElement('img');img.src=p.asset;img.alt=p.name;row.append(img);const info=document.createElement('div'),link=document.createElement('a');link.href='product-'+p.id+'.html';link.textContent=p.name;info.append(link);const option=document.createElement('p');option.textContent=item.option;info.append(option);const controls=document.createElement('div');controls.className='quantity-control';
 [-1,1].forEach(delta=>{const b=document.createElement('button');b.type='button';b.textContent=delta<0?'−':'+';b.setAttribute('aria-label',p.name+' 수량 '+(delta<0?'줄이기':'늘리기'));b.disabled=delta<0?item.qty<=1:item.qty>=99;b.onclick=()=>{const next=read();next[index].qty+=delta;save(next);render()};controls.append(b);if(delta===-1){const output=document.createElement('span');output.textContent=item.qty;controls.append(output)}});info.append(controls);row.append(info);const end=document.createElement('div');end.className='cart-end';const total=document.createElement('p');total.textContent=money(p.price*item.qty);end.append(total);const remove=document.createElement('button');remove.textContent='삭제';remove.onclick=()=>{save(read().filter((_,i)=>i!==index));render();say('상품을 삭제했습니다.')};end.append(remove);row.append(end);basket.append(row)});
 document.querySelector('[data-cart-empty]')?.toggleAttribute('hidden',cart.length>0);document.querySelector('[data-checkout-link]')?.toggleAttribute('hidden',cart.length===0);
 };render();
 const search=document.querySelector('[data-search]');if(search){const apply=()=>{const term=search.value.trim().toLowerCase();let count=0;document.querySelectorAll('.product').forEach(p=>{p.hidden=!p.textContent.toLowerCase().includes(term);if(!p.hidden)count++});document.querySelector('[data-search-count]').textContent=count+'개 제품';document.querySelector('[data-search-empty]').hidden=count>0};search.addEventListener('input',apply);apply()}
})();
