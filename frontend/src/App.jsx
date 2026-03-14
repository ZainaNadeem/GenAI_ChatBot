import { useState, useRef, useEffect } from "react"
import "./App.css"

const API_URL = "http://localhost:8000/chat"

const SUGGESTIONS = [
  "What is Apple's revenue in 2023?",
  "Which company had the highest net income?",
  "How did Tesla's revenue grow?",
  "Compare cash flow in 2022",
]

const COMPANIES = [
  { name: "Microsoft", ticker: "MSFT", change: "+6.9%", pos: true, color: "#3b82f6" },
  { name: "Tesla",     ticker: "TSLA", change: "+19.0%", pos: true, color: "#10b981" },
  { name: "Apple",     ticker: "AAPL", change: "-2.8%",  pos: false, color: "#f59e0b" },
]

const STATS = [
  { label: "Combined Revenue", value: "$692B", sub: "FY2023" },
  { label: "Combined Net Income", value: "$184B", sub: "FY2023" },
  { label: "Avg Profit Margin", value: "25.4%", sub: "3-yr avg" },
  { label: "Data Points", value: "45", sub: "9 filings" },
]

function TickerBar() {
  const items = [...COMPANIES, ...COMPANIES, ...COMPANIES]
  return (
    <div className="ticker-wrap">
      <div className="ticker-track">
        {items.map((c, i) => (
          <span key={i} className="ticker-item">
            <span className="ticker-name">{c.ticker}</span>
            <span className={`ticker-change ${c.pos ? "pos" : "neg"}`}>
              {c.change}
            </span>
            <span className="ticker-sep">·</span>
          </span>
        ))}
      </div>
    </div>
  )
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "Welcome to the BCG Financial Intelligence ChatBot.\n\nI have processed SEC 10-K filings for Microsoft, Tesla and Apple across FY2021–2023 — 45 data points extracted from 9 annual reports.\n\nQuery revenue, net income, cash flow, growth trends or company comparisons below.",
    },
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [apiStatus, setApiStatus] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  useEffect(() => {
    fetch("http://localhost:8000/")
      .then(r => r.ok ? setApiStatus(true) : setApiStatus(false))
      .catch(() => setApiStatus(false))
  }, [])

  const sendMessage = async (text) => {
    const userText = text || input.trim()
    if (!userText) return
    setMessages(prev => [...prev, { role: "user", text: userText }])
    setInput("")
    setLoading(true)
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText }),
      })
      const data = await res.json()
      setMessages(prev => [...prev, { role: "bot", text: data.response }])
    } catch {
      setMessages(prev => [...prev, {
        role: "bot",
        text: "Connection error. Ensure the backend is running on port 8000.",
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="app">

      {/* ── SIDEBAR ── */}
      <aside className="sidebar">
        <div className="sidebar-top">
          <div className="brand">
            <div className="brand-icon">$</div>
            <div className="brand-text">
              <span className="brand-title">BCG GenAI Chatbot</span>
              <span className="brand-sub">Intelligence Terminal</span>
            </div>
          </div>
        </div>

        <div className="sidebar-section">
          <p className="section-label">COVERAGE</p>
          {COMPANIES.map(c => (
            <div key={c.name} className="company-card">
              <div className="company-left">
                <span className="company-bar" style={{ background: c.color }} />
                <div>
                  <p className="company-name">{c.name}</p>
                  <p className="company-ticker">{c.ticker}</p>
                </div>
              </div>
              <span className={`company-pct ${c.pos ? "pos" : "neg"}`}>
                {c.change}
              </span>
            </div>
          ))}
        </div>

        <div className="sidebar-section">
          <p className="section-label">SNAPSHOT</p>
          <div className="stats-grid">
            {STATS.map(s => (
              <div key={s.label} className="stat-card">
                <p className="stat-value">{s.value}</p>
                <p className="stat-label">{s.label}</p>
                <p className="stat-sub">{s.sub}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="sidebar-section">
          <p className="section-label">SOURCE</p>
          <p className="source-text">SEC EDGAR · 10-K Annual Reports</p>
          <p className="source-text">FY2021 · FY2022 · FY2023</p>
        </div>

        <div className="sidebar-footer">
          <div className={`status ${apiStatus ? "on" : "off"}`}>
            <span className="status-dot" />
            <span>{apiStatus ? "Backend Connected" : "Backend Offline"}</span>
          </div>
        </div>
      </aside>

      {/* ── MAIN ── */}
      <div className="main">

        {/* Header */}
        <div className="topbar">
          <div className="topbar-left">
            <h1>Financial Analysis Assistant</h1>
            <p>Natural language queries · SEC 10-K data · FY2021–2023</p>
          </div>
        </div>

        {/* Ticker */}
        <TickerBar />

        {/* Suggestions */}
        <div className="suggestions">
          {SUGGESTIONS.map((s, i) => (
            <button key={i} className="chip" onClick={() => sendMessage(s)}>
              {s}
            </button>
          ))}
        </div>

        {/* Messages */}
        <div className="messages">
          {messages.map((m, i) => (
            <div key={i} className={`msg ${m.role}`}>
              <div className="msg-who">
                {m.role === "bot" ? "▸ TERMINAL" : "▸ YOU"}
              </div>
              <div className={`bubble ${m.role}`}>
                <pre>{m.text}</pre>
              </div>
            </div>
          ))}
          {loading && (
            <div className="msg bot">
              <div className="msg-who">▸ TERMINAL</div>
              <div className="bubble bot typing">
                <span /><span /><span />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="composer">
          <span className="prompt-symbol">$</span>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKey}
            placeholder="Query financial data..."
            disabled={loading}
            autoFocus
          />
          <button onClick={() => sendMessage()} disabled={loading || !input.trim()}>
            Execute
          </button>
        </div>

      </div>
    </div>
  )
}