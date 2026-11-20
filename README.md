## Overview

VitalGraph began with a personal goal—documenting my Armenian ancestry and gathering records for Armenian citizenship. According to guidance I received from the Armenian Consulate in Los Angeles, I need to establish an ancestor’s Armenian ethnicity, document the chain of kinship connecting that ancestor to me, and have every application document translated into Armenian.

Simple enough, right? Not quite.

I spent hours at the county records office in Fresno, searching for birth, marriage, and death certificates under different spellings of family members’ names. A spelling variation could mean finding a record or overlooking it.

Then I had to connect the certificates across generations. Names and other details sometimes differed for the same person, making family relationships harder to establish. I eventually gathered enough evidence through my maternal grandfather to document his Armenian ethnicity and trace the relationships down to me.

I encountered a similar problem when accompanying a family member to the Social Security Administration. What SSA had on file differed from their birth certificate.

I couldn't help but see a broader problem. **Why is connecting and reconciling information across official records so difficult?**

The certificates were created decades apart, using the forms and technology of their time. It makes sense that connecting them takes detective work, but I started thinking about what could make it easier.

In an ideal world, vital records would already use interoperable standards, persistent identifiers, and shared vocabularies with multilingual labels. That would help connect records across systems and generations despite spelling differences, and perhaps identify discrepancies earlier. I could explore the information in Armenian while seeing exactly what each certificate says. The institution reviewing my application could follow those same connections and check the evidence.

But we don't quite live in that world yet. So here I am, building my own multilingual knowledge graph.

When I told my sister about this, she said, “Can’t you just ask Google?” I said, “Google doesn’t have the records I’ve gathered or know how I’ve connected them. It wouldn’t know that Humige, Harry, and Henry refer to the same person, or that a misspelling of our paternal grandparents’ surname originated in Lebanon.” That conversation helped shape the Family Knowledge chatbot. Its goal is to answer from the connected records, identify the supporting documents, and make clear when evidence is incomplete or records disagree.

What began with a citizenship application has become a way for me to explore what linked data can do for my family history.

## Project Scope

The initial proof of concept focuses on family birth, marriage, and death certificates. The current pilot contains five certificates—three birth, one death, and one marriage.

The objective is to demonstrate how information from multiple certificates can be integrated into a unified knowledge graph to:

- Represent individuals and their relationships across generations.
- Connect people to significant life events, including births, marriages and deaths.
- Associate historical certificates with the events and individuals they document.
- Represent dates, places, occupations, and demographic information.
- Preserve the information recorded in the original documents.
- Explore people, relationships, and recorded values in GraphDB.
- Query family relationships and their supporting certificates using SPARQL.
- Test natural-language questions with the Family Knowledge agent.

Person identities are assigned and reviewed manually. The pipeline reuses those identifiers across certificates.

## Ontology and Terminology

VitalGraph reuses [subsets](ontology) of established ontologies and controlled vocabularies to represent information from family birth, marriage, and death certificates.

- **Records in Contexts Ontology (RiC-O 1.1)** provides the core model for people, family relationships, life events, registration activities, and historical records. [Official RiC-O documentation](https://ica-egad.github.io/RiC-O/) · [RiC-O 1.1 ontology reference](https://www.ica.org/standards/RiC/RiC-O_1-1.html)
- **NCI Thesaurus (NCIt)** provides controlled identifiers for categorizing birth, marriage, and death events. [NCIt browser](https://evsexplore.semantics.cancer.gov/evsexplore/welcome?terminology=ncit)
- **Person Ontology** provides properties for representing names and gender. [Person Ontology reference](https://w3id.org/MON/person.owl)
- **FOAF** provides the `foaf:age` property for representing reported age. [FOAF vocabulary specification](https://xmlns.com/foaf/spec/)

**Armenian labels.** Armenian display labels are planned using `rdfs:label` with the `@hy` language tag. Original certificate text is preserved in the source graphs.

## Knowledge Graph Model

Each person has a persistent identifier that connects their appearances across certificates. A person can have a registry name while individual certificates preserve different recorded names and other details.

The dataset is stored in TriG. The default graph contains the person registry, record metadata, life events, registration activities, and links identifying record subjects and event participants. Each certificate’s named graph contains its transcribed values and relationship evidence.

The model distinguishes a life event from its registration activity. People participate in birth, marriage, and death events, while certificates document the corresponding registration activities.

Dates, places, occupations, and demographic groups are represented as resources, with their recorded wording stored inside the relevant certificate graph. Parent and spouse relationships are also asserted within the certificate graph that supplies the evidence.

This structure preserves differences in spellings, ages, places, and demographic values across records while allowing each certificate-specific statement to be traced to its supporting record.

The [model reference](ontology/model-reference.txt) summarizes the classes, properties, and controlled terms used in VitalGraph.

The [single-person example](data-compiled/data_instances/single-person.txt) is a structural template containing placeholders. It illustrates how one persistent person identifier connects appearances across birth, marriage, and death records, with source-specific details in each certificate’s named graph.

The [CSV data dictionary](data-compiled/CSV-DATA-DICTIONARY.md) explains how to enter certificate data, reuse person identifiers, and map CSV fields to RDF.

## Visuals

- [Application Profile — Classes and Relationships](diagrams/VitalGraph-ApplicationProfile-Classes%26Relationships.pdf) shows the classes, relationships, and recorded-value fields used in VitalGraph.
- [UML Diagram](diagrams/VitalGraph-Application-Profile.png) provides the application profile as a UML diagram.
- [Model and Example Records](diagrams/VitalGraph-Model&Example-person-001.png) connects ontology definitions to example people and records.
- [Five-Certificate Pilot](diagrams/VitalGraph-Five-Certificate-Pilot.png) shows the populated graph with family relationships and recorded values.

## Technologies and Standards

| Technology | Purpose |
| --- | --- |
| [RDF](https://www.w3.org/TR/rdf11-concepts/) | Represent people, relationships, events, and records as triples |
| [Turtle](https://www.w3.org/TR/turtle/) | Store ontology subsets as individual RDF graphs |
| [TriG](https://www.w3.org/TR/trig/) | Store the default graph and certificate-specific named graphs in one dataset |
| [OWL](https://www.w3.org/TR/owl2-overview/) / [RDFS](https://www.w3.org/TR/rdf-schema/) | Reuse established classes, properties, hierarchies, and semantic definitions |
| [SPARQL](https://www.w3.org/TR/sparql11-overview/) | Query records, family relationships, recorded values, and supporting certificates |
| [Python](https://docs.python.org/3/) / [RDFLib](https://rdflib.readthedocs.io/) | Build the TriG dataset from certificate CSVs |
| [GraphDB Workbench](https://graphdb.ontotext.com/documentation/11.5/working-with-workbench.html) | Import TriG, visualize the graph, and run SPARQL queries |
| [Talk to Your Graph](https://graphdb.ontotext.com/documentation/11.5/talk-to-graph.html) | Test natural-language questions through the Family Knowledge agent |
| [PlantUML](https://plantuml.com/) | Maintain an editable class and relationship diagram |

SKOS is being considered for future controlled terminology. SHACL validation is planned for a later development phase.

## Development Status

The CSV-to-TriG pipeline is working for the five-certificate pilot. GraphDB Workbench supports visualization and SPARQL queries, which have been used to check recorded values, family relationships, and their supporting certificates.

The **Family Knowledge** agent uses GraphDB’s **Talk to Your Graph** feature, with autocomplete for name discovery. Its answers are checked against verified SPARQL results to identify errors in relationship direction, graph scope, and value retrieval. A [sample conversation](https://dorisavedikian.github.io/VitalGraph/) documents the testing.

Next steps include adding the eight remaining certificates, capturing residence, medical, and burial details, and automating intake from scans and spreadsheets with manual review.

Later work includes civil, medical and church records from Syria and Lebanon, plus searches for immigration, naturalization, and military service records through the National Archives Catalog API. Plans also include Armenian labels, validation, provenance enhancements, and exploring mappings to HL7 FHIR vital-records reporting standards.

See the [Development Roadmap](DEVELOPMENT.md) for details.