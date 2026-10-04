const LEVELS = [
  { name: 'Beginner', icon: '🌱', description: 'Start with basic English skills' },
  { name: 'Intermediate', icon: '📈', description: 'Improve your communication skills' },
  { name: 'Advanced', icon: '🚀', description: 'Master advanced English' },
]

export default function LevelSelection({ level, onChange, disabled }) {
  return (
    <section
      id="level-selection"
      className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8"
    >
      <h2 className="text-2xl font-bold text-slate-800">Choose Your English Level</h2>
      <p className="text-slate-500 mt-2">
        Exercises are generated for the level you select.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
        {LEVELS.map((item) => {
          const active = item.name === level
          return (
            <button
              key={item.name}
              type="button"
              disabled={disabled}
              aria-pressed={active}
              onClick={() => onChange(item.name)}
              className={`text-left p-5 rounded-2xl border-2 transition disabled:opacity-60 disabled:cursor-not-allowed ${
                active
                  ? 'border-blue-600 bg-blue-50 shadow-md'
                  : 'border-slate-200 bg-white hover:border-blue-300 hover:shadow-md'
              }`}
            >
              <div className="text-3xl mb-3">{item.icon}</div>
              <h3 className="text-lg font-semibold text-slate-800">{item.name}</h3>
              <p className="text-slate-500 text-sm mt-1">{item.description}</p>
              {active && (
                <p className="text-blue-600 font-semibold text-sm mt-3">✓ Selected</p>
              )}
            </button>
          )
        })}
      </div>
    </section>
  )
}
