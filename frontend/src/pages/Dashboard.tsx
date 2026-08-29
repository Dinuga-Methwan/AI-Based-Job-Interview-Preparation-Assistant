import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { startInterview } from '../services/api';
export default function Dashboard() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleStartTrack = async (role) => {
    setLoading(true);
    try {
      const data = await startInterview(role);
      if (data && data.session_id) {
        localStorage.setItem('sessionId', data.session_id);
        navigate('/interview');
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full flex flex-col items-center justify-center space-y-12">
      {/* Hero Section */}
      <section className="py-16 text-center">
        <h1 className="text-4xl font-bold mb-4">Start wherever you're interviewing next</h1>
      </section>

      {/* Cards Grid */}
      <div className="w-full grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl">
        {/* Card 1 */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl w-full h-full p-8 hover:-translate-y-1 hover:shadow-lg transition-all cursor-pointer" onClick={() => handleStartTrack('software')}>
          <h2 className="text-2xl font-semibold mb-2">{loading ? 'Starting...' : 'Software Engineer Track'}</h2>
          <p className="text-slate-300">Data structures, systems design</p>
        </div>
        {/* Card 2 */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl w-full h-full p-8 hover:-translate-y-1 hover:shadow-lg transition-all cursor-pointer" onClick={() => handleStartTrack('behavioral')}>
          <h2 className="text-2xl font-semibold mb-2">{loading ? 'Starting...' : 'Behavioral & HR Track'}</h2>
          <p className="text-slate-300">Structure, clarity, substance</p>
        </div>
      </div>
    </div>
  );
}

            <div>
              <div className="w-12 h-12 bg-indigo-500/10 rounded-xl flex items-center justify-center text-indigo-400 mb-6">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
              </div>
              
              <h3 className="text-2xl font-bold text-white mb-3">Software Engineering</h3>
              <p className="text-slate-400 text-sm leading-relaxed mb-6">
                Master data structures, algorithms, system design, and technical communication evaluated by our deep learning AI engine.
              </p>
            </div>

            <div>
               <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold tracking-wider">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse"></span>
                  2 AI TRACKS AVAILABLE
               </div>
            </div>
          </div >

  {/* Product Management Card (Inactive Stub) */ }
  < div className = "bg-[#0D1326]/40 border border-slate-800/50 rounded-3xl p-8 opacity-70 flex flex-col justify-between min-h-[300px]" >
            <div>
              <div className="w-12 h-12 bg-slate-800 rounded-xl flex items-center justify-center text-slate-500 mb-6">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-slate-300 mb-3">Product Management</h3>
              <p className="text-slate-500 text-sm leading-relaxed">
                Strategy, market sizing, feature prioritization, and stakeholder management simulations.
              </p>
            </div>
            <div>
               <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800 border border-slate-700 text-slate-400 text-xs font-semibold tracking-wider">
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-500"></span>
                  COMING SOON
               </div>
            </div>
          </div >

  {/* Data Science Card (Inactive Stub) */ }
  < div className = "bg-[#0D1326]/40 border border-slate-800/50 rounded-3xl p-8 opacity-70 flex flex-col justify-between min-h-[300px]" >
            <div>
              <div className="w-12 h-12 bg-slate-800 rounded-xl flex items-center justify-center text-slate-500 mb-6">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-slate-300 mb-3">Data Science</h3>
              <p className="text-slate-500 text-sm leading-relaxed">
                Machine learning theory, statistical analysis, A/B testing, and model deployment scenarios.
              </p>
            </div>
            <div>
               <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-800 border border-slate-700 text-slate-400 text-xs font-semibold tracking-wider">
                   <span className="w-1.5 h-1.5 rounded-full bg-slate-500"></span>
                  COMING SOON
               </div>
            </div>
          </div >

        </div >
      </div >
    </div >
  );
}
