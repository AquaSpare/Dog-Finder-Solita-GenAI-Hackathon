import { useState } from "react"
import RangeSlider from "./RangeSlider"

const ATTR_LABELS = {
  apartment_friendly: "Apartment Living",
  good_for_novice: "Good For Novice Owners",
  sensitivity: "Sensitivity Level",
  tolerates_alone: "Tolerates Being Alone",
  tolerates_cold: "Tolerates Cold Weather",
  tolerates_hot: "Tolerates Hot Weather",
  friendliness: "All Around Friendliness",
  affectionate_family: "Affectionate With Family",
  kid_friendly: "Kid-Friendly",
  dog_friendly: "Dog Friendly",
  stranger_friendly: "Friendly Toward Strangers",
  health_grooming: "Health & Grooming Needs",
  shedding: "Amount Of Shedding",
  drooling: "Drooling Potential",
  easy_groom: "Easy To Groom",
  general_health: "General Health",
  weight_gain_potential: "Potential For Weight Gain",
  size_score: "Size",
  trainability: "Trainability",
  easy_train: "Easy To Train",
  intelligence: "Intelligence",
  mouthiness: "Potential For Mouthiness",
  prey_drive: "Prey Drive",
  barking: "Tendency To Bark Or Howl",
  wanderlust: "Wanderlust Potential",
  physical_needs: "Physical Needs",
  energy_level: "Energy Level",
  intensity: "Intensity",
  exercise_needs: "Exercise Needs",
  playfulness: "Potential For Playfulness",
}

export { ATTR_LABELS }

export default function CategorySection({ title, attrs, ranges, onRangeChange }) {
  const [open, setOpen] = useState(false)

  const activeCount = attrs.filter(
    (a) => ranges[a] && (ranges[a][0] !== 1 || ranges[a][1] !== 5)
  ).length

  return (
    <div className="border-b border-slate-100 last:border-0">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between py-3 text-sm font-medium text-slate-700 hover:text-orange-500 transition-colors"
      >
        <span>{title}</span>
        <span className="flex items-center gap-2">
          {activeCount > 0 && (
            <span className="bg-orange-100 text-orange-600 text-xs font-semibold px-1.5 py-0.5 rounded-full">
              {activeCount}
            </span>
          )}
          <svg
            className={`w-4 h-4 transition-transform text-slate-400 ${open ? "rotate-180" : ""}`}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </span>
      </button>

      {open && (
        <div className="pb-3 space-y-4">
          {attrs.map((attr) => (
            <div key={attr}>
              <div className="text-xs text-slate-500 mb-1.5">{ATTR_LABELS[attr]}</div>
              <RangeSlider
                min={ranges[attr]?.[0] ?? 1}
                max={ranges[attr]?.[1] ?? 5}
                onChange={(val) => onRangeChange(attr, val)}
              />
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
