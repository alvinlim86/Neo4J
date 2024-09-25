from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j+s://ff389a88.databases.neo4j.io"
AUTH = ("neo4j", "2kSOQH70unww6GZ52gtrbVHd4N-GNutSH0fbe6nPdj4")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
