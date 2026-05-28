import { useNavigate } from "react-router-dom"
import StarRating from "../shared/StarRating"

const SIZE_COLORS = {
  Small: "bg-sky-100 text-sky-700",
  Medium: "bg-teal-100 text-teal-700",
  Large: "bg-violet-100 text-violet-700",
  "Very Large": "bg-rose-100 text-rose-700",
}

const PLACEHOLDER = "https://placehold.co/400x300/f1f5f9/94a3b8?text=🐕"

export default function DogCard({ dog }) {
  const navigate = useNavigate()

  return (
    <article
      onClick={() => navigate(`/dogs/${dog.id}`)}
      className="group bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden cursor-pointer
        hover:shadow-md hover:-translate-y-0.5 transition-all duration-200"
    >
      {/* Image */}
      <div className="relative aspect-[4/3] overflow-hidden bg-slate-100">
        <img
          src={dog.image_url || PLACEHOLDER}
          alt={dog.breed_name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          onError={(e) => { e.target.src = PLACEHOLDER }}
          loading="lazy"
        />
        {/* Gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent" />
        {/* Size pill on image */}
        {dog.size && (
          <span
            className={`absolute top-2 right-2 text-xs font-semibold px-2 py-0.5 rounded-full ${
              SIZE_COLORS[dog.size] || "bg-slate-100 text-slate-600"
            }`}
          >
            {dog.size}
          </span>
        )}
        {/* Breed group on image bottom */}
        {dog.breed_group && (
          <span className="absolute bottom-2 left-2 text-white text-xs font-medium opacity-90">
            {dog.breed_group}
          </span>
        )}
      </div>

      {/* Card body */}
      <div className="p-3">
        <h3 className="font-bold text-slate-800 text-sm mb-2 truncate">{dog.breed_name}</h3>

        {/* Always visible stats */}
        <div className="space-y-1.5">
          <StatRow label="Energy" value={dog.energy_level} color="orange" />
          <StatRow label="Friendliness" value={dog.friendliness} color="rose" />
          <StatRow label="Trainability" value={dog.trainability} color="blue" />
        </div>

        {/* Hover reveal */}
        <div className="overflow-hidden max-h-0 group-hover:max-h-24 transition-all duration-300 ease-in-out">
          <div className="pt-2 mt-2 border-t border-slate-100 space-y-1.5">
            <StatRow label="Adaptability" value={dog.adaptability} color="amber" />
            <StatRow label="Intelligence" value={dog.intelligence} color="blue" />
            <StatRow label="Playfulness" value={dog.playfulness} color="orange" />
          </div>
        </div>
      </div>
    </article>
  )
}

function StatRow({ label, value, color }) {
  return (
    <div className="flex items-center justify-between gap-2">
      <span className="text-xs text-slate-500 truncate flex-shrink-0">{label}</span>
      <StarRating value={value} color={color} />
    </div>
  )
}
