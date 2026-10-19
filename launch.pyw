"""Double-click launcher. No package installation, no account or API key."""
import json, os, socket, subprocess, sys, time, urllib.request, webbrowser
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PORT=8765
def ours():
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:{PORT}/api/members',timeout=1) as r: data=json.load(r)
        return len(data)==736 and data[0].get('rfem_member_id')=='1'
    except Exception:return False
try:
    if not ours():
        runtime=ROOT/'.runtime';runtime.mkdir(exist_ok=True)
        with (runtime/'server.log').open('a',encoding='utf-8') as log:
            subprocess.Popen([sys.executable,'-X','utf8',str(ROOT/'server.py'),'--port',str(PORT)],cwd=ROOT,stdout=log,stderr=log,creationflags=0x08000000 if os.name=='nt' else 0)
        for _ in range(80):
            if ours():break
            time.sleep(.2)
        else:raise RuntimeError('The local app could not start. Check .runtime/server.log. Port 8765 may be in use.')
    webbrowser.open(f'http://127.0.0.1:{PORT}')
except Exception as e:
    import tkinter.messagebox
    tkinter.messagebox.showerror('Stockerau Carbon Atlas',str(e))
