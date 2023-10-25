#run this using /python Neo4jCLI.py
"""//visualize all nodes from one version of kubernetes
MATCH p=(:KubeVersion{kubernetesVersion:"kubernetes-1.29.0-alpha.1"})-[:Contains]->() return p;

//visualize all nodes from two versions of kubernetes
MATCH p=(:KubeVersion{kubernetesVersion:"kubernetes-1.29.0-alpha.1"})-[:Contains]->() 
return p AS a
UNION ALL MATCH p=(:KubeVersion{kubernetesVersion:"kubernetes-1.28.2"})-[:Contains]->()
return p AS a

//list of all dependencies name and version from one version of Kubernetes
MATCH (:KubeVersion{kubernetesVersion:"kubernetes-1.29.0-alpha.1"})-[:Contains]->(p) return p.dependencyVersion,p.dependencyName;

//visualize all versions of kubernetes and their dependencies and relations
MATCH p=()-[:Contains]->() RETURN p;

//list and visualize all versions of kubernetes
MATCH (p:KubeVersion) return p"""
from neo4j import GraphDatabase

def run_cypher_query(driver,query):
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            print(record)

def main():
    uri = "neo4j+s://df706296.databases.neo4j.io"
    username = "neo4j"
    password = "6cJ80Ld1ImFnjbROGGGUeoHNootL7_zHv6aBpqdNHDA"
    driver = GraphDatabase.driver(uri, auth=(username, password))

    while True:
        cypher_query = input("Enter a command (or 'exit' to quit): ")
        if cypher_query.lower() == "k8s-scan --eval --current=1.17.0":
            print("evaluate the security posture of current version")
        elif cypher_query.lower() == "k8s-scan --recommend --current=1.16.9":
            print("recommend next best version after their current version")
        elif cypher_query.lower() == "k8s-scan --analyze --current=1.16.0 --deps":
            print("analyze versions until a certain version")
        elif cypher_query.lower() == "exit":
            break
        else:
            print("not a valid input")
    driver.close()

if __name__ == "__main__":
    main()


