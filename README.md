# VitalGraph

**An RDF knowledge graph for genealogical research and historical vital records, built through the reuse and integration of established Semantic Web ontologies and controlled vocabularies.**

## Overview

VitalGraph began with a personal goal: documenting my Armenian ancestry and gathering the official records needed to apply for Armenian citizenship. According to guidance I received from the Armenian Consulate in Los Angeles, I need to establish an ancestor's Armenian ethnicity and a complete chain of kinship connecting that ancestor to me.

Simple enough, right? Not quite.

As I began examining birth, marriage, and death certificates across generations, I discovered discrepancies in names and identifying information, along with records that didn't explicitly document Armenian ethnicity. I encountered a similar issue when accompanying a family member to the Social Security Administration, where their birth certificate didn't match the information on file.

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
- Validate RDF data against defined structural constraints.
- Query family relationships and historical information using SPARQL.

## Ontology and Terminology

VitalGraph reuses established ontologies and controlled vocabularies to represent information from family birth, marriage, and death certificates.

- **Records in Contexts Ontology (RiC-O 1.1)** provides the core graph structure for representing people, family relationships, life events, registration activities, and historical records, along with associated dates, places, occupations, and demographic information.
- **NCI Thesaurus (NCIt)** provides controlled identifiers for categorizing birth, death, and marriage events.
- **Person Ontology** provides properties for representing personal information, including names and gender.
- **FOAF** provides additional properties for representing personal information, including reported age.

**Armenian labels.** VitalGraph uses `rdfs:label` with the `@hy` language tag to support Armenian-language labels alongside other languages, while preserving the original text recorded in certificates.

## Knowledge Graph Model

VitalGraph uses RiC-O and other established ontologies to represent people, family relationships, life events, and vital records in a connected knowledge graph. Each person has a unique, persistent identifier that connects information across multiple certificates.

Instance data is stored in TriG, with a default graph representing established identities and relationships and named graphs preserving information from individual certificates. This approach supports data provenance, preserves original source information, and accommodates discrepancies across records.

SHACL is used to validate the graph against defined structural and data quality constraints, supporting consistency, integrity, and traceability.

## Technologies and Standards

The project uses or plans to use the following technologies:

| Technology | Purpose |
| --- | --- |
| RDF / Turtle / TriG | Represent genealogical data and named graphs |
| OWL / RDFS | Reuse established ontologies and semantic definitions |
| SKOS | Represent controlled terminology where needed |
| SHACL | Validate graph structure and data constraints |
| SPARQL | Query family relationships and historical records |
| Python / RDFLib | Construct, validate, and query RDF datasets |

## Development Status

VitalGraph is being developed incrementally, beginning with an RDF knowledge graph constructed from historical family birth, marriage, and death certificates. Initial development focuses on ontology reuse, data integration, provenance, SHACL validation, and SPARQL querying.

Future work will expand provenance modeling, incorporate additional archival records, and explore interoperability with vital records standards. The project will also evaluate integrating the OpenAI API to support natural-language questions grounded in the knowledge graph and its supporting source records.

See the [Development Roadmap](DEVELOPMENT.md) for planned extensions.