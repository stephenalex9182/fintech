import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center p-8">
      <div className="max-w-4xl text-center space-y-8">
        <h1 className="text-5xl md:text-7xl font-extrabold bg-gradient-to-r from-blue-400 to-emerald-400 text-transparent bg-clip-text animate-pulse">
          Fintech AI Agent
        </h1>
        <p className="text-xl text-slate-300">
          Your personal AI-powered financial researcher. Analyze stocks, track portfolios, and get real-time sentiment analysis powered by LangGraph.
        </p>
        
        <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-2xl text-left space-y-6">
          <h2 className="text-2xl font-semibold text-emerald-400">How it runs</h2>
          <ol className="list-decimal list-inside space-y-4 text-slate-300">
            <li><strong className="text-white">Authenticate:</strong> Create an account or log in to secure your portfolio data.</li>
            <li><strong className="text-white">Query the AI:</strong> Use natural language to ask for stock analysis (e.g., "What is the trend for RELIANCE.NS?").</li>
            <li><strong className="text-white">Agent Workflow:</strong> The LangGraph AI Agent breaks down your query, fetches live stock data via APIs, and runs technical/sentiment analysis.</li>
            <li><strong className="text-white">Insights:</strong> View the results on your personalized dashboard.</li>
          </ol>
        </div>

        <div className="pt-8">
          <Link href="/login" className="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-full transition-all shadow-lg hover:shadow-blue-500/50">
            Get Started (Login)
          </Link>
        </div>
      </div>
    </div>
  );
}
