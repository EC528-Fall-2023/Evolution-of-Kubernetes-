# Understanding compositional evolution of Kubernetes

## Collaborators

| Role      | Name               | Email                      |
| --------- | ------------------ | -------------------------- |
| Mentor    | Shripad J Nadgowda | shripad.nadgowda@intel.com |
| Developer | Jeffrey Chen       | jchen25@bu.edu             |
| Developer | Jinqi Lu (Kevin)   | jinqilu@bu.edu             |
| Developer | Johnson Yang       | johnsony@bu.edu            |
| Developer | Saurabh Singh      | saurabh2@bu.edu            |
| Developer | Usman Jalil        | ujalil@bu.edu              |

## Sprint Demo Videos
1. https://drive.google.com/file/d/13ZRfemcwVMjYKPPgBF-aMuAYyIu4Uj0r/view?usp=drive_link

## 1. Vision and Goals Of The Project: 

### Background
Kubernetes is incredibly important in the modern cloud as it makes it easier for developers to manage their applications. It provides a framework to manage containerized
applications and services, allowing for deployment and scheduling of containers while upholding scalability. Due to its nature, the software stack of Kubernetes is vastly distributed 
and diverse making it challenging to maintain and update as new releases of stack components become available. 

### Goals
Our primary objective is to develop a method that provides Kubernetes developers with insights into possible vulnerabilities, and other information on both old and new releases of stack components. Key goals for this project include:

- Collecting data about Kubernetes software components 
- Analyzing the chronological evolution of their dependencies
- Building an analytical framework to bring useful insights from this data
- Create a tool for users to view and interact with our analyzed data

## 2. Users/Personas Of The Project:
This project focuses on identifying vulnerabilities and gaps in Kubernetes components, making it relevant to mostly those who plan on developing and maintaining Kubernetes. By knowing which version of each stack component is less vulnerable, developers and maintainers can use those versions to make Kubernetes more secure. By extension, cloud providers generally have APIs that connect to Kubernetes, so a safer Kubernetes would also benefit cloud providers. 

Kubernetes development/maintainers teams
- People who develop Kubernetes would want to see data on their stack components as it lets them know whether they want to upgrade the component to the newest version or the current version is more secure
- People who maintain Kubernetes would like to see the history of these stack components, and they may find a vulnerability in an older version that they might want to patch up 

Cloud providers
- Such as Microsoft Azure, AWS, or Google Cloud
- Google Kubernetes Engine currently only supports up to 1.27.6, the newest version as of October 2023 is up to 1.29 (https://endoflife.date/google-kubernetes-engine) meanwhile Amazon has only started supporting version 1.28 in September of 2023 (https://aws.amazon.com/blogs/containers/amazon-eks-now-supports-kubernetes-version-1-28/).
- Generally, cloud providers use older versions as they have been thoroughly tested for safety while newer versions have not
- Our application can help these cloud providers ascertain whether the new version is an upgrade or not

## 3. Scope and Features Of The Project:

- A script to collect all SBOMs of all versions of Kubernetes
- A parser to parse SBOMs for dependencies
- Storing the dataset of dependencies into a Neo4j graph database
- Designing and developing an analytical framework to extract useful insights from the data
- Users can use a CLI to pull useful information such as a list of dependencies of the current version, how many vulnerabilities each dependency has, and the severity of vulnerability of the dependency if the dependency is found in NIST (National Institute of Standards and Technology) NVD (National Vulnerability Database)
- Users can also be given a recommendation, they will be recommended a version with fewer vulnerabilities
- Because the dependencies making up the Kubernetes SBOM may have their dependencies, and those dependencies may also have their dependencies and so on, for the scope of this project, we have chosen to go at least 2-3 levels deep maximum, 1 level minimum.
  
## 4. Solution Concept

![arch_diagram](https://github.com/EC528-Fall-2023/Evolution-of-Kubernetes-/assets/76934261/57b79a18-efa7-41d9-a48d-2bd58d12a4f3)

1. Kubernetes SBOM
- There exists an open-source program that generates a software bill of materials (SBOM) in SPDX form. Using this, we can create and collect the SBOM.
- The SBOM is a list of components and dependencies that Kubernetes relies on.
- We define dependencies as all the packages that Kubernetes relies on, but are not made or maintained by Kubernetes themselves

2. Dependency Finder
- Parse the SBOMs into CSV files into three files
- The first will be a list of all Kubernetes versions
- The second will be a list of dependencies of all Kubernetes versions
- The third will be a mapping of the Kubernetes version to the dependencies 
- We can pipeline these cvs into Neo4j and it should create a graph mapping our list of Kubernetes versions to their respective dependencies 

3. Neo4j
- Gathering historical data on these dependencies and components and modeling it in neo4j.
- We chose to use a graph-type DB as it can help us track the version upgrades efficiently. For example, if versions 1.16 and 1.17 share the same dependencies as each other, they will share common nodes so if a common dependency is upgraded, we do not need to upgrade the dependencies for each of the versions, rather just upgrading one dependency node will upgrade it for all versions. 
- This lets us have a more efficient analytic query, as we only need one instance of each dependency and component. 

4. Analytic Framework
- Build a system to extract valuable insights
- Analyzing historical data and bringing insights about dependencies, vulnerabilities, release frequency, etc.
- Vulnerabilities can be analyzed using the NIST CVE API, this API can be used to retrieve the list of vulneKubernetes from known components.
- Then we can use GitHub API for data like release frequency, number of commits, and the like.

5. CLI
- The user will interact with our data through the use of a CLI.
- Using commands such as “k8s-scan --eval --current=1.17.0” will evaluate the security posture of your current version which in this case is version 1.17.0.
- Or if the user is using 1.16.9 the command “k8s-scan --recommend --current=1.16.9” can recommend the next best version after their current version.
- Furthermore, the CLI should be able to analyze versions until a certain version, in this case, 1.16.0 using the command “k8s-scan --analyze --current=1.16.0 --deps” will do that. 
- Some basis for whether the next version is better than the current one includes security, and we can determine this through the use of CVSS (Common Vulnerability Scoring System), and only allowing low or no severity to pass through our recommendation. 

6. Extra
- Exploring the inclusion of third-party network and storage plugins if time allows, given Kubernetes' extensive ecosystem.

## 5. Acceptance criteria

Minimum Viable Product:

- Have SBOM of every version of Kubernetes
- A large dataset that's publicly accessible covering the software compositional evolution of Kubernetes with one level of dependency (meaning just the dependencies of Kubernetes)
- An analytical framework that can query each dependency and return the number of vulnerabilities and severity of vulnerability from the NIST NVD, and use GitHub API for other information such as the number of commits, and the percentage that is unreviewed
- Development of a CLI tool for users to visualize the data, and interact with our data
- Validate our end product with a Kubernetes development community, and see if our product resonates with them

Stretch Goals: 

- Include up to 2-3 layers of dependencies in our Neo4j database, and run our analysis tools through those as well

## 6. Release Planning:

### Sprint #1 (Sep 20 - Oct 3)
- Learning about the Kubernetes ecosystem, survey, and review the ecosystem.
- Start some architecture (how to collect data, how to store data, which database to use) not necessarily implementing.

### Sprint #2 (Oct 4 - Oct 17)
- Establish the database infrastructure.
- Determine data storage mechanisms
- Create a Proof of Concept (POC)
- Begin designing the system's architecture
- Divide tasks among team members
- Identify necessary APIs

### Sprint #3 (Oct 18 - Oct 31)
- Develop the system 
- Deliver the first MVP
- Ensure data is accessible and queryable

### Sprint #4 (Nov 1 - Nov 14)
- Fine-tune the system.
- Develop a CLI tool and analytics features.
- Analyze the insights gained from the data.

### Sprint #5 (Nov 15 - Nov 28)
- Getting feedback and putting it into our application
