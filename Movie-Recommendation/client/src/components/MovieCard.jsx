import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Star, Play, Heart, Eye, Film } from 'lucide-react';
import { moviesAPI } from '../services/api';
import toast from 'react-hot-toast';

const MovieCard = ({ movie, showRating = false }) => {
  const [isRating, setIsRating] = useState(false);
  const [userRating, setUserRating] = useState(movie.userRating || 0);
  const [isHovered, setIsHovered] = useState(false);

  const handleRateMovie = async (rating) => {
    if (isRating) return;
    
    setIsRating(true);
    try {
      await moviesAPI.rateMovie(movie.movieId, rating);
      setUserRating(rating);
      toast.success(`Rated "${movie.title}" ${rating} stars`);
    } catch (error) {
      toast.error('Failed to rate movie');
    } finally {
      setIsRating(false);
    }
  };

  const renderStars = (rating, interactive = false, onRate = null) => {
    return (
      <div className="flex items-center space-x-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            onClick={interactive ? () => onRate(star) : undefined}
            disabled={!interactive || isRating}
            className={`${
              interactive 
                ? 'hover:scale-110 transition-transform cursor-pointer' 
                : 'cursor-default'
            } ${
              isRating ? 'opacity-50 cursor-not-allowed' : ''
            }`}
          >
            <Star
              className={`h-4 w-4 ${
                star <= rating
                  ? 'text-yellow-400 fill-current'
                  : 'text-gray-300'
              }`}
            />
          </button>
        ))}
      </div>
    );
  };

  const getGenreColor = (genre) => {
    const colors = {
      'Action': 'bg-red-100 text-red-800',
      'Adventure': 'bg-orange-100 text-orange-800',
      'Animation': 'bg-pink-100 text-pink-800',
      'Children': 'bg-purple-100 text-purple-800',
      'Comedy': 'bg-yellow-100 text-yellow-800',
      'Crime': 'bg-gray-100 text-gray-800',
      'Documentary': 'bg-green-100 text-green-800',
      'Drama': 'bg-blue-100 text-blue-800',
      'Fantasy': 'bg-indigo-100 text-indigo-800',
      'Horror': 'bg-red-100 text-red-800',
      'Mystery': 'bg-gray-100 text-gray-800',
      'Romance': 'bg-pink-100 text-pink-800',
      'Sci-Fi': 'bg-cyan-100 text-cyan-800',
      'Thriller': 'bg-purple-100 text-purple-800',
      'War': 'bg-red-100 text-red-800',
      'Western': 'bg-yellow-100 text-yellow-800',
    };
    return colors[genre] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div
      className="movie-card group"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Link to={`/movies/${movie.movieId}`}>
        {/* Movie Poster Placeholder */}
        <div className="relative mb-4 aspect-[2/3] bg-gradient-to-br from-primary-100 to-primary-200 rounded-lg overflow-hidden">
          <div className="absolute inset-0 flex items-center justify-center">
            <Film className="h-16 w-16 text-primary-400" />
          </div>
          
          {/* Hover Overlay */}
          <div className={`absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center transition-opacity duration-200 ${
            isHovered ? 'opacity-100' : 'opacity-0'
          }`}>
            <Play className="h-12 w-12 text-white" />
          </div>
          
          {/* Rating Badge */}
          {movie.userRating && (
            <div className="absolute top-2 right-2 bg-yellow-400 text-yellow-900 px-2 py-1 rounded-full text-xs font-bold flex items-center">
              <Star className="h-3 w-3 mr-1" />
              {movie.userRating}
            </div>
          )}
        </div>

        {/* Movie Info */}
        <div className="space-y-2">
          <h3 className="font-semibold text-gray-900 line-clamp-2 group-hover:text-primary-600 transition-colors">
            {movie.title}
          </h3>
          
          {/* Genres */}
          {movie.genres && movie.genres.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {movie.genres.slice(0, 2).map((genre) => (
                <span
                  key={genre}
                  className={`px-2 py-1 rounded-full text-xs font-medium ${getGenreColor(genre)}`}
                >
                  {genre}
                </span>
              ))}
              {movie.genres.length > 2 && (
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                  +{movie.genres.length - 2}
                </span>
              )}
            </div>
          )}

          {/* User Rating */}
          {showRating && (
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Your Rating:</span>
                <span className="text-sm font-medium">
                  {userRating ? `${userRating}/5` : 'Not rated'}
                </span>
              </div>
              {renderStars(userRating, true, handleRateMovie)}
            </div>
          )}

          {/* Quick Actions */}
          <div className="flex items-center justify-between pt-2">
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Eye className="h-4 w-4" />
              <span>View Details</span>
            </div>
            <Heart className="h-4 w-4 text-gray-400 hover:text-red-500 transition-colors cursor-pointer" />
          </div>
        </div>
      </Link>
    </div>
  );
};

export default MovieCard;
