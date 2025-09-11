import React, { useState, useEffect } from 'react';
import { 
  Star, 
  Grid, 
  List, 
  ChevronLeft, 
  ChevronRight,
  Filter,
  Calendar,
  Tag,
  X
} from 'lucide-react';
import MovieCard from '../components/MovieCard';
import { moviesAPI } from '../services/api';
import toast from 'react-hot-toast';

const RatedMovies = () => {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({});
  const [viewMode, setViewMode] = useState('grid');
  const [showFilters, setShowFilters] = useState(false);
  
  // Filter states
  const [filters, setFilters] = useState({
    rating: '',
    genre: '',
    year: '',
    page: 1,
    per_page: 12
  });

  // Available genres
  const genres = [
    'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
    'Documentary', 'Drama', 'Fantasy', 'Horror', 'Mystery', 'Romance',
    'Sci-Fi', 'Thriller', 'War', 'Western'
  ];

  const years = Array.from({ length: 30 }, (_, i) => new Date().getFullYear() - i);

  useEffect(() => {
    loadRatedMovies();
  }, [filters]);

  const loadRatedMovies = async () => {
    try {
      setLoading(true);
      const params = { ...filters };
      
      // Remove empty filters
      Object.keys(params).forEach(key => {
        if (params[key] === '' || params[key] === null || params[key] === undefined) {
          delete params[key];
        }
      });

      const response = await moviesAPI.getRatedMovies(params);
      console.log('Rated movies response:', response);
      setMovies(response.data.rated_movies || []);
      setPagination(response.data.pagination || {});
    } catch (error) {
      console.error('Error loading rated movies:', error);
      toast.error('Failed to load rated movies');
    } finally {
      setLoading(false);
    }
  };

  const updateFilters = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const clearFilters = () => {
    setFilters({
      rating: '',
      genre: '',
      year: '',
      page: 1,
      per_page: 12
    });
  };

  const handlePageChange = (newPage) => {
    updateFilters({ page: newPage });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handlePerPageChange = (newPerPage) => {
    updateFilters({ per_page: newPerPage, page: 1 });
  };

  const getActiveFiltersCount = () => {
    return Object.values(filters).filter(value => 
      value && value !== '' && value !== 1 && value !== 12
    ).length;
  };

  const getAverageRating = () => {
    if (movies.length === 0) return 0;
    const totalRating = movies.reduce((sum, movie) => sum + (movie.userRating || 0), 0);
    return (totalRating / movies.length).toFixed(1);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Rated Movies</h1>
          <p className="text-gray-600">
            {pagination.total ? `${pagination.total} movies rated` : 'No movies rated yet'}
            {movies.length > 0 && (
              <span className="ml-2 text-sm">
                • Average rating: {getAverageRating()}/5
              </span>
            )}
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="flex items-center space-x-2 btn-secondary relative"
          >
            <Filter className="h-4 w-4" />
            <span>Filters</span>
            {getActiveFiltersCount() > 0 && (
              <span className="absolute -top-2 -right-2 bg-primary-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {getActiveFiltersCount()}
              </span>
            )}
          </button>
          
          <div className="flex items-center border border-gray-300 rounded-lg">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-2 ${viewMode === 'grid' ? 'bg-primary-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              <Grid className="h-4 w-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 ${viewMode === 'list' ? 'bg-primary-600 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              <List className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Filters */}
      {showFilters && (
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
            <button
              onClick={clearFilters}
              className="text-sm text-primary-600 hover:text-primary-700"
            >
              Clear All
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Rating Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Star className="h-4 w-4 inline mr-1" />
                My Rating
              </label>
              <select
                value={filters.rating}
                onChange={(e) => updateFilters({ rating: e.target.value, page: 1 })}
                className="input-field"
              >
                <option value="">All Ratings</option>
                <option value="1">1 Star</option>
                <option value="2">2 Stars</option>
                <option value="3">3 Stars</option>
                <option value="4">4 Stars</option>
                <option value="5">5 Stars</option>
              </select>
            </div>

            {/* Genre Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Tag className="h-4 w-4 inline mr-1" />
                Genre
              </label>
              <select
                value={filters.genre}
                onChange={(e) => updateFilters({ genre: e.target.value, page: 1 })}
                className="input-field"
              >
                <option value="">All Genres</option>
                {genres.map(genre => (
                  <option key={genre} value={genre}>{genre}</option>
                ))}
              </select>
            </div>

            {/* Year Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Calendar className="h-4 w-4 inline mr-1" />
                Year
              </label>
              <select
                value={filters.year}
                onChange={(e) => updateFilters({ year: e.target.value, page: 1 })}
                className="input-field"
              >
                <option value="">All Years</option>
                {years.map(year => (
                  <option key={year} value={year}>{year}</option>
                ))}
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Active Filters */}
      {getActiveFiltersCount() > 0 && (
        <div className="flex flex-wrap gap-2">
          {filters.rating && (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary-100 text-primary-800">
              Rating: {filters.rating} star{filters.rating !== '1' ? 's' : ''}
              <button
                onClick={() => updateFilters({ rating: '', page: 1 })}
                className="ml-2 hover:text-primary-600"
              >
                <X className="h-3 w-3" />
              </button>
            </span>
          )}
          {filters.genre && (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary-100 text-primary-800">
              Genre: {filters.genre}
              <button
                onClick={() => updateFilters({ genre: '', page: 1 })}
                className="ml-2 hover:text-primary-600"
              >
                <X className="h-3 w-3" />
              </button>
            </span>
          )}
          {filters.year && (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary-100 text-primary-800">
              Year: {filters.year}
              <button
                onClick={() => updateFilters({ year: '', page: 1 })}
                className="ml-2 hover:text-primary-600"
              >
                <X className="h-3 w-3" />
              </button>
            </span>
          )}
        </div>
      )}

      {/* Movies Grid/List */}
      {movies.length > 0 ? (
        <div className={`${
          viewMode === 'grid' 
            ? 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6 gap-6'
            : 'space-y-4'
        }`}>
          {movies.map((movie) => (
            <MovieCard 
              key={movie.movieId} 
              movie={movie} 
              showRating={true}
              viewMode={viewMode}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <Star className="h-16 w-16 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No rated movies found</h3>
          <p className="text-gray-600 mb-4">
            {getActiveFiltersCount() > 0 
              ? 'Try adjusting your filters' 
              : 'Start rating movies to see them here'
            }
          </p>
          {getActiveFiltersCount() > 0 ? (
            <button
              onClick={clearFilters}
              className="btn-primary"
            >
              Clear Filters
            </button>
          ) : (
            <a
              href="/movies"
              className="btn-primary"
            >
              Browse Movies
            </a>
          )}
        </div>
      )}

      {/* Pagination */}
      {pagination.total_pages > 1 && (
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-700">Show:</span>
            <select
              value={filters.per_page}
              onChange={(e) => handlePerPageChange(parseInt(e.target.value))}
              className="input-field w-20"
            >
              <option value={12}>12</option>
              <option value={24}>24</option>
              <option value={48}>48</option>
            </select>
            <span className="text-sm text-gray-700">per page</span>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => handlePageChange(pagination.page - 1)}
              disabled={!pagination.has_prev}
              className="p-2 rounded-lg border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              <ChevronLeft className="h-4 w-4" />
            </button>
            
            <span className="px-4 py-2 text-sm text-gray-700">
              Page {pagination.page} of {pagination.total_pages}
            </span>
            
            <button
              onClick={() => handlePageChange(pagination.page + 1)}
              disabled={!pagination.has_next}
              className="p-2 rounded-lg border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RatedMovies;
