// Landing page component - copy of user provided template
import React, { useEffect, useState, useRef } from "react";
import {
  ArrowRight, Sparkles, Target, Gauge, FileSearch, CheckCircle2,
  Code2, MessagesSquare, Activity, TrendingUp, ClipboardList,
  BookOpen, Layers, Repeat, ShieldCheck, ChevronLeft, ChevronRight,
  type LucideIcon,
} from "lucide-react";
import "../styles/landing.css";



const DIFF_STYLES = [
  { bg: "var(--accent-tint)", text: "var(--accent-strong)", border: "var(--accent-tint)" },
  { bg: "var(--accent-soft)", text: "#2E1B7A", border: "var(--accent-soft)" },
  { bg: "var(--accent)", text: "#FFFFFF", border: "var(--accent)" },
];
const DIFF_LABELS = ["EASY", "MEDIUM", "HARD"];

const TAGS = [
  "Semantic Embeddings", "Cosine Similarity", "Adaptive Difficulty", "Explainable Feedback",
  "Rule-Based Reasoning", "TF-IDF Keyword Gaps", "4-Tier Rubric", "Real-Time Scoring",
];

const STATS = [
  { icon: BookOpen, value: "145", label: "Questions across both tracks" },
  { icon: Layers, value: "3", label: "AI techniques working together" },
  { icon: Gauge, value: "4", label: "Scoring tiers per answer" },
];

const STACK_FEATURES = [
  { icon: BookOpen, t: "Curated Question Bank", d: "105 technical + 40 behavioral questions, each scored against four reference answer tiers." },
  { icon: Repeat, t: "One Session, Full Loop", d: "Answer, get scored, see what's missing, and face a harder or easier question next — no separate tools." },
  { icon: ShieldCheck, t: "Built for Practice, Not Judgement", d: "Feedback names the concepts to add next time, not just a pass or fail number." },
];

const BENTO_ROW1 = [
  { icon: Code2, tag: "Technical", title: "Software Engineer Track", d: "105 questions across data structures, systems design, and problem solving." },
  { icon: MessagesSquare, tag: "Behavioral", title: "Behavioral & HR Track", d: "40 curated questions scored for structure, clarity, and substance." },
  { icon: Activity, tag: "Real-time", title: "Live AI Scoring", d: "Every answer compared against four reference tiers as you type." },
];
const BENTO_ROW2 = [
  { icon: TrendingUp, tag: "Adaptive", title: "Adaptive Difficulty", d: "Questions shift Easy → Hard based on how you're actually performing in the session." },
  { icon: ClipboardList, tag: "Reports", title: "Session Reports", d: "A full readout of every answer, score, and concept you missed — ready to review." },
];

function BentoCard({ icon: Icon, tag, title, d, big }: { icon: LucideIcon; tag: string; title: string; d: string; big?: boolean }) {
  return (
    <div className="irc-bento" style={{ minHeight: big ? 240 : 220 }}>
      <Icon size={big ? 96 : 76} className="irc-bento-icon" style={{ color: "#FFFFFF" }} />
      <span className="irc-bento-tag">{tag}</span>
      <p className="irc-display font-semibold text-[17px] mb-1.5" style={{ color: "var(--on-dark)" }}>{title}</p>
      <p className="text-[13px] leading-relaxed" style={{ color: "var(--on-dark-dim)" }}>{d}</p>
    </div>
  );
}

export default function LandingPage() {
  const circumference = 276;
  const targetScore = 78;
  const [ringOffset, setRingOffset] = useState<number>(circumference);
  const [scoreVal, setScoreVal] = useState<number>(0);
  const [diffIdx, setDiffIdx] = useState<number>(0);
  const [chipsShown, setChipsShown] = useState<number>(0);
  const reduceMotion = useRef<boolean>(
    typeof window !== "undefined" &&
    !!window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches
  );

  useEffect(() => {
    if (reduceMotion.current) {
      setScoreVal(targetScore);
      setRingOffset(circumference - (targetScore / 100) * circumference);
      setDiffIdx(2);
      setChipsShown(2);
      return;
    }
    const t1 = setTimeout(() => {
      setRingOffset(circumference - (targetScore / 100) * circumference);
    }, 300);
    let start: number | null = null;
    const dur = 1400;
    const step = (ts: number) => {
      if (!start) start = ts;
      const p = Math.min((ts - start) / dur, 1);
      setScoreVal(Math.round(p * targetScore));
      if (p < 1) requestAnimationFrame(step);
    };
    const t2 = setTimeout(() => requestAnimationFrame(step), 300);
    const t3 = setTimeout(() => setDiffIdx(1), 1900);
    const t4 = setTimeout(() => setDiffIdx(2), 2600);
    const t5 = setTimeout(() => setChipsShown(1), 2000);
    const t6 = setTimeout(() => setChipsShown(2), 2400);
    return () => [t1, t2, t3, t4, t5, t6].forEach(clearTimeout);
  }, []);

  return (
    <div className="irc-root">


      {/* FLOATING NAV */}
      <div className="sticky top-4 z-30 px-4">
        <nav className="irc-nav-pill max-w-4xl mx-auto px-5 py-2.5 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="irc-live-dot" />
            <span className="irc-display font-semibold text-[14px] tracking-tight">
              READINESS<span style={{ color: "var(--accent)" }}>.</span>COACH
            </span>
          </div>
          <div className="hidden md:flex items-center gap-6 irc-mono text-[11px]" style={{ color: "var(--dim)" }}>
            <span>WHY US</span>
            <span>TRACKS</span>
            <span>HOW IT WORKS</span>
          </div>
          <button className="irc-btn-primary rounded-full px-4 py-2 text-[13px]">Get Started</button>
        </nav>
      </div>

      {/* HERO — framed dark card with oversized wordmark */}
      <section className="relative z-10 max-w-6xl mx-auto px-4 pt-24 pb-16 md:py-24">
        <div className="irc-hero-card rounded-3xl px-6 sm:px-10 pt-14 pb-10">
          <div className="irc-hero-grid" />
          <div className="irc-wordmark-bg">READY</div>
          <div className="relative grid lg:grid-cols-2 gap-14 items-center">
            <div>
              <div
                className="inline-flex items-center gap-2 mb-6 irc-mono text-[11px] px-3 py-1.5 rounded-full"
                style={{ border: "1px solid rgba(255,255,255,0.16)", color: "var(--on-dark-dim)", background: "rgba(255,255,255,0.04)" }}
              >
                <Sparkles size={12} style={{ color: "#B39DFF" }} />
                SCORED BY SEMANTIC SIMILARITY, NOT KEYWORDS
              </div>
              <h1 className="irc-display text-[38px] sm:text-[50px] leading-[1.08] font-semibold tracking-tight" style={{ color: "var(--on-dark)" }}>
                Find out if your answer
                <br />
                was actually <span style={{ color: "#B39DFF" }}>good enough</span>
                <span style={{ color: "#B39DFF" }}>.</span>
              </h1>
              <p className="mt-6 text-[16px] leading-relaxed max-w-md" style={{ color: "var(--on-dark-dim)" }}>
                Practice real interview questions and get scored the way an interviewer
                actually thinks — by meaning, not by matching buzzwords. Difficulty adapts
                to you, question by question.
              </p>
              <div className="mt-8 flex items-center gap-4">
                <button className="irc-btn-white rounded-full px-6 py-3 text-sm flex items-center gap-2">
                  Plan Your Session <ArrowRight size={15} />
                </button>
                <button className="irc-btn-ghost-dark rounded-full px-6 py-3 text-sm">Explore Tracks</button>
              </div>
            </div>

            {/* LIVE CONSOLE DEMO — light panel on dark card */}
            <div className="irc-console rounded-2xl p-6">
              <div className="flex items-center justify-between mb-5">
                <span className="irc-mono text-[11px]" style={{ color: "var(--dim)" }}>SESSION_04 · Q3 OF 5</span>
                <div className="flex items-center gap-1.5">
                  <span className="irc-dot" style={{ background: "var(--border-strong)" }} />
                  <span className="irc-dot" style={{ background: "var(--border-strong)" }} />
                  <span className="irc-live-dot" />
                </div>
              </div>

              <div className="rounded-lg p-4 mb-4" style={{ background: "var(--bg)", border: "1px solid var(--border)" }}>
                <p className="irc-mono text-[10px] mb-2" style={{ color: "var(--dim)" }}>QUESTION — SOFTWARE ENGINEER</p>
                <p className="text-[14px] leading-relaxed">
                  "Explain the difference between a hash map and a binary search tree, and when you'd choose one over the other."
                </p>
              </div>

              <div className="rounded-lg p-4 mb-5" style={{ background: "var(--bg)", border: "1px solid var(--border)" }}>
                <p className="irc-mono text-[10px] mb-2" style={{ color: "var(--dim)" }}>YOUR ANSWER</p>
                <p className="text-[13px] leading-relaxed" style={{ color: "var(--dim)" }}>
                  "A hash map gives average O(1) lookups using a hash function, while a BST keeps
                  elements ordered so you can do range queries and in-order traversal..."
                </p>
              </div>

              <div className="flex items-center gap-5 mb-5">
                <div className="relative w-[92px] h-[92px] flex-shrink-0">
                  <svg width="92" height="92" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="44" strokeWidth="7" className="irc-ring-track" />
                    <circle
                      cx="50" cy="50" r="44"
                      strokeWidth="7"
                      className="irc-ring-progress"
                      strokeDasharray={circumference}
                      strokeDashoffset={ringOffset}
                      transform="rotate(-90 50 50)"
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="irc-display text-[22px] font-semibold">{scoreVal}</span>
                    <span className="irc-mono text-[9px]" style={{ color: "var(--dim)" }}>SCORE</span>
                  </div>
                </div>
                <div className="flex-1">
                  <p className="irc-mono text-[10px] mb-2" style={{ color: "var(--dim)" }}>VERDICT</p>
                  <p className="irc-display font-semibold text-[15px] mb-3" style={{ color: "var(--accent-strong)" }}>Good</p>
                  <p className="irc-mono text-[10px] mb-1.5" style={{ color: "var(--dim)" }}>NEXT DIFFICULTY</p>
                  <div className="flex gap-1.5">
                    {DIFF_LABELS.map((label, i) => (
                      <span
                        key={label}
                        className="irc-diff-pill"
                        style={{
                          color: i === diffIdx ? DIFF_STYLES[i].text : "var(--dim)",
                          background: i === diffIdx ? DIFF_STYLES[i].bg : "transparent",
                          border: `1px solid ${i === diffIdx ? DIFF_STYLES[i].border : "var(--border)"}`,
                        }}
                      >
                        {label}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div>
                <p className="irc-mono text-[10px] mb-2" style={{ color: "var(--dim)" }}>CONCEPTS TO MENTION NEXT TIME</p>
                <div className="flex flex-wrap gap-2">
                  {chipsShown >= 1 && <span className="irc-chip">amortized cost</span>}
                  {chipsShown >= 2 && <span className="irc-chip" style={{ animationDelay: ".1s" }}>tree balancing</span>}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* WHY LEARNERS CHOOSE — text+stats left, stacked cards right */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 py-16 md:py-24 grid lg:grid-cols-2 gap-16">
        <div>
          <h2 className="irc-display text-[28px] sm:text-[32px] font-semibold leading-tight mb-5">
            Why learners keep coming back to Readiness Coach
          </h2>
          <p className="text-[15px] leading-relaxed mb-10" style={{ color: "var(--dim)" }}>
            Built as a real AI system, not a scripted quiz — one that scores meaning, adapts
            in real time, and tells you exactly what to fix before the interview that matters.
          </p>
          <div className="grid grid-cols-3 gap-6">
            {STATS.map((s) => (
              <div key={s.label}>
                <div className="irc-badge-circle mb-3">
                  <s.icon size={20} style={{ color: "var(--accent)" }} />
                </div>
                <p className="irc-display font-semibold text-[26px] leading-none mb-1.5">{s.value}</p>
                <p className="text-[12.5px] leading-snug" style={{ color: "var(--dim)" }}>{s.label}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="flex flex-col gap-4">
          {STACK_FEATURES.map((f) => (
            <div key={f.t} className="irc-stack-card">
              <div className="irc-badge-circle" style={{ background: "rgba(255,255,255,0.06)", border: "1px solid var(--ink-border)" }}>
                <f.icon size={20} style={{ color: "#B39DFF" }} />
              </div>
              <div>
                <p className="irc-display font-semibold text-[15px] mb-1.5" style={{ color: "var(--on-dark)" }}>{f.t}</p>
                <p className="text-[13px] leading-relaxed" style={{ color: "var(--on-dark-dim)" }}>{f.d}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* TAG CLOUD */}
      <section className="relative z-10 max-w-3xl mx-auto px-6 py-16 md:py-24 text-center" style={{ background: "var(--bg-alt)" }}>
        <p className="irc-mono text-[11px] mb-4" style={{ color: "var(--accent)" }}>UNDER THE HOOD</p>
        <h2 className="irc-display text-[26px] sm:text-[30px] font-semibold mb-9">
          Built to think like an interviewer.
        </h2>
        <div className="flex flex-wrap justify-center gap-2.5">
          {TAGS.map((t) => (
            <span key={t} className="irc-pill-tag">
              <span className="irc-pill-dot" /> {t}
            </span>
          ))}
        </div>
      </section>

      {/* WHAT'S INSIDE — boxed band, clear start/end like a card */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 py-10">
        <div className="irc-band-card">
          <div className="flex flex-wrap items-end justify-between gap-4 mb-10">
            <div>
              <p className="irc-mono text-[11px] mb-2" style={{ color: "var(--accent-strong)" }}>WHAT'S INSIDE</p>
              <h2 className="irc-display text-[26px] sm:text-[30px] font-semibold">Five pieces, one session</h2>
              <p className="text-[13.5px] mt-2 max-w-md" style={{ color: "var(--dim)" }}>
                From picking a track to reading your final report — everything happens in one place.
              </p>
            </div>
            <button className="irc-btn-primary rounded-full px-5 py-2.5 text-sm inline-flex items-center gap-2">
              Try a session <ArrowRight size={14} />
            </button>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            {BENTO_ROW1.map((c) => <BentoCard key={c.title} {...c} />)}
          </div>
          <div className="grid md:grid-cols-2 gap-4 mt-4">
            {BENTO_ROW2.map((c) => <BentoCard key={c.title} {...c} big />)}
          </div>

          <div className="flex items-center justify-between mt-10">
            <button className="irc-btn-ghost rounded-full px-5 py-2.5 text-sm" style={{ background: "#fff" }}>View all questions</button>
            <div className="flex gap-2">
              <button className="irc-arrow-btn"><ChevronLeft size={16} /></button>
              <button className="irc-arrow-btn"><ChevronRight size={16} /></button>
            </div>
          </div>
        </div>
      </section>

      {/* CHOOSE YOUR TRACK — asymmetric: solid CTA + 2 track cards */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 py-10">
        <p className="irc-mono text-[11px] mb-2" style={{ color: "var(--accent)" }}>PICK A TRACK</p>
        <h2 className="irc-display text-[26px] sm:text-[30px] font-semibold mb-8">Start wherever you're interviewing next</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="irc-solid-cta">
            <div>
              <p className="irc-display font-semibold text-[20px] mb-2" style={{ color: "#fff" }}>Pick a track and start now</p>
              <p className="text-[13px] leading-relaxed" style={{ color: "rgba(255,255,255,0.8)" }}>
                Free to try. Your first session takes about ten minutes.
              </p>
            </div>
            <button className="irc-btn-white rounded-full px-5 py-2.5 text-sm mt-6 w-fit">Browse all questions</button>
          </div>
          <BentoCard icon={Code2} tag="105 Questions" title="Software Engineer Track" d="Data structures, systems design, and problem solving, scored question by question." big />
          <BentoCard icon={MessagesSquare} tag="40 Questions" title="Behavioral & HR Track" d="Structured, clear answers to the questions every interview panel actually asks." big />
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 py-20">
        <p className="irc-mono text-[11px] mb-2" style={{ color: "var(--accent)" }}>PROCESS</p>
        <h2 className="irc-display text-[28px] sm:text-[32px] font-semibold mb-12">How a session runs</h2>
        <div className="grid md:grid-cols-4 gap-8">
          {[
            { n: "01", t: "Pick your track", d: "Software Engineer or General/HR — 145 curated questions across both." },
            { n: "02", t: "Answer for real", d: "Type your response like you would out loud in the actual interview." },
            { n: "03", t: "Get scored instantly", d: "Sentence embeddings + cosine similarity compare your answer to reference tiers." },
            { n: "04", t: "Difficulty adapts", d: "Score well, the next question gets harder. Struggle, it eases up." },
          ].map((s, i) => (
            <div key={s.n} className="flex gap-4">
              <div className="flex flex-col items-center">
                <div className="irc-num irc-mono">{s.n}</div>
                {i < 3 && <div className="irc-step-line flex-1 mt-2 hidden md:block" />}
              </div>
              <div className="pb-2">
                <p className="irc-display font-semibold text-[15px] mb-1.5">{s.t}</p>
                <p className="text-[13px] leading-relaxed" style={{ color: "var(--dim)" }}>{s.d}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* UNDER THE HOOD DETAIL */}
      <section className="relative z-10 py-16 md:py-24" style={{ background: "var(--bg-alt)", borderTop: "1px solid var(--border)", borderBottom: "1px solid var(--border)" }}>
        <div className="max-w-6xl mx-auto px-6">
          <p className="irc-mono text-[11px] mb-2" style={{ color: "var(--accent-strong)" }}>THE TECHNIQUES</p>
          <h2 className="irc-display text-[28px] sm:text-[32px] font-semibold mb-12">Three techniques doing the work</h2>
          <div className="grid md:grid-cols-3 gap-5">
            {[
              { icon: Target, t: "Semantic Similarity Scoring", d: "384-dimension sentence embeddings compare your answer's meaning against four reference tiers — Excellent through Poor — not just shared keywords.", tag: "cosine similarity" },
              { icon: Gauge, t: "Adaptive Difficulty Engine", d: "A rule-based system shifts each next question between Easy, Medium, and Hard based on how you're actually performing in the session.", tag: "rule-based reasoning" },
              { icon: FileSearch, t: "Explainable Feedback", d: "Keyword-gap analysis surfaces the specific concepts your answer missed, so feedback is something you can act on — not just a number.", tag: "keyword-gap analysis" },
            ].map((f) => (
              <div key={f.t} className="irc-card irc-card-hover rounded-xl p-6">
                <div className="w-10 h-10 rounded-lg flex items-center justify-center mb-5" style={{ background: "var(--accent-tint)", border: "1px solid var(--accent-soft)" }}>
                  <f.icon size={18} style={{ color: "var(--accent)" }} />
                </div>
                <p className="irc-display font-semibold text-[16px] mb-2">{f.t}</p>
                <p className="text-[13.5px] leading-relaxed mb-4" style={{ color: "var(--dim)" }}>{f.d}</p>
                <span className="irc-mono text-[10px]" style={{ color: "var(--accent-strong)" }}>{f.tag}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 py-20">
        <div className="irc-cta-band rounded-2xl px-8 py-14 text-center">
          <h3 className="irc-display text-[26px] sm:text-[32px] font-semibold mb-4">
            Your next interview shouldn't be the first time you find out.
          </h3>
          <p className="text-[14px] mb-8" style={{ color: "var(--dim)" }}>Free to start. No card required.</p>
          <button className="irc-btn-primary rounded-lg px-7 py-3 text-sm inline-flex items-center gap-2">
            Get Started Free <ArrowRight size={15} />
          </button>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="relative z-10 border-t" style={{ borderColor: "var(--border)" }}>
        <div className="max-w-6xl mx-auto px-6 py-8 flex items-center justify-between irc-mono text-[11px]" style={{ color: "var(--dim)" }}>
          <span className="flex items-center gap-2"><span className="irc-live-dot" /> READINESS.COACH</span>
          <span className="flex items-center gap-1.5"><CheckCircle2 size={12} /> © 2026</span>
        </div>
      </footer>
    </div>
  );
}
            </div >
          </div >
        </div >
      </section >

  {/* ========================================================= */ }
{/* SECTION 6: INTERACTIVE TRACKS & CAPABILITIES (Slide 6) - Sleek */ }
{/* ========================================================= */ }
<section id="tracks" className="w-full h-[120vh] sm:h-screen snap-center shrink-0 flex flex-col items-center justify-center px-6 py-12">
  <div className="w-full max-w-5xl mx-auto">
    <div className="text-center mb-8">
      <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">Track Capabilities</h2>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      {/* Track 1 */}
      <div
        onClick={() => handleStartTrack('Software Engineer')}
        className="bg-[#0D1326] border border-slate-800/80 rounded-2xl p-6 hover:border-indigo-500/50 transition-colors cursor-pointer flex flex-col justify-between shadow-sm group"
      >
        <div>
          <h3 className="text-lg font-bold text-white group-hover:text-indigo-400 transition-colors mb-3">
            Software Engineer
          </h3>
          <p className="text-slate-400 text-xs leading-relaxed mb-4">
            Core focus: Data Structures & Algorithms, systems design, and code logic complexity evaluation.
          </p>
        </div>
        <button className="text-left text-indigo-500 text-sm font-semibold group-hover:text-indigo-400 transition-colors">
          Launch →
        </button>
      </div>

      {/* Track 2 */}
      <div
        onClick={() => handleStartTrack('Behavioral & HR')}
        className="bg-[#0D1326] border border-slate-800/80 rounded-2xl p-6 hover:border-indigo-500/50 transition-colors cursor-pointer flex flex-col justify-between shadow-sm group"
      >
        <div>
          <h3 className="text-lg font-bold text-white group-hover:text-indigo-400 transition-colors mb-3">
            Behavioral & HR
          </h3>
          <p className="text-slate-400 text-xs leading-relaxed mb-4">
            Core focus: Culture fit, STAR method frameworks, tone analysis, empathy, and communication clarity.
          </p>
        </div>
        <button className="text-left text-indigo-500 text-sm font-semibold group-hover:text-indigo-400 transition-colors">
          Launch →
        </button>
      </div>

      {/* Track 3 */}
      <div
        onClick={() => handleStartTrack('System Design')}
        className="bg-[#0D1326] border border-slate-800/80 rounded-2xl p-6 hover:border-indigo-500/50 transition-colors cursor-pointer flex flex-col justify-between shadow-sm group"
      >
        <div>
          <h3 className="text-lg font-bold text-white group-hover:text-indigo-400 transition-colors mb-3">
            System Design
          </h3>
          <p className="text-slate-400 text-xs leading-relaxed mb-4">
            Core focus: Scalability, distributed systems, architectural trade-offs, and resilience patterns.
          </p>
        </div>
        <button className="text-left text-indigo-500 text-sm font-semibold group-hover:text-indigo-400 transition-colors">
          Launch →
        </button>
      </div>
    </div>

    {/* Visual Comparison Table */}
    <div className="overflow-x-auto bg-[#0D1326] border border-slate-800/80 rounded-2xl p-6 shadow-sm">
      <table className="w-full text-left border-collapse min-w-[700px]">
        <thead>
          <tr className="border-b border-slate-800 text-xs">
            <th className="pb-3 px-3 text-slate-500 font-semibold uppercase tracking-wider">Feature / Track</th>
            <th className="pb-3 px-3 text-slate-300 font-medium">Software Engineer</th>
            <th className="pb-3 px-3 text-slate-300 font-medium">Behavioral & HR</th>
            <th className="pb-3 px-3 text-slate-300 font-medium">System Design</th>
          </tr>
        </thead>
        <tbody className="text-xs">
          <tr className="border-b border-slate-800/50">
            <td className="py-4 px-3 font-medium text-slate-400">Core Focus</td>
            <td className="py-4 px-3 text-slate-500">DSA</td>
            <td className="py-4 px-3 text-slate-500">STAR Method</td>
            <td className="py-4 px-3 text-slate-500">Architecture</td>
          </tr>
          <tr className="border-b border-slate-800/50">
            <td className="py-4 px-3 font-medium text-slate-400">AI Scoring Model</td>
            <td className="py-4 px-3 text-slate-500">Logic validation</td>
            <td className="py-4 px-3 text-slate-500">Empathy & clarity</td>
            <td className="py-4 px-3 text-slate-500">Trade-offs</td>
          </tr>
          <tr>
            <td className="py-4 px-3 font-medium text-slate-400">Real-time Feedback</td>
            <td className="py-4 px-3 text-indigo-400 font-medium">✓</td>
            <td className="py-4 px-3 text-indigo-400 font-medium">✓</td>
            <td className="py-4 px-3 text-indigo-400 font-medium">✓</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

{/* ========================================================= */ }
{/* SECTION 7: CLOSING CTA & FOOTER (Slide 7 and 8 combined) - Sleek */ }
{/* ========================================================= */ }
<section className="w-full h-screen snap-center shrink-0 flex flex-col justify-between pt-24 text-center">
  <div className="w-full max-w-3xl mx-auto px-6 flex-grow flex flex-col justify-center">
    <h2 className="text-3xl sm:text-5xl font-bold text-white tracking-tight mb-6">Ready to Ace Your Interview?</h2>
    <p className="text-slate-400 text-sm sm:text-base leading-relaxed mb-10">
      Thank you for exploring our AI-Powered Job Interview Assistant architecture. The next step is on you.
    </p>
    <div>
      <a
        href="#tracks"
        className="bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-10 py-4 rounded-xl shadow-lg shadow-indigo-500/20 transition-all duration-200 inline-block text-sm"
      >
        Start Your Session Now
      </a>
    </div>
  </div>

  <footer className="w-full border-t border-slate-800/80 bg-[#0D1326] px-6 py-10 mt-12 shrink-0">
    <div className="max-w-4xl mx-auto flex flex-col items-center text-center space-y-6">
      <blockquote className="text-lg sm:text-xl italic font-medium text-slate-400 max-w-2xl leading-relaxed">
        "Good design is obvious. Great design is transparent, immersive, and built entirely around user confidence."
      </blockquote>

      <div className="w-full pt-8 border-t border-slate-800/50 flex flex-col sm:flex-row justify-between items-center text-xs text-slate-500 gap-4">
        <div>© {new Date().getFullYear()} Readiness Coach. All rights reserved.</div>
        <div className="flex gap-6 font-medium">
          <span className="text-indigo-400 hover:text-indigo-300 transition-colors cursor-pointer">www.readiness.coach</span>
          <span className="text-indigo-400 hover:text-indigo-300 transition-colors cursor-pointer">support@readiness.coach</span>
        </div>
      </div>
    </div>
  </footer>
</section>

    </div >
  );
}
