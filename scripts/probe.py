import urllib.request, json, sys
U=[
 ("espn news","https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news?team=11&limit=5"),
 ("espn team injuries","https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams/11/injuries"),
 ("espn league injuries","https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/injuries"),
 ("espn transactions","https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/transactions?team=11"),
 ("espn core transactions","https://sports.core.api.espn.com/v2/sports/hockey/leagues/nhl/transactions?limit=5"),
 ("espn sched broadcasts","https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/teams/11/schedule?seasontype=2"),
 ("nhl prospects","https://api-web.nhle.com/v1/prospects/NJD"),
 ("nhl franchise","https://api.nhle.com/stats/rest/en/franchise"),
 ("records season results","https://records.nhl.com/site/api/franchise-season-results?cayenneExp=franchiseId=23&sort=seasonId&dir=DESC"),
 ("records skater","https://records.nhl.com/site/api/franchise-skater-records?cayenneExp=franchiseId=23"),
 ("records totals","https://records.nhl.com/site/api/franchise-team-totals?cayenneExp=franchiseId=23"),
 ("nhl draft picks year","https://records.nhl.com/site/api/draft?cayenneExp=draftYear=2025%20and%20triCode=%22NJD%22"),
 ("ahl hockeytech","https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=teams&groupTeamsBy=division&context=overall&site_id=1&season=90&league_id=4&key=50c2cd9b5e18e390&client_code=ahl&lang=en&fmt=json"),
 ("ahl seasons","https://lscluster.hockeytech.com/feed/?feed=modulekit&view=seasons&key=50c2cd9b5e18e390&client_code=ahl&fmt=json"),
 ("mlb transactions","https://statsapi.mlb.com/api/v1/transactions?teamId=143&startDate=2026-10-01&endDate=2026-11-25"),
 ("mlb milb iron pigs","https://statsapi.mlb.com/api/v1/teams/1410?hydrate=standings"),
 ("mlb affiliates","https://statsapi.mlb.com/api/v1/teams/affiliates?teamIds=143"),
 ("mlb prospects","https://statsapi.mlb.com/api/v1/draft/prospects/2026?teamId=143&limit=3"),
 ("mlb draft","https://statsapi.mlb.com/api/v1/draft/2026?teamId=143"),
 ("mlb team history","https://statsapi.mlb.com/api/v1/teams/143/history"),
 ("mlb all hitting","https://statsapi.mlb.com/api/v1/stats?stats=season&group=hitting&sportId=1&season=2026&limit=3&playerPool=all"),
 ("mlb broadcasts sched","https://statsapi.mlb.com/api/v1/schedule?sportId=1&teamId=143&season=2026&gameType=R&hydrate=broadcasts(all)&startDate=2026-09-01&endDate=2026-09-03"),
 ("espn mlb news","https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/news?team=22&limit=3"),
 ("espn mlb injuries","https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams/22/injuries"),
 ("capwages njd","https://capwages.com/teams/new_jersey_devils"),
]
for n,u in U:
  try:
    r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0','Origin':'https://watts31.github.io'}),timeout=25)
    b=r.read().decode('utf8','replace')
    print(f"=== {n} {r.status} CORS={r.headers.get('access-control-allow-origin')} len={len(b)}")
    if n=='capwages njd':
      i=b.find('__NEXT_DATA__'); j=b.find('raft',i); print(b[j-300:j+700] if j>0 else 'no draft')
    else: print(b[:900].replace('\n',' '))
  except Exception as e: print(f"=== {n} ERR {e}")
