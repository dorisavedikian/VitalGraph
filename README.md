## Overview

VitalGraph began with a personal goal: documenting my Armenian ancestry and gathering the official records needed to apply for Armenian citizenship. According to guidance I received from the Armenian Consulate in Los Angeles, I need to establish an ancestor's Armenian ethnicity and a complete chain of kinship connecting that ancestor to me. I also need every document for my application translated into Armenian.

Simple enough, right? Not quite.

I went through birth, marriage, and death certificates across several generations. Sometimes two records that pointed to the same person gave different names or disagreed on other details. I eventually found enough evidence to document my ancestor’s Armenian ethnicity and trace each generation down to me. What surprised me was that something as small as a misspelled name could make it harder to prove one link in the chain my application depended on.

Even finding the records took some detective work. I spent hours at the county records office in Fresno, searching under different spellings of family members’ names to locate the documents I needed. Those small differences affected whether I could find a record in the first place.

I ran into the same kind of problem when I went with a family member to the Social Security Administration. What SSA had on file differed from what was on their birth certificate.

I couldn't help but see a broader problem: **Why is connecting and reconciling information across official records so difficult?**

I started thinking about what would have made the process easier. The certificates I was working with were created decades apart, using the forms and technology of their time. It makes sense that connecting them today still takes some detective work.

In an ideal world, vital records would already use interoperable standards, persistent identifiers, and shared vocabularies with labels in multiple languages. That would make it easier to connect records across government systems and generations, even when names are spelled differently. I could explore those records in Armenian, still see exactly what each certificate says, and assemble the evidence I need for my citizenship application.

But we don't quite live in that world yet. So here I am, building my own multi-lingual knowledge graph. 

VitalGraph uses RDF and other Semantic Web technologies to connect historical records and represent family relationships. Its extensible model reuses selected classes and properties from RiC-O and other established ontologies, along with terms from the NCI Thesaurus (NCIt) to classify life events. By preserving provenance, VitalGraph lets me identify discrepancies across records and trace them back to the original evidence. In future development, I plan to extend the graph to include family photographs and records of immigration, naturalization, and military service.

What began with a citizenship application has become a way for me to explore what linked data can do for family history.

When I told my sister about this, she said, “Can’t you just ask Google?” I said, “Google would be guessing. And no, Google doesn't know my birthdate or when our parents got married." That became the idea behind the Family Knowledge chatbot. The goal is for it to answer from the records I’ve connected, show which documents support each answer, and make clear when the evidence is incomplete or when two records disagree.

## Project Scope

The initial proof of concept focuses on family birth, marriage, and death certificates. The current pilot contains five certificates—three birth, one death, and one marriage.

The objective is to demonstrate how information from multiple certificates can be integrated into a unified knowledge graph to:

- Represent individuals and their relationships across generations.
- Connect people to significant life events, including births, marriages and deaths.
- Associate historical certificates with the events and individuals they document.
- Represent dates, places, occupations, and demographic information.
- Preserve information recorded in the original documents.
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

VitalGraph uses RiC-O and other established ontologies to represent people, family relationships, life events, and vital records in a connected knowledge graph. Each person has a persistent identifier that connects their appearances across certificates. A person can have a registry name while individual certificates preserve different recorded names and other details.

Instance data is stored in TriG. The default graph contains the person registry, record metadata, life events, registration activities, and links identifying record subjects and event participants. Each certificate has a named graph containing its transcribed values and relationship evidence.

The model distinguishes a life event from its registration activity. People participate in birth, marriage, and death events. A certificate is connected to its registration activity through rico:documents, with the inverse expressed through rico:documentedBy.

Dates, places, occupations, and demographic groups are represented as resources. Their recorded wording is stored on those resources inside the relevant certificate graph. Parent and spouse relationships are also asserted within the certificate graph that supplies the evidence.

This structure allows multiple certificates to record different spellings, ages, places, or demographic values for the same person while retaining the source of each statement. 

This approach supports data provenance, preserves original source information, and accommodates discrepancies across records.

The [model reference](ontology/model-reference.txt) summarizes the classes, properties, and controlled terms used in VitalGraph.

The [single-person example](data-compiled/data_instances/single-person.txt) is a structural template containing placeholders. It illustrates how one persistent person identifier connects appearances across birth, marriage, and death records, with source-specific details in each certificate’s named graph.

The [CSV data dictionary](data-compiled/CSV-DATA-DICTIONARY.md) explains how to enter certificate data, reuse person identifiers, and map CSV fields to RDF.

## Visuals

- [Application Profile — Classes and Relationships](diagrams/VitalGraph-ApplicationProfile-Classes%26Relationships.pdf) shows the classes, relationships, and recorded-value fields used in VitalGraph.
- [Editable UML Diagram](diagrams/VitalGraph-Application-Profile.puml) provides the application profile as PlantUML source. A [rendered version](diagrams/VitalGraph-Application-Profile.png) is also available.
- [Model and Example Records](diagrams/VitalGraph-Model%26Example-Records.png) connects ontology definitions to example people and records.
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

SKOS is being considered for future natively controlled terminology. SHACL validation is planned for a later development phase.

## Development Status

The current pilot contains five family certificates—three birth certificates, one death certificate, and one marriage certificate. Certificate transcriptions are entered through five CSV files and converted to TriG using Python and RDFLib. Persistent person identifiers connect appearances across records, while certificate-specific named graphs preserve the original wording and relationship evidence.

GraphDB Workbench is used to explore the dataset visually and run SPARQL queries. Verified queries retrieve certificate counts, family relationships, names, dates, places, occupations, and demographic values with their supporting records. The repository includes an application-profile diagram, editable PlantUML source, and screenshots of the model and populated pilot.

The **Family Knowledge** agent uses GraphDB’s **Talk to Your Graph** feature to answer natural-language questions. Autocomplete supports name discovery. Testing has produced successful answers alongside errors involving relationship direction, graph scope, and retrieval of literal values. Agent answers are checked against direct SPARQL results. A [sample conversation](docs/index.html) documents the testing, and the accompanying converter creates readable HTML from GraphDB chat exports.

Next, I plan to add the eight remaining family certificates and capture more of what they document, including residences, medical information, and burial details. I also plan to automate data entry from scanned PDFs and spreadsheets into the existing CSV-to-RDF workflow, with review of transcriptions and person identities before integration.

Later work will expand the graph with family photographs and additional archival records. This includes investigating civil-registration, migration, residence, and church records concerning my father and grandparents in Syria and Lebanon, tracing my father’s birthplace in Syria and his subsequent move to Lebanon. I also plan to explore the National Archives Catalog API for immigration, naturalization, and military service records.

The roadmap also covers Armenian display labels, SHACL validation, expanded provenance as necessary, and possible interoperability with vital-records standards.

See the [Development Roadmap](DEVELOPMENT.md) for details.