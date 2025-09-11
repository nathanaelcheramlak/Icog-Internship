from math import log1p
from database.utils import get_db_session

class RecommendationEngine:
    def __init__(self, user_id, movie_id=None):
        self.user_id = 123
        self.movie_id = movie_id
        self.session = get_db_session()

    def get_recommendations(self, limit=10, method="collaborative"):
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
        """
        Collaborative filtering:
        - Find top neighbor users by number of co-rated movies (cap neighbors)
        - For those neighbors, aggregate their ratings for movies the target user hasn't rated
        - Score is a neighbor-weighted average rating (neighbors weighted by number of common movies)
        """
        cypher = """
            MATCH (u1:User {userId: $userId})-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2:User)
            WITH u1, u2, COUNT(m) AS common_movies
            ORDER BY common_movies DESC
            LIMIT 50

            // neighbors u2 preserved with their common_movies
            MATCH (u2)-[r:RATED]->(rec:Movie)
            WHERE NOT (u1)-[:RATED]->(rec)
            WITH rec, u2, common_movies, r.rating AS neighbor_rating

            // compute weight-adjusted sums
            WITH rec.movieId AS movieId, rec.title AS title,
                 sum(neighbor_rating * common_movies) AS weighted_rating_sum,
                 sum(common_movies) AS total_weight,
                 COUNT(DISTINCT u2) AS neighbor_count

            WITH movieId, title,
                 CASE WHEN total_weight > 0 THEN toFloat(weighted_rating_sum) / toFloat(total_weight) ELSE 0 END AS score,
                 neighbor_count

            RETURN movieId, title, score, neighbor_count
            ORDER BY score DESC, neighbor_count DESC
            LIMIT $limit
        """
        return self.session.run(cypher, {"userId": self.user_id, "limit": limit}).data()

    def _get_similar_recommendations(self, limit=10):
        """
        Movie-to-movie similarity based on shared genres.
        Requires self.movie_id.
        Returns similarity score = number of shared genres, plus optional user rating for that similar movie.
        """
        if not self.movie_id:
            raise ValueError("movie_id required for similarity recommendations")

        cypher = """
            MATCH (source:Movie {movieId: $movieId})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(similar:Movie)
            WHERE source <> similar
            WITH similar, COUNT(DISTINCT g) AS common_genres
            OPTIONAL MATCH (u:User {userId: $userId})-[ur:RATED]->(similar)
            WITH similar, common_genres, 
                 CASE WHEN ur IS NULL THEN NULL ELSE ur.rating END AS user_rating,
                 CASE WHEN ur IS NULL THEN false ELSE true END AS has_rated
            RETURN similar.movieId AS movieId,
                   similar.title AS title,
                   common_genres AS similarity_score,
                   user_rating,
                   has_rated
            ORDER BY similarity_score DESC, title ASC
            LIMIT $limit
        """
        return self.session.run(cypher, {"userId": self.user_id, "movieId": self.movie_id, "limit": limit}).data()

    def _get_content_based_recommendations(self, limit=10):
        """Content-based recommendations - simpler approach"""
        cypher = """
            // Get user's top 3 favorite genres based on ratings >= 3
            MATCH (u:User {userId: $userId})-[r:RATED]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
            WHERE r.rating >= 3.0
            WITH g.name AS genre, COUNT(*) AS genre_count
            ORDER BY genre_count DESC
            LIMIT 3
            WITH collect(genre) AS favorite_genres
            
            // If no favorite genres, get any genres from user's rated movies
            OPTIONAL MATCH (:User {userId: $userId})-[:RATED]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
            WITH favorite_genres, 
                CASE WHEN size(favorite_genres) = 0 
                    THEN collect(DISTINCT g.name) 
                    ELSE favorite_genres 
                END AS target_genres
            
            // Find movies that match these genres and user hasn't rated
            MATCH (rec:Movie)-[:HAS_GENRE]->(g:Genre)
            WHERE g.name IN target_genres
            AND NOT EXISTS((:User {userId: $userId})-[:RATED]->(rec))
            WITH rec, COUNT(DISTINCT g) AS matching_genres_count
            RETURN rec.movieId AS movieId,
                rec.title AS title,
                matching_genres_count AS relevance_score
            ORDER BY matching_genres_count DESC, rec.title ASC
            LIMIT $limit
        """
        result = self.session.run(cypher, {"userId": self.user_id, "limit": limit}).data()
        print("Content-based recommendations:", result)
        return result


    def _get_popular_recommendations(self, limit=10):
        """
        Popular movies user hasn't seen.
        Score = rating_count * avg_rating (popularity_score)
        """
        cypher = """
            MATCH (m:Movie)<-[r:RATED]-(:User)
            WHERE NOT EXISTS((:User {userId: $userId})-[:RATED]->(m))
            WITH m, COUNT(r) AS rating_count, AVG(r.rating) AS avg_rating
            WITH m, rating_count, avg_rating, rating_count * avg_rating AS popularity_score
            RETURN m.movieId AS movieId, m.title AS title,
                   rating_count, round(avg_rating,2) AS avg_rating,
                   popularity_score
            ORDER BY popularity_score DESC, rating_count DESC
            LIMIT $limit
        """
        return self.session.run(cypher, {"userId": self.user_id, "limit": limit}).data()

    def _get_hybrid_recommendations(self, limit=10):
        """
        Hybrid: gather from collaborative / content / popular, normalize each method's score to [0,1],
        then compute a weighted combination. Returns movies sorted by combined_score.
        """
        # fetch more from each source to allow combination variety
        coll = self._get_collaborative_recommendations(limit * 2)
        cont = self._get_content_based_recommendations(limit * 2)
        pop = self._get_popular_recommendations(limit * 2)

        # normalize scores per source
        # collaborative: uses 'score'
        coll_scores = [r.get('score', 0) for r in coll]
        cont_scores = [r.get('relevance_score', 0) for r in cont]
        pop_scores = [r.get('popularity_score', 0) for r in pop]

        def normalize(list_vals):
            if not list_vals:
                return {}
            mx = max(list_vals)
            mn = min(list_vals)
            if mx == mn:
                # if all equal, map non-zero to 1.0
                return {v: (1.0 if v > 0 else 0.0) for v in list_vals}
            return {v: (float(v - mn) / float(mx - mn)) for v in list_vals}

        # Build maps by movieId for dedup
        all_recs = {}
        # helper to get normalized value by value lists (we'll compute per-item normalized by value)
        coll_norm_map = normalize(coll_scores)
        cont_norm_map = normalize(cont_scores)
        pop_norm_map = normalize(pop_scores)

        # add from collaborative
        for r in coll:
            mid = r['movieId']
            score_raw = r.get('score', 0)
            norm_score = coll_norm_map.get(score_raw, 0.0)
            all_recs.setdefault(mid, {"movieId": mid, "title": r.get('title'), "sources": set()})
            all_recs[mid].update({"collab_score": norm_score})
            all_recs[mid]["sources"].add("collaborative")

        # add from content
        for r in cont:
            mid = r['movieId']
            score_raw = r.get('relevance_score', 0)
            norm_score = cont_norm_map.get(score_raw, 0.0)
            all_recs.setdefault(mid, {"movieId": mid, "title": r.get('title'), "sources": set()})
            all_recs[mid].update({"content_score": norm_score, "matching_genres": r.get('matching_genres')})
            all_recs[mid]["sources"].add("content_based")

        # add from popular
        for r in pop:
            mid = r['movieId']
            score_raw = r.get('popularity_score', 0)
            norm_score = pop_norm_map.get(score_raw, 0.0)
            all_recs.setdefault(mid, {"movieId": mid, "title": r.get('title'), "sources": set()})
            all_recs[mid].update({"popular_score": norm_score})
            all_recs[mid]["sources"].add("popular")

        # compute combined score: give more weight to collaborative and content, but keep popularity
        results = []
        for mid, info in all_recs.items():
            coll_s = info.get('collab_score', 0.0)
            cont_s = info.get('content_score', 0.0)
            pop_s = info.get('popular_score', 0.0)
            # example weights (tune as needed)
            combined = 0.5 * coll_s + 0.35 * cont_s + 0.15 * pop_s
            # slightly boost items recommended by multiple methods
            source_count = len(info.get('sources', []))
            combined *= (1.0 + 0.05 * (source_count - 1))
            results.append({
                "movieId": mid,
                "title": info.get("title"),
                "combined_score": round(combined, 4),
                "sources": list(info.get("sources"))
            })

        results.sort(key=lambda x: x['combined_score'], reverse=True)
        return results[:limit]

    def get_user_profile(self):
        """
        Returns user's rating summary, average rating, recent rated movies, and top genre preferences.
        """
        cypher = """
            MATCH (u:User {userId: $userId})-[r:RATED]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
            WITH u, COUNT(r) AS total_ratings, AVG(r.rating) AS avg_rating,
                 collect(DISTINCT {movieId: m.movieId, title: m.title, rating: r.rating})[0..10] AS recent_ratings

            // genre-level stats
            MATCH (u)-[r2:RATED]->(m2:Movie)-[:HAS_GENRE]->(g2:Genre)
            WITH u, total_ratings, avg_rating, recent_ratings,
                 g2.name AS genre, COUNT(*) AS genre_count, AVG(r2.rating) AS avg_genre_rating
            ORDER BY genre_count DESC
            WITH u, total_ratings, avg_rating, recent_ratings,
                 collect({genre: genre, count: genre_count, avg_rating: round(avg_genre_rating, 2)}) AS genre_preferences

            OPTIONAL MATCH (u)-[:HAS_TAG]->(t:Movie)
            WITH total_ratings, round(avg_rating, 2) AS avg_rating, recent_ratings, genre_preferences,
                 COUNT(DISTINCT t) AS tagged_movies

            RETURN total_ratings, avg_rating, recent_ratings, genre_preferences, tagged_movies
        """
        return self.session.run(cypher, {"userId": self.user_id}).single()

    def get_movie_similarity(self, other_movie_id):
        """
        Returns genre overlap and rating-similarity (if possible).
        Requires APOC for cosine similarity on rating vectors; if not available rating_similarity will be 0.
        """
        cypher = """
            MATCH (m1:Movie {movieId: $movieId1})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(m2:Movie {movieId: $movieId2})
            WITH m1, m2, COUNT(DISTINCT g) AS common_genres

            OPTIONAL MATCH (u1:User)-[r1:RATED]->(m1)
            OPTIONAL MATCH (u2:User)-[r2:RATED]->(m2)
            WITH m1, m2, common_genres, collect(r1.rating) AS ratings1, collect(r2.rating) AS ratings2

            RETURN m1.title AS movie1, m2.title AS movie2,
                   common_genres AS genre_similarity,
                   CASE WHEN size(ratings1) > 0 AND size(ratings2) > 0
                        THEN apoc.algo.cosineSimilarity(ratings1, ratings2)
                        ELSE 0 END AS rating_similarity
        """
        return self.session.run(cypher, {"movieId1": self.movie_id, "movieId2": other_movie_id}).single()

    def explain_recommendation(self, movie_id):
        """
        Return why a given movie was recommended (liked similar movies, shared genres, friends who rated it).
        """
        cypher = """
            MATCH (u:User {userId: $userId})
            OPTIONAL MATCH (u)-[r:RATED]->(rated:Movie)-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(rec:Movie {movieId: $movieId})
            WHERE r.rating >= 4.0
            WITH rec, collect(DISTINCT rated.title) AS similar_rated, collect(DISTINCT g.name) AS common_genres

            OPTIONAL MATCH (u)-[:FRIENDS_WITH]-(friend:User)-[fr:RATED]->(rec)
            RETURN rec.title AS movie_title,
                   similar_rated AS liked_similar_movies,
                   common_genres AS common_genres,
                   collect(DISTINCT friend.userId) AS friends_who_rated,
                   collect(DISTINCT fr.rating) AS friend_ratings
        """
        return self.session.run(cypher, {"userId": self.user_id, "movieId": movie_id}).single()
