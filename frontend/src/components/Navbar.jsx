import { Link } from "react-router-dom"

export default function Navbar() {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-screen-xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 text-slate-800 no-underline">
          <span className="text-2xl">🐾</span>
          <span className="font-bold text-xl tracking-tight text-orange-500">PawFinder</span>
        </Link>
        <nav className="flex items-center gap-6 text-sm text-slate-500">
          <Link to="/" className="hover:text-orange-500 transition-colors no-underline">
            All Breeds
          </Link>
        </nav>
      </div>
    </header>
  )
}
