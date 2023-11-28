from neo4j import GraphDatabase, RoutingControl
from tabulate import tabulate
import pandas as pd

def evaluate(driver_vul, version, list):
    #run cypher query
    records, summary, keys = driver_vul.execute_query(
        "MATCH (:KubeVersion{kubernetesVersion:$version})-[:Contains]->(p) return p.NAME, p.INSTALLED, p.`FIXED-IN`, p.TYPE, p.VULNERABILITY, p.SEVERITY",
        {"version":version},routing = RoutingControl.READ, database = "neo4j"
    )
    df = pd.DataFrame(records,columns=['NAME','INSTALLED','FIXED-IN','TYPE','VULNERABILITY','SEVERITY'])
    if(len(records) == 0):
        #if no vulnerabilities found, we likely do not have the data
        print("data missing from our database")
        return
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
    else:
        #print data such as total vulnerabilities, and their distribution
        print("total vulnerabilities in version",version, "is",len(records), "with distribution as followed: ")
        print(df['SEVERITY'].value_counts().to_string())
        print("or in terms of percentages:")
        print(df['SEVERITY'].value_counts(normalize=True).to_string())

def vulnerability(driver_vul,code,list):
    #run cypher query
    records, summary, keys = driver_vul.execute_query(
        "MATCH (Vulnerability{VULNERABILITY:$CVE})<-[:Contains]-(p) return p.kubernetesVersion, p.Date",
        {"CVE":code},routing = RoutingControl.READ, database = "neo4j"
    )

    if(list):
        df = pd.DataFrame(records,columns=['VERSION','DATE'])
        print(tabulate(df,headers='keys',tablefmt='psql'))
    else:
        print("total versions of Kubernetes this vulnerability was found in is", len(records))

def recommend(driver_vul,version,list):
    #arbitrary mapping, will likely change later
    mapping = {
            'Critical':5, 'High':4, 'Medium':3, 'Low':2, 'Negligible':1, 'Unknown':0
        }
    #init dataframe for storing data
    #df = pd.DataFrame(columns=['VERSION','AVERAGE VULNERABILITY SCORE'])
    with open('k8s-scan/versions_chrono.txt','r') as chrono:
        current_best_version = ''
        current_best_num = float("inf")
        versions_to_scan = []
        for line in chrono:
        #find occurance of our version in the choronological list
            line = line.strip()
            versions_to_scan.append(line)
            if(line == version):
                break
        
        for version in reversed(versions_to_scan):
            runsum = 0
            records, summary, keys = driver_vul.execute_query(
                "MATCH (:KubeVersion{kubernetesVersion:$version})-[:Contains]->(p) return p.SEVERITY",
                {"version":version},routing = RoutingControl.READ, database = "neo4j"
            )
            #if there are vulnerabilities found, gives average of arbitrary measurement given by mapping earlier
            if(len(records) != 0):
                for vul in records:
                    runsum += mapping[vul["p.SEVERITY"]]
                #average out the runsum
                runsum = runsum
                if (runsum < current_best_num):
                    current_best_num = runsum
                    current_best_version = version
                #df_temp = pd.DataFrame([[version,runsum/len(records)]],columns=['VERSION','AVERAGE VULNERABILITY SCORE'])
                #df = pd.concat([df,df_temp],ignore_index = True)
            #add a penalty for newer versions, as they have a more unknown element, more likely to have undiscovered vulnerabilities
    print("recommended version to update to is", current_best_version, "with a total vulnerability score of", current_best_num)
        
