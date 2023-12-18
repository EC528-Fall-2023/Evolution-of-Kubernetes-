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
5. https://drive.google.com/file/d/19VJi6bQ8xvRXiXvO3ERp-DK-vOgiNeaG/view?usp=sharing

## Slides 
1. https://docs.google.com/presentation/d/1g55eJtPw-Nqs4UGdct1RVzj7Tn9rZ_vOGkU5aett7ns/edit
2. https://docs.google.com/presentation/d/1zIL7WitdqtMgJpEo_-UIM9woRG7rn-oMftZ20LrrP9c/edit
3. https://docs.google.com/presentation/d/1UTrj0KQ0ppcm8Q9sv9N-m2D3Me5nAtBGVq8rKRGSyEg/edit?usp=drive_link
4. https://docs.google.com/presentation/d/1AmgHdyM-yIxjLIGZsndIq9-3fskL1LESKNORodOOZZ8/edit?usp=sharing
5. https://docs.google.com/presentation/d/1N0XLtZRzZZPRJ7e_dLIAeLBIfQEIo5b2en3o4dZNekw/edit?usp=sharing

## Final Presentation
- Slides: https://docs.google.com/presentation/d/111rjcjIpRUrm66KTL0s7DLwvaXM5tL32xusVaPkmevY/edit?usp=sharing
- Video: https://drive.google.com/file/d/1hH2lV2tA4Uf3NrLAzUNJ_YGq4g82V3Hz/view?usp=drive_link

## 1. Vision and Goals Of The Project: 

### Background
Kubernetes is incredibly important in the modern cloud as it makes it easier for developers to manage their applications. It provides a framework to manage containerized applications and services, allowing for deployment and scheduling of containers while upholding scalability. Due to its use of open-source dependencies, the software stack of Kubernetes is vastly distributed and diverse making it challenging to maintain and update as new releases of stack components become available. 

### Goals
Our primary objective is to develop a method that provides Kubernetes developers with insights into possible vulnerabilities on both old and new releases of stack components. Key goals for this project include:

- Collecting data about Kubernetes software components
- Analyzing the chronological evolution of their vulnerabilities
- Create a tool for users to view and interact with our analyzed data
- Implement a timeline UI to depict analysis results


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
- Users can use a CLI to retrieve useful information such as a list of dependencies of the current version, how many vulnerabilities each dependency has, and the severity of vulnerability of the dependency if the dependency is found in NIST (National Institute of Standards and Technology) NVD (National Vulnerability Database) and the OSV (Open Source Vulnerabilities) database
- Users would also be given a recommended version of a specified component depending on the data gathered regarding that component
- The end result should include data as an analysis over time. This includes information such as how many dependencies have changed on average. Why are they changing (Vulnerabilities being patched or just an update?), and the scope of change in dependencies (For example when comparing 1.20 vs 1.19, is it a big release or only a few dependencies changes?)

## 4. Kubernetes SBOM Structure
![Screenshot 2023-12-10 at 9 18 18 PM](https://github.com/EC528-Fall-2023/Evolution-of-Kubernetes-/assets/74789609/157e1289-afbe-43b9-8ac1-92fde8ff48e3)
## 5. Solution Concept
![Screenshot 2023-12-10 at 9 28 36 PM](https://github.com/EC528-Fall-2023/Evolution-of-Kubernetes-/assets/74789609/4e8e3b6d-be53-4038-ae2d-851c263de7f7)


1. Kubernetes SBOM
- There exists an open-source program that generates a software bill of materials (SBOM) in SPDX or JSON format. Using this, we can create and collect the SBOMs of each Kubernetes version. Because the JSON format is more readable and easier to work with, we will be using that. 
- The SBOM is a list of components and dependencies that Kubernetes relies on.
- We define dependencies as all the packages that Kubernetes relies on, but are not made or maintained by Kubernetes themselves

2. Grype & Syft
- Python script to iterate through SBOMs and fetch images
- Grype tool to scan images for vulnerabilities
- Syft tool to scan images for additonal dependencies
- Remove fetched images after scanning

4. Neo4j
- Gathering historical data on these dependencies and components and modeling it in Neo4j.
- We chose to use a graph-type DB as it can help us track the version upgrades efficiently. For example, if versions 1.16 and 1.17 share the same dependencies as each other, they will share common nodes so if a common dependency is upgraded, we do not need to upgrade the dependencies for each of the versions, rather just upgrading one dependency node will upgrade it for all versions. 
- This lets us have a more efficient analytic query, as we only need one instance of each dependency and component.
- Hosted on the cloud to circumvent problems with free Neo4j instances (such as automatic pausing of database after a few days, limited nodes and storage)

4. API Server
- Query data from Neo4j
- Limited querying options
- Used to hide our Neo4j instance
- Documentation can be found here: https://k8svul.asleague.org/docs

5. CLI Tool
- Queries data from Neo4j DB through API calls to our API server
- Analyzing historical data and bringing insights about dependencies, vulnerabilities, etc.
- The user will interact with our data through the use of a CLI by specifying a version to analyze, and what they would like to analyze
- Some basis for whether the next version is better than the current one includes the frequency of severity level (how many criticals, how many highs, etc)
- Results can also be shown as tables
- Refer to the CLI folder for more specific instructions

6. Visual UI
- Stacked bar graph depecting vulnerabilities of each Kubernetes version
- React.js frontend, fetches data from API and hosted on [GitHub Pages](https://ec528-fall-2023.github.io/Evolution-of-Kubernetes-/)
- Separate vulnerabilties by a.) severity, or b.) discovered before vs after respective Kubernetes version

7. Extra
- Map the analysis over time onto a timeline UI
- Exploring the inclusion of third-party network and storage plugins if time allows, given Kubernetes' extensive ecosystem.

## 6. Acceptance criteria

Minimum Viable Product:

- SBOMs of every version of Kubernetes
- Collection of vulnerabilities of images found in SBOMs
- Publicly available dataset of collected data
- Developed API to query each dependency for number and severity of vulnerabilities
- CLI tool to allow users to interact with collected data


Stretch Goals: 
- Visual UI to depict analysis results
- Investigate other tools within the K8s ecosystem (Docker, runc, Prometheus, etc.)
- Validate our end results with the Kubernetes development community

## 7. Release Planning:

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
- Finish collecting data with GRYPE/SYFT script
- Create NIST script to collect entry dates and descriptions of vulnerabilities
- Import data into Neo4j and merge data
- Add more queries to CLI
  

### Sprint #5 (Nov 15 - Nov 28)
- Create and deploy [Interactive UI](https://ec528-fall-2023.github.io/Evolution-of-Kubernetes-/) to present vulnerability data
- Extract dates of kuberentes versions and vulnerability entries
- Implement vulnerability searching and scoring for CLI
- Implement reverse proxy on cloud VM to expose neo4j instance


