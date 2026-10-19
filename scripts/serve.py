from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--author',action='store_true');args=parser.parse_args()
 root=ROOT/('author-site' if args.author else 'site');port=8092 if args.author else 8091
 print(f'East Project: http://127.0.0.1:{port}',flush=True)
 ThreadingHTTPServer(('127.0.0.1',port),partial(SimpleHTTPRequestHandler,directory=str(root))).serve_forever()
