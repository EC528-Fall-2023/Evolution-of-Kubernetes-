import click
from .dependencies_func import *
from .vulnerabilities_func import *


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
    dependencies(version,list)

#create command of comparing dependencies
@click.command()
@click.argument('version1', type=str)
@click.argument('version2', type=str)
@click.option('--list/--no-list', default=False, help='[default = false] toggle list all data')
def comp(version1,version2,list):
    """compare dependencies of two chosen versions"""
    compare(version1,version2,list)

@click.command()
@click.argument('version', type=str)
@click.option('--list/--no-list', default=False, help='[default = false] toggle list all data')
def eval(version,list):
    '''evaluate security posture of chosen version'''
    evaluate(version,list)

@click.command()
@click.argument('code',type=str)
@click.option('--list/--no-list', default=False, help='[default = false] toggle list all data')
def vul(code,list):
    '''find all versions of Kubernetes with a given vulnerability code'''
    vulnerability(code,list)

@click.command()
@click.argument('version',type=str)
@click.argument('critical_mapping',required=False,default=5)
@click.argument('high_mapping',required=False,default=4)
@click.argument('medium_mapping',required=False,default=3)
@click.argument('low_mapping',required=False,default=2)
@click.argument('negligible_mapping',required=False,default=1)
@click.argument('unknown_mapping',required=False,default=0)
def rec(version,critical_mapping,high_mapping,medium_mapping,low_mapping,negligible_mapping,unknown_mapping):
    '''recommend a less vulnerable version of Kubernetes based on input'''
    recommend(version,critical_mapping,high_mapping,medium_mapping,low_mapping,negligible_mapping,unknown_mapping)

# Add commands to the CLI group
cli.add_command(dep)
cli.add_command(comp)
cli.add_command(eval)
cli.add_command(vul)
cli.add_command(rec)

if __name__ == "__main__":
    cli()
