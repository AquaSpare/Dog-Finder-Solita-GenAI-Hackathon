const SORT_OPTIONS = [
  { label: "Breed Name A→Z", value: "breed_name:asc" },
  { label: "Breed Name Z→A", value: "breed_name:desc" },
  { label: "Most Energetic", value: "energy_level:desc" },
  { label: "Friendliest", value: "friendliness:desc" },
  { label: "Best for Training", value: "trainability:desc" },
  { label: "Most Intelligent", value: "intelligence:desc" },
  { label: "Most Playful", value: "playfulness:desc" },
  { label: "Best with Kids", value: "kid_friendly:desc" },
  { label: "Most Adaptable", value: "adaptability:desc" },
]

export default function SortBar({ total, sortBy, sortOrder, onSortChange }) {
  const current = `${sortBy}:${sortOrder}`

  return (
    <div className="flex items-center justify-between mb-4">
      <p className="text-sm text-slate-500">
        <span className="font-semibold text-slate-800">{total}</span> breed{total !== 1 ? "s" : ""} found
      </p>
      <div className="flex items-center gap-2">
        <label className="text-sm text-slate-500 hidden sm:block">Sort by</label>
        <select
          value={current}
          onChange={(e) => {
            const [by, order] = e.target.value.split(":")
            onSortChange(by, order)
          }}
          className="text-sm border border-slate-200 rounded-lg px-3 py-1.5 bg-white text-slate-700 cursor-pointer focus:outline-none focus:ring-2 focus:ring-orange-300"
        >
          {SORT_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}
