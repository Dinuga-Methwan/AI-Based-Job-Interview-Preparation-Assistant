import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { submitUserAnswer } from '../services/api';

export default function InterviewRoom() {
  const navigate = useNavigate();
  const [answerText, setAnswerText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!answerText.trim()) return;
    setIsSubmitting(true);
    try {
      await submitUserAnswer(1, answerText);
      navigate('/results');
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-slate-950 text-slate-100 min-h-screen">
      <div className="max-w-3xl mx-auto mt-10 p-6">
        {/* Progress indicator */}
        <div className="text-sm mb-2 text-slate-400">Question 1 of 5</div>
        {/* Placeholder question */}
        <h2 className="text-2xl font-semibold text-slate-100 mb-6">
          Sample interview question goes here?
        </h2>
        {/* Answer textarea */}
        <textarea
          value={answerText}
          onChange={(e) => setAnswerText(e.target.value)}
          disabled={isSubmitting}
          className="w-full h-64 p-4 bg-slate-900 text-slate-100 border border-slate-700 rounded-lg focus:ring-2 focus:ring-indigo-500 resize-none"
          placeholder="Type your answer..."
        />
        {/* Submit button */}
        <button
          onClick={handleSubmit}
          disabled={isSubmitting || !answerText.trim()}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg mt-4 font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSubmitting ? 'Scoring...' : 'Submit Answer'}
        </button>
      </div>
    </div>
  );
}

<div className="flex justify-end">
  <button
    type="submit"
    disabled={isEvaluating}
    className={`flex items-center justify-center font-semibold px-8 py-3.5 rounded-xl shadow-lg transition-all duration-300 ${isEvaluating ? 'bg-indigo-500/50 text-indigo-200 cursor-wait animate-pulse' : 'bg-indigo-600 hover:bg-indigo-500 text-white'}`}
  >
    {isEvaluating ? (
      <>
        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        AI is evaluating...
      </>
    ) : 'Submit Answer'}
  </button>
</div>
        </form >
      </div >
    </div >
  );
}
