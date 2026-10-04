const AREAS = [
  {
    title: 'Reading',
    icon: '📖',
    description: 'Read an AI-written passage and answer 10 questions.',
    card: 'bg-blue-50',
    badge: 'bg-blue-100',
  },
  {
    title: 'Writing',
    icon: '✍️',
    description: 'Write a short text and get detailed AI feedback.',
    card: 'bg-purple-50',
    badge: 'bg-purple-100',
  },
  {
    title: 'Vocabulary',
    icon: '📚',
    description: 'Learn a new word with a meaning, example and a 10-question quiz.',
    card: 'bg-green-50',
    badge: 'bg-green-100',
  },
  {
    title: 'Grammar',
    icon: '📝',
    description: 'Learn a grammar rule and test it with 10 questions.',
    card: 'bg-orange-50',
    badge: 'bg-orange-100',
  },
]

export default function AreaCards({ selected, recommended, onSelect, disabled }) {
  return (
    <section>
      <h2 className="text-2xl font-bold text-slate-800 mb-4">Pick a Skill</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {AREAS.map((area) => (
          <button
            key={area.title}
            type="button"
            disabled={disabled}
            onClick={() => onSelect(area.title)}
            className={`${area.card} p-6 rounded-2xl border text-left transition hover:shadow-lg hover:-translate-y-1 disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:translate-y-0 ${
              selected === area.title
                ? 'border-blue-500 ring-2 ring-blue-200'
                : 'border-slate-200'
            }`}
          >
            <div
              className={`${area.badge} w-14 h-14 rounded-2xl flex items-center justify-center text-3xl`}
            >
              {area.icon}
            </div>
            <h3 className="text-xl font-bold text-slate-800 mt-4">{area.title}</h3>
            <p className="text-slate-600 text-sm mt-2">{area.description}</p>
            {recommended === area.title && (
              <p className="mt-3 inline-block text-xs font-semibold text-amber-700 bg-amber-100 rounded-full px-3 py-1">
                ⭐ Coach recommends
              </p>
            )}
            <div className="mt-4 text-blue-600 font-semibold">Start Practice →</div>
          </button>
        ))}
      </div>
    </section>
  )
}
