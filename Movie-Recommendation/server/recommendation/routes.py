from flask import jsonify, Blueprint
from utils import get_user_id_from_token

rec_bp = Blueprint("recommendations", __name__)

@rec_bp.route('/movies/recommended', methods=['GET'])
def get_recommended_movies():
    """Get movie recommendations for the user"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        # Here you would implement Neo4j recommendation query
        # This could be based on user's rating history, similar users, etc.
        # Example: movies = neo4j_query("""
        #   MATCH (u:User {id: $user_id})-[:RATED]->(:Rating)-[:FOR_MOVIE]->(m:Movie)
        #   WITH u, m ORDER BY m.average_rating DESC
        #   RETURN m LIMIT 10
        # """, user_id=user_id)
        
        movies = []  # This would be populated from Neo4j
        
        return jsonify({
            "recommended_movies": [movie.to_dict() for movie in movies]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500