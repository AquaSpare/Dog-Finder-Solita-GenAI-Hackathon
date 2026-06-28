const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000"

const RANGE_ATTR_MAP = {
  apartment_friendly: ["min_apartment_friendly", "max_apartment_friendly"],
  good_for_novice: ["min_good_for_novice", "max_good_for_novice"],
  sensitivity: ["min_sensitivity", "max_sensitivity"],
  tolerates_alone: ["min_tolerates_alone", "max_tolerates_alone"],
  tolerates_cold: ["min_tolerates_cold", "max_tolerates_cold"],
  tolerates_hot: ["min_tolerates_hot", "max_tolerates_hot"],
  friendliness: ["min_friendliness", "max_friendliness"],
  affectionate_family: ["min_affectionate_family", "max_affectionate_family"],
  kid_friendly: ["min_kid_friendly", "max_kid_friendly"],
  dog_friendly: ["min_dog_friendly", "max_dog_friendly"],
  stranger_friendly: ["min_stranger_friendly", "max_stranger_friendly"],
  health_grooming: ["min_health_grooming", "max_health_grooming"],
  shedding: ["min_shedding", "max_shedding"],
  drooling: ["min_drooling", "max_drooling"],
  easy_groom: ["min_easy_groom", "max_easy_groom"],
  general_health: ["min_general_health", "max_general_health"],
  weight_gain_potential: ["min_weight_gain_potential", "max_weight_gain_potential"],
  size_score: ["min_size_score", "max_size_score"],
  trainability: ["min_trainability", "max_trainability"],
  easy_train: ["min_easy_train", "max_easy_train"],
  intelligence: ["min_intelligence", "max_intelligence"],
  mouthiness: ["min_mouthiness", "max_mouthiness"],
  prey_drive: ["min_prey_drive", "max_prey_drive"],
  barking: ["min_barking", "max_barking"],
  wanderlust: ["min_wanderlust", "max_wanderlust"],
  physical_needs: ["min_physical_needs", "max_physical_needs"],
  energy_level: ["min_energy_level", "max_energy_level"],
  intensity: ["min_intensity", "max_intensity"],
  exercise_needs: ["min_exercise_needs", "max_exercise_needs"],
  playfulness: ["min_playfulness", "max_playfulness"],
}

export function buildQuery(filters = {}, sort = {}) {
  const params = new URLSearchParams()

  if (filters.breedGroups?.length) {
    params.set("breed_group", filters.breedGroups[0])
  }
  if (filters.sizes?.length === 1) {
    params.set("size", filters.sizes[0])
  }

  if (filters.ranges) {
    for (const [attr, [min, max]] of Object.entries(filters.ranges)) {
      const keys = RANGE_ATTR_MAP[attr]
      if (!keys) continue
      if (min !== 1) params.set(keys[0], min)
      if (max !== 5) params.set(keys[1], max)
    }
  }

  if (sort.sortBy) params.set("sort_by", sort.sortBy)
  if (sort.sortOrder) params.set("sort_order", sort.sortOrder)

  return params
}

export async function fetchDogs(filters = {}, sort = {}) {
  const params = buildQuery(filters, sort)
  const res = await fetch(`${BASE}/dogs?${params}`)
  if (!res.ok) throw new Error("Failed to fetch dogs")
  return res.json()
}

export async function fetchDog(id) {
  const res = await fetch(`${BASE}/dogs/${id}`)
  if (!res.ok) throw new Error("Dog not found")
  return res.json()
}

export async function chatWithDog(id, question, sessionId = null) {
  const res = await fetch(`${BASE}/dogs/${id}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, session_id: sessionId }),
  })
  if (!res.ok) throw new Error("Chat request failed")
  return res.json()
}
