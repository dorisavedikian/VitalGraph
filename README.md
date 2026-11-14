## Overview

VitalGraph began with a personal goal: documenting my Armenian ancestry and gathering the official records needed to apply for Armenian citizenship. According to guidance I received from the Armenian Consulate in Los Angeles, I need to establish an ancestor's Armenian ethnicity and a complete chain of kinship connecting that ancestor to me.

Simple enough, right? Not quite.

As I examined birth, marriage, and death certificates across several generations, I found differences in the names and other identifying details recorded for the same people. Fortunately, the records contain enough consistent evidence to document my Armenian ancestry and establish each family relationship connecting me to my ancestor. Other historical records point to Armenian origins. If I had to rely on those clues alone, I would need to look for additional ways to document my Armenian ethnicity.

I encountered a similar discrepancy when I accompanied a family member to the Social Security Administration (SSA). Information on their birth certificate differed from what SSA had on file.

I couldn't help but see a broader problem: **Why is connecting and reconciling information across official records so difficult?**

In an ideal world, vital records would already be represented using interoperable standards, persistent identifiers, and shared vocabularies, making it easier to connect information across systems and generations.

But we don't quite live in that world. So here I am, building my own multi-lingual knowledge graph. 

VitalGraph uses RDF, established ontologies, and Semantic Web technologies to connect historical records, represent family relationships, preserve provenance, and identify discrepancies without losing the original evidence. What began as a citizenship application has become a personal exploration of how linked data can make historical information more accessible, connected, and meaningful.

## Project Scope

The initial proof of concept focuses exclusively on birth, marriage and death certificates from family members.

The objective is to demonstrate how information from multiple certificates can be integrated into a unified knowledge graph to:

- Represent individuals and their relationships across generations.
- Connect people to significant life events, including births, marriages and deaths.
- Associate historical certificates with the events and individuals they document.
- Represent dates, places, occupations, and demographic information.
- Preserve information recorded in the original documents.
- Explore people, relationships, and recorded values in GraphDB.
- Query family relationships and their supporting certificates using SPARQL.
- Test natural-language questions with the Family Knowledge agent.

## Ontology and Terminology

VitalGraph reuses established ontologies and controlled vocabularies to represent information from family birth, marriage, and death certificates.

- **Records in Contexts Ontology (RiC-O 1.1)** provides the core graph structure for representing people, family relationships, life events, registration activities, and historical records, along with associated dates, places, occupations, and demographic information.
- **NCI Thesaurus (NCIt)** provides controlled identifiers for categorizing birth, death, and marriage events.
- **Person Ontology** provides properties for representing personal information, including names and gender.
- **FOAF** provides additional properties for representing personal information, including reported age.

**Armenian labels.** Armenian display labels are planned using `rdfs:label` with the `@hy` language tag. Original certificate text is preserved in the source graphs.

## Knowledge Graph Model

VitalGraph uses RiC-O and other established ontologies to represent people, family relationships, life events, and vital records in a connected knowledge graph. Each person has a unique, persistent identifier that connects information across multiple certificates.

Instance data is stored in TriG, with a default graph representing persistent person identities and record and event metadata and named graphs preserving individual certificates’ transcriptions and relationship evidence. This approach supports data provenance, preserves original source information, and accommodates discrepancies across records.

The Python build checks CSV structure and references. SPARQL checks confirm that expected relationships and recorded values appear in their supporting certificate graphs.

## Technologies and Standards

The project uses or plans to use the following technologies:

| Technology | Purpose |
| --- | --- |
| RDF / Turtle / TriG | Represent genealogical data and named graphs |
| OWL / RDFS | Reuse established ontologies and semantic definitions |
| SKOS | Represent controlled terminology where needed |
| SPARQL | Query family relationships and historical records |
| Python / RDFLib | Build TriG from the certificate CSVs |
| GraphDB Workbench | Import TriG, visualize the graph, and run SPARQL |
| Talk to Your Graph | Test natural-language questions through the Family Knowledge agent |

## Development Status

VitalGraph is being developed incrementally, starting with historical family birth, marriage, and death certificates. The pilot converts certificate transcriptions from CSV to TriG, preserving original wording and keeping each certificate’s evidence in its own named graph. GraphDB Workbench is used to visualize the dataset and run SPARQL queries that connect recorded values and family relationships to their supporting certificates.

The **Family Knowledge** agent is being tested through GraphDB’s **Talk to Your Graph** feature. Its natural-language answers are compared with verified SPARQL results to check that they return the recorded values and cite the correct certificates.

Later phases will add Armenian display labels and SHACL validation, extend provenance modeling, incorporate additional archival records, and explore interoperability with vital records standards.

See the [Development Roadmap](DEVELOPMENT.md) for details.