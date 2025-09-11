from flask import jsonify, Blueprint, request
from utils.utils import get_user_id_from_token
from .model import RecommendationEngine

rec_bp = Blueprint("recommendations", __name__)

@rec_bp.route('/', methods=['GET'])
def get_recommended_movies():
    """Get movie recommendations for the user"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        # Get query parameters
        method = request.args.get('method', 'hybrid')  # collaborative, content_based, popular, hybrid
        limit = int(request.args.get('limit', 10))
        movie_id = request.args.get('movie_id')  # For similarity-based recommendations
        
        # Initialize recommendation engine
        engine = RecommendationEngine(user_id=user_id, movie_id=movie_id)
        
        # Get recommendations based on specified method
        recommendations = engine.get_recommendations(limit=limit, method=method)
        
        return jsonify({
            "recommended_movies": recommendations,
            "method": method,
            "limit": limit,
            "user_id": user_id
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rec_bp.route('/profile', methods=['GET'])
def get_user_recommendation_profile():
    """Get user's recommendation profile and preferences"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        engine = RecommendationEngine(user_id=user_id)
        profile = engine.get_user_profile()
        
        return jsonify({
            "user_profile": profile,
            "user_id": user_id
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rec_bp.route('/similarity', methods=['GET'])
def get_movie_similarity():
    """Get similarity between two movies"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        movie_id1 = request.args.get('movie_id1')
        movie_id2 = request.args.get('movie_id2')
        
        if not movie_id1 or not movie_id2:
            return jsonify({"error": "Both movie_id1 and movie_id2 are required"}), 400
        
        engine = RecommendationEngine(user_id=user_id, movie_id=movie_id1)
        similarity = engine.get_movie_similarity(movie_id2)
        
        return jsonify({
            "similarity": similarity,
            "movie_id1": movie_id1,
            "movie_id2": movie_id2
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@rec_bp.route('/explain', methods=['GET'])
def explain_recommendation():
    """Explain why a movie was recommended"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        movie_id = request.args.get('movie_id')
        if not movie_id:
            return jsonify({"error": "movie_id parameter is required"}), 400
        
        engine = RecommendationEngine(user_id=user_id)
        explanation = engine.explain_recommendation(movie_id)
        
        return jsonify({
            "explanation": explanation,
            "movie_id": movie_id,
            "user_id": user_id
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500