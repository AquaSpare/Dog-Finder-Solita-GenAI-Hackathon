const CATEGORY_COLORS = {
  adaptability: { filled: "bg-amber-400", empty: "bg-amber-100" },
  friendliness: { filled: "bg-rose-400", empty: "bg-rose-100" },
  health: { filled: "bg-emerald-400", empty: "bg-emerald-100" },
  trainability: { filled: "bg-blue-400", empty: "bg-blue-100" },
  physical: { filled: "bg-orange-400", empty: "bg-orange-100" },
}

export default function StatBar({ label, value, category = "adaptability" }) {
  const { filled, empty } = CATEGORY_COLORS[category] || CATEGORY_COLORS.adaptability
  const rounded = Math.round(value ?? 0)

  return (
    <div className="flex items-center gap-3">
      <span className="text-sm text-slate-600 w-48 flex-shrink-0">{label}</span>
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map((i) => (
          <div
            key={i}
            className={`w-3 h-3 rounded-full ${i <= rounded ? filled : empty}`}
          />
        ))}
      </div>
      <span className="text-xs text-slate-400 w-6">{value ? value.toFixed(1) : "—"}</span>
    </div>
  )
}
