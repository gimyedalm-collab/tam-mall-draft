"""Create a separate Cafe24 skin candidate. Original files are never overwritten."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,json,re,shutil,zipfile,tempfile,hashlib
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Regions(HTMLParser):
 def __init__(self,source):
  super().__init__(convert_charrefs=False);self.source=source;self.offsets=[0];self.stack=[];self.matches=[]
  for m in re.finditer('\n',source):self.offsets.append(m.end())
  self.feed(source)
 def source_offset(self):line,col=self.getpos();return self.offsets[line-1]+col
 def handle_starttag(self,tag,attrs):
  if tag in VOID:return
  attrs=dict(attrs);classes=attrs.get('class','').split();kind=None
  if attrs.get('id')=='header' or (tag=='header' and 'header' in classes):kind='header'
  if attrs.get('id')=='footer' or (tag=='footer' and 'footer' in classes):kind='footer'
  self.stack.append((tag,self.source_offset(),kind))
 def handle_startendtag(self,tag,attrs):pass
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:
    _,start,kind=self.stack[i];del self.stack[i:]
    if kind:self.matches.append((start,self.source.find('>',self.source_offset())+1,kind))
    return

def patch_layout(source,checkout=False):
 if 'TAM-INTEGRATION-V2' in source:return source,{'status':'already-integrated'}
 if not re.search(r'</head\s*>',source,re.I) or not re.search(r'<body\b',source,re.I):return source,{'status':'manual','reason':'full head/body layout not found'}
 changes=[];replacements=[]
 if not checkout:
  found=Regions(source).matches
  for kind in ['header','footer']:
   matches=[x for x in found if x[2]==kind]
   if len(matches)==1:
    start,end,_=matches[0];replacements.append((start,end,f'<!--@import(/tam/partials/{kind}.html)-->'));changes.append(kind+' replaced')
   elif not matches:
    imports=list(re.finditer(r'<!--\s*@import\((/[^)]*/'+kind+r'\.html)\)\s*-->',source,re.I))
    if len(imports)==1:
     m=imports[0];replacements.append((m.start(),m.end(),f'<!--@import(/tam/partials/{kind}.html)-->'));changes.append(kind+' import replaced')
  if len(changes)!=2:return source,{'status':'manual','reason':'header/footer must each match exactly once','matched':changes}
 for start,end,value in sorted(replacements,reverse=True):source=source[:start]+value+source[end:]
 includes='<!-- TAM-INTEGRATION-V2: retains original scripts, modules and forms -->\n<!--@css(/tam/assets/native-commerce.css)-->\n'
 if not checkout:includes+='<!--@css(/tam/assets/chrome.css)-->\n<!--@js(/tam/assets/chrome.js)-->\n'
 includes+='<!--@css(/tam/assets/quality.css)-->\n'
 source=re.sub(r'</head\s*>',lambda m:includes+m.group(0),source,count=1,flags=re.I)
 cls='tam-checkout' if checkout else 'tam-native'
 def body(m):
  tag=m.group(0)
  if re.search(r'\bclass\s*=',tag,re.I):return re.sub(r'(\bclass\s*=\s*)([\"\x27])(.*?)\2',lambda c:c[1]+c[2]+c[3]+' '+cls+c[2],tag,count=1,flags=re.I|re.S)
  return tag[:-1]+f' class="{cls}">'
 source=re.sub(r'<body\b[^>]*>',body,source,count=1,flags=re.I)
 return source,{'status':'candidate','changes':changes+['add scoped theme; preserve existing head and body content']}

def extract_checked(archive,target):
 with zipfile.ZipFile(archive) as z:
  total=sum(i.file_size for i in z.infolist())
  if total>2_000_000_000:raise ValueError('Skin archive exceeds 2 GB uncompressed')
  for info in z.infolist():
   name=info.filename.replace('\\','/');dest=(target/name).resolve()
   if not dest.is_relative_to(target.resolve()) or ':' in name:raise ValueError('Unsafe archive path: '+name)
   if ((info.external_attr>>16)&0o170000)==0o120000:raise ValueError('Archive symlinks are unsupported')
  z.extractall(target)

def integrate(source,package,output):
 source=source.resolve();output=output.resolve();package=package.resolve()
 if output.exists():raise ValueError('Output already exists; choose a new candidate directory')
 if output.is_relative_to(source) or source.is_relative_to(output):raise ValueError('Source and output must be separate')
 if not (package/'tam'/'assets'/'native-commerce.css').exists():raise ValueError('V2 package not found')
 with tempfile.TemporaryDirectory(prefix='tam-skin-') as temp:
  origin=source
  if source.is_file():
   if not zipfile.is_zipfile(source):raise ValueError('Source must be a skin directory or zip')
   origin=Path(temp);extract_checked(source,origin)
   if not (origin/'layout').exists():
    candidates=[p.parent for p in origin.rglob('layout') if p.is_dir() and (p/'basic').is_dir()]
    if len(candidates)!=1:raise ValueError('Select one PC or mobile skin root, containing layout/basic')
    origin=candidates[0]
  if not (origin/'layout').is_dir():raise ValueError('Expected a skin root containing layout/')
  if any(p.is_symlink() for p in origin.rglob('*')):raise ValueError('Skin symlinks are unsupported')
  shutil.copytree(origin,output)
  # Never silently replace a pre-existing /tam project.
  if (output/'tam').exists():raise ValueError('Source already contains /tam; candidate copied but integration stopped for review')
  shutil.copytree(package/'tam',output/'tam')
  report={'status':'draft candidate; Cafe24 validation required','source':str(source),'layouts':{},'commerce_files_preserved':{},'home_switch':'not performed'}
  for f in (output/'layout').rglob('*.html'):
   raw=f.read_bytes()
   try:text=raw.decode('utf-8-sig')
   except UnicodeDecodeError:report['layouts'][str(f.relative_to(output))]={'status':'manual','reason':'non UTF-8 encoding'};continue
   if '<body' not in text.lower():continue
   checkout='order' in f.as_posix().lower() or 'mcafe24order' in text.lower()
   patched,state=patch_layout(text,checkout);report['layouts'][f.relative_to(output).as_posix()]=state
   if patched!=text:f.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+patched.encode('utf-8'))
  for rel in ['product/detail.html','order/basket.html','order/orderform.html','member/login.html','member/join.html','myshop/coupon/coupon.html']:
   a=origin/rel;b=output/rel
   if a.exists():
    assert a.read_bytes()==b.read_bytes(),rel
    report['commerce_files_preserved'][rel]=hashlib.sha256(a.read_bytes()).hexdigest()
  report['manual_layouts']=[k for k,v in report['layouts'].items() if v['status']=='manual']
  report['candidate_layouts']=[k for k,v in report['layouts'].items() if v['status']=='candidate']
  (output/'TAM_INTEGRATION_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
  return report
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',required=True,type=Path);p.add_argument('--package',type=Path,default=Path(__file__).resolve().parent/'cafe24');p.add_argument('--output',required=True,type=Path);args=p.parse_args();print(json.dumps(integrate(args.source,args.package,args.output),ensure_ascii=False,indent=2))
