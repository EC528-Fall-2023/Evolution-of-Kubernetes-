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
2. https://drive.google.com/file/d/19RKdk28hIlycdg6E-IVRdQniK853RX3h/view?usp=drive_link
3. https://drive.google.com/file/d/1OckXILuWEGGWwAhdlucARE14L7jsiLW2/view?usp=drive_link
4. https://drive.google.com/file/d/1iot6vwi4wF8RssavVJ6McwnL0deej4fw/view?usp=sharing

## Slides 
1. https://docs.google.com/presentation/d/1g55eJtPw-Nqs4UGdct1RVzj7Tn9rZ_vOGkU5aett7ns/edit
2. https://docs.google.com/presentation/d/1zIL7WitdqtMgJpEo_-UIM9woRG7rn-oMftZ20LrrP9c/edit
3. https://docs.google.com/presentation/d/1UTrj0KQ0ppcm8Q9sv9N-m2D3Me5nAtBGVq8rKRGSyEg/edit?usp=drive_link
4. https://docs.google.com/presentation/d/1AmgHdyM-yIxjLIGZsndIq9-3fskL1LESKNORodOOZZ8/edit?usp=sharing


## 1. Vision and Goals Of The Project: 

### Background
Kubernetes is incredibly important in the modern cloud as it makes it easier for developers to manage their applications. It provides a framework to manage containerized applications and services, allowing for deployment and scheduling of containers while upholding scalability. Due to its use of open-source dependencies, the software stack of Kubernetes is vastly distributed and diverse making it challenging to maintain and update as new releases of stack components become available. 

### Goals
Our primary objective is to develop a method that provides Kubernetes developers with insights into possible vulnerabilities on both old and new releases of stack components. Key goals for this project include:

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
- Our application can help these cloud providers decide whether they want to support the newer versions as well or not

## 3. Scope and Features Of The Project:

- A script to collect all SBOMs of all versions of Kubernetes
- A parser to parse SBOMs for dependencies
- Storing the dataset of dependencies into a Neo4j graph database
- Designing and developing an analytical framework to extract useful insights from the data
- Users can use a CLI to pull useful information such as a list of dependencies of the current version, how many vulnerabilities each dependency has, and the severity of vulnerability of the dependency if the dependency is found in NIST (National Institute of Standards and Technology) NVD (National Vulnerability Database) and the OSV (Open Source Vulnerabilities) database
- Users would also be given a recommended version of a specified component depending on the data gathered regarding that component
- The end result should include data as an analysis over time. This includes information such as how many dependencies have changed on average. Why are they changing (Vulnerabilities being patched or just an update?), and the scope of change in dependencies (For example when comparing 1.20 vs 1.19, is it a big release or only a few dependencies changes?)
  
## 4. Solution Concept

![image](https://github.com/EC528-Fall-2023/Evolution-of-Kubernetes-/assets/34695547/6c1d214a-6d66-49a8-997c-e636e01b9274)

1. Kubernetes SBOM
- There exists an open-source program that generates a software bill of materials (SBOM) in SPDX or JSON format. Using this, we can create and collect the SBOMs of each Kubernetes version. Because the JSON format is more readable and easier to work with, we will be using that. 
- The SBOM is a list of components and dependencies that Kubernetes relies on.
- We define dependencies as all the packages that Kubernetes relies on, but are not made or maintained by Kubernetes themselves

2. Dependency Finder
- Parse the SBOMs into three CSV files 
- The first will be a list of all Kubernetes versions
- The second will be a list of dependencies of all Kubernetes versions
- The third will be a mapping of the Kubernetes version to the dependencies 
- We can pipeline the information from the CSV files into Neo4j and it should create a graph mapping our list of Kubernetes versions to their respective dependencies 

3. Neo4j
- Gathering historical data on these dependencies and components and modeling it in Neo4j.
- We chose to use a graph-type DB as it can help us track the version upgrades efficiently. For example, if versions 1.16 and 1.17 share the same dependencies as each other, they will share common nodes so if a common dependency is upgraded, we do not need to upgrade the dependencies for each of the versions, rather just upgrading one dependency node will upgrade it for all versions. 
- This lets us have a more efficient analytic query, as we only need one instance of each dependency and component. 

4. Analytic Framework
- Build a system to extract valuable insights
- Analyzing historical data and bringing insights about dependencies, vulnerabilities, release frequency, etc.
- Vulnerabilities can be analyzed using the NIST and OSV APIs, these APIs can be used to retrieve the list of vulneKubernetes from known components.

5. CLI
- The user will interact with our data through the use of a CLI by specifying a version to analyze, and what they would like to analyze
- Some basis for whether the next version is better than the current one includes security, and we can determine this through the use of CVSS (Common Vulnerability Scoring System), and only allowing low or no severity to pass through our recommendation
- Users can navigate the data visually through the Neo4j UI
- Results can also be shown as tables
- Refer to the CLI folder for more specific instructions

6. Extra
- Map the analysis over time onto a timeline UI
- Exploring the inclusion of third-party network and storage plugins if time allows, given Kubernetes' extensive ecosystem.

## 5. Acceptance criteria

Minimum Viable Product:

- Have SBOM of every version of Kubernetes
- A large dataset that's publicly accessible covering the software compositional evolution of Kubernetes with one level of dependency (meaning just the dependencies of Kubernetes)
- An analytical framework that can query each dependency and return the number of vulnerabilities and severity of vulnerability from the NIST and OSV databases
- Development of a CLI tool for users to visualize the data, and interact with our data
- Validate our end product with a Kubernetes development community, and see if our product resonates with them

Stretch Goals: 
- Implement a timeline UI (separate from graph database UI) to depict analysis results
- Also analyze the security posture of 5-6 tools within the Kubernetes Ecosystem (such as network plugins, container runtime tools(docker, runc), stack monitoring tools(Prometheus))

## 6. Release Planning:

### Sprint #1 (Sep 20 - Oct 3)
- Learn about the Kubernetes ecosystem, survey, and review the ecosystem.
- Start some architecture (how to collect data, how to store data, which database to use) not necessarily implementing.
- Begin designing the system's architecture 
- Look into the NIST API and Neo4j
- Extract all SBOMS


### Sprint #2 (Oct 4 - Oct 17)
- Establish the database infrastructure.
- Determine data storage mechanisms
- Begin querying vulnerabilities in the NIST API (and OSV API)
- Identify necessary APIs


### Sprint #3 (Oct 18 - Oct 31)
- Started to develop CLI Tool
- Deployed script
- Downloaded/extracted k8s sboms
- Generated SBOMS from container images using SYFT
- Generated vulerable pakcages from container images using GRYPE


### Sprint #4 (Nov 1 - Nov 14)
- Finish GRYPE/SYFT script 
- Import data into Neo4j
- Merge the Neo4j DB that has images, binaries and tar folders with the Neo4j DB that has dependeices
- Analyze the insights gained from the data
- Add more queries to CLI
  

### Sprint #5 (Nov 15 - Nov 28)
- Complete MVP
- Getting feedback and putting it into our application


