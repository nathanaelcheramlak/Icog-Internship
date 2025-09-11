from database.utils import get_db_session

def create_neo4j_user(uuid):
    try:
        with get_db_session() as session:
            # MERGE will create if not exists, return whether it was created
            result = session.run(
                "MERGE (u:User {userId: $uuid}) "
                "RETURN CASE WHEN EXISTS((u)-[:CREATED]-(:System)) THEN false ELSE true END as created",
                uuid=uuid
            )
            
            created = result.single()["created"]
            if not created:
                print(f"Warning: User with uuid {uuid} already exists!")
            
            return created
            
    except Exception as e:
        print(f"Error creating user: {e}")
        return False