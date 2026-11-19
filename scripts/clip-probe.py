# Temporary: find goal clip links for recent Devils games and check whether they can play inside another site.
import json, re, urllib.request, os
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36'}
os.makedirs('cliptest', exist_ok=True)
out=open('cliptest/report.txt','w')
def log(*a): print(*a); print(*a, file=out)
def get(u, head=False):
    req=urllib.request.Request(u, headers=UA, method='HEAD' if head else 'GET')
    try:
        r=urllib.request.urlopen(req, timeout=20)
        return r.status, dict(r.headers), (b'' if head else r.read())
    except urllib.error.HTTPError as e: return e.code, dict(e.headers or {}), b''
    except Exception as e: return 'ERR '+str(e), {}, b''
st,_,b=get('https://api-web.nhle.com/v1/club-schedule-season/NJD/now'); log('schedule',st)
games=json.loads(b or b'{}').get('games',[])
pick=[g for g in games if g.get('gameState') in ('OFF','FINAL')][-1:]+[g for g in games if g.get('gameState') in ('LIVE','CRIT')]
urls=set()
for g in pick:
    gid=g['id']; st,_,b=get(f'https://api-web.nhle.com/v1/gamecenter/{gid}/landing'); log('== game',gid,g.get('gameState'),st)
    open(f'cliptest/landing_{gid}.json','wb').write(b)
    d=json.loads(b or b'{}')
    for per in d.get('summary',{}).get('scoring',[]):
        for gl in per.get('goals',[]):
            keep={k:v for k,v in gl.items() if any(s in k.lower() for s in ('clip','highlight','video','url','replay'))}
            log('  goal',gl.get('lastName',{}).get('default'),gl.get('timeInPeriod'),json.dumps(keep)[:600])
            for v in keep.values():
                if isinstance(v,str) and v.startswith('http'): urls.add(v)
                if isinstance(v,int) and v>1000: urls.add(f'clipid:{v}')
log('\nURLs:',len(urls))
checked=0
for u in sorted(urls):
    if checked>=4: break
    cands=[u] if not u.startswith('clipid:') else [f"https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId={u[7:]}", f"https://www.nhl.com/video/embed/{u[7:]}"]
    for c in cands:
        st,h,body=get(c)
        hl={k:v for k,v in h.items() if k.lower() in ('x-frame-options','content-security-policy','content-type')}
        log('###',c,st,json.dumps(hl)[:500])
        txt=body.decode('utf-8','replace')
        for m in sorted(set(re.findall(r'https?://[^"\'\s<>]+\.(?:mp4|m3u8)[^"\'\s<>]*',txt)))[:5]: log('   media:',m)
        for m in sorted(set(re.findall(r'players\.brightcove\.net/[^"\'\s<>]+',txt)))[:3]: log('   bc:',m)
        for m in sorted(set(re.findall(r'"(?:accountId|playerId|videoId|data-account|data-player|data-video-id)"\s*[:=]\s*"?([\w-]+)',txt)))[:6]: log('   id:',m)
    checked+=1
out.close()
