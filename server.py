"""
幼师助手 — 本地服务（零依赖，Python 3 标准库即可）
启动：python server.py
"""
import json
import os
import sys
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

# 修复 Windows GBK 编码下 emoji 打印问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, 'data', 'records')
os.makedirs(DATA_DIR, exist_ok=True)

class APIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/records':
            self.list_records()
        elif path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(os.path.join(HERE, 'index.html'), 'rb') as f:
                self.wfile.write(f.read())
        else:
            super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/api/records':
            self.save_record()
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        path = urlparse(self.path).path
        if path == '/api/records':
            self.clear_records()
        elif path.startswith('/api/records/'):
            rid = path.split('/')[-1]
            self.delete_record(rid)
        else:
            self.send_response(404)
            self.end_headers()

    def _json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def _read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return None
        try:
            return json.loads(self.rfile.read(length).decode('utf-8'))
        except Exception:
            return None

    # ---- API handlers ----
    def list_records(self):
        records = []
        for fname in os.listdir(DATA_DIR):
            if fname.endswith('.json'):
                try:
                    with open(os.path.join(DATA_DIR, fname), 'r', encoding='utf-8') as f:
                        records.append(json.load(f))
                except Exception:
                    pass
        records.sort(key=lambda r: r.get('savedAt', ''), reverse=True)
        self._json(records)

    def save_record(self):
        data = self._read_body()
        if not data:
            return self._json({'error': '无效数据'}, 400)
        rid = data.get('id') or int(datetime.now().timestamp() * 1000)
        data['id'] = rid
        data['savedAt'] = data.get('savedAt') or datetime.now().isoformat()
        fpath = os.path.join(DATA_DIR, f'{rid}.json')
        with open(fpath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self._json({'ok': True, 'id': rid})

    def delete_record(self, rid):
        try:
            rid_int = int(rid)
        except ValueError:
            return self._json({'error': '无效ID'}, 400)
        fpath = os.path.join(DATA_DIR, f'{rid_int}.json')
        if os.path.exists(fpath):
            os.remove(fpath)
            return self._json({'ok': True})
        return self._json({'error': '记录不存在'}, 404)

    def clear_records(self):
        count = 0
        for fname in os.listdir(DATA_DIR):
            if fname.endswith('.json'):
                os.remove(os.path.join(DATA_DIR, fname))
                count += 1
        self._json({'ok': True, 'deleted': count})


if __name__ == '__main__':
    port = 5000
    server = HTTPServer(('0.0.0.0', port), APIHandler)
    import sys
    try:
        print('\n  [幼师助手] 已启动!')
    except UnicodeEncodeError:
        print('\n  [Teacher Helper] Started!')
    print(f'  浏览器打开: http://localhost:{port}')
    print(f'  数据文件夹: {DATA_DIR}')
    print('  按 Ctrl+C 停止\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  已停止。')
        server.server_close()
