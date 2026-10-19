from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'site'
if __name__=='__main__':
 print('East Project: http://127.0.0.1:8091',flush=True)
 ThreadingHTTPServer(('127.0.0.1',8091),partial(SimpleHTTPRequestHandler,directory=str(root))).serve_forever()
