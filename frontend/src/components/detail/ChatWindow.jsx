import { useRef, useEffect, useState } from "react"
import { chatWithDog } from "../../api/dogs"

export default function ChatWindow({ dogId, dogName }) {
  const [messages, setMessages] = useState([])
  const [sessionId, setSessionId] = useState(null)
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const scrollRef = useRef(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages, loading])

  async function handleSubmit(e) {
    e.preventDefault()
    const question = input.trim()
    if (!question || loading) return

    setInput("")
    setError(null)
    setMessages((prev) => [...prev, { role: "user", text: question }])
    setLoading(true)

    try {
      const data = await chatWithDog(dogId, question, sessionId)
      setSessionId(data.session_id)
      setMessages((prev) => [...prev, { role: "ai", text: data.answer }])
    } catch {
      setError("Failed to get a response. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden flex flex-col">
      {/* Header */}
      <div className="px-5 py-4 border-b border-slate-100 flex items-center gap-3">
        <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center text-lg">
          🐾
        </div>
        <div>
          <h3 className="font-semibold text-slate-800 text-sm">Ask about {dogName}</h3>
          <p className="text-xs text-slate-400">Powered by AI</p>
        </div>
      </div>

      {/* Messages */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-3 min-h-64 max-h-96"
      >
        {messages.length === 0 && !loading && (
          <div className="flex flex-col items-center justify-center h-40 text-slate-300">
            <span className="text-4xl mb-2">💬</span>
            <p className="text-sm">Ask anything about the {dogName}!</p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            {msg.role === "ai" && (
              <div className="w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center text-sm mr-2 flex-shrink-0 mt-0.5">
                🐾
              </div>
            )}
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
                msg.role === "user"
                  ? "bg-slate-800 text-white rounded-tr-sm"
                  : "bg-slate-50 text-slate-700 border border-slate-100 rounded-tl-sm"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center text-sm mr-2 flex-shrink-0 mt-0.5">
              🐾
            </div>
            <div className="bg-slate-50 border border-slate-100 rounded-2xl rounded-tl-sm px-4 py-3">
              <div className="flex gap-1">
                {[0, 1, 2].map((i) => (
                  <div
                    key={i}
                    className="w-2 h-2 bg-slate-300 rounded-full animate-bounce"
                    style={{ animationDelay: `${i * 150}ms` }}
                  />
                ))}
              </div>
            </div>
          </div>
        )}

        {error && (
          <p className="text-xs text-rose-500 text-center py-1">{error}</p>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-slate-100 flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={`Ask about the ${dogName}...`}
          disabled={loading}
          className="flex-1 text-sm border border-slate-200 rounded-xl px-3.5 py-2.5 focus:outline-none focus:ring-2 focus:ring-orange-300 disabled:opacity-50 placeholder:text-slate-400"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="bg-orange-500 hover:bg-orange-600 disabled:opacity-40 disabled:cursor-not-allowed
            text-white rounded-xl px-4 py-2.5 text-sm font-medium transition-colors flex items-center gap-1"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </form>
    </div>
  )
}
