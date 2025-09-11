from database.utils import get_db_session

class RecommendationEngine:
    def __init__(self, user_id, movie_id=None):
        self.user_id = user_id
        self.movie_id = movie_id
        self.session = get_db_session()

    def get_recommendations(self, limit=10, method="collaborative"):
        """Get recommendations using specified method"""
        if method == "collaborative":
            return self._get_collaborative_recommendations(limit)
        elif method == "similarity":
            return self._get_similar_recommendations(limit)
        elif method == "content_based":
            return self._get_content_based_recommendations(limit)
        elif method == "popular":
            return self._get_popular_recommendations(limit)
        elif method == "hybrid":
            return self._get_hybrid_recommendations(limit)
        else:
            raise ValueError("Unknown recommendation method. Choose from: collaborative, similarity, content_based, popular, hybrid")

    def _get_collaborative_recommendations(self, limit=10):
        """Collaborative filtering based on user similarity"""

        cypher = """
            MATCH (u1:User {userId: $userId})-[:RATED]->(m:Movie)<-[:RATED]-(u2:User)
            WITH u1, u2, COUNT(m) AS common_movies
            ORDER BY common_movies DESC
            LIMIT 50   // cap neighbors

            MATCH (u2)-[r:RATED]->(rec:Movie)
            WHERE NOT (u1)-[:RATED]->(rec)
            WITH rec, AVG(toFloat(r.rating)) AS avg_rating, COUNT(DISTINCT u2) AS common_count
            RETURN rec.movieId AS movieId,
                rec.title AS title,
                avg_rating,
                common_count,
                avg_rating * log10(common_count + 1) AS score
            ORDER BY score DESC
            LIMIT $limit
        """

        # Run query and fetch results
        return self.session.run(
            cypher, {"userId": self.user_id, "limit": limit}
        ).data()

    def _get_similar_recommendations(self, limit=10):
        """Content-based similarity recommendations"""
        if not self.movie_id:
            raise ValueError("movie_id required for similarity recommendations")
        
        cypher = """
            MATCH (source:Movie {movieId: $movieId})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(similar:Movie)
            WHERE source <> similar
            OPTIONAL MATCH (u:User {userId: $userId})-[r:RATED]->(similar)
            WITH similar, 
                 COUNT(DISTINCT g) AS common_genres,
                 r.rating AS user_rating,
                 EXISTS((u)-[:RATED]->(similar)) AS has_rated
            RETURN similar.movieId AS movieId,
                   similar.title AS title,
                   common_genres AS similarity_score,
                   user_rating,
                   has_rated
            ORDER BY common_genres DESC, similar.title ASC
            LIMIT $limit
        """
        return self.session.run(cypher, {"userId": self.user_id, "movieId": self.movie_id, "limit": limit}).data()

    def _get_content_based_recommendations(self, limit=10):
        """Content-based recommendations - more efficient version"""
        cypher = """
            // Get user's favorite genres and find recommended movies in one query
            MATCH (u:User {userId: $userId})-[r:RATED]->(rated:Movie)-[:HAS_GENRE]->(fav_genre:Genre)
            WHERE r.rating >= 4.0
            WITH fav_genre.name AS favorite_genre, COUNT(*) AS genre_count
            ORDER BY genre_count DESC
            LIMIT 3
            
            // For each favorite genre, find recommended movies
            MATCH (rec:Movie)-[:HAS_GENRE]->(g:Genre {name: favorite_genre})
            WHERE NOT EXISTS((:User {userId: $userId})-[:RATED]->(rec))
            WITH rec, g.name AS genre, COUNT(*) AS overlap
            
            // Aggregate by movie
            WITH rec, 
                collect(genre) AS matching_genres, 
                COUNT(genre) AS genre_match_count
            
            RETURN rec.movieId AS movieId,
                rec.title AS title,
                matching_genres,
                genre_match_count AS relevance_score
            ORDER BY genre_match_count DESC, rec.title ASC
            LIMIT $limit
        """
        return self.session.run(cypher, {"userId": self.user_id, "limit": limit}).data()
    
    def _get_popular_recommendations(self, limit=10):
        """Popular movies that user hasn't seen"""
        cypher = """
            MATCH (m:Movie)<-[r:RATED]-(:User)
            WHERE NOT EXISTS((:User {userId: $userId})-[:RATED]->(m))
            WITH m, 
                COUNT(r) AS rating_count, 
                AVG(r.rating) AS avg_rating
            WITH m, rating_count, avg_rating,
                rating_count * avg_rating AS popularity_score
            RETURN m.movieId AS movieId,
                m.title AS title,
                rating_count,
                avg_rating,
                popularity_score
            ORDER BY popularity_score DESC
            LIMIT $limit
        """
        return self.session.run(cypher, {"userId": self.user_id, "limit": limit}).data()
    
    def _get_hybrid_recommendations(self, limit=10):
        """Hybrid approach combining multiple methods"""
        # Get recommendations from different methods
        collaborative = self._get_collaborative_recommendations(limit * 2)
        content_based = self._get_content_based_recommendations(limit * 2)
        popular = self._get_popular_recommendations(limit * 2)
        
        # Combine and deduplicate
        all_recs = {}
        for rec_list in [collaborative, content_based, popular]:
            for rec in rec_list:
                movie_id = rec['movieId']
                if movie_id not in all_recs:
                    all_recs[movie_id] = rec
                    all_recs[movie_id]['sources'] = 1
                else:
                    all_recs[movie_id]['sources'] += 1
        
        # Sort by number of sources (methods that recommended it) and score
        sorted_recs = sorted(all_recs.values(), 
                           key=lambda x: (x.get('sources', 0), 
                                         x.get('score', 0) or 
                                         x.get('similarity_score', 0) or 
                                         x.get('popularity_score', 0)), 
                           reverse=True)
        
        return sorted_recs[:limit]

    def get_user_profile(self):
        """Get user's rating profile and preferences"""
        cypher = """
            // Get user's ratings and genre preferences
            MATCH (u:User {userId: $userId})-[r:RATED]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
            WITH u, 
                COUNT(r) AS total_ratings,
                AVG(r.rating) AS avg_rating,
                collect(DISTINCT {movieId: m.movieId, title: m.title, rating: r.rating})[0..10] AS recent_ratings
            
            // Get genre preferences with proper counting
            MATCH (u:User {userId: $userId})-[r:RATED]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
            WITH u, total_ratings, avg_rating, recent_ratings,
                g.name AS genre,
                COUNT(*) AS genre_count,
                AVG(r.rating) AS avg_genre_rating
            ORDER BY genre_count DESC
            WITH u, total_ratings, avg_rating, recent_ratings,
                collect({genre: genre, count: genre_count, avg_rating: round(avg_genre_rating, 2)}) AS genre_preferences
            
            // Get tagged movies count
            OPTIONAL MATCH (u)-[:TAGGED]->(m2:Movie)
            WITH u, total_ratings, avg_rating, recent_ratings, genre_preferences,
                COUNT(DISTINCT m2) AS tagged_movies
            
            RETURN total_ratings, 
                round(avg_rating, 2) AS avg_rating, 
                recent_ratings, 
                genre_preferences, 
                tagged_movies
        """
        return self.session.run(cypher, {"userId": self.user_id}).single()

    def get_movie_similarity(self, other_movie_id):
        """Calculate similarity between two movies"""
        cypher = """
            MATCH (m1:Movie {movieId: $movieId1})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(m2:Movie {movieId: $movieId2})
            WITH m1, m2, COUNT(DISTINCT g) AS common_genres
            
            OPTIONAL MATCH (u:User)-[r1:RATED]->(m1)
            OPTIONAL MATCH (u:User)-[r2:RATED]->(m2)
            WITH m1, m2, common_genres,
                 collect(r1.rating) AS ratings1,
                 collect(r2.rating) AS ratings2
            
            RETURN m1.title AS movie1,
                   m2.title AS movie2,
                   common_genres AS genre_similarity,
                   CASE WHEN size(ratings1) > 0 AND size(ratings2) > 0 
                        THEN apoc.algo.cosineSimilarity(ratings1, ratings2) 
                        ELSE 0 END AS rating_similarity
        """
        return self.session.run(cypher, {"movieId1": self.movie_id, "movieId2": other_movie_id}).single()

    def explain_recommendation(self, movie_id):
        """Explain why a movie was recommended to the user"""
        cypher = """
            // Check if user has rated similar movies
            MATCH (u:User {userId: $userId})-[r:RATED]->(rated:Movie)-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(rec:Movie {movieId: $movieId})
            WHERE r.rating >= 4.0
            WITH rec, collect(DISTINCT rated.title) AS similar_rated, collect(DISTINCT g.name) AS common_genres
            
            // Check if friends rated this movie
            OPTIONAL MATCH (u)-[:FRIENDS_WITH]-(friend:User)-[fr:RATED]->(rec)
            
            RETURN rec.title AS movie_title,
                   similar_rated AS liked_similar_movies,
                   common_genres AS common_genres,
                   collect(DISTINCT friend.userId) AS friends_who_rated,
                   collect(DISTINCT fr.rating) AS friend_ratings
        """
        return self.session.run(cypher, {"userId": self.user_id, "movieId": movie_id}).single()