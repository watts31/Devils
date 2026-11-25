import urllib.request, json, re
def get(u):
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0','Origin':'https://watts31.github.io'}),timeout=30); return r, r.read().decode('utf8','replace')
def show(n,u,f=None):
  try:
    r,b=get(u); print(f"=== {n} {r.status} CORS={r.headers.get('access-control-allow-origin')} len={len(b)}")
    print((f(b) if f else b[:700]).replace('\n',' ')[:1500])
  except Exception as e: print(f"=== {n} ERR {e}")
heads=lambda b:' | '.join(a['headline']+' ['+','.join(str(c.get('teamId','')) for c in a.get('categories',[]) if c.get('type')=='team')+']' for a in json.loads(b).get('articles',[])[:8])
show('news team=nj','https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news?team=nj&limit=8',heads)
show('news teams/11/news','https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams/11/news?limit=8',heads)
show('now api','https://now.core.api.espn.com/v1/sports/news?sport=hockey&league=nhl&team=11&limit=8',lambda b:' | '.join(h.get('headline','') for h in json.loads(b).get('headlines',[])[:8]))
show('news limit50 filter','https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news?limit=50',lambda b:str(sum(1 for a in json.loads(b)['articles'] if any(c.get('teamId')==11 for c in a.get('categories',[]))))+' of 50 tagged NJ')
show('mlb news teams/22','https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams/22/news?limit=8',heads)
show('mlb league injuries','https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/injuries',lambda b:str([t['displayName'] for t in json.loads(b).get('injuries',[])][:5]))
show('nhl franchise skaters','https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=true&isGame=false&sort=%5B%7B%22property%22:%22points%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=5&cayenneExp=franchiseId%3D23%20and%20gameTypeId%3D2%20and%20seasonId%3C%3D20262027%20and%20seasonId%3E%3D19171918')
show('nhl franchise goalies','https://api.nhle.com/stats/rest/en/goalie/summary?isAggregate=true&isGame=false&sort=%5B%7B%22property%22:%22wins%22,%22direction%22:%22DESC%22%7D%5D&start=0&limit=3&cayenneExp=franchiseId%3D23%20and%20gameTypeId%3D2%20and%20seasonId%3C%3D20262027%20and%20seasonId%3E%3D19171918')
show('mlb career team','https://statsapi.mlb.com/api/v1/stats?stats=career&group=hitting&teamId=143&sortStat=homeRuns&limit=5&playerPool=all',lambda b:str([(s['player']['fullName'],s['stat'].get('homeRuns')) for s in json.loads(b)['stats'][0]['splits'][:5]]))
show('mlb franchise leaders','https://statsapi.mlb.com/api/v1/teams/143/leaders?leaderCategories=homeRuns&statType=career&limit=5')
show('mlb standings 1980','https://statsapi.mlb.com/api/v1/standings?leagueId=104&season=1980',lambda b:str([(t['team']['name'],t['wins'],t['losses']) for r in json.loads(b)['records'] for t in r['teamRecords'] if t['team']['id']==143]))
show('mlb postseason series','https://statsapi.mlb.com/api/v1/schedule/postseason/series?sportId=1&season=2008&teamId=143',lambda b:str([(s['series']['id'],s['games'][-1]['teams']['home']['team']['name'],s['games'][-1]['teams']['home'].get('isWinner')) for s in json.loads(b).get('series',[])]))
show('mlb milb stats','https://statsapi.mlb.com/api/v1/stats?stats=season&group=hitting&sportId=11&teamId=1410&season=2026&limit=3&playerPool=all',lambda b:str([(s['player']['fullName'],s['stat']['ops'],s.get('team',{}).get('name')) for s in json.loads(b)['stats'][0]['splits'][:3]]))
show('espn sched broadcast fields','https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams/11/schedule?seasontype=2',lambda b:json.dumps([e['competitions'][0].get('broadcasts') for e in json.loads(b)['events'][20:22]]))
def cw(b):
  i=b.find('id="__NEXT_DATA__"'); j=b.find('>',i)+1; k=b.find('</script>',j); d=json.loads(b[j:k])
  out=[]
  def walk(x,p):
    if isinstance(x,dict):
      for kk,v in x.items():
        if re.search('pick|draft',kk,re.I) and not re.search('draft_year|draftYear',kk): out.append(p+'.'+kk+'='+json.dumps(v)[:300])
        walk(v,p+'.'+kk)
    elif isinstance(x,list):
      for i,v in enumerate(x[:3]): walk(v,p+f'[{i}]')
  walk(d,'');return ' || '.join(out[:8])
show('capwages picks','https://capwages.com/teams/new_jersey_devils',cw)
show('capwages draft page','https://capwages.com/teams/new_jersey_devils/draft-picks',lambda b:b[b.find('__NEXT_DATA__'):][:200])
show('nhl tv sched api','https://api-web.nhle.com/v1/club-schedule-season/NJD/now',lambda b:json.dumps(json.loads(b)['games'][30].get('tvBroadcasts')))
