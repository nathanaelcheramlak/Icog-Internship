from flask import request, jsonify, Blueprint
from utils.utils import get_user_id_from_token
from database.utils import get_db_session
from database.neo4j_connection import Neo4jConnection
movies_bp = Blueprint("movies", __name__)

@movies_bp.route('/', methods=['GET'])
def get_movies():
    """Get all movies with optional filtering and pagination"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        # Get query parameters
        genre = request.args.get('genre')
        year = request.args.get('year')
        title_filter = request.args.get('title', '')
        min_rating = request.args.get('min_rating')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        skip = (page - 1) * per_page

        # Build base query and parameters
        base_query = """
        MATCH (m:Movie)
        WHERE m.title CONTAINS $title_filter
        """
        
        params = {
            "title_filter": title_filter, 
            "skip": skip, 
            "limit": per_page,
            "user_id": user_id
        }
        
        # Add genre filter
        if genre:
            base_query += """
            MATCH (m)-[:HAS_GENRE]->(g:Genre {name: $genre})
            """
            params["genre"] = genre
        
        # Add year filter (assuming year might be in title or we need to extract it)
        if year:
            base_query += """
            AND m.title =~ $year_pattern
            """
            params["year_pattern"] = f'.*\\\\({year}\\\\)$'  # Proper escaping for regex

        # Add minimum rating filter
        rating_subquery = ""
        if min_rating:
            rating_subquery = """
            MATCH (u:User)-[r:RATED]->(m)
            WITH m, avg(r.rating) AS avg_rating
            WHERE avg_rating >= $min_rating
            """
            params["min_rating"] = float(min_rating)
        
        # Main query to get movies with user-specific data
        main_query = base_query + rating_subquery + """
        OPTIONAL MATCH (u:User {userId: $user_id})-[r:RATED]->(m)
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[hl:HAS_LINK]->()
        WITH m, 
            collect(DISTINCT g.name) AS genres,
            r.rating AS user_rating,
            exists((u)-[:RATED]->(m)) AS has_rated,
            hl.imdbId AS imdbId, 
            hl.tmdbId AS tmdbId  
        RETURN m.movieId AS movieId, 
            m.title AS title,
            imdbId,             
            tmdbId,             
            genres,
            user_rating,
            has_rated
        ORDER BY m.title
        SKIP $skip
        LIMIT $limit
        """
        
        # Count query for pagination
        count_query = base_query + rating_subquery + """
        RETURN count(DISTINCT m) AS total_count
        """

        movies = []
        total_count = 0

        with get_db_session() as session:
            # Get total count
            count_result = session.run(count_query, {k: v for k, v in params.items() if k not in ['skip', 'limit']})
            total_record = count_result.single()
            total_count = total_record["total_count"] if total_record else 0
            
            # Get paginated movies
            result = session.run(main_query, params)
            
            for record in result:
                movies.append({
                    "movieId": record["movieId"],
                    "title": record["title"].strip("'"),
                    "imdbId": record["imdbId"],
                    "tmdbId": record["tmdbId"],
                    "genres": record["genres"],
                    "userRating": record["user_rating"],
                    "hasRated": record["has_rated"]
                })
        
        return jsonify({
            "movies": movies,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total_count,
                "total_pages": (total_count + per_page - 1) // per_page,
                "has_next": page * per_page < total_count,
                "has_prev": page > 1
            }
        })
        
    except ValueError as e:
        return jsonify({"error": "Invalid parameter value"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@movies_bp.route('/<string:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Get a specific movie by ID"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        # Convert movie_id to integer (assuming movie IDs are integers)
        try:
            movie_id_int = int(movie_id)
        except ValueError:
            return jsonify({"error": "Movie ID must be a valid integer"}), 400

        # Neo4j query to get specific movie with detailed information
        query = """
        MATCH (m:Movie {movieId: $movie_id})
        
        // Get genres
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        
        // Get user's rating if exists
        OPTIONAL MATCH (u:User {userId: $user_id})-[r:RATED]->(m)
        
        // Get external links (adjust based on your data model)
        OPTIONAL MATCH (m)-[hl:HAS_LINK]->()
        
        WITH m, 
             collect(DISTINCT g.name) AS genres,
             r.rating AS user_rating,
             exists((u)-[:RATED]->(m)) AS has_rated,
             hl.imdbId AS imdbId,
             hl.tmdbId AS tmdbId
        
        RETURN m.movieId AS movieId,
               m.title AS title,
               genres,
               user_rating,
               has_rated,
               imdbId,
               tmdbId
        """

        with get_db_session() as session:
            result = session.run(query, {"movie_id": movie_id_int, "user_id": user_id})
            record = result.single()
            
            if not record:
                return jsonify({"error": "Movie not found"}), 404
            
            # Convert Neo4j record to dictionary
            movie_data = {
                "movieId": record["movieId"],
                "title": record["title"],
                "genres": record["genres"],
                "userRating": record["user_rating"],
                "hasRated": record["has_rated"],
                "imdbId": record["imdbId"],
                "tmdbId": record["tmdbId"]
            }
        
        return jsonify({"movie": movie_data})
        
    except ValueError as e:
        return jsonify({"error": "Invalid movie ID format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@movies_bp.route('/rate', methods=['POST'])
def rate_movie():
    """Simpler rating function"""
    try:
        user_id = get_user_id_from_token()
        data = request.get_json()
        movie_id = int(data['movie_id'])
        rating = float(data['rating'])
        print(f"User {user_id} is rating movie {movie_id} with {rating}")
        if rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be between 1 and 5"}), 400

        neo4j_conn = Neo4jConnection.get_instance()
        
        def create_rating(tx):
            result = tx.run(
                """
                MERGE (u:User {userId: $user_id})
                MERGE (m:Movie {movieId: $movie_id})
                MERGE (u)-[r:RATED]->(m)
                SET r.rating = $rating, r.timestamp = timestamp()
                RETURN r.rating AS rating, m.title AS title
                """,
                user_id=user_id, movie_id=movie_id, rating=rating
            )
            return result.single()
        
        with neo4j_conn.get_write_session() as session:
            result = session.execute_write(create_rating)
            
            if not result:
                return jsonify({"error": "Failed to create rating"}), 500
            print(result)
            return jsonify({
                "message": "Rating submitted successfully",
                "movie_id": movie_id,
                "rating": rating,
                "movie_title": result["title"]
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@movies_bp.route('/search', methods=['GET'])
def search_movies():
    """Search movies by title, director, or genre"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        query = request.args.get('q')
        if not query:
            return jsonify({"error": "Search query is required"}), 400
        
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        skip = (page - 1) * per_page

        # Neo4j search query with fuzzy matching and ranking
        search_query = """
        // Search in movie titles (case-insensitive)
        MATCH (m:Movie)
        WHERE toLower(m.title) CONTAINS toLower($query)
        
        OPTIONAL MATCH (u:User {userId: $user_id})-[r:RATED]->(m)
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[hl:HAS_LINK]->()
        
        WITH m, 
             collect(DISTINCT g.name) AS genres,
             r.rating AS user_rating,
             exists((u)-[:RATED]->(m)) AS has_rated,
             hl.imdbId AS imdbId,
             hl.tmdbId AS tmdbId,
             // Calculate relevance score based on title match
             CASE 
                 WHEN toLower(m.title) STARTS WITH toLower($query) THEN 2.0
                 WHEN toLower(m.title) CONTAINS toLower($query) THEN 1.0
                 ELSE 0.5
             END AS relevance_score
        
        RETURN m.movieId AS movieId,
               m.title AS title,
               genres,
               user_rating,
               has_rated,
               imdbId,
               tmdbId,
               relevance_score
        ORDER BY relevance_score DESC, m.title ASC
        SKIP $skip
        LIMIT $limit
        """

        # Count query for pagination
        count_query = """
        MATCH (m:Movie)
        WHERE toLower(m.title) CONTAINS toLower($query)
        RETURN count(m) AS total_count
        """

        movies = []
        total_count = 0

        with get_db_session() as session:
            # Get total count
            count_result = session.run(count_query, {"query": query})
            total_record = count_result.single()
            total_count = total_record["total_count"] if total_record else 0
            
            # Get search results
            result = session.run(search_query, {
                "query": query,
                "user_id": user_id,
                "skip": skip,
                "limit": per_page
            })
            
            for record in result:
                movies.append({
                    "movieId": record["movieId"],
                    "title": record["title"],
                    "genres": record["genres"],
                    "userRating": record["user_rating"],
                    "hasRated": record["has_rated"],
                    "imdbId": record["imdbId"],
                    "tmdbId": record["tmdbId"],
                    "relevanceScore": record["relevance_score"]
                })
        
        return jsonify({
            "results": movies,
            "query": query,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total_count,
                "total_pages": (total_count + per_page - 1) // per_page if total_count > 0 else 0,
                "has_next": page * per_page < total_count,
                "has_prev": page > 1
            }
        })
        
    except ValueError as e:
        return jsonify({"error": "Invalid page or per_page value"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@movies_bp.route('/rated', methods=['GET'])
def get_rated_movies():
    """Get rated movies with parameterized sorting"""
    try:
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({"error": "Authentication required"}), 401
        
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        skip = (page - 1) * per_page
        
        sort_by = request.args.get('sort_by', 'timestamp')
        sort_order = request.args.get('sort_order', 'desc')
        
        # Safe parameterized query
        rated_query = """
        MATCH (u:User {userId: $user_id})-[r:RATED]->(m:Movie)
        OPTIONAL MATCH (m)-[:HAS_GENRE]->(g:Genre)
        OPTIONAL MATCH (m)-[hl:HAS_LINK]->()
        
        WITH m, r, hl,
             collect(DISTINCT g.name) AS genres,
             r.rating AS user_rating,
             r.timestamp AS rating_timestamp
        
        RETURN m.movieId AS movieId,
               m.title AS title,
               genres,
               user_rating,
               rating_timestamp,
               hl.imdbId AS imdbId,
               hl.tmdbId AS tmdbId
        ORDER BY 
            CASE $sort_by 
                WHEN 'rating' THEN user_rating
                WHEN 'timestamp' THEN rating_timestamp
                ELSE toLower(m.title)
            END
        """ + ("DESC" if sort_order == 'desc' else "ASC") + """
        SKIP $skip
        LIMIT $limit
        """

        count_query = """
        MATCH (:User {userId: $user_id})-[r:RATED]->(m:Movie)
        RETURN count(m) AS total_count
        """

        movies = []
        total_count = 0

        with get_db_session() as session:
            count_result = session.run(count_query, {"user_id": user_id})
            total_record = count_result.single()
            total_count = total_record["total_count"] if total_record else 0
            
            result = session.run(rated_query, {
                "user_id": user_id,
                "skip": skip,
                "limit": per_page,
                "sort_by": sort_by
            })
            
            for record in result:
                movies.append({
                    "movieId": record["movieId"],
                    "title": record["title"],
                    "genres": record["genres"],
                    "userRating": record["user_rating"],
                    "ratingTimestamp": record["rating_timestamp"],
                    "imdbId": record["imdbId"],
                    "tmdbId": record["tmdbId"]
                })
        
        return jsonify({
            "rated_movies": movies,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total_count,
                "total_pages": (total_count + per_page - 1) // per_page if total_count > 0 else 0,
                "has_next": page * per_page < total_count,
                "has_prev": page > 1
            },
            "sorting": {
                "sort_by": sort_by,
                "sort_order": sort_order
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500