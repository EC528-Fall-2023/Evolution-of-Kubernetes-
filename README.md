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


## 1.Vision and Goals Of The Project: ww
Our main goal is to create a method for users of Kubernetes to have insight on the effects of new releases. 

Some goals of this project include:
- Gather data about Kubernetes software components 
- Measure chronological evolution of their dependencies
- Build an analytic framework to bring useful insights from this data
- Helping existing users for their onward journey from our insights

## 2.Users/Personas Of The Project:
Our project is a deep dive into the vulnerabilities and gaps in maintenance of kubernetes, therefore our core user base will be any developer who uses Kubernetes.

It targets:
- Kubernetes development/maintainers teams
- Kubernetes users
- Third party enterprise users

## 3.Scope and Features Of The Project:
- Collecting and analyzing historical data related to Kubernetes’ software components, their dependencies, and how they have evolved over time. 
- Store dataset using a graphQL database
- Design and develop an analytical framework to extract useful insights from the data

## 4.Solution Concept
Our solution will start with creating/collecting a software bill of materials (SBOM) of Kubernetes (1.18 version onwards support SBOM).
This is basically a list of components and dependencies that the software, in our case ,Kubernetes, rely on. 
Then gather data on the history of these dependencies and components, and model the data. 
Finally, we would like to build a system to extract useful insights from the data to pass on to our users, such data includes, a sufficient version of Kubernetes for our users that covers their needs, whether a certain version is more secure than a different version, etc. 
Furthermore, because Kubernetes have a massive ecosystem with many third party, independent projects, not maintained by Kubernetes itself, if time permits we will expand our data collection to include these third party network and storage plugins.

## 5.Acceptance criteria
- A large dataset that's publicly accessible covering the software compositional evolution of Kubernetes. 
- Build CLI for users to visualize the data, and interact with our data
- Validate our end product with a kubernetes development community, see if our product resonates with them

## 6.Release Planning:
First Sprint (groundwork)
- Learning about Kubernetes ecosystem, survey, and review the ecosystem.
- Start some architecture (how to collect data, how to store data, which database to use) not necessarily implementing.

Second sprint: (building foundations)
- Set up database
- Figure out how to store data
- POC
- Bootstrapping design
- Building up system/architecture
- Divison of work
- What APIs to use?

Third sprint:  
- Building system 
- First MVP
- Have data, queriable, 

Fourth Sprint
- Fine tune 
- Build CLI, analytics, What are we learning from data?

Fifth Sprint
- Getting feedback and putting it into our application
