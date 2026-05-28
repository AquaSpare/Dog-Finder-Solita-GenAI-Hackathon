import CategorySection from "./CategorySection"

const BREED_GROUPS = [
  "Working Dogs",
  "Herding Dogs",
  "Mixed Breed Dogs",
  "Companion Dogs",
  "Hybrid Dogs",
  "Terrier Dogs",
  "Hound Dogs",
  "Sporting Dogs",
]

const SIZES = ["Small", "Medium", "Large", "Very Large"]

const CATEGORIES = [
  {
    title: "Adaptability",
    attrs: [
      "apartment_friendly",
      "good_for_novice",
      "sensitivity",
      "tolerates_alone",
      "tolerates_cold",
      "tolerates_hot",
    ],
  },
  {
    title: "Friendliness",
    attrs: ["friendliness", "affectionate_family", "kid_friendly", "dog_friendly", "stranger_friendly"],
  },
  {
    title: "Health & Grooming",
    attrs: ["health_grooming", "shedding", "drooling", "easy_groom", "general_health", "weight_gain_potential"],
  },
  {
    title: "Trainability",
    attrs: ["trainability", "easy_train", "intelligence", "mouthiness", "prey_drive", "barking", "wanderlust"],
  },
  {
    title: "Physical Needs",
    attrs: ["physical_needs", "energy_level", "intensity", "exercise_needs", "playfulness"],
  },
]

export function countActiveFilters(breedGroups, sizes, ranges) {
  const rangeActive = Object.values(ranges).filter(([min, max]) => min !== 1 || max !== 5).length
  return breedGroups.length + sizes.length + rangeActive
}

export default function FilterPanel({ breedGroups, sizes, ranges, onBreedGroupChange, onSizeChange, onRangeChange, onClear }) {
  const activeCount = countActiveFilters(breedGroups, sizes, ranges)

  return (
    <aside className="w-full bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-slate-800 text-sm">Filters</span>
          {activeCount > 0 && (
            <span className="bg-orange-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">
              {activeCount}
            </span>
          )}
        </div>
        {activeCount > 0 && (
          <button
            onClick={onClear}
            className="text-xs text-orange-500 hover:text-orange-700 font-medium transition-colors"
          >
            Clear all
          </button>
        )}
      </div>

      <div className="p-4 space-y-4 overflow-y-auto max-h-[calc(100vh-10rem)]">
        {/* Breed Group */}
        <div>
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
            Breed Group
          </div>
          <div className="grid grid-cols-1 gap-1">
            {BREED_GROUPS.map((g) => (
              <label key={g} className="flex items-center gap-2 cursor-pointer group">
                <input
                  type="checkbox"
                  checked={breedGroups.includes(g)}
                  onChange={() => onBreedGroupChange(g)}
                  className="w-3.5 h-3.5 rounded border-slate-300 text-orange-500 accent-orange-500 cursor-pointer"
                />
                <span className="text-sm text-slate-600 group-hover:text-slate-800 transition-colors">
                  {g}
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Size */}
        <div>
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
            Size
          </div>
          <div className="flex flex-wrap gap-1.5">
            {SIZES.map((s) => (
              <button
                key={s}
                onClick={() => onSizeChange(s)}
                className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-colors ${
                  sizes.includes(s)
                    ? "bg-orange-500 text-white"
                    : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                }`}
              >
                {s}
              </button>
            ))}
          </div>
        </div>

        {/* Attribute categories */}
        <div>
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
            Traits (1–5)
          </div>
          {CATEGORIES.map((cat) => (
            <CategorySection
              key={cat.title}
              title={cat.title}
              attrs={cat.attrs}
              ranges={ranges}
              onRangeChange={onRangeChange}
            />
          ))}
        </div>
      </div>
    </aside>
  )
}
