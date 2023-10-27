#run this using 'python .\Neo4jCLI.py'
from neo4j import GraphDatabase
import argparse

def main():
    uri = "neo4j+s://df706296.databases.neo4j.io"
    username = "neo4j"
    password = "6cJ80Ld1ImFnjbROGGGUeoHNootL7_zHv6aBpqdNHDA"
    driver = GraphDatabase.driver(uri, auth=(username, password))

    parser = argparse.ArgumentParser(description="Tool to analyze vulnerabilities in dependencies of Kubernetes")
    parser.add_argument("version",metavar="V",type=str,help="Version of Kubernetes you would like to scan")
    parser.add_argument("-e","--evaluate",action="store_true",help="evaluate security posture of chosen version")
    parser.add_argument("-r","--recommend",action="store_true",help="choose next version with less or equal vulnerabilities")
    parser.add_argument("-a","--analyze",action="store_true",help="analyze all versions released up till selected version")
    parser.add_argument("-c","--compare",action="store_true",help="compare two chosen versions")
    parser.add_argument("-l","--list",action="store_true",help="toggle whether to list all data or not")
    args = parser.parse_args()
    if not (args.evaluate or args.recommend or args.analyze or args.compare):
        parser.error('No action requested, add -h for help')
    if(args.evaluate):
        with driver.session() as session:
            result = session.run("MATCH (:KubeVersion{kubernetesVersion:'kubernetes-1.29.0-alpha.1'})-[:Contains]->(p) return p.dependencyVersion,p.dependencyName")
            print(len(result))
            if(args.list):
                for record in result:
                    print(record)
    driver.close()
    
if __name__ == "__main__":
    main()


"""
uri = "neo4j+s://df706296.databases.neo4j.io"
    username = "neo4j"
    password = "6cJ80Ld1ImFnjbROGGGUeoHNootL7_zHv6aBpqdNHDA"
    driver = GraphDatabase.driver(uri, auth=(username, password))

    driver.close()


//visualize all nodes from one version of kubernetes
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
MATCH (p:KubeVersion) return p

def run_cypher_query(driver,query):
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            print(record)
"""


