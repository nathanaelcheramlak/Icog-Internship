import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { moviesAPI, recommendationsAPI } from '../services/api';
import { 
  Film, 
  Star, 
  Search, 
  TrendingUp, 
  Clock,
  Heart,
  Play
} from 'lucide-react';
import MovieCard from '../components/MovieCard';
import SearchBox from '../components/SearchBox';
import toast from 'react-hot-toast';

const Home = () => {
  const { user } = useAuth();
  const [featuredMovies, setFeaturedMovies] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [recentMovies, setRecentMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadHomeData();
  }, []);

  const loadHomeData = async () => {
    try {
      setLoading(true);
      console.log('Loading home data...');
      
      // Load featured movies (popular movies)
      const featuredResponse = await moviesAPI.getMovies({ 
        per_page: 6, 
        min_rating: 4.0 
      });
      console.log('Featured movies response:', featuredResponse);
      setFeaturedMovies(featuredResponse.data.movies || []);

      // Load recommendations
      const recResponse = await recommendationsAPI.getRecommendations({ 
        limit: 6, 
        method: 'hybrid' 
      });
      console.log('Recommendations response:', recResponse);
      setRecommendations(recResponse.data.recommended_movies || []);

      // Load recent movies
      const recentResponse = await moviesAPI.getMovies({ 
        per_page: 6 
      });
      console.log('Recent movies response:', recentResponse);
      setRecentMovies(recentResponse.data.movies || []);

    } catch (error) {
      console.error('Error loading home data:', error);
      toast.error('Failed to load home data');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
    // Redirect to movies page with search query
    window.location.href = `/movies?search=${encodeURIComponent(query)}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your personalized recommendations...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-2xl p-8 text-white">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">
            Welcome back, {user?.username}!
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-primary-100">
            Discover your next favorite movie with AI-powered recommendations
          </p>
          
          <div className="max-w-2xl mx-auto">
            <SearchBox 
              onSearch={handleSearch}
              placeholder="Search for movies, genres, or actors..."
              className="w-full"
            />
          </div>
          
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link 
              to="/movies" 
              className="flex items-center space-x-2 bg-white text-primary-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors"
            >
              <Film className="h-5 w-5" />
              <span>Browse Movies</span>
            </Link>
            <Link 
              to="/recommendations" 
              className="flex items-center space-x-2 bg-primary-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-400 transition-colors"
            >
              <Star className="h-5 w-5" />
              <span>Get Recommendations</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card p-6 text-center">
          <Film className="h-8 w-8 text-primary-600 mx-auto mb-2" />
          <h3 className="text-2xl font-bold text-gray-900">10,000+</h3>
          <p className="text-gray-600">Movies Available</p>
        </div>
        <div className="card p-6 text-center">
          <Star className="h-8 w-8 text-yellow-500 mx-auto mb-2" />
          <h3 className="text-2xl font-bold text-gray-900">4.5</h3>
          <p className="text-gray-600">Average Rating</p>
        </div>
        <div className="card p-6 text-center">
          <TrendingUp className="h-8 w-8 text-green-500 mx-auto mb-2" />
          <h3 className="text-2xl font-bold text-gray-900">95%</h3>
          <p className="text-gray-600">Recommendation Accuracy</p>
        </div>
      </div>

      {/* Recommendations Section */}
      {recommendations.length > 0 && (
        <section>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-3xl font-bold text-gray-900 flex items-center">
              <Star className="h-8 w-8 text-yellow-500 mr-3" />
              Recommended for You
            </h2>
            <Link 
              to="/recommendations" 
              className="text-primary-600 hover:text-primary-700 font-medium"
            >
              View All →
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
            {recommendations.map((movie) => (
              <MovieCard key={movie.movieId} movie={movie} />
            ))}
          </div>
        </section>
      )}

      {/* Featured Movies Section */}
      {featuredMovies.length > 0 && (
        <section>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-3xl font-bold text-gray-900 flex items-center">
              <Heart className="h-8 w-8 text-red-500 mr-3" />
              Featured Movies
            </h2>
            <Link 
              to="/movies?featured=true" 
              className="text-primary-600 hover:text-primary-700 font-medium"
            >
              View All →
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
            {featuredMovies.map((movie) => (
              <MovieCard key={movie.movieId} movie={movie} />
            ))}
          </div>
        </section>
      )}

      {/* Recent Movies Section */}
      {recentMovies.length > 0 && (
        <section>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-3xl font-bold text-gray-900 flex items-center">
              <Clock className="h-8 w-8 text-blue-500 mr-3" />
              Recently Added
            </h2>
            <Link 
              to="/movies" 
              className="text-primary-600 hover:text-primary-700 font-medium"
            >
              View All →
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
            {recentMovies.map((movie) => (
              <MovieCard key={movie.movieId} movie={movie} />
            ))}
          </div>
        </section>
      )}

      {/* Call to Action */}
      <div className="bg-gray-100 rounded-2xl p-8 text-center">
        <h3 className="text-2xl font-bold text-gray-900 mb-4">
          Ready to discover your next favorite movie?
        </h3>
        <p className="text-gray-600 mb-6">
          Our AI-powered recommendation system learns from your preferences to suggest movies you'll love.
        </p>
        <div className="flex flex-wrap justify-center gap-4">
          <Link 
            to="/recommendations" 
            className="btn-primary flex items-center space-x-2"
          >
            <Play className="h-5 w-5" />
            <span>Get Recommendations</span>
          </Link>
          <Link 
            to="/movies" 
            className="btn-secondary flex items-center space-x-2"
          >
            <Search className="h-5 w-5" />
            <span>Browse Movies</span>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;
