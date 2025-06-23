import React, { useState, useEffect } from 'react';
import { FaGithub, FaTwitter, FaLinkedin, FaEnvelope } from 'react-icons/fa';
import './App.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');
  const [isPageScrollable, setIsPageScrollable] = useState(false);

  useEffect(() => {
    fetchStats();
  }, []);

  useEffect(() => {
    const checkScrollable = () => {
      const isScrollable = document.body.scrollHeight > window.innerHeight;
      setIsPageScrollable(isScrollable);
    };

    checkScrollable();
    window.addEventListener('resize', checkScrollable);
    
    const observer = new MutationObserver(checkScrollable);
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true
    });

    return () => {
      window.removeEventListener('resize', checkScrollable);
      observer.disconnect();
    };
  }, [results, loading, stats]);

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/stats`);
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE}/api/similarity_search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          k: 10,
          min_score: 0.25
        })
      });

      if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResults(data.results || []);
      
      fetchStats();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatScore = (score) => {
    return (score * 100).toFixed(1);
  };

  const highlightQuery = (text, query) => {
    if (!query) return text;
    
    const words = query.toLowerCase().split(' ');
    let highlighted = text;
    
    words.forEach(word => {
      const regex = new RegExp(`(${word})`, 'gi');
      highlighted = highlighted.replace(regex, '<mark>$1</mark>');
    });
    
    return highlighted;
  };

  return (
    <div className={`min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-emerald-950 relative overflow-hidden ${!isPageScrollable ? 'flex flex-col' : ''}`}>
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-emerald-800 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-green-800 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-blob animation-delay-2000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-teal-800 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-blob animation-delay-4000"></div>
      </div>

      <header className="relative z-10 py-8">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center">
            <h1 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-emerald-400 via-green-300 to-teal-400 bg-clip-text text-transparent mb-4">
              Research Assistant
            </h1>
            <p className="text-xl text-emerald-200/70 font-light">
              Ask questions about research papers and get cited answers
            </p>
          </div>
        </div>
      </header>

      <main className={`relative z-10 max-w-6xl mx-auto px-6 ${!isPageScrollable ? 'flex-1 flex flex-col' : 'pb-8'}`}>
        <div className="mb-12">
          <form onSubmit={handleSearch} className="max-w-4xl mx-auto">
            <div className="relative">
              <div className="glass-card p-6">
                <div className="flex gap-4">
                  <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask a question about the research papers..."
                    className="flex-1 bg-black/20 backdrop-blur-md border border-emerald-800/30 rounded-2xl px-6 py-4 text-emerald-100 placeholder-emerald-300/50 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/50 transition-all duration-300"
                  />
                  <button 
                    type="submit" 
                    disabled={loading}
                    className="glass-button px-8 py-4 rounded-2xl font-semibold text-white transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? (
                      <div className="flex items-center gap-2">
                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                        Searching...
                      </div>
                    ) : (
                      'Search'
                    )}
                  </button>
                </div>
              </div>
            </div>
          </form>

          {error && (
            <div className="mt-6 max-w-4xl mx-auto">
              <div className="glass-card border-red-400/30 bg-red-500/10 p-4 rounded-2xl">
                                        <div className="text-red-300 text-center">
                  Error: {error}
                </div>
              </div>
            </div>
          )}
        </div>

        <div className={`space-y-6 ${!isPageScrollable ? 'flex-1' : ''}`}>
          {stats && (
            <div className="glass-card p-6 rounded-2xl">
              <div className="flex flex-wrap items-center justify-between gap-4 text-emerald-200/80">
                <div className="flex items-center gap-6">
                  <div className="text-lg">
                    <span className="font-semibold text-emerald-300">{stats.total_chunks}</span> chunks available
                  </div>
                  {results.length > 0 && (
                    <div className="text-lg">
                      <span className="font-semibold text-green-300">{results.length}</span> results found
                    </div>
                  )}
                </div>
                
                {stats.top_referenced_papers && stats.top_referenced_papers.length > 0 && (
                  <div className="flex items-center gap-4">
                    <span className="text-sm text-emerald-300/60">Most referenced:</span>
                    <div className="flex gap-2">
                      {stats.top_referenced_papers.slice(0, 3).map((paper, index) => (
                        <div key={paper.source_doc_id} className="text-xs bg-black/20 backdrop-blur-sm px-3 py-1 rounded-full border border-emerald-700/30">
                          {paper.source_doc_id.replace('.pdf', '')}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {results.map((result, index) => (
            <div key={result.id} className="glass-card p-8 rounded-2xl hover:scale-[1.02] transition-all duration-300">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-gradient-to-r from-emerald-600 to-green-600 rounded-full flex items-center justify-center text-emerald-100 font-bold text-lg border border-emerald-500/30">
                    {index + 1}
                  </div>
                  <div className="text-emerald-200/80">
                    <div className="font-semibold">{result.metadata.source_doc_id}</div>
                    <div className="text-sm text-emerald-300/60">{result.metadata.journal}</div>
                  </div>
                </div>
                
                <div className="flex items-center gap-4">
                  <div className="text-right text-emerald-200/80">
                    <div className="text-sm text-emerald-300/60">Relevance</div>
                    <div className="font-bold text-lg text-emerald-300">
                      {formatScore(result.score)}%
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="mb-6">
                <h3 className="text-xl font-semibold text-emerald-100 mb-3">
                  {result.metadata.section_heading}
                </h3>
                <div 
                  className="text-emerald-100/90 leading-relaxed text-lg"
                  dangerouslySetInnerHTML={{
                    __html: highlightQuery(result.text, query)
                  }}
                />
              </div>

              <div className="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-emerald-800/30">
                <div className="flex items-center gap-6 text-sm text-emerald-300/60">
                  <span>Published: {result.metadata.publish_year}</span>
                  <span>Referenced: {result.metadata.usage_count} times</span>
                </div>
                
                {result.metadata.link && (
                  <a 
                    href={result.metadata.link} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="glass-button-sm px-4 py-2 rounded-xl text-sm font-medium text-emerald-100 hover:scale-105 transition-all duration-300"
                  >
                    View Source
                  </a>
                )}
              </div>
            </div>
          ))}

          {!loading && results.length === 0 && query && (
            <div className="glass-card p-12 rounded-2xl text-center">
              <div className="text-emerald-200/60 text-xl">
                No results found for "<span className="text-emerald-400">{query}</span>"
              </div>
              <div className="text-emerald-300/40 mt-2">
                Try different keywords or a broader search
              </div>
            </div>
          )}

          {!query && (
            <div className="glass-card p-12 rounded-2xl text-center">
              <div className="text-emerald-200/80 text-xl mb-4">
                Try these example searches:
              </div>
              <div className="flex flex-wrap justify-center gap-3">
                {[
                  "What is velvet bean?",
                  "Transformer attention mechanism",
                  "Intercropping mucuna with maize",
                  "How do neural networks work?"
                ].map((example) => (
                  <button
                    key={example}
                    onClick={() => setQuery(example)}
                    className="glass-button-sm px-4 py-2 rounded-xl text-sm font-medium text-emerald-100 hover:scale-105 transition-all duration-300"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className={`relative z-20 ${isPageScrollable ? 'mt-16' : ''}`}>
        <div className="glass-card border-t border-white/10 p-6">
          <div className="max-w-6xl mx-auto flex items-center justify-between">
            <div className="text-emerald-300/50 text-sm">
              © 2024 Research Assistant. Powered by AI.
            </div>
            
            <div className="flex items-center gap-4">
              <a href="https://github.com/anistark/research-assistant" target="_blank" rel="noopener noreferrer" 
                 className="social-icon p-3 rounded-full text-emerald-300/60 hover:text-emerald-100 hover:scale-110 transition-all duration-300">
                <FaGithub size={20} />
              </a>
              <a href="https://x.com/kranirudha" target="_blank" rel="noopener noreferrer"
                 className="social-icon p-3 rounded-full text-white/60 hover:text-white hover:scale-110 transition-all duration-300">
                <FaTwitter size={20} />
              </a>
              <a href="https://linkedin.com/in/kranirudha" target="_blank" rel="noopener noreferrer"
                 className="social-icon p-3 rounded-full text-white/60 hover:text-white hover:scale-110 transition-all duration-300">
                <FaLinkedin size={20} />
              </a>
              <a href="mailto:hi@anirudha.dev" target="_blank" rel="noopener noreferrer"
                 className="social-icon p-3 rounded-full text-white/60 hover:text-white hover:scale-110 transition-all duration-300">
                <FaEnvelope size={20} />
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
