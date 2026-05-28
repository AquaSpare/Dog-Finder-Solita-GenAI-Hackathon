import { useState, useEffect } from "react"
import { useParams } from "react-router-dom"
import { fetchDog } from "../api/dogs"
import HeroSection from "../components/detail/HeroSection"
import StatCategory from "../components/detail/StatCategory"
import ChatWindow from "../components/detail/ChatWindow"
import LoadingSpinner from "../components/shared/LoadingSpinner"

const STAT_CATEGORIES = [
  {
    title: "Adaptability",
    category: "adaptability",
    attrs: [
      { key: "adaptability", label: "Overall Adaptability" },
      { key: "apartment_friendly", label: "Apartment Living" },
      { key: "good_for_novice", label: "Good For Novice Owners" },
      { key: "sensitivity", label: "Sensitivity Level" },
      { key: "tolerates_alone", label: "Tolerates Being Alone" },
      { key: "tolerates_cold", label: "Tolerates Cold Weather" },
      { key: "tolerates_hot", label: "Tolerates Hot Weather" },
    ],
  },
  {
    title: "Friendliness",
    category: "friendliness",
    attrs: [
      { key: "friendliness", label: "All Around Friendliness" },
      { key: "affectionate_family", label: "Affectionate With Family" },
      { key: "kid_friendly", label: "Kid-Friendly" },
      { key: "dog_friendly", label: "Dog Friendly" },
      { key: "stranger_friendly", label: "Friendly Toward Strangers" },
    ],
  },
  {
    title: "Health & Grooming",
    category: "health",
    attrs: [
      { key: "health_grooming", label: "Health & Grooming Needs" },
      { key: "shedding", label: "Amount Of Shedding" },
      { key: "drooling", label: "Drooling Potential" },
      { key: "easy_groom", label: "Easy To Groom" },
      { key: "general_health", label: "General Health" },
      { key: "weight_gain_potential", label: "Potential For Weight Gain" },
    ],
  },
  {
    title: "Trainability",
    category: "trainability",
    attrs: [
      { key: "trainability", label: "Trainability" },
      { key: "easy_train", label: "Easy To Train" },
      { key: "intelligence", label: "Intelligence" },
      { key: "mouthiness", label: "Potential For Mouthiness" },
      { key: "prey_drive", label: "Prey Drive" },
      { key: "barking", label: "Tendency To Bark Or Howl" },
      { key: "wanderlust", label: "Wanderlust Potential" },
    ],
  },
  {
    title: "Physical Needs",
    category: "physical",
    attrs: [
      { key: "physical_needs", label: "Physical Needs" },
      { key: "energy_level", label: "Energy Level" },
      { key: "intensity", label: "Intensity" },
      { key: "exercise_needs", label: "Exercise Needs" },
      { key: "playfulness", label: "Potential For Playfulness" },
    ],
  },
]

export default function DogDetailPage() {
  const { id } = useParams()
  const [dog, setDog] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    fetchDog(id)
      .then(setDog)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return (
    <div className="max-w-screen-xl mx-auto px-4 py-12">
      <LoadingSpinner size="lg" />
    </div>
  )

  if (error || !dog) return (
    <div className="max-w-screen-xl mx-auto px-4 py-12 text-center text-slate-400">
      <p className="text-5xl mb-3">🐕</p>
      <p className="text-lg font-medium">Breed not found</p>
    </div>
  )

  return (
    <div className="max-w-screen-xl mx-auto px-4 py-6">
      <HeroSection dog={dog} />

      {/* Stats + Chat */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Stats — 2 cols on lg */}
        <div className="lg:col-span-2 space-y-4">
          <div className="grid sm:grid-cols-2 gap-4">
            {STAT_CATEGORIES.map((cat) => (
              <StatCategory
                key={cat.title}
                title={cat.title}
                attrs={cat.attrs}
                dog={dog}
                category={cat.category}
              />
            ))}
          </div>
        </div>

        {/* Chat */}
        <div className="lg:col-span-1">
          <div className="sticky top-20">
            <ChatWindow dogId={dog.id} dogName={dog.breed_name} />
          </div>
        </div>
      </div>
    </div>
  )
}
