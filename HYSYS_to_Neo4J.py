import win32com.client as win32
import neo4j

def openHysys(hyFilePath):
    """Opens the specified HYSYS file."""
    hyApp = win32.Dispatch('HYSYS.Application')
    hyCase = hyApp.SimulationCases.Open(hyFilePath)
    hyCase.Visible = True  # Set to False to hide HYSYS window
    return hyCase

def extract_flowsheets(hyCase):
    """Extracts flowsheets from the HYSYS case."""
    flowsheets = []
    for flowsheet in hyCase.Flowsheet.MaterialStreams:  # Assuming material streams represent flowsheets
        flowsheet_data = {
            "name": flowsheet.Name,
            "description": flowsheet.Description,
            # Add other desired properties here (e.g., type)
        }
        flowsheets.append(flowsheet_data)
    return flowsheets

def extract_unit_operations(hyCase):
    """Extracts unit operations from the HYSYS case."""
    unit_operations = []
    for unit_operation in hyCase.Flowsheet.Operations:
        unit_operation_data = {
            "name": unit_operation.Name,
            "type": unit_operation.Type,
            "location": unit_operation.Location,  # Assuming location property exists
            # Add other desired attributes here
        }
        unit_operations.append(unit_operation_data)
    return unit_operations

def extract_streams(hyCase):
    """Extracts streams (connections) from the HYSYS case."""
    streams = []
    for stream in hyCase.Flowsheet.MaterialStreams:  # Assuming material streams represent connections
        source = stream.Inlet.Block.Name
        target = stream.Outlet.Block.Name
        stream_data = {
            "name": stream.Name,
            "type": "Material",  # Assuming material streams
            "source": source,
            "target": target,
        }
        streams.append(stream_data)
    return streams

def convert_to_cypher(flowsheets, unit_operations, streams):
    """Converts extracted data into Cypher queries."""
    cypher_queries = []
    for flowsheet in flowsheets:
        cypher_queries.append(f"CREATE (f:Flowsheet {{ name: '{flowsheet['name']}', description: '{flowsheet['description']}' }})")
    for unit_operation in unit_operations:
        cypher_queries.append(f"CREATE (u:UnitOperation {{ name: '{unit_operation['name']}', type: '{unit_operation['type']}', location: '{unit_operation['location']}' }})")
    for stream in streams:
        cypher_queries.append(f"MATCH (s1:UnitOperation {{ name: '{stream['source']}' }}), (s2:UnitOperation {{ name: '{stream['target']}' }}) CREATE (s1)-[:{stream['type']}]->(s2)")
    return cypher_queries

def connect_to_neo4j(username="neo4j", password="neo4j_password"):
    """Connects to the Neo4J database."""
    driver = neo4j.GraphDatabase.driver("bolt://localhost:7687", auth=(username, password))
    session = driver.session()
    return session

def main():
    """Main function to open HYSYS, extract data, and upload to Neo4J."""
    hyFilePath = "path/to/your/hysys/file.hsc"  # Replace with your file path
    hyCase = openHysys(hyFilePath)

    flowsheets = extract_flowsheets(hyCase)
    unit_operations = extract_unit_operations(hyCase)
    streams = extract_streams(hyCase)

    cypher_queries = convert_to_cypher(flowsheets, unit_operations, streams)

    session = connect_to_neo4j()
    for query in cypher_queries:
        session.run(query)

    session.close()

if __name__ == "__main__":
    main()