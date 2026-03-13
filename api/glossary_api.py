from flask import Flask, jsonify, request
import json
import threading
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
_file_lock = threading.Lock()

GLOSSARY_PATH = Path("memory/glossary/unknown_words.json")
LEARNED_PATH = Path("memory/glossary/learned_words.json")

@app.route('/glossary/pending', methods=['GET'])
def get_pending():
    """Return all PENDING_LOOKUP words"""
    try:
        data = json.loads(GLOSSARY_PATH.read_text())
        pending = [w for w in data if w['status'] == 'PENDING_LOOKUP']
        return jsonify(pending)
    except:
        return jsonify([])

@app.route('/glossary/resolve', methods=['POST'])
def resolve_word():
    """Mark a word as resolved with definition and plane"""
    body = request.json
    word = body.get('word')
    definition = body.get('definition')
    plane = body.get('plane')

    with _file_lock:
        try:
            data = json.loads(GLOSSARY_PATH.read_text())
        except Exception:
            data = []
        for entry in data:
            if entry['word'] == word:
                entry['status'] = 'RESOLVED'
                entry['definition'] = definition
                entry['plane'] = plane
                entry['resolved'] = datetime.now().isoformat()
        GLOSSARY_PATH.write_text(json.dumps(data, indent=2))
    return jsonify({"status": "ok", "word": word})

@app.route('/curiosity/pending', methods=['GET'])
def get_curiosity_pending():
    """Return unanswered questions"""
    try:
        path = Path("memory/curiosity/questions_queue.json")
        data = json.loads(path.read_text())
        pending = [q for q in data if q['status'] == 'PENDING_ANSWER']
        return jsonify(pending[:3])  # budget limit — 3 at a time
    except:
        return jsonify([])

@app.route('/curiosity/answer', methods=['POST'])
def answer_question():
    """Store answer to a question"""
    body = request.json
    question = body.get('question')
    answer = body.get('answer')
    source = body.get('source')

    path = Path("memory/curiosity/questions_queue.json")
    with _file_lock:
        try:
            data = json.loads(path.read_text())
        except Exception:
            data = []
        for entry in data:
            if entry['question'] == question:
                entry['status'] = 'ANSWERED'
                entry['answer'] = answer
                entry['source'] = source
                entry['answered'] = datetime.now().isoformat()
        path.write_text(json.dumps(data, indent=2))
    return jsonify({"status": "ok"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "AIA API live"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5679, debug=False)
