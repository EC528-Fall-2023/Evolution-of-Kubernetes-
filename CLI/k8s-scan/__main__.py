import click
from .dependencies_func import *
from .vulnerabilities_func import *

def isvalid(driver_dep,version):
    valid_version = False
    records,summary,keys = driver_dep.execute_query(
        "MATCH (p:KubeVersion) return p.kubernetesVersion",
        routing = RoutingControl.READ, database = "neo4j"
    )
    for record in records:
        if version == record['p.kubernetesVersion']:
            valid_version = True
    return valid_version

def init():
    #initialize neo4j
    uri_dep = "neo4j+s://871cd47b.databases.neo4j.io"
    username_dep = "neo4j"
    password_dep = "AMEtby3GbTe-EfVY6XU04yoggqmTiRQsFcTzi7lvh6g"
    driver_dep = GraphDatabase.driver(uri_dep, auth=(username_dep, password_dep))
    return driver_dep

#initialize CLI
@click.group()
def cli():
    """A tool for evaluating security posture of your Kubernetes version, analyzing its dependencies, and recommending you a better version"""

#create command of dependencies
@click.command()
@click.argument('version', type=str)
@click.option('--list/--no-list', default=False, help='[default = false] toggle list all data')
def dep(version,list):
    """list all dependencies of select version"""
    driver_dep = init()
    if not(isvalid(driver_dep,version)):
            raise click.ClickException('Invalid version entered, refer to list of valid entries in valid_versions_dep or --help for help')
    dependencies(driver_dep,version,list)
    driver_dep.close()

#create command of comparing dependencies
@click.command()
@click.argument('version1', type=str)
@click.argument('version2', type=str)
@click.option('--list/--no-list', default=False, help='[default = false] toggle list all data')
def comp(version1,version2,list):
    """compare dependencies of two chosen versions"""
    driver_dep = init()
    if not(isvalid(driver_dep,version1)):
            raise click.ClickException('Invalid version entered, refer to list of valid entries in valid_versions_dep or --help for help')
    if not(isvalid(driver_dep,version2)):
            raise click.ClickException('Invalid version entered, refer to list of valid entries in valid_versions_dep or --help for help')
    compare(driver_dep,version1,version2,list)
    driver_dep.close()

@click.command()
@click.argument('version', type=str)
@click.option('--list/--no-list', default=False, help='[default = false] toggle list all data')
def eval(version,list):
    '''evaluate security posture of chosen version'''
    driver_vul = init()
    if not(isvalid(driver_vul,version)):
        raise click.ClickException('Invalid version entered, refer to list of valid entries in valid_versions_vul or --help for help')
    evaluate(driver_vul,version,list)
    driver_vul.close()

@click.command()
@click.argument('code',type=str)
@click.option('--list/--no-list', default=False, help='[default = false] toggle list all data')
def vul(code,list):
    '''find all versions of Kubernetes with a given vulnerability code'''
    driver_vul = init()
    vulnerability(driver_vul,code,list)
    driver_vul.close()

@click.command()
@click.argument('version',type=str)
@click.option('--list/--no-list', default=False, help='[default = false] toggle list all data')
def rec(version,list):
    '''recommend a less vulnerable version of Kubernetes based on input'''
    driver_vul = init()
    recommend(driver_vul,version,list)
    driver_vul.close()

# Add commands to the CLI group
cli.add_command(dep)
cli.add_command(comp)
cli.add_command(eval)
cli.add_command(vul)
cli.add_command(rec)

if __name__ == "__main__":
    cli()
