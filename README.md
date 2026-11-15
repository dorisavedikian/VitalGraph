## Overview

VitalGraph began with a personal goal: documenting my Armenian ancestry and gathering the official records needed to apply for Armenian citizenship. According to guidance I received from the Armenian Consulate in Los Angeles, I need to establish an ancestor's Armenian ethnicity and a complete chain of kinship connecting that ancestor to me. I also need every document for my application translated into Armenian.

Simple enough, right? Not quite.

I went through birth, marriage, and death certificates across several generations. Sometimes two records that pointed to the same person gave different names or disagreed on other details. I eventually found enough evidence to document my ancestor’s Armenian ethnicity and trace each generation down to me. What stuck with me was how much of that work came down to piecing together what each record actually said.

I ran into the same kind of problem when I went with a family member to the Social Security Administration. What SSA had on file differed from what was on their birth certificate.

I couldn't help but see a broader problem: **Why is connecting and reconciling information across official records so difficult?**

I started thinking about what would have made the process easier. In an ideal world, vital records would already use interoperable standards, persistent identifiers, and shared vocabularies with labels in multiple languages. That would make it easier to connect records across government systems and generations, even when names are spelled differently. I could explore those records in Armenian, still see exactly what each certificate says, and assemble the evidence I need for my citizenship application.

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

VitalGraph reuses [subsets](/Volumes/SIROD/development/vitalGraph/ontology) of established ontologies and controlled vocabularies to represent information from family birth, marriage, and death certificates.

- **Records in Contexts Ontology (RiC-O 1.1)** provides the core graph structure for people, family relationships, life events, registration activities, and historical records, along with dates, places, occupations, and demographic information. [RiC-O 1.1 reference](https://www.ica.org/standards/RiC/RiC-O_1-1.html)
- **NCI Thesaurus (NCIt)** provides controlled identifiers for categorizing birth, marriage, and death events. [NCIt browser](https://evsexplore.semantics.cancer.gov/evsexplore/overview)
- **Person Ontology** provides properties for representing names and gender. [Person Ontology reference](https://w3id.org/MON/person.owl)
- **FOAF** provides the `foaf:age` property for representing reported age. [FOAF vocabulary specification](https://xmlns.com/foaf/spec/#term_age)

**Armenian labels.** Armenian display labels are planned using `rdfs:label` with the `@hy` language tag. Original certificate text is preserved in the source graphs.

## Knowledge Graph Model

VitalGraph uses RiC-O and other established ontologies to represent people, family relationships, life events, and vital records in a connected knowledge graph. Each person has a unique, persistent identifier that connects information across multiple certificates.

Instance data is stored in TriG, with a default graph representing persistent person identities and record and event metadata and named graphs preserving individual certificates’ transcriptions and relationship evidence. This approach supports data provenance, preserves original source information, and accommodates discrepancies across records.

The [model reference](ontology/model-reference.txt) summarizes the classes, properties, and controlled terms used to represent people, relationships, life events, and certificates.

The [single-person example](data-compiled/data_instances/single-person.txt) uses placeholders to illustrate how VitalGraph structures data for one person across birth, marriage, and death certificates. The default graph uses a unique person identifier to link that person to all three life events and their corresponding records. Each certificate’s named graph uses the same identifier and preserves the details and relationships documented by that source.

## Technologies and Standards

The project uses or plans to use the following technologies:

| Technology | Purpose |
| --- | --- |
| [RDF](https://www.w3.org/TR/rdf11-concepts/) | Represent people, relationships, events, and records as triples |
| [Turtle](https://www.w3.org/TR/turtle/) | Write individual RDF graphs in a readable text format |
| [TriG](https://www.w3.org/TR/trig/) | Store the default graph and certificate-specific named graphs in one dataset |
| [OWL](https://www.w3.org/TR/owl2-overview/) / [RDFS](https://www.w3.org/TR/rdf-schema/) | Reuse established ontologies and semantic definitions |
| [SKOS](https://www.w3.org/TR/skos-reference/) | Represent controlled terminology where needed |
| [SPARQL](https://www.w3.org/TR/sparql11-overview/) | Query family relationships and historical records |
| [Python](https://docs.python.org/3/) / [RDFLib](https://rdflib.readthedocs.io/) | Build TriG from the certificate CSVs |
| [GraphDB Workbench](https://graphdb.ontotext.com/documentation/10.8/working-with-workbench.html) | Import TriG, visualize the graph, and run SPARQL |
| [Talk to Your Graph](https://graphdb.ontotext.com/documentation/11.5/talk-to-graph.html) | Test natural-language questions through the Family Knowledge agent |

## Development Status

VitalGraph is being developed incrementally, starting with historical family birth, marriage, and death certificates. The pilot reuses established ontologies and converts certificate transcriptions from CSV to TriG. It preserves the original wording and keeps each certificate’s evidence in its own named graph. GraphDB Workbench is used to visualize the dataset and run SPARQL queries that trace recorded values and family relationships to their supporting certificates.

The **Family Knowledge** agent uses GraphDB’s **Talk to Your Graph** feature to answer natural-language questions. Its answers are tested against verified SPARQL results to check that they report the recorded values and cite the correct certificates.

Next, I plan to add the eight remaining family certificates and capture more of what they document, including residences, medical information, and burial details. I also plan to automate data entry from scanned PDFs, spreadsheets, and CSV files by mapping source data into the existing CSV-to-RDF workflow.

Later work will add family photographs and use the National Archives Catalog API to find immigration, naturalization, and military service records. The roadmap also covers Armenian display labels, SHACL validation, expanded provenance, and interoperability with vital-records standards.

See the [Development Roadmap](DEVELOPMENT.md) for details.