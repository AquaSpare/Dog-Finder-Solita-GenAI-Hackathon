export default function StarRating({ value, color = "orange" }) {
  const colorMap = {
    orange: "bg-orange-400",
    rose: "bg-rose-400",
    amber: "bg-amber-400",
    emerald: "bg-emerald-400",
    blue: "bg-blue-400",
    slate: "bg-slate-300",
  }
  const filled = colorMap[color] || colorMap.orange

  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((i) => (
        <div
          key={i}
          className={`w-2.5 h-2.5 rounded-full ${i <= Math.round(value ?? 0) ? filled : "bg-slate-200"}`}
        />
      ))}
    </div>
  )
}
