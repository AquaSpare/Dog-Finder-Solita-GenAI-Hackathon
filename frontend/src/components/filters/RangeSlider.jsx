import { useRef } from "react"

export default function RangeSlider({ min, max, onChange }) {
  const trackRef = useRef(null)

  const pct = (v) => ((v - 1) / 4) * 100

  function handleMin(e) {
    const val = parseInt(e.target.value)
    onChange([Math.min(val, max), max])
  }

  function handleMax(e) {
    const val = parseInt(e.target.value)
    onChange([min, Math.max(val, min)])
  }

  const leftPct = pct(min)
  const rightPct = pct(max)

  return (
    <div className="px-1">
      <div className="relative h-5 flex items-center" ref={trackRef}>
        {/* Track background */}
        <div className="absolute w-full h-1.5 bg-slate-200 rounded-full" />
        {/* Active track fill */}
        <div
          className="absolute h-1.5 bg-orange-400 rounded-full"
          style={{ left: `${leftPct}%`, right: `${100 - rightPct}%` }}
        />
        {/* Min handle */}
        <input
          type="range"
          min={1}
          max={5}
          step={1}
          value={min}
          onChange={handleMin}
          className="absolute w-full appearance-none bg-transparent cursor-pointer
            [&::-webkit-slider-thumb]:appearance-none
            [&::-webkit-slider-thumb]:w-4
            [&::-webkit-slider-thumb]:h-4
            [&::-webkit-slider-thumb]:rounded-full
            [&::-webkit-slider-thumb]:bg-white
            [&::-webkit-slider-thumb]:border-2
            [&::-webkit-slider-thumb]:border-orange-500
            [&::-webkit-slider-thumb]:shadow-sm
            [&::-webkit-slider-thumb]:cursor-pointer
            [&::-webkit-slider-track]:appearance-none
            [&::-webkit-slider-track]:bg-transparent
            [&::-moz-range-thumb]:w-4
            [&::-moz-range-thumb]:h-4
            [&::-moz-range-thumb]:rounded-full
            [&::-moz-range-thumb]:bg-white
            [&::-moz-range-thumb]:border-2
            [&::-moz-range-thumb]:border-orange-500
            [&::-moz-range-thumb]:cursor-pointer"
          style={{ zIndex: min === max ? 5 : 3 }}
        />
        {/* Max handle */}
        <input
          type="range"
          min={1}
          max={5}
          step={1}
          value={max}
          onChange={handleMax}
          className="absolute w-full appearance-none bg-transparent cursor-pointer
            [&::-webkit-slider-thumb]:appearance-none
            [&::-webkit-slider-thumb]:w-4
            [&::-webkit-slider-thumb]:h-4
            [&::-webkit-slider-thumb]:rounded-full
            [&::-webkit-slider-thumb]:bg-white
            [&::-webkit-slider-thumb]:border-2
            [&::-webkit-slider-thumb]:border-orange-500
            [&::-webkit-slider-thumb]:shadow-sm
            [&::-webkit-slider-thumb]:cursor-pointer
            [&::-webkit-slider-track]:appearance-none
            [&::-webkit-slider-track]:bg-transparent
            [&::-moz-range-thumb]:w-4
            [&::-moz-range-thumb]:h-4
            [&::-moz-range-thumb]:rounded-full
            [&::-moz-range-thumb]:bg-white
            [&::-moz-range-thumb]:border-2
            [&::-moz-range-thumb]:border-orange-500
            [&::-moz-range-thumb]:cursor-pointer"
          style={{ zIndex: 4 }}
        />
      </div>
      <div className="flex justify-between text-xs text-slate-400 mt-1">
        <span>{min}</span>
        <span>{max}</span>
      </div>
    </div>
  )
}
