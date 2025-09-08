import {
	FireIcon,
	StarIcon,
	HeartIcon,
	ArrowRightOnRectangleIcon,
} from "@heroicons/react/24/solid";

const Navbar = ({ activeTab, setActiveTab, onLogout }) => {
	return (
		<nav className="bg-white shadow-lg rounded-full mx-auto max-w-2xl mb-10">
			<div className="flex justify-center items-center p-2">
				<button
					className={`flex items-center px-4 py-2 rounded-full mx-1 transition-all duration-200 ${
						activeTab === "trending"
							? "bg-blue-600 text-white"
							: "text-gray-600 hover:bg-gray-100"
					}`}
					onClick={() => setActiveTab("trending")}
				>
					<FireIcon className="w-5 h-5 mr-2" />
					Trending
				</button>
				<button
					className={`flex items-center px-4 py-2 rounded-full mx-1 transition-all duration-200 ${
						activeTab === "my-ratings"
							? "bg-blue-600 text-white"
							: "text-gray-600 hover:bg-gray-100"
					}`}
					onClick={() => setActiveTab("my-ratings")}
				>
					<StarIcon className="w-5 h-5 mr-2" />
					My Ratings
				</button>
				<button
					className={`flex items-center px-4 py-2 rounded-full mx-1 transition-all duration-200 ${
						activeTab === "recommendations"
							? "bg-blue-600 text-white"
							: "text-gray-600 hover:bg-gray-100"
					}`}
					onClick={() => setActiveTab("recommendations")}
				>
					<HeartIcon className="w-5 h-5 mr-2" />
					Recommendations
				</button>
				<button
					className="flex items-center px-4 py-2 rounded-full mx-1 text-gray-600 hover:bg-gray-100 transition-all duration-200"
					onClick={onLogout}
				>
					<ArrowRightOnRectangleIcon className="w-5 h-5 mr-2" />
					Logout
				</button>
			</div>
		</nav>
	);
};

export default Navbar;
