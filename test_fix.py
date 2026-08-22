import urllib.parse
import re
from app import app

def get_session_question_ids(client, role='Software Engineer'):
    q_ids = []
    res = client.get(f'/interview?role={role}')
    session_url = res.headers['Location']
    
    for _ in range(5):
        res_page = client.get(session_url)
        html = res_page.data.decode('utf-8')
        m = re.search(r'name="question_id"\s+value="(\d+)"', html)
        if m:
            q_id = int(m.group(1))
            q_ids.append(q_id)
            
            m_sess = re.search(r'name="session_id"\s+value="(\d+)"', html)
            sess_id = int(m_sess.group(1))
            
            res_sub = client.post('/submit_answer', data={
                'session_id': sess_id,
                'question_id': q_id,
                'answer_text': 'Sample response.'
            })
            if 'Location' in res_sub.headers:
                session_url = res_sub.headers['Location']
                
    return q_ids

if __name__ == '__main__':
    client = app.test_client()
    s1_q_ids = get_session_question_ids(client, 'Software Engineer')
    s2_q_ids = get_session_question_ids(client, 'Software Engineer')

    print(f"Session 1 Question IDs: {s1_q_ids}")
    print(f"Session 2 Question IDs: {s2_q_ids}")

    assert len(s1_q_ids) == 5, f"Expected 5 questions in Session 1, got {len(s1_q_ids)}"
    assert len(s2_q_ids) == 5, f"Expected 5 questions in Session 2, got {len(s2_q_ids)}"
    assert len(s1_q_ids) == len(set(s1_q_ids)), "Duplicates found within Session 1!"
    assert len(s2_q_ids) == len(set(s2_q_ids)), "Duplicates found within Session 2!"
    assert s1_q_ids != s2_q_ids, "Session 1 and Session 2 received identical question sets!"

    print("\n✓ RANDOMIZATION VERIFIED: Different sessions receive distinct, randomly selected question sets without internal duplicates!")
