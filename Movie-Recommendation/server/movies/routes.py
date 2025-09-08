from flask import request, jsonify, Blueprint
from utils import get_user_id_from_token

movies_bp = Blueprint("movies", __name__)

@movies_bp.route('/movies', methods=['GET'])
def get_movies():
    """Get all movies with optional filtering and pagination"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        # Get query parameters
        genre = request.args.get('genre')
        year = request.args.get('year')
        director = request.args.get('director')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Here you would implement Neo4j query to get movies
        # Example: movies = neo4j_query("MATCH (m:Movie) RETURN m")
        # For now, return placeholder response
        movies = []  # This would be populated from Neo4j
        
        return jsonify({
            "movies": [movie.to_dict() for movie in movies],
            "page": page,
            "per_page": per_page,
            "total": len(movies)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@movies_bp.route('/movies/<string:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get a specific movie by ID"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        # Here you would implement Neo4j query to get specific movie
        # Example: movie = neo4j_query("MATCH (m:Movie {id: $movie_id}) RETURN m", movie_id=movie_id)
        # For now, return placeholder response
        movie = None  # This would be populated from Neo4j
        
        if not movie:
            return jsonify({"error": "Movie not found"}), 404
        
        return jsonify({"movie": movie.to_dict()})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@movies_bp.route('/rate', methods=['POST'])
def rate_movie():
    """Rate a movie (1-5 stars)"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        data = request.json
        movie_id = data.get('movie_id')
        rating = data.get('rating')
        
        if not movie_id or not rating:
            return jsonify({"error": "Movie ID and rating are required"}), 400
        
        if not isinstance(rating, (int, float)) or rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be a number between 1 and 5"}), 400
        
        # Here you would implement Neo4j query to create/update rating
        # Example: neo4j_query("""
        #   MERGE (u:User {id: $user_id})-[:RATED]->(r:Rating)-[:FOR_MOVIE]->(m:Movie {id: $movie_id})
        #   SET r.rating = $rating, r.timestamp = datetime()
        #   RETURN r
        # """, user_id=user_id, movie_id=movie_id, rating=rating)
        
        return jsonify({
            "message": "Rating submitted successfully",
            "movie_id": movie_id,
            "rating": rating
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@movies_bp.route('/movies/search', methods=['GET'])
def search_movies():
    """Search movies by title, director, or genre"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        query = request.args.get('q')
        if not query:
            return jsonify({"error": "Search query is required"}), 400
        
        # Here you would implement Neo4j search query
        # Example: movies = neo4j_query("""
        #   MATCH (m:Movie)
        #   WHERE m.title CONTAINS $query OR m.director CONTAINS $query OR m.genre CONTAINS $query
        #   RETURN m
        # """, query=query)
        
        movies = []  # This would be populated from Neo4j
        
        return jsonify({
            "results": [movie.to_dict() for movie in movies],
            "query": query
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500