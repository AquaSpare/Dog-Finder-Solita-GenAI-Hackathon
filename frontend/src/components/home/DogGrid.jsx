import DogCard from "./DogCard"
import LoadingSpinner from "../shared/LoadingSpinner"

export default function DogGrid({ dogs, loading, error }) {
  if (loading) return <LoadingSpinner size="lg" />

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-slate-400">
        <span className="text-5xl mb-3">⚠️</span>
        <p className="text-lg font-medium">Failed to load breeds</p>
        <p className="text-sm mt-1">{error}</p>
      </div>
    )
  }

  if (!dogs.length) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-slate-400">
        <span className="text-5xl mb-3">🔍</span>
        <p className="text-lg font-medium">No breeds match your filters</p>
        <p className="text-sm mt-1">Try adjusting your filter settings</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-4 gap-4">
      {dogs.map((dog) => (
        <DogCard key={dog.id} dog={dog} />
      ))}
    </div>
  )
}
