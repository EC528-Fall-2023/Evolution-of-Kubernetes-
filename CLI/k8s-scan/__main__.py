import click
from .dependencies_func import *
from .vulnerabilities_func import *

def init_dep():
    #initialize neo4j
    uri_dep = "neo4j+s://df706296.databases.neo4j.io"
    username_dep = "neo4j"
    password_dep = "6cJ80Ld1ImFnjbROGGGUeoHNootL7_zHv6aBpqdNHDA"
    driver_dep = GraphDatabase.driver(uri_dep, auth=(username_dep, password_dep))
    return driver_dep

def init_vul():
    uri_vul = "neo4j+s://8f379252.databases.neo4j.io"
    username_vul = "neo4j"
    password_vul = "c3IuMZl-ui58QJTrIMraZGM81u7QxiL6ZivuWxBhM0s"
    driver_vul = GraphDatabase.driver(uri_vul, auth=(username_vul, password_vul))
    return driver_vul

#initialize CLI
@click.group()
def cli():
    """Your CLI Tool"""

#create command of dependencies
@click.command()
@click.argument('version', type=str)
@click.option('--list/--no-list', default=False, help='[default = false] toggle list all data')
def dependencies(version,list):
    """list all dependencies of select version"""
    driver_dep = init_dep()
    if not(isvalid_dep(driver_dep,version)):
            raise click.ClickException('Invalid version entered, refer to list of valid entries in valid_versions_dep or --help for help')
    dependencies_dep(driver_dep,version,list)
    driver_dep.close()

#create command of comparing dependencies
@click.command()
@click.argument('version1', type=str)
@click.argument('version2', type=str)
@click.option('--list/--no-list', default=False, help='[default = false] toggle list all data')
def compare(version1,version2,list):
    """compare dependencies of two chosen versions"""
    driver_dep = init_dep()
    if not(isvalid_dep(driver_dep,version1)):
            raise click.ClickException('Invalid version entered, refer to list of valid entries in valid_versions_dep or --help for help')
    if not(isvalid_dep(driver_dep,version2)):
            raise click.ClickException('Invalid version entered, refer to list of valid entries in valid_versions_dep or --help for help')
    compare_dep(driver_dep,version1,version2,list)
    driver_dep.close()

@click.command()
@click.argument('version', type=str)
@click.option('--list/--no-list', default=False, help='[default = false] toggle list all data')
def evaluate(version,list):
    '''evaluate security posture of chosen version'''
    driver_vul = init_vul()
    if not(isvalid_vul(driver_vul,version)):
        raise click.ClickException('Invalid version entered, refer to list of valid entries in valid_versions_vul or --help for help')
    evaluate_vul(driver_vul,version,list)

# Add commands to the CLI group
cli.add_command(dependencies)
cli.add_command(compare)
cli.add_command(evaluate)

if __name__ == "__main__":
    cli()
