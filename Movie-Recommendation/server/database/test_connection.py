"""
Test Neo4j database connection.

This script attempts to establish a connection to a Neo4j database and runs a simple query to verify connectivity.
"""
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "password"

def test_connection(uri: str, user: str, password: str) -> bool:
    """
    Attempts to connect to the Neo4j database and run a test query.
    Returns True if successful, False otherwise.
    """
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run("RETURN 'Hello, Neo4j!' AS message").single()
            message = result["message"] if result else None
            print(f"Connection successful. Message: {message}")
            return True
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if driver:
            driver.close()
    return False

if __name__ == "__main__":
    success = test_connection(URI, USER, PASSWORD)
    if not success:
        print("Failed to connect to Neo4j database.")