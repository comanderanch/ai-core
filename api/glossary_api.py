from flask import Flask, jsonify, request, send_from_directory
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

@app.route('/interact', methods=['POST'])
def interact():
    """Single interaction endpoint for UI"""
    import sys, uuid
    sys.path.insert(0, '/home/comanderanch/ai-core-standalone')
    from student.mission import MissionBlock, run_mission, SessionTracker

    body = request.json
    text = body.get('text', '')

    block = MissionBlock(
        mission_id=f"UI_{uuid.uuid4().hex[:8].upper()}",
        input_text=text,
        expected_domain="memory",
        difficulty=0.5,
        tags=["ui", "interaction", "live"]
    )

    tracker = SessionTracker()
    result = run_mission(block, tracker=tracker)

    recalled = result.get("recalled_episodes", [])
    origin_active = any("Commander Hagerty" in ep or "Haskell Texas" in ep for ep in recalled)

    return jsonify({
        "input":                text,
        "recalled_episodes":    recalled,
        "resonance":            result.get("resonance_map", {}),
        "dominant_plane":       result.get("dominant_plane", ""),
        "band":                 result.get("evaluation_band", ""),
        "ethics_score":         result.get("ethics_score", 0),
        "questions":            result.get("aia_questions", []),
        "consensus_agreement":  result.get("consensus_agreement", 0),
        "avg_resonance":        result.get("avg_resonance", 0),
        "origin_memory_active": origin_active,
    })


@app.route('/curiosity/answer_with_ollama', methods=['POST'])
def answer_with_ollama():
    """Use local Ollama to answer a curiosity question"""
    import subprocess
    body = request.json
    question = body.get('question', '')

    prompt = f"""Answer this question concisely in 2-3 sentences with facts only.
No opinions. No caveats. Just the factual answer.
Question: {question}"""

    try:
        result = subprocess.run(
            ['ollama', 'run', 'llama3.1:8b', prompt],
            capture_output=True, text=True, timeout=30,
            cwd='/home/comanderanch/ai-core-standalone'
        )
        answer = result.stdout.strip()
        return jsonify({"answer": answer, "source": "ollama/llama3.1:8b"})
    except Exception as e:
        return jsonify({"answer": None, "source": None, "error": str(e)})


@app.route('/', methods=['GET'])
@app.route('/ui', methods=['GET'])
def serve_ui():
    """Serve the AIA chat interface"""
    return send_from_directory('/home/comanderanch/ai-core-standalone/ui', 'aia_chat.html')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "AIA API live"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5679, debug=False)
