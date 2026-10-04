import { useCallback, useEffect, useRef, useState } from 'react'
import {
  generateExercise,
  getClientId,
  getProgress,
  saveProgress,
} from './api'
import AreaCards from './components/AreaCards'
import LevelSelection from './components/LevelSelection'
import ProgressPanel from './components/ProgressPanel'
import QuizPractice from './components/QuizPractice'
import WritingPractice from './components/WritingPractice'

const THEME_KEY = 'aiEnglishCoachTheme'

function getInitialTheme() {
  try {
    const saved = localStorage.getItem(THEME_KEY)
    if (saved === 'dark' || saved === 'light') return saved
  } catch {
    // storage unavailable: use the system setting below
  }
  return window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function App() {
  const [theme, setTheme] = useState(getInitialTheme)
  const [clientId] = useState(getClientId)
  const [level, setLevel] = useState('Beginner')
  const [area, setArea] = useState('')
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [progress, setProgress] = useState(null)

  const practiceRef = useRef(null)
  const activeRequest = useRef({ id: 0, controller: null })

  // Apply the theme to <html> and remember it.
  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
    try {
      localStorage.setItem(THEME_KEY, theme)
    } catch {
      // ignore: the theme still works for this visit
    }
  }, [theme])

  // Load saved progress once.
  useEffect(() => {
    const controller = new AbortController()
    getProgress(clientId, controller.signal)
      .then(setProgress)
      .catch(() => {
        // The panel simply stays hidden if the backend is not reachable yet.
      })
    return () => controller.abort()
  }, [clientId])

  const generate = useCallback(async (nextArea, nextLevel) => {
    // Only the newest request may update the screen.
    activeRequest.current.controller?.abort()
    const controller = new AbortController()
    const id = activeRequest.current.id + 1
    activeRequest.current = { id, controller }

    setLoading(true)
    setError('')
    setSession(null)

    try {
      const data = await generateExercise({
        area: nextArea,
        level: nextLevel,
        signal: controller.signal,
      })
      if (activeRequest.current.id !== id) return
      setSession(data)
    } catch (err) {
      if (err.name === 'AbortError' || activeRequest.current.id !== id) return
      setError(err.message)
    } finally {
      if (activeRequest.current.id === id) setLoading(false)
    }
  }, [])

  function handleSelectArea(nextArea) {
    setArea(nextArea)
    generate(nextArea, level)
    setTimeout(() => {
      practiceRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, 100)
  }

  function handleLevelChange(nextLevel) {
    setLevel(nextLevel)
    if (area) generate(area, nextLevel)
  }

  function handleNewPractice() {
    if (area) generate(area, level)
  }

  async function handleComplete(score, total) {
    if (!session) return
    try {
      const stats = await saveProgress({
        clientId,
        area: session.area,
        level: session.level,
        score,
        total,
      })
      setProgress(stats)
    } catch {
      // Saving progress is optional; the practice result is already on screen.
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-blue-600">AI English Coach</h1>
            <p className="text-sm text-slate-500 mt-1">
              Your personal AI-powered English learning platform
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => setTheme((value) => (value === 'dark' ? 'light' : 'dark'))}
              aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
              title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
              className="px-4 py-2.5 rounded-lg border border-slate-300 text-slate-700 font-medium hover:bg-slate-50 transition"
            >
              {theme === 'dark' ? '☀️ Light' : '🌙 Dark'}
            </button>
            <button
              type="button"
              onClick={() =>
                document
                  .getElementById('level-selection')
                  ?.scrollIntoView({ behavior: 'smooth' })
              }
              className="hidden sm:block bg-blue-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition"
            >
              Start Learning
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-10 space-y-10">
        <section>
          <h2 className="text-3xl font-bold text-slate-800">Improve Your English 🚀</h2>
          <p className="text-slate-600 mt-2">
            Practise reading, writing, vocabulary and grammar with fresh AI exercises.
          </p>
          <p className="text-sm text-blue-600 mt-3 font-medium">Current level: {level}</p>
        </section>

        <ProgressPanel progress={progress} />

        <LevelSelection level={level} onChange={handleLevelChange} disabled={loading} />

        <AreaCards
          selected={area}
          recommended={progress?.recommendation?.area}
          onSelect={handleSelectArea}
          disabled={loading}
        />

        <section ref={practiceRef} aria-live="polite">
          {loading && (
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 text-center">
              <div className="text-5xl mb-4">🤖</div>
              <h3 className="text-xl font-semibold text-slate-800">
                AI is preparing your exercise...
              </h3>
              <p className="text-slate-500 mt-2">
                Creating a fresh {level} {area} practice. This can take up to a minute.
              </p>
            </div>
          )}

          {!loading && error && (
            <div className="bg-red-50 border border-red-200 text-red-700 rounded-2xl p-6">
              <div className="text-3xl mb-3">⚠️</div>
              <h3 className="font-bold text-lg">Something went wrong</h3>
              <p className="mt-2">{error}</p>
              <button
                type="button"
                onClick={handleNewPractice}
                className="mt-5 bg-red-600 text-white px-5 py-2.5 rounded-lg font-semibold hover:bg-red-700 transition"
              >
                Try Again
              </button>
            </div>
          )}

          {!loading && !error && session && session.area === 'Writing' && (
            <WritingPractice
              key={session.session_id}
              level={session.level}
              exercise={session.exercise}
              onNew={handleNewPractice}
              onComplete={handleComplete}
            />
          )}

          {!loading && !error && session && session.area !== 'Writing' && (
            <QuizPractice
              key={session.session_id}
              area={session.area}
              level={session.level}
              exercise={session.exercise}
              onNew={handleNewPractice}
              onComplete={handleComplete}
            />
          )}
        </section>
      </main>

      <footer className="text-center text-sm text-slate-400 py-8">
        AI English Coach · Built with React, FastAPI and CrewAI
      </footer>
    </div>
  )
}

export default App
