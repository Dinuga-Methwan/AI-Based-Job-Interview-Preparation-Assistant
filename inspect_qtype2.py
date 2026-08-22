import os, sqlite3

def main():
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Fetch all rows with their question_type
    cur.execute('SELECT id, question_type, question_text FROM Questions')
    rows = cur.fetchall()
    print('--- All rows with question_type repr ---')
    for row in rows:
        qid, qtype, qtext = row
        # Show repr, length, and maybe hex representation of bytes
        try:
            qtype_repr = repr(qtype)
            qtype_len = len(qtype)
            qtype_bytes = qtype.encode('utf-8')
        except Exception as e:
            qtype_repr = f'<error {e}>'
            qtype_len = 0
            qtype_bytes = b''
        print(f'ID:{qid} | type:{qtype_repr} | len:{qtype_len} | bytes:{qtype_bytes}')
    # Show rows where question_type matches exactly 'Behavioral'
    cur.execute("SELECT id, question_text FROM Questions WHERE question_type = 'Behavioral'")
    exact = cur.fetchall()
    print('\n--- Rows with exact question_type = "Behavioral" ---')
    if exact:
        for r in exact:
            print(f'ID:{r[0]} | text:{r[1][:80]}...')
    else:
        print('None')
    # Now query for team & environment within Behavioral rows
    cur.execute("SELECT id, question_text FROM Questions WHERE question_type = 'Behavioral' AND question_text LIKE ? AND question_text LIKE ?", ('%team%','%environment%'))
    team_env = cur.fetchall()
    print('\n--- Rows matching Behavioral & team & environment ---')
    if team_env:
        for r in team_env:
            print(f'ID:{r[0]} | text:{r[1][:120]}...')
    else:
        print('None')
    conn.close()

if __name__ == '__main__':
    main()
