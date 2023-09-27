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


## 1. Vision and Goals Of The Project: 
Our primary objective is to develop a method that provides Kubernetes users with insights into the impacts of new releases. Key goals for this project include:

- Collecting data about Kubernetes software components 
- Analyzing the chronological evolution of their dependencies
- Building an analytical framework to bring useful insights from this data
- Assisting existing users for their onward journey from our insights

## 2. Users/Personas Of The Project:
This project focuses on identifying vulnerabilities and gaps in Kubernetes maintenance, making it relevant to a wide range of users, including:

- Kubernetes development/maintainers teams
- Cloud providers

## 3. Scope and Features Of The Project:
- Collecting and analyzing historical data related to Kubernetes’ software components, their dependencies, and how they have evolved over time. 
- Storing the dataset into a Neo4j graph database
- Designing and developing an analytical framework to extract useful insights from the data

## 4. Solution Concept
Our solution involves several stages:

- Creation and collection of a software bill of materials (SBOM) for Kubernetes (supported from version 1.18 onwards). This includes listing the components and dependencies that Kubernetes relies on.
- Gathering historical data on these dependencies and components, followed by data modeling.
- Building a system to extract valuable insights:
    - Analyzing historical data and bring insights about dependencies, vulnerabilities, release frequency, etc.
    - Assessing the user's current software version and determining whether they should evaluate that version or consider upgrading to the next version.
- Exploring the inclusion of third-party network and storage plugins if time allows, given Kubernetes' extensive ecosystem.

## 5. Acceptance criteria
- A large dataset that's publicly accessible covering the software compositional evolution of Kubernetes. 
- Development of a CLI tool for users to visualize the data, and interact with our data
- Validate our end product with a kubernetes development community, see if our product resonates with them

## 6. Release Planning:
### Sprint #1 (Sep 20 - Oct 3)
- Learning about Kubernetes ecosystem, survey, and review the ecosystem.
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
