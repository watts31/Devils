import urllib.request, json, re, datetime
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read().decode('utf8','replace')
h=get('https://capwages.com/teams/vancouver_canucks')
i=h.find('id="__NEXT_DATA__"'); j=h.find('>',i)+1; k=h.find('</script>',j); pp=json.loads(h[j:k])['props']['pageProps']
ts=pp['data'].get('teamSummary') or pp.get('teamSummary') or {}
print('SUMMARY',json.dumps(ts)[:600])
today=datetime.date(2026,11,25)
def age(b):
  try: d=datetime.datetime.strptime(b.replace('.',''),'%b %d, %Y').date(); return today.year-d.year-((today.month,today.day)<(d.month,d.day))
  except: return None
def money(x): return int(re.sub(r'[^0-9]','',x or '0') or 0)
out={'F':[],'D':[],'G':[]}
ro=pp['data']['roster']
for key,grp in [('forwards','F'),('defense','D'),('goalies','G'),('long-term injured reserve',None)]:
  for p in ro.get(key,[]) or []:
    last,_,first=p['name'].partition(', '); name=f"{first} {last}".strip()
    pos='/'.join([x for x,_ in sorted((p.get('positions') or {}).items(),key=lambda kv:-kv[1])][:2]) or p.get('pos','')
    g=grp or ('G' if 'G' in pos else 'D' if pos.startswith('D') else 'F')
    hits={}; status=''; endseason=''
    for c in p.get('contracts',[]):
      for d in c.get('details',[]):
        hits[d['season']]=money(d.get('capHit'))
      last_s=max((d['season'] for d in c.get('details',[])),default='')
      if last_s>=endseason: endseason=last_s; status=c.get('expiryStatus','')
    yrs=len([s for s in hits if s>='2026-27' and hits[s]>0])
    cur=hits.get('2026-27',0); nxt=hits.get('2027-28')
    row=[name,pos,age(p.get('born','')),cur,yrs,'UFA' if 'UFA' in status else 'RFA' if 'RFA' in status else status,'LTIR' if key.startswith('long') else '']
    if nxt and nxt!=cur: row.append(nxt)
    elif row[6]=='': row=row[:6]
    out[g].append(row)
for g in out: out[g].sort(key=lambda r:-r[3])
cap={'limit':money(str((ts.get('upperLimit') or 0))),'total':money(str((ts.get('capHit') or {}).get('total',0))),'space':money(str(ts.get('capSpace') or 0)),'overage':0,**out}
print('CAPJSON',json.dumps(cap))
s=json.loads(get('https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams/van/schedule?seasontype=2'))
M={'TB':'TBL','NJ':'NJD','LA':'LAK','SJ':'SJS','UTAH':'UTA'}
past=[];up=[]
for e in s['events']:
  c=e['competitions'][0]; cs=c['competitors']; me=[x for x in cs if x['team']['abbreviation']=='VAN'][0]; op=[x for x in cs if x is not me][0]
  t=e['date'].replace(':00Z','Z') if e['date'].count(':')==2 else e['date']
  opp=M.get(op['team']['abbreviation'],op['team']['abbreviation']); home=1 if me['homeAway']=='home' else 0
  if c['status']['type']['completed']: past.append((t,opp,home,int(float(me['score']['displayValue'])),int(float(op['score']['displayValue']))))
  else: up.append((t,opp,home))
print('GAMES',json.dumps(past+up))
print('RECORD',s['team'].get('recordSummary'),s['team'].get('standingSummary'))
