import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { moviesAPI, recommendationsAPI } from '../services/api';
import { 
  Star, 
  Calendar, 
  Clock, 
  Tag, 
  ArrowLeft,
  Heart,
  Share2,
  Play,
  ThumbsUp,
  ThumbsDown
} from 'lucide-react';
import MovieCard from '../components/MovieCard';
import toast from 'react-hot-toast';

const MovieDetail = () => {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [similarMovies, setSimilarMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [rating, setRating] = useState(0);
  const [isRating, setIsRating] = useState(false);
  const [explanation, setExplanation] = useState(null);
  const [showExplanation, setShowExplanation] = useState(false);

  useEffect(() => {
    loadMovieDetails();
  }, [id]);

  const loadMovieDetails = async () => {
    try {
      setLoading(true);
      
      // Load movie details
      const movieResponse = await moviesAPI.getMovie(id);
      const movieData = movieResponse.data.movie;
      setMovie(movieData);
      setRating(movieData.userRating || 0);

      // Load similar movies
      const similarResponse = await recommendationsAPI.getRecommendations({
        method: 'content_based',
        movie_id: id,
        limit: 6
      });
      setSimilarMovies(similarResponse.data.recommended_movies || []);

    } catch (error) {
      console.error('Error loading movie details:', error);
      toast.error('Failed to load movie details');
    } finally {
      setLoading(false);
    }
  };

  const handleRateMovie = async (newRating) => {
    if (isRating) return;
    
    setIsRating(true);
    try {
      await moviesAPI.rateMovie(id, newRating);
      setRating(newRating);
      toast.success(`Rated "${movie.title}" ${newRating} stars`);
    } catch (error) {
      toast.error('Failed to rate movie');
    } finally {
      setIsRating(false);
    }
  };

  const handleGetExplanation = async () => {
    try {
      const response = await recommendationsAPI.explainRecommendation(id);
      setExplanation(response.data.explanation);
      setShowExplanation(true);
    } catch (error) {
      toast.error('Failed to get explanation');
    }
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

  const renderStars = (currentRating, interactive = false) => {
    return (
      <div className="flex items-center space-x-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            onClick={interactive ? () => handleRateMovie(star) : undefined}
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
              className={`h-6 w-6 ${
                star <= currentRating
                  ? 'text-yellow-400 fill-current'
                  : 'text-gray-300'
              }`}
            />
          </button>
        ))}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!movie) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Movie not found</h2>
          <Link to="/movies" className="btn-primary">
            Back to Movies
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Back Button */}
      <Link 
        to="/movies" 
        className="inline-flex items-center space-x-2 text-primary-600 hover:text-primary-700 transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        <span>Back to Movies</span>
      </Link>

      {/* Movie Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-2xl p-8 text-white">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Movie Poster */}
          <div className="flex-shrink-0">
            <div className="w-64 h-96 bg-gradient-to-br from-primary-100 to-primary-200 rounded-lg overflow-hidden">
              <div className="w-full h-full flex items-center justify-center">
                <Play className="h-16 w-16 text-primary-400" />
              </div>
            </div>
          </div>

          {/* Movie Info */}
          <div className="flex-1 space-y-4">
            <div>
              <h1 className="text-4xl font-bold mb-2">{movie.title}</h1>
              <div className="flex items-center space-x-4 text-primary-100">
                <div className="flex items-center space-x-1">
                  <Calendar className="h-4 w-4" />
                  <span>2023</span>
                </div>
                <div className="flex items-center space-x-1">
                  <Clock className="h-4 w-4" />
                  <span>120 min</span>
                </div>
              </div>
            </div>

            {/* Genres */}
            {movie.genres && movie.genres.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {movie.genres.map((genre) => (
                  <span
                    key={genre}
                    className="px-3 py-1 rounded-full text-sm font-medium bg-white bg-opacity-20 text-white"
                  >
                    {genre}
                  </span>
                ))}
              </div>
            )}

            {/* Rating Section */}
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-semibold mb-2">Your Rating</h3>
                <div className="flex items-center space-x-4">
                  {renderStars(rating, true)}
                  <span className="text-lg font-medium">
                    {rating ? `${rating}/5` : 'Not rated'}
                  </span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap gap-4">
                <button className="flex items-center space-x-2 bg-white bg-opacity-20 hover:bg-opacity-30 px-4 py-2 rounded-lg transition-colors">
                  <Heart className="h-4 w-4" />
                  <span>Add to Favorites</span>
                </button>
                <button className="flex items-center space-x-2 bg-white bg-opacity-20 hover:bg-opacity-30 px-4 py-2 rounded-lg transition-colors">
                  <Share2 className="h-4 w-4" />
                  <span>Share</span>
                </button>
                <button 
                  onClick={handleGetExplanation}
                  className="flex items-center space-x-2 bg-white bg-opacity-20 hover:bg-opacity-30 px-4 py-2 rounded-lg transition-colors"
                >
                  <ThumbsUp className="h-4 w-4" />
                  <span>Why Recommended?</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Movie Details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Description */}
          <div className="card p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">About this movie</h2>
            <p className="text-gray-700 leading-relaxed">
              This is a placeholder description for the movie. In a real application, 
              this would come from the movie database and include plot summary, cast information, 
              and other relevant details about the film.
            </p>
          </div>

          {/* External Links */}
          {(movie.imdbId || movie.tmdbId) && (
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">External Links</h3>
              <div className="flex space-x-4">
                {movie.imdbId && (
                  <a
                    href={`https://www.imdb.com/title/${movie.imdbId}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center space-x-2 text-primary-600 hover:text-primary-700 transition-colors"
                  >
                    <span className="font-medium">IMDb</span>
                    <ArrowLeft className="h-4 w-4 rotate-45" />
                  </a>
                )}
                {movie.tmdbId && (
                  <a
                    href={`https://www.themoviedb.org/movie/${movie.tmdbId}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center space-x-2 text-primary-600 hover:text-primary-700 transition-colors"
                  >
                    <span className="font-medium">TMDb</span>
                    <ArrowLeft className="h-4 w-4 rotate-45" />
                  </a>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Stats */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Your Rating</span>
                <span className="font-medium">{rating || 'Not rated'}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Movie ID</span>
                <span className="font-medium">{movie.movieId}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Genres</span>
                <span className="font-medium">{movie.genres?.length || 0}</span>
              </div>
            </div>
          </div>

          {/* Recommendation Explanation Modal */}
          {showExplanation && explanation && (
            <div className="card p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Why Recommended?</h3>
                <button
                  onClick={() => setShowExplanation(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              <p className="text-gray-700">{explanation}</p>
            </div>
          )}
        </div>
      </div>

      {/* Similar Movies */}
      {similarMovies.length > 0 && (
        <section>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Similar Movies</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
            {similarMovies.map((similarMovie) => (
              <MovieCard key={similarMovie.movieId} movie={similarMovie} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
};

export default MovieDetail;
