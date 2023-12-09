from tabulate import tabulate
import pandas as pd
import requests

def evaluate(version, list):
    #run cypher query
    url = f"https://k8svul.asleague.org/eval/{version}"
    #url = f"http://127.0.0.1:8000/eval/{version}"
    records = requests.get(url).json()

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

def vulnerability(code,list):
    #run cypher query
    url = f"https://k8svul.asleague.org/vul/{code}"
    #url = f"http://127.0.0.1:8000/vul/{code}"
    records = requests.get(url).json()
    if(len(records) == 0):
        #if no version found, vulnerability is not found in our db
        print("data missing from our database")
        return
    if(list):
        df = pd.DataFrame(records,columns=['VERSION','DATE'])
        print(tabulate(df,headers='keys',tablefmt='psql'))
    else:
        print("total versions of Kubernetes this vulnerability was found in is", len(records))

def recommend(version,cm,hm,mm,lm,nm,um):
    #arbitrary mapping, will likely change later
    mapping = {
            'Critical':cm, 'High':hm, 'Medium':mm, 'Low':lm, 'Negligible':nm, 'Unknown':um
        }
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
        if (len(versions_to_scan) == 628):
            print("version does not exist, try again")
            return
        print("processing",end="",flush=True)
        for version in reversed(versions_to_scan):
            print(".",end="",flush=True)
            runsum = 0
            #url = f"http://127.0.0.1:8000/rec/{version}"
            url = f"https://k8svul.asleague.org/rec/{version}"
            records = requests.get(url).json()
            #if there are vulnerabilities found, gives average of arbitrary measurement given by mapping earlier
            if(len(records) != 0):
                for vul in records:
                    runsum += mapping[vul[0]]
                #average out the runsum
                runsum = runsum
                if (runsum < current_best_num):
                    current_best_num = runsum
                    current_best_version = version
            #add a penalty for newer versions, as they have a more unknown element, more likely to have undiscovered vulnerabilities
    print("")
    print("recommended version to update to is", current_best_version, "with a total vulnerability score of", current_best_num)
        
