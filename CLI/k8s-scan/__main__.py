import argparse
from .dependencies_func import *
from .vulnerabilities_func import *


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
