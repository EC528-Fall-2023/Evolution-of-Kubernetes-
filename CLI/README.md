# CLI Tool

The CLI Tool gives you access to the data we have accumulated such as dependencies and vulnerabilities of a select version of Kubernetes

## Installation

Git Clone this repo to get started.

```bash
git clone https://github.com/EC528-Fall-2023/Evolution-of-Kubernetes-.git
```

Will need Pandas, Neo4j, and Tabulate if you do not already have those libraries installed.

```bash
pip install Neo4j
pip install pandas
pip install tabulate
```

## Usage

Refer to valid_versions.txt for versions of Kubernetes that this software supports.
Don't forget to change directories into the CLI folder.

```bash
usage: k8s-scan.py [-h] [-d] [-c] [-e] [-r] [-l] V [V_]

Tool to analyze vulnerabilities in dependencies of Kubernetes

positional arguments:
  V                   version of Kubernetes you would like to scan
  V_                  second version of Kubernetes, required for comparisons else leave empty

options:
  -h, --help          show this help message and exit
  -d, --dependencies  list all dependencies of select version
  -c, --compare       compare dependencies of two chosen versions
  -e, --evaluate      evaluate security posture of chosen version
  -r, --recommend     choose next version with less or equal vulnerabilities
  -l, --list          [default = false] toggle whether to list all data or not
```

## Example

```bash
cd .\CLI

# help
python .\k8s-scan.py -h

# return number of dependencies from kubernetes version 1.26.8
python .\k8s-scan.py -d kubernetes-1.26.8

# list dependencies from kubernetes version 1.26.8
python .\k8s-scan.py -d -l kubernetes-1.26.8

# return number of same, updated, new, and outdated dependencies between kubernetes version 1.26.8 and 1.15.3
python .\k8s-scan.py -c kubernetes-1.26.8 kubernetes-1.15.3

# list the same, updated, new, and outdated dependencies between kubernetes version 1.26.8 and 1.15.3
python .\k8s-scan.py -c -l kubernetes-1.26.8 kubernetes-1.15.3
```