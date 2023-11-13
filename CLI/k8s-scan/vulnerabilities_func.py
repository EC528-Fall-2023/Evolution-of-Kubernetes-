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
    #print data such as total vulnerabilities, and their distribution
    print("total vulnerabilities in version",version, "is",len(records), "with distribution as followed: ")
    print(df['SEVERITY'].value_counts().to_string())
    print("or in terms of percentages:")
    print(df['SEVERITY'].value_counts(normalize=True).to_string())
    #print if list is true
    if(list):
        #create mapping to custom sort pandas dataframe
        mapping = {
            'Critical':0, 'High':1, 'Medium':2, 'Low':3, 'Negligible':4, 'Unknown':5
        }
        df['sorting'] = df['SEVERITY'].apply(lambda state: mapping[state])
        df.sort_values(by=['sorting'],inplace=True,ignore_index=True)
        df.drop('sorting',axis=1,inplace=True)
        print(tabulate(df,headers='keys',tablefmt='psql'))