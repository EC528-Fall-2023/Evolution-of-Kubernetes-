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
        #if no data found, vulnerability is not found in our db
        print("vulnerability not found or missing from our database")
        return
    df = pd.DataFrame(records,columns=['VERSION','DATE'])
    df.drop_duplicates(inplace=True,ignore_index=True)
    if(list):
        print(tabulate(df,headers='keys',tablefmt='psql'))
    else:
        print("total versions of Kubernetes this vulnerability was found in is", len(df.index))

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
        
def compareV(version_1,version_2,list):
    url = f"https://k8svul.asleague.org/eval/{version_1}"
    #url = f"http://127.0.0.1:8000/eval/{version_1}"
    records_1 = requests.get(url).json()

    url = f"https://k8svul.asleague.org/eval/{version_2}"
    #url = f"http://127.0.0.1:8000/eval/{version_2}"
    records_2 = requests.get(url).json()

    if(len(records_1) == 0) and (len(records_2) == 0):
        #if no dependencies, we are likely missing the data
        print("data of both versions from our database")
        return
    elif(len(records_1) == 0):
        print("data of " + version_1 + " missing from our database")
        return
    elif(len(records_2) == 0):
        print("data of " + version_2 + " missing from our database")
        return
    
    #find which of the two is more recent, will be used later
    with open('k8s-scan/versions_chrono.txt','r') as chrono:
        for line_num, line in enumerate(chrono):
            line = line.strip()
            if (line == version_1): index_1 = line_num
            if (line == version_2): index_2 = line_num
        if (index_1 < index_2):
            df_1 = pd.DataFrame(records_1,columns=['NAME','INSTALLED','FIXED-IN','TYPE','VULNERABILITY','SEVERITY']) #df_1 is recent -> records_1 in this case
            df_2 = pd.DataFrame(records_2,columns=['NAME','INSTALLED','FIXED-IN','TYPE','VULNERABILITY','SEVERITY'])
            recent = version_1
            older = version_2
        else:
            df_1 = pd.DataFrame(records_2,columns=['NAME','INSTALLED','FIXED-IN','TYPE','VULNERABILITY','SEVERITY']) #df_1 is recent -> records_2 in this case
            df_2 = pd.DataFrame(records_1,columns=['NAME','INSTALLED','FIXED-IN','TYPE','VULNERABILITY','SEVERITY'])
            recent = version_2
            older = version_1
    
    #create dataframe with exact same vulnerabilities
    df_same = pd.merge(df_1,df_2,how='inner',on=['NAME','INSTALLED','FIXED-IN','TYPE','VULNERABILITY','SEVERITY'])
    
    #delete all entries that are exactly the same dependencies
    df_1 = pd.concat([df_1,df_same],ignore_index=True)
    df_2 = pd.concat([df_2,df_same],ignore_index=True)
    df_1.drop_duplicates(keep=False,ignore_index=True,inplace=True)
    df_2.drop_duplicates(keep=False,ignore_index=True,inplace=True)
    #create dataframe with updated dependencies 
    df_updated = pd.merge(df_1,df_2,how='inner',on=['NAME','FIXED-IN','TYPE','VULNERABILITY','SEVERITY'])
    #df_updated.rename(columns={"INSTALLED_x":"INSTALLED version_1","INSTALLED_y":"Installed version_2"},inplace=True)

    #delete all entries that are updated dependencies
    df_1.rename(columns={"INSTALLED":"INSTALLED_x"},inplace=True)
    df_2.rename(columns={"INSTALLED":"INSTALLED_y"},inplace=True)
    df_1 = pd.concat([df_1,df_updated],join='inner',ignore_index=True)
    df_2 = pd.concat([df_2,df_updated],join='inner',ignore_index=True)
    df_1.drop_duplicates(keep=False,ignore_index=True,inplace=True)
    df_2.drop_duplicates(keep=False,ignore_index=True,inplace=True)
    
    #rename for clarity
    df_updated.rename(columns={"INSTALLED_x":"INSTALLED IN "+recent,"INSTALLED_y":"INSTALLED IN "+older},inplace=True)
    df_1.rename(columns={"INSTALLED_x":"INSTALLED"},inplace=True)
    df_2.rename(columns={"INSTALLED_y":"INSTALLED"},inplace=True)
    
    #prints the dataframe if requested to
    if(list):
        print("Same vulnerabilitiies [Common vulnerability and version]")
        print(tabulate(df_same,headers='keys',tablefmt='psql'))
        print("Updated vulnerabilities [Common vulnerabilities but with a different version]")
        print(tabulate(df_updated,headers='keys',tablefmt='psql'))
        print("New vulnerabilities [All vulnerabilities found in newer version: " + recent + " but not in older version]")
        print(tabulate(df_1,headers='keys',tablefmt='psql'))
        print("Resolved vulnerabilities [All vulnerabilities found in older version: " + older + " but not in newer version]")
        print(tabulate(df_2,headers='keys',tablefmt='psql'))
    else:
        #displaying data
        #prints the data
        print("number of same vulnerabilities:",len(df_same))
        print("number of updated vulnerabilities:", len(df_updated))
        print("number of new vulnerabilities", len(df_1)) #new version
        print("number of resolved vulnerabilities:", len(df_2)) #old version