import { useState } from 'react'
import { evaluateWriting } from '../api'

const MIN_CHARS = 10

function FeedbackRow({ title, text }) {
  return (
    <div>
      <h4 className="font-semibold text-slate-800">{title}</h4>
      <p className="text-slate-600 mt-1">{text}</p>
    </div>
  )
}

export default function WritingPractice({ level, exercise, onNew, onComplete }) {
  const [text, setText] = useState('')
  const [busy, setBusy] = useState(false)
  const [feedback, setFeedback] = useState(null)
  const [error, setError] = useState('')

  const trimmed = text.trim()
  const words = trimmed ? trimmed.split(/\s+/).length : 0
  const canSubmit = trimmed.length >= MIN_CHARS && !busy && !feedback

  async function submit() {
    if (!canSubmit) return
    setBusy(true)
    setError('')
    try {
      const data = await evaluateWriting({
        level,
        topic: exercise.topic,
        instructions: exercise.instructions,
        answer: trimmed,
      })
      setFeedback(data.feedback)
      onComplete?.(data.feedback.score, 10)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
      <p className="text-sm text-purple-600 font-semibold">✍️ Writing Practice</p>
      <p className="text-sm text-slate-500 mt-1">Level: {level}</p>

      <div className="bg-purple-50 border border-purple-200 rounded-xl p-5 mt-5">
        <h3 className="text-xl font-bold text-slate-800">{exercise.title}</h3>
        <p className="text-slate-700 mt-3">
          <strong>Topic:</strong> {exercise.topic}
        </p>
        <p className="text-slate-700 mt-2">
          <strong>Instructions:</strong> {exercise.instructions}
        </p>
        <p className="text-slate-700 mt-2">
          <strong>Recommended length:</strong> {exercise.recommended_length}
        </p>
        <p className="text-slate-700 mt-2">
          <strong>Focus:</strong> {exercise.focus}
        </p>
      </div>

      <label htmlFor="writing-answer" className="block font-semibold text-slate-800 mt-6">
        Your answer
      </label>
      <textarea
        id="writing-answer"
        value={text}
        onChange={(event) => setText(event.target.value)}
        disabled={busy || Boolean(feedback)}
        rows={9}
        maxLength={6000}
        placeholder="Write your answer here..."
        className="w-full mt-2 border border-slate-300 rounded-xl p-4 focus:outline-none focus:ring-2 focus:ring-purple-300 disabled:bg-slate-50"
      />
      <p className="text-sm text-slate-500 mt-1">{words} words</p>

      {error && (
        <p className="mt-3 bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 text-sm">
          {error}
        </p>
      )}

      {!feedback && (
        <button
          type="button"
          onClick={submit}
          disabled={!canSubmit}
          className="mt-4 px-6 py-3 rounded-lg bg-purple-600 text-white font-semibold hover:bg-purple-700 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {busy ? 'AI is checking your writing...' : 'Get AI Feedback'}
        </button>
      )}

      {feedback && (
        <div className="mt-8 border-t border-slate-200 pt-6 space-y-4">
          <div className="text-center">
            <div className="text-5xl mb-2">⭐</div>
            <h2 className="text-3xl font-bold text-slate-800">
              Score: {feedback.score} / 10
            </h2>
            <p className="text-slate-600 mt-2">{feedback.summary}</p>
          </div>

          <FeedbackRow title="Grammar" text={feedback.grammar} />
          <FeedbackRow title="Vocabulary" text={feedback.vocabulary} />
          <FeedbackRow title="Spelling and punctuation" text={feedback.spelling_punctuation} />
          <FeedbackRow title="Structure" text={feedback.structure} />

          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-green-50 border border-green-200 rounded-xl p-4">
              <h4 className="font-semibold text-green-800">What you did well</h4>
              <ul className="list-disc list-inside text-slate-700 mt-2 space-y-1">
                {feedback.strengths.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
            <div className="bg-orange-50 border border-orange-200 rounded-xl p-4">
              <h4 className="font-semibold text-orange-800">What to improve</h4>
              <ul className="list-disc list-inside text-slate-700 mt-2 space-y-1">
                {feedback.improvements.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-xl p-4">
            <h4 className="font-semibold text-slate-800">Corrected version</h4>
            <p className="text-slate-700 mt-2 whitespace-pre-line">
              {feedback.corrected_version}
            </p>
          </div>

          <p className="bg-blue-50 border border-blue-200 text-blue-800 rounded-xl p-4">
            💡 <strong>Tip:</strong> {feedback.tip}
          </p>

          <div className="text-center">
            <button
              type="button"
              onClick={onNew}
              className="px-6 py-3 rounded-lg bg-purple-600 text-white font-semibold hover:bg-purple-700"
            >
              New Writing Task
            </button>
          </div>
        </div>
      )}
    </section>
  )
}
