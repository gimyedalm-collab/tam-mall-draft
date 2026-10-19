"""Format supplied Cloud information without changing ordered INCI or facts."""
from bs4 import BeautifulSoup
import html,re

def normalize(text):
    return ' '.join(text.replace('\ufeff','').split())

def compact_information(original):
    soup=BeautifulSoup(original,'html.parser')
    paragraphs=soup.select('.product-info > div > p')
    assert len(paragraphs)==7
    facts=normalize(paragraphs[0].get_text())
    labels=['용량 및 중량','제품 주요 사양','사용 기한','사용 방법','화장품책임판매업자','제조국','품질보증 기준','탐뷰티 고객상담실']
    positions=[facts.index(label) for label in labels]
    values=[facts[pos+len(label):(positions[i+1] if i+1<len(labels) else len(facts))].strip() for i,(pos,label) in enumerate(zip(positions,labels))]
    assert normalize(' '.join(f'{k} {v}' for k,v in zip(labels,values)))==facts
    rows=''.join(f'<div><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>' for k,v in zip(labels,values))
    lists=[]
    for i,p in enumerate(paragraphs[1:],1):
        text=normalize(p.get_text())
        match=re.fullmatch(r'\[\s*탐 뷰티 더 클라우드 블러 크림 블러셔(\d{2})\s+([^\]]+)\]\s*(.*)',text)
        assert match and int(match[1])==i
        lists.append(f'<div class="inci-shade"><h3>{match[1]} {html.escape(match[2].strip())}</h3><p>{html.escape(match[3])}</p></div>')
    return '<details class="product-info"><summary>제품 정보 · 전성분</summary><div><dl class="product-facts">'+rows+'</dl><h2 class="inci-title">전성분</h2>'+''.join(lists)+'</div></details>'

def registration_information(source):
    """Native text avoids doubling small-print size with 860px raster panels."""
    soup=BeautifulSoup(source,'html.parser')
    info=soup.select_one('.product-info')
    rows=[]
    for row in info.select('.product-facts > div'):
        label=html.escape(row.dt.get_text());value=html.escape(row.dd.get_text())
        label=label.replace('화장품책임판매업자','화장품책임<br>판매업자').replace('탐뷰티 고객상담실','탐뷰티<br>고객상담실')
        rows.append(f'<tr><th scope="row" style="width:100px;padding:5px 10px 5px 0;border-bottom:1px solid #eee9ef;vertical-align:top;text-align:left;font-weight:500;word-break:normal;overflow-wrap:anywhere;">{label}</th><td style="padding:5px 0;border-bottom:1px solid #eee9ef;vertical-align:top;overflow-wrap:anywhere;">{value}</td></tr>')
    inci=[]
    for group in info.select('.inci-shade'):
        title=html.escape(group.h3.get_text());body=html.escape(group.p.get_text())
        inci.append(f'<div style="margin:0 0 14px;"><h3 style="font-size:13px;line-height:1.5;font-weight:600;margin:0 0 4px;color:#39323c;">{title}</h3><p style="margin:0;overflow-wrap:anywhere;word-break:normal;">{body}</p></div>')
    return '<div data-tam-product-info="cloud-blush" style="padding:24px 4%;background:#fff;color:#49434b;text-align:left;font-family:Arial,sans-serif;font-size:12px;line-height:1.5;box-sizing:border-box;"><h2 style="font-size:15px;line-height:1.5;margin:0 0 14px;font-weight:600;color:#29242c;">제품 정보 · 전성분</h2><table style="border-collapse:collapse;table-layout:fixed;width:100%;font-size:12px;line-height:1.5;color:inherit;margin:0 0 20px;"><tbody>'+''.join(rows)+'</tbody></table><h2 style="font-size:14px;line-height:1.5;margin:0 0 12px;font-weight:600;">전성분</h2>'+''.join(inci)+'</div>'
