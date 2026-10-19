import sys, json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from carbon import DATASETS,fetch_dataset
def fetch(key):
    d=fetch_dataset(key)
    return {k:d[k] for k in ('key','declared_unit','declared_amount','scenarios','version')}
if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=5) as pool:
        for d in pool.map(fetch,DATASETS): print(json.dumps(d))
