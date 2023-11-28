from neo4j import GraphDatabase, RoutingControl
from tabulate import tabulate
import pandas as pd
import os

def dependencies(driver_dep,version,list):
    #run cypher query 
    records,summary,keys = driver_dep.execute_query(
        "MATCH (:KubeVersion{kubernetesVersion:$version})-[:Depends_On]->(p) return p.dependencyName,p.dependencyVersion",
        {"version":version}, routing = RoutingControl.READ, database = "neo4j"
    )

    #print list of dependencies if user requests it
    if(list):
        df = pd.DataFrame(records,columns=['dependency name','dependency version'])
        print(tabulate(df,headers='keys',tablefmt='psql'))
    else:
        #print dependencies data
        print("total dependencies in version",version,"is",len(records))
    

def compare(driver_dep,version_1,version_2,list):
    #separate based on if both version + name is same, name is same different version, both are different
    records_1,summary,keys = driver_dep.execute_query(
        "MATCH (:KubeVersion{kubernetesVersion:$version})-[:Depends_On]->(p) return p.dependencyName, p.dependencyVersion",
        {"version":version_1}, routing = RoutingControl.READ, database = "neo4j"
    )
    records_2,summary,keys = driver_dep.execute_query(
        "MATCH (:KubeVersion{kubernetesVersion:$version})-[:Depends_On]->(p) return p.dependencyName, p.dependencyVersion",
        {"version":version_2}, routing = RoutingControl.READ, database = "neo4j"
    )

    
    #find which of the two is more recent, will be used later
    with open('k8s-scan/versions_chrono.txt','r') as chrono:
        for line_num, line in enumerate(chrono):
            line = line.strip()
            if (line == version_1): index_1 = line_num
            if (line == version_2): index_2 = line_num
        if (index_1 < index_2):
            df_1 = pd.DataFrame(records_1,columns=['dependency name','dependency version']) #df_1 is recent -> records_1 in this case
            df_2 = pd.DataFrame(records_2,columns=['dependency name','dependency version'])
            recent = version_1
            older = version_2
        else:
            df_1 = pd.DataFrame(records_2,columns=['dependency name','dependency version']) #df_1 is recent -> records_2 in this case
            df_2 = pd.DataFrame(records_1,columns=['dependency name','dependency version'])
            recent = version_2
            older = version_1
    
    #create dataframe with exact same dependencies
    df_same = pd.merge(df_1,df_2,how='inner',on=['dependency name','dependency version'])
    
    #delete all entries that are exactly the same dependencies
    df_1 = pd.concat([df_1,df_same],ignore_index=True)
    df_2 = pd.concat([df_2,df_same],ignore_index=True)
    df_1.drop_duplicates(keep=False,ignore_index=True,inplace=True)
    df_2.drop_duplicates(keep=False,ignore_index=True,inplace=True)

    #create dataframe with updated dependencies 
    df_updated = pd.merge(df_1,df_2,how='inner',on=['dependency name'])
    df_updated.rename(columns={"dependency version_x":"dependency version_1","dependency version_y":"dependency version_2"},inplace=True)
    
    #delete all entries that are updated dependencies
    df_1.rename(columns={"dependency version":"dependency version_1"},inplace=True)
    df_2.rename(columns={"dependency version":"dependency version_2"},inplace=True)
    df_1 = pd.concat([df_1,df_updated],join='inner',ignore_index=True)
    df_2 = pd.concat([df_2,df_updated],join='inner',ignore_index=True)
    df_1.drop_duplicates(keep=False,ignore_index=True,inplace=True)
    df_2.drop_duplicates(keep=False,ignore_index=True,inplace=True)
    
    #rename for clarity
    df_updated.rename(columns={"dependency version_1":"dependencies version from "+recent,"dependency version_2":"dependencies version from "+older},inplace=True)
    df_1.rename(columns={"dependency version_1":"dependency version"},inplace=True)
    df_2.rename(columns={"dependency version_2":"dependency version"},inplace=True)
    
    #prints the dataframe if requested to
    if(list):
        print("Same dependencies [Common dependencies and version]")
        print(tabulate(df_same,headers='keys',tablefmt='psql'))
        print("Updated dependencies [Common dependencies but with a different version]")
        print(tabulate(df_updated,headers='keys',tablefmt='psql'))
        print("New dependencies [All dependencies found in newer version: " + recent + " but not in older version]")
        print(tabulate(df_1,headers='keys',tablefmt='psql'))
        print("Outdated dependencies [All dependencies found in older version: " + older + " but not in newer version]")
        print(tabulate(df_2,headers='keys',tablefmt='psql'))
    else:
        #displaying data
        #prints the data
        print("number of same dependencies:",len(df_same))
        print("number of updated dependencies:", len(df_updated))
        print("number of new dependencies", len(df_1)) #new version
        print("number of outdated dependencies:", len(df_2)) #old version