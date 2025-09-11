from .neo4j_connection import Neo4jConnection

def get_db_session():
    """Get a Neo4j session for database operations"""
    return Neo4jConnection.get_instance().get_session()