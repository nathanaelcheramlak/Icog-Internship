import { FilmIcon } from "@heroicons/react/24/solid";
import MovieCard from "./MovieCard";

const MoviesContainer = ({ movies, onRateMovie }) => {
	if (movies.length === 0) {
		return (
			<div className="text-center py-16 bg-white rounded-lg shadow">
				<FilmIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
				<h3 className="text-xl font-semibold text-gray-500">No movies found</h3>
				<p className="text-gray-400">Try searching for a movie title</p>
			</div>
		);
	}

	return (
		<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
			{movies.map((movie) => (
				<MovieCard key={movie.id} movie={movie} onRate={onRateMovie} />
			))}
		</div>
	);
};

export default MoviesContainer;
