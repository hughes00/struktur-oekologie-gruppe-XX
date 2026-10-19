"""Local-only server: serves only web assets and a fixed public-dataset API."""
import argparse, csv, io, json, mimetypes, threading, time
from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from carbon import ROOT, DATASETS, quantities, fetch_dataset, cached_dataset

MEMBERS=quantities()
STATE={}; LOCK=threading.Lock(); REFRESH_LOCK=threading.Lock()

def load_cached():
    for key in DATASETS:
        try: STATE[key]={'dataset':cached_dataset(key),'status':'cached','error':None}
        except Exception as e: STATE[key]={'dataset':None,'status':'unavailable','error':str(e)}

def refresh():
    if not REFRESH_LOCK.acquire(False): return
    def one(key):
        try: result={'dataset':fetch_dataset(key),'status':'live','error':None}
        except Exception as e:
            with LOCK: previous=STATE.get(key,{}).get('dataset')
            result={'dataset':previous,'status':'cached' if previous else 'unavailable','error':str(e)}
        with LOCK: STATE[key]=result
    try:
        with ThreadPoolExecutor(max_workers=5) as pool: list(pool.map(one,DATASETS))
    finally: REFRESH_LOCK.release()

class Handler(BaseHTTPRequestHandler):
    def respond(self,code,content,ctype='application/json; charset=utf-8'):
        if not isinstance(content,bytes): content=content.encode('utf-8')
        self.send_response(code); self.send_header('Content-Type',ctype); self.send_header('Content-Length',str(len(content)))
        self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(content)
    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/api/members': return self.respond(200,json.dumps(MEMBERS,ensure_ascii=False))
        if path=='/api/datasets':
            with LOCK: payload={'datasets':dict(STATE),'refreshing':REFRESH_LOCK.locked()}
            return self.respond(200,json.dumps(payload,ensure_ascii=False))
        if path=='/api/inventory.csv': return self.respond(200,(ROOT/'data/member_quantities.csv').read_bytes(),'text/csv; charset=utf-8')
        # Fixed allow-list prevents serving .3dm, .git, credentials and local paths.
        assets={'/':'index.html','/app.js':'app.js','/calc.js':'calc.js','/style.css':'style.css','/meshes.json':'meshes.json',
          '/vendor/three.module.min.js':'vendor/three.module.min.js','/vendor/OrbitControls.js':'vendor/OrbitControls.js'}
        if path not in assets: return self.respond(404,'{"error":"Not found"}')
        file=ROOT/'web'/assets[path]
        return self.respond(200,file.read_bytes(),(mimetypes.guess_type(file.name)[0] or 'text/plain')+'; charset=utf-8')
    def do_POST(self):
        if self.headers.get('Origin') not in (None,f'http://{self.headers.get("Host")}'):
            return self.respond(403,'{"error":"Local origin required"}')
        if urlparse(self.path).path!='/api/refresh': return self.respond(404,'{}')
        threading.Thread(target=refresh,daemon=True).start()
        return self.respond(202,'{"refreshing":true}')
    def log_message(self,format,*args): pass

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765); args=parser.parse_args()
    load_cached();threading.Thread(target=refresh,daemon=True).start()
    print(f'Stockerau Carbon Inventory: http://127.0.0.1:{args.port}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
