import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000"
SESSION = requests.Session()

def print_json(label, data):
    print(f"=== {label} ===")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print()

def register_user(username, email, password):
    url = f"{BASE_URL}/api/register"
    payload = {"username": username, "email": email, "password": password}
    resp = SESSION.post(url, json=payload)
    try:
        data = resp.json()
    except Exception:
        data = {"status_code": resp.status_code, "text": resp.text}
    print_json("Register Response", data)
    return resp.ok

def login_user(username, password):
    url = f"{BASE_URL}/api/login"
    payload = {"username": username, "password": password}
    resp = SESSION.post(url, json=payload)
    data = resp.json()
    print_json("Login Response", data)
    return resp.ok, data.get("user", {})

def start_interview(job_role):
    url = f"{BASE_URL}/api/interview/start"
    payload = {"job_role": job_role}
    resp = SESSION.post(url, json=payload)
    data = resp.json()
    print_json("Interview Start Response", data)
    return data.get("session_id"), data.get("question")

def answer_question(session_id, question_id, answer_text):
    url = f"{BASE_URL}/api/interview/answer"
    payload = {"session_id": session_id, "question_id": question_id, "answer_text": answer_text}
    resp = SESSION.post(url, json=payload)
    data = resp.json()
    print_json("Answer Response", data)
    return data

def fetch_report(session_id):
    url = f"{BASE_URL}/api/report/{session_id}"
    resp = SESSION.get(url)
    data = resp.json()
    print_json("Report Response", data)
    return data

if __name__ == "__main__":
    # Adjust these credentials as needed
    test_username = "test_user_api"
    test_email = "test_user_api@example.com"
    test_password = "TestPass123!"

    # 1. Register (ignore error if already exists)
    try:
        register_user(test_username, test_email, test_password)
    except Exception as e:
        print(f"Register failed: {e}", file=sys.stderr)

    # 2. Login
    ok, user_info = login_user(test_username, test_password)
    if not ok:
        sys.exit("Login failed – aborting script")

    # 3. Start interview
    session_id, question = start_interview("Software Engineer")
    if not session_id or not question:
        sys.exit("Failed to start interview – aborting script")

    # 4. Submit a strong answer (you may replace this with a real answer)
    strong_answer = "I have extensive experience designing scalable systems, leading teams, and delivering high‑quality software on time."
    answer_response = answer_question(session_id, question["id"], strong_answer)

    # 5. Fetch report
    fetch_report(session_id)
