import React, { useState } from "react";
import { MagnifyingGlassIcon } from "@heroicons/react/24/solid";

const SearchBar = ({ onSearchResults, placeholder }) => {
	const [query, setQuery] = useState("");
	const [isLoading, setIsLoading] = useState(false);
	const [error, setError] = useState("");

	const handleSearch = async (searchQuery) => {
		if (!searchQuery.trim()) {
			setError("Please enter a search term");
			return;
		}

		setIsLoading(true);
		setError("");

		try {
			// Simulated API call - replace with actual API
			await new Promise((resolve) => setTimeout(resolve, 1000));

			// Mock data - replace with actual API response
			const mockResults = [
				{
					id: 1,
					title: "Inception",
					description:
						"A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
					rating: 8.8,
					poster:
						"https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_FMjpg_UX1000_.jpg",
					genre: ["Action", "Sci-Fi", "Thriller"],
					year: 2010,
					duration: "2h 28m",
					userRating: 0,
				},
				{
					id: 2,
					title: "The Dark Knight",
					description:
						"When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
					rating: 9.0,
					poster:
						"https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_FMjpg_UX1000_.jpg",
					genre: ["Action", "Crime", "Drama"],
					year: 2008,
					duration: "2h 32m",
					userRating: 0,
				},
			];

			onSearchResults(mockResults);
		} catch (err) {
			setError("Failed to search movies. Please try again.");
			console.error("Search error:", err);
		} finally {
			setIsLoading(false);
		}
	};

	const handleSubmit = (e) => {
		e.preventDefault();
		handleSearch(query);
	};

	return (
		<div className="w-full max-w-2xl mx-auto mb-10">
			<form onSubmit={handleSubmit}>
				<div className="relative">
					<div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
						<MagnifyingGlassIcon className="w-5 h-5 text-gray-400" />
					</div>
					<input
						type="text"
						className="w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500"
						placeholder={placeholder}
						value={query}
						onChange={(e) => setQuery(e.target.value)}
						disabled={isLoading}
					/>
					<button
						type="submit"
						className="text-white absolute right-2.5 bottom-2.5 bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
						disabled={isLoading}
					>
						{isLoading ? "Searching..." : "Search"}
					</button>
				</div>
			</form>

			{error && (
				<div className="mt-2 text-red-500 text-sm text-center">{error}</div>
			)}
		</div>
	);
};

export default SearchBar;
