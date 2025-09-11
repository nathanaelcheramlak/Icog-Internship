import React, { useState, useEffect } from 'react';
import { recommendationsAPI } from '../services/api';
import { 
  Star, 
  Filter, 
  RefreshCw, 
  Brain, 
  Users, 
  TrendingUp,
  Sparkles,
  Info
} from 'lucide-react';
import MovieCard from '../components/MovieCard';
import toast from 'react-hot-toast';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [method, setMethod] = useState('hybrid');
  const [limit, setLimit] = useState(12);
  const [profile, setProfile] = useState(null);
  const [showProfile, setShowProfile] = useState(false);

  const methods = [
    {
      id: 'hybrid',
      name: 'Hybrid',
      description: 'Combines collaborative and content-based filtering',
      icon: Brain,
      color: 'text-purple-600'
    },
    {
      id: 'collaborative',
      name: 'Collaborative',
      description: 'Based on similar users\' preferences',
      icon: Users,
      color: 'text-blue-600'
    },
    {
      id: 'content_based',
      name: 'Content-Based',
      description: 'Based on movie features and genres',
      icon: Filter,
      color: 'text-green-600'
    },
    {
      id: 'popular',
      name: 'Popular',
      description: 'Most popular movies overall',
      icon: TrendingUp,
      color: 'text-orange-600'
    }
  ];

  useEffect(() => {
    loadRecommendations();
    loadProfile();
  }, [method, limit]);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      const response = await recommendationsAPI.getRecommendations({
        method,
        limit
      });
      setRecommendations(response.data.recommended_movies || []);
    } catch (error) {
      console.error('Error loading recommendations:', error);
      toast.error('Failed to load recommendations');
    } finally {
      setLoading(false);
    }
  };

  const loadProfile = async () => {
    try {
      const response = await recommendationsAPI.getProfile();
      setProfile(response.data.user_profile);
    } catch (error) {
      console.error('Error loading profile:', error);
    }
  };

  const handleMethodChange = (newMethod) => {
    setMethod(newMethod);
  };

  const handleRefresh = () => {
    loadRecommendations();
  };

  const getMethodInfo = (methodId) => {
    return methods.find(m => m.id === methodId) || methods[0];
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <Sparkles className="h-8 w-8 text-yellow-500 mr-3" />
            Recommendations
          </h1>
          <p className="text-gray-600">
            Discover movies tailored to your preferences
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setShowProfile(!showProfile)}
            className="flex items-center space-x-2 btn-secondary"
          >
            <Info className="h-4 w-4" />
            <span>Your Profile</span>
          </button>
          <button
            onClick={handleRefresh}
            className="flex items-center space-x-2 btn-primary"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Method Selection */}
      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommendation Method</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {methods.map((methodOption) => {
            const Icon = methodOption.icon;
            const isSelected = method === methodOption.id;
            
            return (
              <button
                key={methodOption.id}
                onClick={() => handleMethodChange(methodOption.id)}
                className={`p-4 rounded-lg border-2 transition-all duration-200 text-left ${
                  isSelected
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center space-x-3 mb-2">
                  <Icon className={`h-6 w-6 ${methodOption.color}`} />
                  <span className="font-medium text-gray-900">{methodOption.name}</span>
                </div>
                <p className="text-sm text-gray-600">{methodOption.description}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Current Method Info */}
      <div className="bg-gradient-to-r from-primary-50 to-primary-100 rounded-lg p-6">
        <div className="flex items-center space-x-3">
          {(() => {
            const Icon = getMethodInfo(method).icon;
            return <Icon className="h-6 w-6 text-primary-600" />;
          })()}
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {getMethodInfo(method).name} Recommendations
            </h3>
            <p className="text-gray-600">{getMethodInfo(method).description}</p>
          </div>
        </div>
      </div>

      {/* Results Count */}
      <div className="flex items-center justify-between">
        <p className="text-gray-600">
          {recommendations.length} recommendations found
        </p>
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-700">Show:</span>
          <select
            value={limit}
            onChange={(e) => setLimit(parseInt(e.target.value))}
            className="input-field w-20"
          >
            <option value={6}>6</option>
            <option value={12}>12</option>
            <option value={24}>24</option>
            <option value={48}>48</option>
          </select>
        </div>
      </div>

      {/* Recommendations Grid */}
      {recommendations.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6 gap-6">
          {recommendations.map((movie, index) => (
            <div key={movie.movieId} className="relative">
              <MovieCard movie={movie} showRating={true} />
              {/* Recommendation Rank */}
              <div className="absolute -top-2 -right-2 bg-primary-600 text-white text-xs font-bold rounded-full h-6 w-6 flex items-center justify-center">
                {index + 1}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <Star className="h-16 w-16 mx-auto" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No recommendations available</h3>
          <p className="text-gray-600 mb-4">
            Try rating some movies first to get personalized recommendations
          </p>
          <button
            onClick={handleRefresh}
            className="btn-primary"
          >
            Refresh Recommendations
          </button>
        </div>
      )}

      {/* User Profile Modal */}
      {showProfile && profile && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900">Your Recommendation Profile</h3>
                <button
                  onClick={() => setShowProfile(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Profile Summary</h4>
                  <p className="text-gray-700">{profile.summary || 'No profile summary available'}</p>
                </div>
                
                {profile.preferences && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Preferences</h4>
                    <div className="space-y-2">
                      {Object.entries(profile.preferences).map(([key, value]) => (
                        <div key={key} className="flex justify-between">
                          <span className="text-gray-600 capitalize">{key.replace('_', ' ')}</span>
                          <span className="font-medium">{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {profile.ratings_count && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Activity</h4>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Movies Rated</span>
                      <span className="font-medium">{profile.ratings_count}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Recommendations;
