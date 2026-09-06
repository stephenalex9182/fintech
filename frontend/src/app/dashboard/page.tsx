"use client";

import { useState } from "react";
import Link from "next/link";

export default function Dashboard() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleResearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query) return;
    setLoading(true);
    
    // Simulate AI delay for showcase
    setTimeout(() => {
      setResults(`Simulated AI Response for: "${query}"\n\nThe LangGraph agent has analyzed the technical indicators and recent news sentiment. The stock shows a bullish trend with an RSI of 62. News sentiment is highly positive.`);
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4 md:p-8">
      <header className="flex justify-between items-center mb-12 border-b border-slate-800 pb-6">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-emerald-400 text-transparent bg-clip-text">
          Fintech Dashboard
        </h1>
        <Link href="/" className="text-slate-400 hover:text-white transition-colors">
          Sign Out
        </Link>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: AI Agent Query */}
        <div className="lg:col-span-2 space-y-8">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
            <h2 className="text-xl font-semibold mb-4 text-emerald-400">Ask the Financial AI Agent</h2>
            <form onSubmit={handleResearch} className="flex gap-4">
              <input 
                type="text" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Analyze Apple stock..." 
                className="flex-1 px-4 py-3 bg-slate-950 border border-slate-800 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent text-white outline-none transition-all"
              />
              <button 
                type="submit" 
                disabled={loading}
                className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg transition-all disabled:opacity-50"
              >
                {loading ? "Researching..." : "Analyze"}
              </button>
            </form>
            
            {results && (
              <div className="mt-6 p-4 bg-slate-950 rounded-lg border border-slate-800 whitespace-pre-wrap text-slate-300">
                {results}
              </div>
            )}
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl h-64 flex flex-col items-center justify-center text-slate-500">
            {/* Placeholder for Charts */}
            <svg className="w-16 h-16 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"></path></svg>
            <p>Advanced Charts & Portfolio Analytics will appear here</p>
          </div>
        </div>

        {/* Right Column: Portfolio / Watchlist */}
        <div className="space-y-8">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
            <h2 className="text-xl font-semibold mb-4 text-blue-400">My Portfolio</h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-3 bg-slate-950 rounded-lg border border-slate-800">
                <div>
                  <p className="font-bold">AAPL</p>
                  <p className="text-sm text-slate-400">10 Shares</p>
                </div>
                <div className="text-right">
                  <p className="font-bold text-emerald-400">+$124.50</p>
                  <p className="text-sm text-slate-400">Avg: $150.00</p>
                </div>
              </div>
              <div className="flex justify-between items-center p-3 bg-slate-950 rounded-lg border border-slate-800">
                <div>
                  <p className="font-bold">RELIANCE.NS</p>
                  <p className="text-sm text-slate-400">50 Shares</p>
                </div>
                <div className="text-right">
                  <p className="font-bold text-emerald-400">+₹4,500</p>
                  <p className="text-sm text-slate-400">Avg: ₹2,400</p>
                </div>
              </div>
            </div>
            <button className="w-full mt-6 py-2 border border-slate-700 hover:bg-slate-800 rounded-lg text-sm text-slate-300 transition-colors">
              + Add Holding
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
