const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000';

// Start a new interview session
export async function startInterview(jobRole) {
  const response = await fetch(`${BASE_URL}/api/interview/start`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    // Backend expects the key "job_role"
    body: JSON.stringify({ job_role: jobRole }),
  });
  return response.json();
}

// Submit an answer for the current question
export async function submitUserAnswer(sessionId, questionId, answerText) {
  const response = await fetch(`${BASE_URL}/api/interview/answer`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    // Backend expects "session_id", "question_id", and "answer_text"
    body: JSON.stringify({
      session_id: sessionId,
      question_id: questionId,
      answer_text: answerText,
    }),
  });
  return response.json();
}

// Retrieve the final report for a session
export async function getReport(sessionId) {
  const response = await fetch(`${BASE_URL}/api/report/${sessionId}`);
  return response.json();
}

export default { startInterview, submitUserAnswer, getReport };
