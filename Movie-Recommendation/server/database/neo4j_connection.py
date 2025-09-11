from neo4j import GraphDatabase
import neo4j
import os

class Neo4jConnection:
    _instance = None
    
    def __init__(self):
        if Neo4jConnection._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() instead.")
        
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")
        
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        Neo4jConnection._instance = self
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Neo4jConnection()
        return cls._instance
    
    def close(self):
        if self.driver:
            self.driver.close()
            Neo4jConnection._instance = None
    
    def get_session(self):
        return self.driver.session()
    
    def get_write_session(self):
        """Get a session with write access"""
        return self.driver.session(default_access_mode=neo4j.WRITE_ACCESS)
    
    def get_read_session(self):
        """Get a session with read access"""
        return self.driver.session(default_access_mode=neo4j.READ_ACCESS)