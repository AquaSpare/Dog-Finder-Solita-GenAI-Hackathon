export default function LoadingSpinner({ size = "md" }) {
  const sizes = { sm: "w-5 h-5", md: "w-8 h-8", lg: "w-12 h-12" }
  return (
    <div className="flex justify-center items-center py-12">
      <div
        className={`${sizes[size]} border-4 border-slate-200 border-t-orange-500 rounded-full animate-spin`}
      />
    </div>
  )
}
