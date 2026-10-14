from flask import Flask, jsonify, send_from_directory
import requests, bs4, feedparser, re, time
from urllib.parse import urljoin,urlparse
app=Flask(__name__,static_folder='.')
CANDIDATES=[('Mick Willing','Camden'),('Peter Gangemi','Castle Hill'),('Kalvin Biag','Prospect'),('Carolyn Martin','Coogee'),('Michael Gencher','Pittwater'),('Philip Longley','Wakehurst'),('Kate Beaumont','Maroubra'),('Ken Kozak','Wyong'),('Mohit Kumar','Riverstone'),('Adelaide Cuneo','Manly'),('Paul Ell','South Coast'),('Georgina Valjak','Winston Hills')]
BASE='https://nswliberal.org.au'
SOCIAL=('facebook.com','instagram.com','tiktok.com','x.com','twitter.com','youtube.com')
cache={'at':0,'data':None}
def fetch():
    people=[]
    for name,seat in CANDIDATES:
        slug=re.sub('[^a-z0-9]+','-',name.lower()).strip('-'); url=f'{BASE}/{slug}'
        p={'name':name,'seat':seat,'profile':url,'social':[],'status':'not checked'}
        try:
            r=requests.get(url,timeout=7,headers={'User-Agent':'Mozilla/5.0 (compatible; PublicLinkMonitor/1.0)'})
            if r.ok:
                soup=bs4.BeautifulSoup(r.text,'html.parser')
                links=set()
                for a in soup.select('a[href]'):
                    link=urljoin(url,a['href']);host=urlparse(link).hostname or ''
                    if any(host==d or host.endswith('.'+d) for d in SOCIAL): links.add(link.split('?')[0])
                p['social']=sorted(links);p['status']='profile checked' if links else 'no public handles found on profile'
            else:p['status']=f'profile HTTP {r.status_code}'
        except requests.RequestException:p['status']='profile unavailable'
        people.append(p)
    # Public RSS feeds may be available on some sites, but social platforms usually block anonymous post access.
    return {'candidates':people,'posts':[],'checked_at':int(time.time()),'note':'No social posts are asserted without a verified public feed. Social URLs are discovered from candidate profile links only.'}
@app.get('/')
def index():return send_from_directory('.','index.html')
@app.get('/api/feed')
def feed():
    if cache['data'] is None or time.time()-cache['at']>900:
        cache['data']=fetch();cache['at']=time.time()
    return jsonify(cache['data'])
if __name__=='__main__':app.run(host='0.0.0.0',port=8000)
