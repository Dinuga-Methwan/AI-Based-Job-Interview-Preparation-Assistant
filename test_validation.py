import urllib.parse
import re
from app import app

def test_validation():
    client = app.test_client()

    res = client.get('/interview?role=Software+Engineer')
    session_url = res.headers['Location']
    parsed = urllib.parse.urlparse(session_url)
    session_id = int(urllib.parse.parse_qs(parsed.query)['session_id'][0])

    res_page = client.get(session_url)
    html = res_page.data.decode('utf-8')
    m = re.search(r'name="question_id"\s+value="(\d+)"', html)
    q_id = int(m.group(1))

    # 1. Test 1-word answer
    r_short = client.post('/submit_answer', data={
        'session_id': session_id,
        'question_id': q_id,
        'answer_text': 'Yes'
    })
    assert r_short.status_code == 200, f"Expected 200 re-render, got {r_short.status_code}"
    assert b'Please provide a more complete answer' in r_short.data
    print("✓ Validation caught 1-word answer ('Yes')")

    # 2. Test 2-word answer
    r_2words = client.post('/submit_answer', data={
        'session_id': session_id,
        'question_id': q_id,
        'answer_text': 'Not sure'
    })
    assert r_2words.status_code == 200
    assert b'Please provide a more complete answer' in r_2words.data
    print("✓ Validation caught 2-word answer ('Not sure')")

    # 3. Test valid 3-word answer
    r_valid = client.post('/submit_answer', data={
        'session_id': session_id,
        'question_id': q_id,
        'answer_text': 'Compiler translates code'
    })
    assert r_valid.status_code == 302, f"Expected 302 redirect on valid submission, got {r_valid.status_code}"
    print("✓ Valid 3-word answer ('Compiler translates code') passed validation and was submitted to AI scorer!")

if __name__ == '__main__':
    test_validation()
