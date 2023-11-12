#run this using 'python .\Neo4jCLI.py'
#pip install neo4j, pip install pandas, pip install tabulate
from neo4j import GraphDatabase, RoutingControl
from tabulate import tabulate
import pandas as pd
import argparse

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

def isvalid_vul(driver_vul,version):
    valid_version = False
    records,summary,keys = driver_vul.execute_query(
        "MATCH (p:KubeVersion) return p.VERSION",
        routing = RoutingControl.READ, database = "neo4j"
    )
    for record in records:
        if version == record['p.VERSION']:
            valid_version = True
    return valid_version

def dependencies(driver_dep,version,list):
    #run cypher query 
    records,summary,keys = driver_dep.execute_query(
        "MATCH (:KubeVersion{kubernetesVersion:$version})-[:Contains]->(p) return p.dependencyName,p.dependencyVersion",
        {"version":version}, routing = RoutingControl.READ, database = "neo4j"
    )
    #print dependencies data
    print("total dependencies in version",version,"is",len(records))
    #print list of dependencies if user requests it
    if(list):
        df = pd.DataFrame(records,columns=['dependency name','dependency version'])
        print(tabulate(df,headers='keys',tablefmt='psql'))
    

def compare(driver_dep,version_1,version_2,list):
    #separate based on if both version + name is same, name is same different version, both are different
    records_1,summary,keys = driver_dep.execute_query(
        "MATCH (:KubeVersion{kubernetesVersion:$version})-[:Contains]->(p) return p.dependencyName, p.dependencyVersion",
        {"version":version_1}, routing = RoutingControl.READ, database = "neo4j"
    )
    records_2,summary,keys = driver_dep.execute_query(
        "MATCH (:KubeVersion{kubernetesVersion:$version})-[:Contains]->(p) return p.dependencyName, p.dependencyVersion",
        {"version":version_2}, routing = RoutingControl.READ, database = "neo4j"
    )

    #rewrite version for search in versions_chrono.txt
    version_1 = "v" + version_1.replace("kubernetes-",'')
    version_2 = "v" + version_2.replace("kubernetes-",'')
    #find which of the two is more recent, will be used later
    with open("versions_chrono.txt",'r') as chrono:
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

    ##displaying data
    #prints the data
    print("number of same dependencies:",len(df_same))
    print("number of updated dependencies:", len(df_updated))
    print("number of new dependencies", len(df_1)) #new version
    print("number of outdated dependencies:", len(df_2)) #old version
    
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
        print(tabulate(df,headers='keys',tablefmt='psq1'))

def main():
    #login to neo4j
    uri_dep = "neo4j+s://df706296.databases.neo4j.io"
    username_dep = "neo4j"
    password_dep = "6cJ80Ld1ImFnjbROGGGUeoHNootL7_zHv6aBpqdNHDA"
    driver_dep = GraphDatabase.driver(uri_dep, auth=(username_dep, password_dep))

    uri_vul = "neo4j+s://8f379252.databases.neo4j.io"
    username_vul = "neo4j"
    password_vul = "c3IuMZl-ui58QJTrIMraZGM81u7QxiL6ZivuWxBhM0s"
    driver_vul = GraphDatabase.driver(uri_vul, auth=(username_vul, password_vul))

    #argument parser for CLI
    parser = argparse.ArgumentParser(description="Tool to analyze vulnerabilities in dependencies of Kubernetes")
    parser.add_argument("version",metavar="V",type=str,help="version of Kubernetes you would like to scan")
    parser.add_argument("version_",metavar="V_",nargs='?',type=str,help="second version of Kubernetes, required for comparisons else leave empty")
    parser.add_argument("-d","--dependencies",action="store_true",help="list all dependencies of select version")
    parser.add_argument("-c","--compare",action="store_true",help="compare dependencies of two chosen versions")
    parser.add_argument("-e","--evaluate",action="store_true",help="evaluate security posture of chosen version")
    parser.add_argument("-r","--recommend",action="store_true",help="choose next version with less or equal vulnerabilities")
    #parser.add_argument("-a","--analyze",action="store_true",help="analyze all versions released up till selected version")
    parser.add_argument("-l","--list",action="store_true",help="[default = false] toggle whether to list all data or not")
    args = parser.parse_args()
    
    #check if any function is called, if not return error
    if not (args.dependencies or args.evaluate or args.recommend or args.compare):
        parser.error('No action requested, add -h for help')

    #do function based on input
    if(args.dependencies):
        #check if version is valid first
        if not(isvalid_dep(driver_dep,args.version)):
            parser.error('Invalid version entered, refer to list of valid entries in valid_versions_dep or -h for help')
        dependencies(driver_dep,args.version,args.list)
    if(args.compare):
        #check if version is valid first
        if not(isvalid_dep(driver_dep,args.version)):
            parser.error('Invalid version entered, refer to list of valid entries in valid_versions_dep or -h for help')
        #checks if second argument is none or invalid, gives proper response to error
        if (args.version_ == None):
            parser.error('Second version entry is not defined, add -h for help')
        elif not(isvalid_dep(driver_dep,args.version_)):
            parser.error('Invalid second version entered, refer to list of valid entries of -h for help')
        compare(driver_dep,args.version,args.version_,args.list)
    if(args.evaluate):
        if not(isvalid_vul(driver_vul,args.version)):
            parser.error('Invalid version entered, refer to list of valid entries in valid_versions_vul or -h for help')
        evaluate(driver_vul,args.version,args.list)
    driver_dep.close()
    
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


