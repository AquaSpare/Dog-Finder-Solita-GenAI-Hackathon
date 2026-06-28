import { useNavigate } from "react-router-dom"

const PLACEHOLDER = "https://placehold.co/800x500/f1f5f9/94a3b8?text=🐕"

const SIZE_COLORS = {
  Small: "bg-sky-100 text-sky-700",
  Medium: "bg-teal-100 text-teal-700",
  Large: "bg-violet-100 text-violet-700",
  "Very Large": "bg-rose-100 text-rose-700",
}

export default function HeroSection({ dog }) {
  const navigate = useNavigate()

  return (
    <div>
      {/* Back button */}
      <button
        onClick={() => navigate(-1)}
        className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-orange-500 transition-colors mb-6"
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        All Breeds
      </button>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden mb-6">
        <div className="lg:flex">
          {/* Image */}
          <div className="lg:w-2/5 aspect-[4/3] lg:aspect-auto bg-slate-100 flex-shrink-0">
            <img
              src={dog.image_url || PLACEHOLDER}
              alt={dog.breed_name}
              className="w-full h-full object-cover"
              onError={(e) => { e.target.src = PLACEHOLDER }}
            />
          </div>

          {/* Info */}
          <div className="p-6 lg:p-8 flex flex-col justify-center">
            <div className="flex flex-wrap gap-2 mb-3">
              {dog.breed_group && (
                <span className="bg-orange-100 text-orange-700 text-xs font-semibold px-2.5 py-1 rounded-full">
                  {dog.breed_group}
                </span>
              )}
              {dog.size && (
                <span
                  className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
                    SIZE_COLORS[dog.size] || "bg-slate-100 text-slate-600"
                  }`}
                >
                  {dog.size}
                </span>
              )}
            </div>

            <h1 className="text-3xl lg:text-4xl font-bold text-slate-800 mb-4">
              {dog.breed_name}
            </h1>

            {/* Quick stats grid */}
            <div className="grid grid-cols-3 gap-4 mb-4">
              {dog.height && <StatChip label="Height" value={dog.height} />}
              {dog.weight && <StatChip label="Weight" value={dog.weight} />}
              {dog.life_span && <StatChip label="Life Span" value={dog.life_span} />}
            </div>

            {dog.description && (
              <p className="text-sm text-slate-600 leading-relaxed">
                {dog.description}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

function StatChip({ label, value }) {
  return (
    <div className="bg-slate-50 rounded-xl p-3 text-center">
      <div className="text-xs text-slate-500 mb-1">{label}</div>
      <div className="text-xs font-semibold text-slate-700 leading-tight">{value}</div>
    </div>
  )
}
