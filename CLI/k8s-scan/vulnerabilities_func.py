from neo4j import GraphDatabase, RoutingControl
from tabulate import tabulate
import pandas as pd

def isvalid_dep(driver_dep,version):
    valid_version = False
    records,summary,keys = driver_dep.execute_query(
        "MATCH (p:KubeVersion) return p.kubernetesVersion",
        routing = RoutingControl.READ, database = "neo4j"
    )
    for record in records:
        if version == record['p.kubernetesVersion']:
            valid_version = True
    return valid_version

def evaluate(driver_vul, version, list):
    #run cypher query
    records, summary, keys = driver_vul.execute_query(
        "MATCH (:KubeVersion{VERSION:$version})-[:contains]->(p) return p.NAME, p.INSTALLED, p.`FIXED-IN`, p.TYPE, p.VULNERABILITY, p.SEVERITY",
        {"version":version},routing = RoutingControl.READ, database = "neo4j"
    )
    df = pd.DataFrame(records,columns=['NAME','INSTALLED','FIXED-IN','TYPE','VULNERABILITY','SEVERITY'])
    series = df['SEVERITY'].value_counts().to_string()
    print(series)
    print("total vulnerabilities in version",version, "is",len(records), "with distribution as followed: ")
    print(df['SEVERITY'].value_counts().to_string())
    print("or in terms of percentages:")
    print(df['SEVERITY'].value_counts(normalize=True).to_string())
    if(list):
        print(tabulate(df,headers='keys',tablefmt='psql'))