import { Routes, Route } from "react-router-dom"
import Navbar from "./components/Navbar"
import HomePage from "./pages/HomePage"
import DogDetailPage from "./pages/DogDetailPage"

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/dogs/:id" element={<DogDetailPage />} />
      </Routes>
    </div>
  )
}
