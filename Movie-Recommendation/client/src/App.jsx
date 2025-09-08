import { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import SearchBar from "./components/SearchBox";
import MoviesContainer from "./components/MovieContainer";

const App = () => {
	const [movies, setMovies] = useState([]);
	const [userRatings, setUserRatings] = useState({});
	const [activeTab, setActiveTab] = useState("trending");
	const [trendingMovies, setTrendingMovies] = useState([]);

	// Load trending movies on component mount
	useEffect(() => {
		// Simulated API call for trending movies
		const loadTrendingMovies = async () => {
			try {
				// Mock data - replace with actual API call
				const mockTrending = [
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
						id: 3,
						title: "The Shawshank Redemption",
						description:
							"Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
						rating: 9.3,
						poster:
							"https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_FMjpg_UX1000_.jpg",
						genre: ["Drama"],
						year: 1994,
						duration: "2h 22m",
						userRating: 0,
					},
					{
						id: 4,
						title: "Pulp Fiction",
						description:
							"The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
						rating: 8.9,
						poster:
							"https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzJjNDymmYzYzYmM3XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
						genre: ["Crime", "Drama"],
						year: 1994,
						duration: "2h 34m",
						userRating: 0,
					},
				];

				setTrendingMovies(mockTrending);
			} catch (error) {
				console.error("Failed to load trending movies:", error);
			}
		};

		loadTrendingMovies();
	}, []);

	const handleSearchResults = (searchResults) => {
		// Add any existing user ratings to the search results
		const ratedResults = searchResults.map((movie) => ({
			...movie,
			userRating: userRatings[movie.id] || 0,
		}));

		setMovies(ratedResults);
	};

	const handleRateMovie = (movieId, rating) => {
		// Update user ratings
		setUserRatings((prev) => ({
			...prev,
			[movieId]: rating,
		}));

		// Update movies with the new rating
		setMovies((prevMovies) =>
			prevMovies.map((movie) =>
				movie.id === movieId ? { ...movie, userRating: rating } : movie
			)
		);

		// Update trending movies with the new rating
		setTrendingMovies((prevMovies) =>
			prevMovies.map((movie) =>
				movie.id === movieId ? { ...movie, userRating: rating } : movie
			)
		);
	};

	const handleLogout = () => {
		// Implement logout logic here
		alert("Logout functionality would be implemented here");
	};

	// Get movies to display based on active tab
	const getMoviesToDisplay = () => {
		switch (activeTab) {
			case "my-ratings":
				// Filter movies that have been rated by the user
				return Object.keys(userRatings).length > 0
					? [...movies, ...trendingMovies]
							.filter((movie) => userRatings[movie.id] > 0)
							.filter(
								(movie, index, self) =>
									index === self.findIndex((m) => m.id === movie.id)
							)
					: [];

			case "recommendations":
				// For demo purposes, show highly rated movies as recommendations
				return trendingMovies.filter((movie) => movie.rating >= 8.5);

			case "trending":
			default:
				return trendingMovies;
		}
	};

	return (
		<div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-100 py-12 px-4">
			<div className="max-w-7xl mx-auto">
				<div className="text-center mb-6">
					<h1 className="text-4xl font-bold text-gray-800 mb-3">
						Movie Search App
					</h1>
					<p className="text-gray-600">
						Discover, search, and rate your favorite movies
					</p>
				</div>

				<Navbar
					activeTab={activeTab}
					setActiveTab={setActiveTab}
					onLogout={handleLogout}
				/>

				{activeTab === "trending" && (
					<>
						<SearchBar
							onSearchResults={handleSearchResults}
							placeholder="Search for movies by title..."
						/>

						<h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
							{movies.length > 0 ? "Search Results" : "Trending Movies"}
						</h2>
					</>
				)}

				{activeTab === "my-ratings" && (
					<h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
						My Rated Movies
					</h2>
				)}

				{activeTab === "recommendations" && (
					<h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
						Recommended For You
					</h2>
				)}

				<MoviesContainer
					movies={
						movies.length > 0 && activeTab === "trending"
							? movies
							: getMoviesToDisplay()
					}
					onRateMovie={handleRateMovie}
				/>
			</div>
		</div>
	);
};

export default App;
