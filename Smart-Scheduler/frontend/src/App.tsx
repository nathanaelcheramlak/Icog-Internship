import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import SchedulePage from "./pages/Schedule";
import TaskGraph from "./components/TaskGraph";

export default function App() {
	return (
		<BrowserRouter>
			<nav className="p-4 bg-gray-100 flex gap-4">
				<Link to="/">Tasks</Link>
				<Link to="/schedule">Schedule</Link>
			</nav>
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/schedule" element={<SchedulePage />} />
				<Route path="/graph" element={<TaskGraph />} />
			</Routes>
		</BrowserRouter>
	);
}
