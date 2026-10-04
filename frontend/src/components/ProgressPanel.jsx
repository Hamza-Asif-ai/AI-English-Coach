const AREA_ORDER = ['Reading', 'Writing', 'Vocabulary', 'Grammar']

function Stat({ label, value }) {
  return (
    <div className="bg-slate-50 rounded-xl border border-slate-200 p-4 text-center">
      <div className="text-2xl font-bold text-slate-800">{value}</div>
      <div className="text-xs text-slate-500 mt-1">{label}</div>
    </div>
  )
}

export default function ProgressPanel({ progress }) {
  if (!progress) return null

  return (
    <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8">
      <h2 className="text-2xl font-bold text-slate-800">Your Progress</h2>

      <div className="grid grid-cols-3 gap-4 mt-5">
        <Stat label="Practices" value={progress.total_practices} />
        <Stat label="Average score" value={`${progress.average_score}%`} />
        <Stat
          label="Day streak"
          value={progress.streak > 0 ? `🔥 ${progress.streak}` : '0'}
        />
      </div>

      <div className="mt-6 space-y-3">
        {AREA_ORDER.map((area) => {
          const info = progress.per_area?.[area] ?? { count: 0, average: 0 }
          return (
            <div key={area}>
              <div className="flex justify-between text-sm text-slate-600">
                <span className="font-medium">{area}</span>
                <span>
                  {info.count > 0 ? `${info.average}% (${info.count})` : 'not tried yet'}
                </span>
              </div>
              <div className="h-2 bg-slate-100 rounded-full mt-1 overflow-hidden">
                <div
                  className="h-full bg-blue-500 rounded-full transition-all"
                  style={{ width: `${info.average}%` }}
                />
              </div>
            </div>
          )
        })}
      </div>

      {progress.recommendation && (
        <p className="mt-6 bg-amber-50 border border-amber-200 text-amber-800 rounded-xl p-4 text-sm">
          <strong>Coach says:</strong> {progress.recommendation.reason}
        </p>
      )}
    </section>
  )
}
