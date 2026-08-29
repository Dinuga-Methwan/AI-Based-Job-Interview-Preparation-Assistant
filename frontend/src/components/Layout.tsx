import React from 'react';
import { Link, Outlet } from 'react-router-dom';

export default function Layout() {
  return (
    <div className="absolute inset-0 z-40 bg-slate-950 text-slate-100 flex flex-col overflow-x-hidden">
      {/* Fixed top navbar */}
      <nav className="fixed top-0 left-0 right-0 bg-slate-900 bg-opacity-90 backdrop-blur-md z-40 h-16 flex items-center px-4 shadow-md">
        <div className="max-w-7xl mx-auto w-full flex justify-between items-center">
          <div className="text-xl font-bold">READINESS.COACH</div>
          <div className="flex items-center gap-8">
            <Link to="/" className="hover:underline">Home</Link>
            <Link to="/dashboard" className="hover:underline">Dashboard</Link>
          </div>
        </div>
      </nav>
      {/* Main content area with padding to avoid overlap */}
      <main className="flex-grow pt-24 pb-12 px-6 w-full max-w-7xl mx-auto">
        <Outlet />
      </main>
    </div>
  );
}
