import StatBar from "./StatBar"

export default function StatCategory({ title, attrs, dog, category }) {
  return (
    <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
      <h3 className="font-semibold text-slate-800 mb-4">{title}</h3>
      <div className="space-y-3">
        {attrs.map(({ key, label }) => (
          <StatBar key={key} label={label} value={dog[key]} category={category} />
        ))}
      </div>
    </div>
  )
}
