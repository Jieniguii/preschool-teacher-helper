"""
幼师助手 — 本地服务
启动后老师浏览器访问 http://localhost:5000 即可使用
所有数据保存在 data/records/ 文件夹
"""
import json
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'records')
os.makedirs(DATA_DIR, exist_ok=True)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/records', methods=['GET'])
def list_records():
    """获取全部记录，按时间倒序"""
    records = []
    for fname in os.listdir(DATA_DIR):
        if fname.endswith('.json'):
            try:
                with open(os.path.join(DATA_DIR, fname), 'r', encoding='utf-8') as f:
                    rec = json.load(f)
                records.append(rec)
            except Exception:
                pass
    records.sort(key=lambda r: r.get('savedAt', ''), reverse=True)
    return jsonify(records)


@app.route('/api/records', methods=['POST'])
def save_record():
    """保存一条记录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效数据'}), 400
    rid = data.get('id') or int(datetime.now().timestamp() * 1000)
    data['id'] = rid
    data['savedAt'] = data.get('savedAt') or datetime.now().isoformat()
    fpath = os.path.join(DATA_DIR, f'{rid}.json')
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return jsonify({'ok': True, 'id': rid})


@app.route('/api/records/<int:rid>', methods=['DELETE'])
def delete_record(rid):
    """删除一条记录"""
    fpath = os.path.join(DATA_DIR, f'{rid}.json')
    if os.path.exists(fpath):
        os.remove(fpath)
        return jsonify({'ok': True})
    return jsonify({'error': '记录不存在'}), 404


@app.route('/api/records', methods=['DELETE'])
def clear_records():
    """清空全部记录"""
    count = 0
    for fname in os.listdir(DATA_DIR):
        if fname.endswith('.json'):
            os.remove(os.path.join(DATA_DIR, fname))
            count += 1
    return jsonify({'ok': True, 'deleted': count})


if __name__ == '__main__':
    print('\n  🦞 幼师助手已启动！')
    print('  ─────────────────────────')
    print('  浏览器打开: http://localhost:5000')
    print('  数据保存在: data/records/')
    print('  按 Ctrl+C 停止服务\n')
    app.run(host='0.0.0.0', port=5000, debug=False)
