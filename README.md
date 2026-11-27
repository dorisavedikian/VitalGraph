## Overview

VitalGraph began with a personal goal—documenting my Armenian ancestry for a citizenship application. The Armenian Consulate in Los Angeles advised me to establish an ancestor’s Armenian ethnicity, document the chain of kinship connecting that ancestor to me, and have the application documents translated into Armenian.

Simple enough, right? Not quite.

I spent hours at the county records office in Fresno searching for birth, marriage, and death certificates under different spellings of family members’ names. Connecting those records across generations meant reconciling names and other details. I eventually gathered enough evidence through my maternal grandfather to document his Armenian ethnicity and trace the relationships down to me.

I encountered a similar problem while accompanying a family member to the Social Security Administration. What SSA had on file differed from their birth certificate.

I couldn't help but see a broader problem.

**Why is connecting and reconciling information across official records so difficult?**

In an ideal world, vital records would use interoperable standards, persistent identifiers, and shared vocabularies with multilingual labels. That would help connect records across systems and generations despite spelling differences, and perhaps identify discrepancies earlier. I could explore my family’s records in Armenian, follow the connections across generations, and see exactly which documents support them. Someone reviewing my application could follow that same evidence.

But we don't quite live in that world yet. So here I am, building my own multilingual knowledge graph.

When I told my sister, she asked, “Can’t you just ask Google?” I explained that Google wouldn’t have the records I’d gathered or the connections I’d worked out—that Humige, Harry, and Henry referred to the same person, or that a misspelling of our paternal grandparents’ surname originated in Lebanon.

That conversation helped shape the Family Knowledge chatbot. Its goal is to answer questions from the connected records, identify the supporting records, and show where information is missing or conflicting.

What began with a citizenship application has become a way for me to explore what linked data can do for my family history.

## Project Scope

The initial proof of concept focuses on family birth, marriage, and death certificates. 

The objective is to demonstrate how information from multiple certificates can be integrated into a unified knowledge graph to:

- Represent individuals and their relationships across generations.
- Connect people to significant life events, including births, marriages and deaths.
- Associate historical certificates with the events and individuals they document.
- Represent dates, places, occupations, and demographic information.
- Preserve the information recorded in the original documents.
- Explore people, relationships, and recorded values in GraphDB.
- Query family relationships and their supporting certificates using SPARQL.
- Test natural-language questions with the Family Knowledge agent.

## Privacy

The repository includes diagrams, screenshots, and sample conversations that show selected information from the family graph. The underlying certificates, CSV transcriptions, and populated RDF dataset are excluded to protect family members’ privacy.

The [single-person example](data-compiled/data_instances/single-person.trig) contains placeholders and illustrates how one person identifier connects appearances across hypothetical birth, marriage, and death records, with details preserved in each certificate’s named graph.

## Ontology and Terminology

VitalGraph reuses [subsets](ontology) of established ontologies and controlled vocabularies to represent information from family birth, marriage, and death certificates.

- **Records in Contexts Ontology (RiC-O 1.1)** provides the core model for people, family relationships, life events, registration activities, and historical records. [Official RiC-O documentation](https://ica-egad.github.io/RiC-O/) · [RiC-O 1.1 ontology reference](https://www.ica.org/standards/RiC/RiC-O_1-1.html)
- **NCI Thesaurus (NCIt)** provides controlled identifiers for categorizing birth, marriage, and death events. [NCIt browser](https://evsexplore.semantics.cancer.gov/evsexplore/welcome?terminology=ncit)
- **Person Ontology** provides properties for representing names and gender. [Person Ontology reference](https://w3id.org/MON/person.owl)
- **FOAF** provides the `foaf:age` property for representing reported age. [FOAF vocabulary specification](https://xmlns.com/foaf/spec/)
- **RDF Schema (RDFS)** provides labels, class hierarchies, and links to related resources through properties such as `rdfs:label`, `rdfs:subClassOf`, and `rdfs:seeAlso`. [RDFS specification](https://www.w3.org/TR/rdf-schema/)
- **Armenian labels.** Armenian labels use `rdfs:label` with the `@hy` language tag for ontology terms and instance resources, including people, places, records, and events. Original certificate text is preserved in the source graphs. See the [Armenian glossary of terms](VG-glossary-of-terms-hy.md).

See [Attributions and third-party licenses](ontology/ATTRIBUTIONS.md) for source credits, license information, and details of the extracted subsets.

## Knowledge Graph Model

The VitalGraph application profile documents how selected terms from RiC-O and other vocabularies represent family certificate data. The diagram shows its classes and relationships, while the CSV data dictionary and generation script describe and implement local data-entry rules. Formal validation is planned.

Person identities are assigned and reviewed manually. Each person has a persistent identifier reused across certificates and a preferred name in the person registry. Individual certificates preserve the names and details recorded there.

The dataset is stored in TriG. The default graph contains the person registry, record metadata, life events, registration activities, and links identifying record subjects and event participants. Each certificate’s named graph contains its transcribed values and recorded relationships, allowing those statements to be traced to their source.

The model distinguishes life events from registration activities. People participate in birth, marriage, and death events, while certificates document the corresponding registration activities.

Dates, places, occupations, and demographic groups are represented as resources, with their recorded wording stored in the relevant certificate graph. Parent and spouse relationships are asserted within the graph of the supporting certificate. This structure preserves differences in spellings, ages, places, and demographic values across records.

The [model reference](ontology/model-reference.ttl) summarizes the classes, properties, and controlled terms used in VitalGraph.

The [CSV data dictionary](data-compiled/CSV-DATA-DICTIONARY.md) explains how to enter certificate data, reuse person identifiers, and map CSV fields to RDF.

The dataset is generated from the CSV files by [`scripts/build_graph.py`](scripts/build_graph.py).

## Visuals

- [Application Profile — Classes and Relationships](diagrams/VitalGraph-ApplicationProfile-Classes%26Relationships.pdf) shows the classes, relationships, and recorded-value fields used in VitalGraph.
- [UML Diagram](diagrams/VitalGraph-Application-Profile.png) provides the application profile as a UML diagram.
- [Model and Example Data Instance](diagrams/VitalGraph-Model&Example-person-001.png) illustrates the model using a single person, `person-001`, and hypothetical birth, marriage, and death certificates.
- [13-Certificate Pilot](diagrams/VitalGraph-Five-Certificate-Pilot.png) shows the populated graph with family relationships and recorded values drawn from thirteen certificates.

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
| [OpenAI API](https://platform.openai.com/docs/overview) | Provide the language model used by the Family Knowledge agent through GraphDB |
| [PlantUML](https://plantuml.com/) | Maintain an editable class and relationship diagram |
| [SKOS](https://www.w3.org/TR/skos-reference/) (as-needed) | Define and organize new controlled terminology developed for VitalGraph |
| [SHACL](https://www.w3.org/TR/shacl/) (planned) | Express application-profile constraints as shapes and validate the RDF dataset |

## Development Status

GraphDB Workbench supports visualization and SPARQL queries, which have been used to check recorded values, family relationships, and their supporting certificates.

The **Family Knowledge** agent uses GraphDB’s **Talk to Your Graph** feature, with autocomplete for name discovery. Its answers are checked against verified SPARQL results to identify errors in relationship direction, graph scope, and value retrieval. A [sample conversation](https://dorisavedikian.github.io/VitalGraph/) documents the testing.

Next steps include capturing additional information such as residence, medical, and burial details, and automating intake from scans and spreadsheets with manual review.

Later work includes civil, medical and church records from the U.S., Syria and Lebanon, plus searches for immigration, naturalization, and military service records through the U.S. National Archives Catalog API. Plans also include Armenian labels, validation and provenance enhancements on the existing and future records, and exploring mappings to HL7 FHIR vital-records reporting standards.

See the [Development Roadmap](DEVELOPMENT.md) for details.

## Feedback and contributions

This is a personal project. Questions, corrections, and suggestions are welcome through GitHub issues, particularly on the RDF model, terminology reuse, Armenian labels and provenance.

