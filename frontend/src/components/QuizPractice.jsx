import { useState } from 'react'

const LETTERS = ['A', 'B', 'C', 'D']

const TITLES = {
  Reading: { icon: '📖', label: 'Reading Practice' },
  Vocabulary: { icon: '📚', label: 'Vocabulary Practice' },
  Grammar: { icon: '📝', label: 'Grammar Practice' },
}

function ExerciseHeader({ area, exercise }) {
  if (area === 'Reading') {
    return (
      <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 mb-6">
        <h3 className="text-xl font-bold text-slate-800">{exercise.title}</h3>
        <p className="text-slate-700 mt-3 leading-relaxed whitespace-pre-line">
          {exercise.passage}
        </p>
      </div>
    )
  }

  if (area === 'Vocabulary') {
    return (
      <div className="bg-green-50 border border-green-200 rounded-xl p-5 mb-6">
        <div className="flex flex-wrap items-baseline gap-3">
          <h3 className="text-3xl font-bold text-slate-800">{exercise.word}</h3>
          <span className="text-sm italic text-slate-500">{exercise.part_of_speech}</span>
        </div>
        <p className="text-slate-700 mt-3">
          <strong>Meaning:</strong> {exercise.meaning}
        </p>
        <p className="text-slate-700 mt-2">
          <strong>Example:</strong> {exercise.example}
        </p>
        <p className="text-slate-700 mt-2">
          <strong>Synonyms:</strong> {exercise.synonyms.join(', ')}
        </p>
      </div>
    )
  }

  return (
    <div className="bg-orange-50 border border-orange-200 rounded-xl p-5 mb-6">
      <h3 className="text-xl font-bold text-slate-800">{exercise.topic}</h3>
      <p className="text-slate-700 mt-3 leading-relaxed whitespace-pre-line">
        {exercise.rule}
      </p>
    </div>
  )
}

export default function QuizPractice({ area, level, exercise, onNew, onComplete }) {
  // Every quiz area now sends a list of 10 questions (older single-question data still works).
  const questions = exercise.questions ?? (exercise.question ? [exercise.question] : [])
  const total = questions.length
  const heading = TITLES[area]

  const [current, setCurrent] = useState(0)
  const [answers, setAnswers] = useState({})
  const [submitted, setSubmitted] = useState(false)

  const score = questions.reduce(
    (sum, item, index) => sum + (answers[index] === item.answer ? 1 : 0),
    0,
  )
  const allAnswered = questions.every((_, index) => answers[index])
  const question = questions[current]

  function choose(letter) {
    if (submitted) return
    setAnswers((previous) => ({ ...previous, [current]: letter }))
  }

  function submit() {
    if (!allAnswered || submitted) return
    setSubmitted(true)
    onComplete?.(score, total)
  }

  return (
    <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <p className="text-sm text-blue-600 font-semibold">
            {heading.icon} {heading.label}
          </p>
          <p className="text-sm text-slate-500 mt-1">Level: {level}</p>
        </div>
        {!submitted && total > 1 && (
          <p className="text-sm text-slate-500">
            Question {current + 1} of {total}
          </p>
        )}
      </div>

      <ExerciseHeader area={area} exercise={exercise} />

      {!submitted ? (
        <>
          {total > 1 && (
            <div className="flex flex-wrap gap-2 mb-5" aria-label="Question navigation">
              {questions.map((_, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => setCurrent(index)}
                  className={`w-9 h-9 rounded-lg text-sm font-semibold border transition ${
                    index === current
                      ? 'bg-blue-600 text-white border-blue-600'
                      : answers[index]
                        ? 'bg-green-100 text-green-800 border-green-300'
                        : 'bg-white text-slate-600 border-slate-300 hover:border-blue-300'
                  }`}
                >
                  {index + 1}
                </button>
              ))}
            </div>
          )}

          <p className="text-lg font-semibold text-slate-800">{question.question}</p>

          <div className="mt-4 space-y-3">
            {LETTERS.map((letter) => {
              const picked = answers[current] === letter
              return (
                <button
                  key={letter}
                  type="button"
                  onClick={() => choose(letter)}
                  className={`w-full text-left px-4 py-3 rounded-xl border-2 transition ${
                    picked
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-slate-200 hover:border-blue-300'
                  }`}
                >
                  <span className="font-bold text-slate-700 mr-3">{letter}.</span>
                  {question.options[letter]}
                </button>
              )
            })}
          </div>

          <div className="flex items-center justify-between mt-6">
            <button
              type="button"
              onClick={() => setCurrent((value) => value - 1)}
              disabled={current === 0}
              className="px-5 py-2.5 rounded-lg border border-slate-300 text-slate-700 font-medium disabled:opacity-40"
            >
              ← Previous
            </button>

            {current < total - 1 ? (
              <button
                type="button"
                onClick={() => setCurrent((value) => value + 1)}
                className="px-5 py-2.5 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700"
              >
                Next →
              </button>
            ) : (
              <button
                type="button"
                onClick={submit}
                disabled={!allAnswered}
                className="px-5 py-2.5 rounded-lg bg-green-600 text-white font-semibold hover:bg-green-700 disabled:opacity-40 disabled:cursor-not-allowed"
              >
                Submit Answers
              </button>
            )}
          </div>

          {current === total - 1 && !allAnswered && total > 1 && (
            <p className="text-sm text-amber-700 mt-3">
              Answer all questions before submitting (unanswered:{' '}
              {questions
                .map((_, index) => index + 1)
                .filter((number) => !answers[number - 1])
                .join(', ')}
              ).
            </p>
          )}
        </>
      ) : (
        <>
          <div className="text-center mb-6">
            <div className="text-5xl mb-2">{score === total ? '🎉' : '👏'}</div>
            <h2 className="text-3xl font-bold text-slate-800">
              Your Score: {score} / {total}
            </h2>
          </div>

          <div className="space-y-4">
            {questions.map((item, index) => {
              const userAnswer = answers[index]
              const correct = userAnswer === item.answer
              return (
                <div
                  key={index}
                  className={`rounded-xl border p-5 ${
                    correct ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
                  }`}
                >
                  <p className="font-semibold text-slate-800">
                    {total > 1 ? `${index + 1}. ` : ''}
                    {item.question}
                  </p>
                  <p className="text-sm mt-2">
                    <strong>Your answer:</strong> {userAnswer}. {item.options[userAnswer]}{' '}
                    {correct ? '✅' : '❌'}
                  </p>
                  {!correct && (
                    <p className="text-sm mt-1">
                      <strong>Correct answer:</strong> {item.answer}. {item.options[item.answer]}
                    </p>
                  )}
                  {item.explanation && (
                    <p className="text-sm text-slate-600 mt-2">{item.explanation}</p>
                  )}
                </div>
              )
            })}
          </div>

          <div className="text-center mt-8">
            <button
              type="button"
              onClick={onNew}
              className="px-6 py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700"
            >
              New {area} Practice
            </button>
          </div>
        </>
      )}
    </section>
  )
}
