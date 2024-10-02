from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j+s://ff389a88.databases.neo4j.io"
AUTH = ("neo4j", "2kSOQH70unww6GZ52gtrbVHd4N-GNutSH0fbe6nPdj4")

#Connect by initialising driver
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

#querying the database

# Get the name of all 42 year-olds
records, summary, keys = driver.execute_query(
    "MATCH (p:Person {age: $age}) RETURN p.name AS name",
    age=42,
    database_="neo4j",
)

# Loop through results and do something with them
for person in records:
    print(person)

# Summary information
print("The query `{query}` returned {records_count} records in {time} ms.".format(
    query=summary.query, records_count=len(records),
    time=summary.result_available_after,
))
