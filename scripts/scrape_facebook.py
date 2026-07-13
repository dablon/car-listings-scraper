#!/usr/bin/env python3
"""Facebook Marketplace Scraper via l.facebook.com"""
import subprocess,re,sys,json
FB="https://l.facebook.com/marketplace/item"

def c(s):
 d={"&#xf1;":"ñ","&#xe1;":"á","&#xf3;":"ó","&#xe9;":"é","&#xfa;":"ú","&#xfc;":"ü","&iacute;":"í","&eacute;":"é","&oacute;":"ó","&uacute;":"ú","&ntilde;":"ñ","&nbsp;":" ","&middot;":"·","&amp;":"&"}
 for k,v in d.items():s=s.replace(k,v)
 return re.sub(r"\s+"," ",s).strip()

def km(d):
 m=re.search(r"(\d+)\s*mil\s*km",d,re.I)
 if m:return str(int(m.group(1))*1000)
 m=re.search(r"(\d{1,3}[.,]\d{3})\s*kms?",d,re.I)
 if m:return m.group(1).replace(".","").replace(",","")
 m=re.search(r"Kilometraje:?\s*([\d.,]+)",d)
 if m:return m.group(1).replace(".","").replace(",","")
 return""

def pr(t):
 t=c(t)
 return t if"por"in t.lower()or"item"in t.lower()else""

def scrape(id):
 url=f"{FB}/{id}/"
 r=subprocess.run(["curl","-s","-L","-A","Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36","-H","Accept: text/html,application/xhtml+xml","-H","Accept-Language: es-CO,es,en;q=0.9",url],capture_output=True,text=True,timeout=20)
 h=r.stdout
 if len(h)<1000:return None
 tm=re.search(r'<meta property="og:title" content="([^"]+)"',h)
 dm=re.search(r'<meta property="og:description" content="([^"]+)"',h)
 pm=re.search(r"class='f3'[^>]*>\s*([^<]+)",h)
 lm=re.search(r"Listed \w+ in ([^<\n]+)",h)
 title=c(tm.group(1))if tm else""
 desc=c(dm.group(1))if dm else""
 price=pr(pm.group(1))if pm else""
 loc=c(lm.group(1))if lm else""
 ym=re.search(r"Año:\s*(\d{4})",desc)
 if not ym:ym=re.search(r"\b(19\d{2}|20\d{2})\b",title)
 if not ym:ym=re.search(r"\b(19\d{2}|20\d{2})\b",desc)
 year=ym.group(1)if ym else""
 km_val=km(desc)
 em=re.search(r"Motor:\s*([\d.,]+\s*[^\n<]*)",desc)
 if not em:em=re.search(r"Motor\s*([\d.,]+\s*[^\n<]*)",desc)
 eng=em.group(1).strip()if em else""
 eng=re.sub(r"\s+"," ",eng)
 trm=re.search(r"Transmisión:\s*(\w+)",desc)
 trans=trm.group(1)if trm else""
 if not trans:
  if"automática"in desc.lower()or"automatic"in desc.lower():trans="Automática"
  elif"mecánica"in desc.lower()or"mecanico"in desc.lower():trans="Mecánica"
 dvm=re.search(r"Tracción:\s*(\w+)",desc)
 if not dvm:dvm=re.search(r"Traccion\s*(\w+)",desc)
 drv=dvm.group(1)if dvm else""
 if not drv:
  if"4x4"in desc or"4wd"in desc.lower()or"tracción"in desc.lower():drv="4x4"
  elif"4x2"in desc:drv="4x2"
 hp=""
 if eng:
  if"3.6"in eng:hp="285 HP"
  elif"3.8"in eng:hp="202 HP"
  elif"3.2"in eng:hp="271 HP"
  elif"4.0"in eng:hp="236-270 HP"
  elif"2.0"in eng:hp="270-285 HP"
  elif"2.4"in eng:hp="177 HP"
  elif"1.8"in eng:hp="132 HP"
  elif"1.6"in eng:hp="115 HP"
  elif"1.5"in eng:hp="85-88 HP"
  elif"1.4"in eng:hp="95-97 HP"
  elif"1.3"in eng:hp="85 HP"
 return{"id":id,"title":title,"price":price,"year":year,"km":km_val,"engine":eng,"transmission":trans,"drivetrain":drv,"hp_estimate":hp,"location":loc,"description":desc,"link":f"https://facebook.com/marketplace/item/{id}/","source":"facebook"}

if __name__=="__main__":
 if len(sys.argv)<2:print("Usage: python3 scrape_facebook.py <listing_id>");sys.exit(1)
 result=scrape(sys.argv[1])
 if result:print(json.dumps(result,indent=2,ensure_ascii=False))
 else:print(f"Error: Could not scrape listing {sys.argv[1]}")
