import { useState, useEffect, useRef, useCallback } from "react"
import { fetchDogs } from "../api/dogs"
import FilterPanel, { countActiveFilters } from "../components/filters/FilterPanel"
import DogGrid from "../components/home/DogGrid"
import SortBar from "../components/home/SortBar"

const ALL_RANGE_ATTRS = [
  "apartment_friendly", "good_for_novice", "sensitivity", "tolerates_alone",
  "tolerates_cold", "tolerates_hot", "friendliness", "affectionate_family",
  "kid_friendly", "dog_friendly", "stranger_friendly", "health_grooming",
  "shedding", "drooling", "easy_groom", "general_health", "weight_gain_potential",
  "size_score", "trainability", "easy_train", "intelligence", "mouthiness",
  "prey_drive", "barking", "wanderlust", "physical_needs", "energy_level",
  "intensity", "exercise_needs", "playfulness",
]

const DEFAULT_RANGES = Object.fromEntries(ALL_RANGE_ATTRS.map((a) => [a, [1, 5]]))

export default function HomePage() {
  const [dogs, setDogs] = useState([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [breedGroups, setBreedGroups] = useState([])
  const [sizes, setSizes] = useState([])
  const [ranges, setRanges] = useState(DEFAULT_RANGES)

  const [sortBy, setSortBy] = useState("breed_name")
  const [sortOrder, setSortOrder] = useState("asc")

  const [mobileFilterOpen, setMobileFilterOpen] = useState(false)

  const debounceRef = useRef(null)

  const load = useCallback(async (filters, sort) => {
    setLoading(true)
    setError(null)
    try {
      const data = await fetchDogs(filters, sort)
      setDogs(data.items)
      setTotal(data.total)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      load({ breedGroups, sizes, ranges }, { sortBy, sortOrder })
    }, 300)
    return () => clearTimeout(debounceRef.current)
  }, [breedGroups, sizes, ranges, sortBy, sortOrder, load])

  function toggleBreedGroup(g) {
    setBreedGroups((prev) =>
      prev.includes(g) ? prev.filter((x) => x !== g) : [...prev, g]
    )
  }

  function toggleSize(s) {
    setSizes((prev) =>
      prev.includes(s) ? prev.filter((x) => x !== s) : [...prev, s]
    )
  }

  function handleRangeChange(attr, val) {
    setRanges((prev) => ({ ...prev, [attr]: val }))
  }

  function clearAll() {
    setBreedGroups([])
    setSizes([])
    setRanges(DEFAULT_RANGES)
  }

  const activeCount = countActiveFilters(breedGroups, sizes, ranges)

  return (
    <div className="max-w-screen-xl mx-auto px-4 py-6">
      {/* Hero heading */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Find Your Perfect Dog Breed</h1>
        <p className="text-slate-500 text-sm mt-1">
          Explore {total > 0 ? total : "391"} breeds and find the one that fits your lifestyle
        </p>
      </div>

      <div className="flex gap-6">
        {/* Sidebar filter — desktop */}
        <div className="hidden lg:block w-72 flex-shrink-0">
          <div className="sticky top-20">
            <FilterPanel
              breedGroups={breedGroups}
              sizes={sizes}
              ranges={ranges}
              onBreedGroupChange={toggleBreedGroup}
              onSizeChange={toggleSize}
              onRangeChange={handleRangeChange}
              onClear={clearAll}
            />
          </div>
        </div>

        {/* Main content */}
        <div className="flex-1 min-w-0">
          <SortBar
            total={total}
            sortBy={sortBy}
            sortOrder={sortOrder}
            onSortChange={(by, order) => { setSortBy(by); setSortOrder(order) }}
          />
          <DogGrid dogs={dogs} loading={loading} error={error} />
        </div>
      </div>

      {/* Mobile filter button */}
      <button
        onClick={() => setMobileFilterOpen(true)}
        className="lg:hidden fixed bottom-6 right-6 bg-orange-500 hover:bg-orange-600 text-white
          rounded-full px-4 py-3 shadow-lg flex items-center gap-2 text-sm font-semibold z-40 transition-colors"
      >
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-.293.707L13 13.414V19a1 1 0 01-.553.894l-4 2A1 1 0 017 21v-7.586L3.293 6.707A1 1 0 013 6V4z"
          />
        </svg>
        Filters
        {activeCount > 0 && (
          <span className="bg-white text-orange-500 text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center">
            {activeCount}
          </span>
        )}
      </button>

      {/* Mobile filter drawer */}
      {mobileFilterOpen && (
        <div className="lg:hidden fixed inset-0 z-50 flex">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setMobileFilterOpen(false)}
          />
          <div className="relative ml-auto w-80 max-w-full bg-slate-50 h-full overflow-y-auto shadow-xl">
            <div className="flex items-center justify-between p-4 border-b border-slate-200 bg-white">
              <span className="font-semibold text-slate-800">Filters</span>
              <button
                onClick={() => setMobileFilterOpen(false)}
                className="text-slate-400 hover:text-slate-600"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="p-4">
              <FilterPanel
                breedGroups={breedGroups}
                sizes={sizes}
                ranges={ranges}
                onBreedGroupChange={toggleBreedGroup}
                onSizeChange={toggleSize}
                onRangeChange={handleRangeChange}
                onClear={clearAll}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
