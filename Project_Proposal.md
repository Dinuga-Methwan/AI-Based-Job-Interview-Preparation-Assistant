# Project Proposal – Automated Job‑Interview Assistant

## 1. Background of the Selected Problem
Recruiters and job‑seekers alike struggle with **behavioral and technical interview preparation**. Candidates often lack structured practice, receive vague feedback, and cannot gauge how well they are performing. Companies spend considerable time evaluating interview answers manually, leading to inconsistency and bias.

The **AI‑driven interview coach** addresses this gap by providing an interactive web‑based mock interview that scores answers, highlights missing concepts, and adapts difficulty in real time.

## 2. Problem Statement
Design and implement an end‑to‑end system that automatically evaluates a user’s free‑text interview responses, supplies explainable feedback, and dynamically adjusts question difficulty based on performance.

Key challenges:
1. Semantic similarity between user answer and an “Excellent” reference answer (requires robust embedding).
2. Explainable feedback – identify which key concepts are missing without quoting the user.
3. Adaptive difficulty – raise or lower question difficulty after each answer.
4. Usable UI – a lightweight Flask web app that runs locally with a clean report page.

## 3. Objectives of the Proposed AI Solution
| # | Objective |
|---|-----------|
| 1 | Compute a similarity score (cosine similarity of sentence‑transformer embeddings) for each answer. |
| 2 | Map the score to a label (Excellent / Good / Average / Poor) using calibrated thresholds. |
| 3 | Generate concise, generic feedback (no user‑quote) based on the label and question category (Technical / Behavioral). |
| 4 | Extract top‑N keywords from the reference answer (TF‑IDF) and flag missing concepts in the user answer. |
| 5 | Update the session’s difficulty (`Easy`, `Medium`, `Hard`) after each answer using `get_next_difficulty`. |
| 6 | Present a final report showing per‑question scores, missing concepts, and the difficulty trajectory. |

## 4. Target Users
| Role | Needs |
|------|-------|
| **Job‑seekers / students** | Structured practice, instant feedback, confidence building. |
| **Career‑services staff** | Scalable mock‑interview tool for workshops and counseling. |
| **Recruiters / HR** | Quick pre‑screening of candidate responses (optional future extension). |

## 5. Proposed AI Techniques
| Component | Technique | Library |
|-----------|-----------|---------|
| Embedding / similarity | Sentence‑Transformer (`all‑MiniLM‑L6‑v2`) → cosine similarity | `sentence_transformers` |
| Keyword extraction | TF‑IDF vectorizer fitted on all *Excellent* reference answers; top‑N terms selected | `scikit‑learn` (`TfidfVectorizer`) |
| Missing‑concept detection | Cleaned‑text substring match against extracted keywords (case‑insensitive, hyphen‑normalized) | Custom code in `ai/feedback_engine.py` |
| Adaptive difficulty | Rule‑based state machine (`get_next_difficulty`) that moves one step up/down based on label | Pure Python |
| Feedback generation | Rule‑based template dictionary (`FEEDBACK_RULES`) with category‑aware random selection | Pure Python |

## 6. Justification for Selecting the AI Techniques
| Technique | Why it fits this project |
|-----------|--------------------------|
| Sentence‑Transformer | Small model, fast inference on CPU, high‑quality semantic embeddings – ideal for real‑time scoring in a local Flask app. |
| TF‑IDF keyword extraction | No need for heavy language models; works well on the limited corpus of reference answers and gives deterministic, interpretable keywords. |
| Rule‑based difficulty | Guarantees predictable behavior, easy to audit, and matches the educational purpose (no black‑box decisions). |
| Template feedback | Provides consistent, non‑biased advice; avoids the “quote‑bug” by never inserting user text. |
| Pure‑Python implementation | Keeps the dependency footprint minimal, simplifies deployment for students on Windows machines. |

## 7. Expected System Inputs and Outputs
| Interaction | Input | Processing | Output |
|-------------|-------|------------|--------|
| Start interview | Job role selection (e.g., “General/HR”) | Create a `Sessions` row (`current_difficulty = 'Medium'`) | Interview page with first question |
| Answer submission | `question_id`, free‑text `answer_text` | 1️⃣ Score via embeddings 2️⃣ Generate feedback 3️⃣ Update difficulty 4️⃣ Store in `UserAnswers` | Redirect to next question (or report) |
| Final report | Session ID (URL) | Aggregate `UserAnswers` + session difficulty history | HTML table: Question, Score, Feedback, Missing concepts, Difficulty column |
| API / script usage | `question_id`, `user_answer` (function call) | `run_pipeline` in `test_cases.py` | JSON dict with all fields (score, similarity, feedback, etc.) |

## 8. Proposed Tools and Technologies
| Layer | Tool / Tech |
|-------|-------------|
| Backend | Flask (Python 3.14) |
| Database | SQLite (`database.db`) – lightweight, file‑based |
| AI / NLP | `sentence_transformers`, `scikit-learn`, `nltk` (stop‑words) |
| Front‑end | Jinja2 templates (`templates/*.html`), vanilla CSS (styled with modern colors, pills for missing concepts) |
| Testing | `pytest` (unit tests in `test_difficulty.py`, `test_cases.py`) |
| Version control | Git (project already in a repo) |
| Deployment (future) | Docker container or simple `python -m flask run` for cross‑platform use |

## 9. Initial System Diagram / Workflow
```
+-------------------+      +----------------------+      +-------------------+
|  User (Browser)   | ---> | Flask Routes (app.py)| ---> | SQLite DB (Sessions|
|  - selects role   |      |  - /interview         |      |  & UserAnswers)   |
|  - submits answer | <--- |  - /submit_answer     | <--- |                   |
+-------------------+      +----------------------+      +-------------------+
                                   |
                                   v
                     +---------------------------+
                     | AI Processing (ai/*.py)   |
                     |  - nlp_processor.py       |
                     |      * embed, clean, TF‑IDF|
                     |  - scorer.py (cosine)     |
                     |  - feedback_engine.py     |
                     +---------------------------+
                                   |
                                   v
                     +---------------------------+
                     | Adaptive Difficulty Logic |
                     |  get_next_difficulty()    |
                     +---------------------------+
                                   |
                                   v
                     +---------------------------+
                     | Render next question /     |
                     | final report (HTML)        |
                     +---------------------------+
```

## 10. Work Division Among Members
| Member | Responsibilities |
|--------|------------------|
| **Alice** (Project Lead) | Architecture, Flask routes, session management, documentation. |
| **Bob** (NLP Engineer) | Embedding model integration, TF‑IDF pipeline, cleaning utilities. |
| **Cara** (Feedback & UX) | Design of feedback templates, UI/UX styling, missing‑concept pill UI. |
| **Dan** (Testing & CI) | Write/maintain pytest suite, automate regression tests, CI pipeline. |
| **Eve** (Data & DB) | Prepare `behavioral_labeled_dataset.csv`, seed DB, ensure schema consistency. |

*(Adjust names/roles to match your actual team.)*

## 11. Timeline for Completing the Work
| Week | Milestone |
|------|-----------|
| **1** | Finalize data schema, seed DB, verify reference answers. |
| **2** | Implement and test embedding + similarity scoring (`scorer.py`). |
| **3** | Build TF‑IDF keyword extractor, integrate into `feedback_engine.py`. |
| **4** | Add adaptive difficulty logic, debug prints, and DB read‑back verification. |
| **5** | UI polishing – missing‑concept pills, difficulty column, responsive design. |
| **6** | Write full pytest suite (including `test_difficulty.py` & pipeline tests). |
| **7** | Conduct end‑to‑end interview session testing, fix bugs, prepare documentation. |
| **8** | Final review, create project report, package for distribution (optional Docker). |

## 12. References
1. Reimers, N., & Gurevych, I. (2020). *Sentence‑Transformers: Multilingual Sentence Embeddings using BERT.* https://arxiv.org/abs/2004.09813
2. Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval.* Cambridge University Press.
3. STAR Method – Situation, Task, Action, Result (behavioral interview technique).
4. Flask Documentation – https://flask.palletsprojects.com/
5. SQLite – https://sqlite.org/docs.html
6. NLTK Stop‑words – https://www.nltk.org/

---
*Prepared by the development team of the Automated Job‑Interview Assistant (Spring 2026).*
