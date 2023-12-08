# CLI Tool

The CLI Tool gives you access to the data we have accumulated such as dependencies and vulnerabilities of a select version of Kubernetes

## Installation

Git Clone this repo to get started.

```bash
git clone https://github.com/EC528-Fall-2023/Evolution-of-Kubernetes-.git
```

Install required dependencies

```bash
cd ./CLI
pip install -r requirements.txt
```

## Usage

Refer to valid_versions_dep.txt or valid_versions_vul.txt for versions of Kubernetes that this software supports.
valid_versions_dep.txt is for dependency functions (dep, comp)
valid_versions_vul.txt is for vulnerability functions (eval, vul, rec)

```bash
Usage: python -m k8s-scan [OPTIONS] COMMAND [ARGS]...

  A tool for evaluating security posture of your Kubernetes version, analyzing
  its dependencies, and recommending you a better version

Options:
  --help  Show this message and exit.

Commands:
  comp  compare dependencies of two chosen versions
  dep   list all dependencies of select version
  eval  evaluate security posture of chosen version
  rec   recommend a less vulnerable version of Kubernetes based on input
  vul   find all versions of Kubernetes with a given vulnerability code
```

## Example

```bash
cd .\CLI

# help
python -m k8s-scan.py --help

# return number of dependencies from kubernetes version 1.26.8
python -m k8s-scan dep v1.26.8

# list dependencies from kubernetes version 1.26.8
python -m k8s-scan dep --list v1.26.8

# return number of same, updated, new, and outdated dependencies between kubernetes version 1.26.8 and 1.15.3
python -m k8s-scan comp v1.26.8 v1.15.3

# list the same, updated, new, and outdated dependencies between kubernetes version 1.26.8 and 1.15.3
python -m k8s-scan comp --list v1.26.8 v1.15.3

# return amount of vulnerabilities, and their spread found in kubernetes version 1.21.12
python -m k8s-scan eval v1.21.12

# list the vulnerabilities found in kubernetes version 1.21.12
python -m k8s-scan eval --list v1.21.12

# return amount of versions of Kubernetes that vulnerability with CVE code CVE-2010-0928 was found in
python -m k8s-scan vul CVE-2010-0928

# list the versions of Kubernetes that vulnerability with CVE code CVE-2010-0928 was found in
python -m k8s-scan vul --list CVE-2010-0928

# recommends a less vulnerable version after v1.20.15 with default mapping
python -m k8s-scan rec v1.20.15

# recommends a less vulnerable version after v1.20.15 with custom mapping
python -m k8s-scan rec v1.20.15 10 10 10 10 10 10
```

## Custom recommendation mapping in depth
If you want a version with less of a certain vulnerability, give that vulnerability a much higher weight in the mapping. The help for the command can be seen below. The mapping is in the order of critical, high, medium, low, negligible, unknown. 

```bash
Usage: python -m k8s-scan rec [OPTIONS] VERSION [CRITICAL_MAPPING]
                              [HIGH_MAPPING] [MEDIUM_MAPPING] [LOW_MAPPING]
                              [NEGLIGIBLE_MAPPING] [UNKNOWN_MAPPING]

  recommend a less vulnerable version of Kubernetes based on input

Options:
  --help  Show this message and exit.
```

Some examples can be seen below. You do not have to use powers of 10.

```bash
# Looking for a version that has fewer critical vulnerabilities and you do not care about the rest
python -m k8s-scan rec VERSION 100 0 0 0 0 0

# Looking for a version where you do want critical, high, or medium and do not care about the rest
python -m k8s-scan rec VERSION 100 100 100 0 0 0

# Same scenario as above but you would prefer mediums then highs then criticals (in that order)
python -m k8s-scan rec VERSION 10000 1000 100 0 0 0

# Looking for a version but you care about each vulnerability, but would prefer lower vulnerabilities
python -m k8s-scan rec VERSION 100000 10000 1000 100 10 1

```
