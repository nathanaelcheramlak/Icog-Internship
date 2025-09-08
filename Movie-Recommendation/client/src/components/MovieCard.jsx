import { useState } from "react";
import {
	StarIcon,
	CalendarIcon,
	ClockIcon,
	FilmIcon,
} from "@heroicons/react/24/solid";

const MovieCard = ({ movie, onRate }) => {
	const [userRating, setUserRating] = useState(movie.userRating || 0);
	const [hoverRating, setHoverRating] = useState(0);

	const handleRating = (rating) => {
		setUserRating(rating);
		if (onRate) {
			onRate(movie.id, rating);
		}
	};

	const renderStars = () => {
		return [1, 2, 3, 4, 5].map((star) => (
			<button
				key={star}
				className="focus:outline-none transition-transform duration-150 hover:scale-110"
				onClick={() => handleRating(star)}
				onMouseEnter={() => setHoverRating(star)}
				onMouseLeave={() => setHoverRating(0)}
				aria-label={`Rate ${star} stars`}
			>
				<StarIcon
					className={`w-7 h-7 ${
						star <= (hoverRating || userRating)
							? "text-yellow-400 fill-current"
							: "text-gray-300"
					}`}
				/>
			</button>
		));
	};

	return (
		<div className="bg-white rounded-2xl overflow-hidden shadow-lg transition-all duration-300 hover:shadow-xl h-full flex flex-col">
			<div className="relative">
				<img
					src={movie.poster}
					alt={movie.title}
					className="w-full h-72 object-cover"
				/>
				<div className="absolute top-4 right-4 bg-black bg-opacity-70 text-yellow-400 py-1 px-3 rounded-full flex items-center">
					<StarIcon className="w-5 h-5 mr-1" />
					<span className="font-bold">{movie.rating.toFixed(1)}</span>
				</div>
			</div>

			<div className="p-6 flex flex-col flex-grow">
				<div className="flex justify-between items-start mb-3">
					<h2 className="text-2xl font-bold text-gray-800">{movie.title}</h2>
					<span className="text-gray-500 flex items-center">
						<CalendarIcon className="w-5 h-5 mr-1" />
						{movie.year}
					</span>
				</div>

				<div className="flex items-center text-gray-600 mb-4">
					<ClockIcon className="w-5 h-5 mr-1" />
					<span className="mr-4">{movie.duration}</span>
					<FilmIcon className="w-5 h-5 mr-1" />
					<span>{movie.genre.join(" • ")}</span>
				</div>

				<p className="text-gray-600 mb-6 leading-relaxed flex-grow">
					{movie.description || "No description available."}
				</p>

				<div className="flex flex-wrap gap-2 mb-6">
					{movie.genre.map((genre, index) => (
						<span
							key={index}
							className="bg-blue-100 text-blue-800 text-xs font-medium px-3 py-1 rounded-full"
						>
							{genre}
						</span>
					))}
				</div>

				<div className="border-t pt-4 mt-auto">
					<h3 className="text-lg font-semibold text-gray-800 mb-2">
						Rate this movie
					</h3>
					<div className="flex items-center">
						<div className="flex mr-4">{renderStars()}</div>
						<span className="text-gray-700 font-medium">
							{userRating > 0 ? `${userRating}.0` : "Not rated"}
						</span>
					</div>
				</div>
			</div>
		</div>
	);
};

export default MovieCard;
