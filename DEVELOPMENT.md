# VitalGraph Development Roadmap

VitalGraph is being developed incrementally, starting with an RDF knowledge graph built from family birth, marriage, and death certificates. The initial pilot reuses established ontologies, converts certificate transcriptions from CSV to RDF, and uses GraphDB to visualize the dataset and run SPARQL queries. It also tests the Family Knowledge agent’s ability to answer natural-language questions and cite the certificates that support its answers.

The following areas outline opportunities to extend the project beyond its initial proof of concept. For background and project scope, see the [README](README.md).

## Planned Development

### 1. Armenian Display Labels

Add reviewed Armenian labels using `rdfs:label` with `@hy`, starting with the people and terms visible in the graph. Test an Armenian-language question against its verified SPARQL result.

### 2. SHACL Validation

Introduce SHACL in a later phase. Run the shapes against the pilot dataset and a separate deliberately invalid example to verify that the expected violation is reported.

### 3. Provenance and Data Lineage

Extend the existing source-tracking approach by evaluating the W3C Provenance Ontology (PROV-O) to document how information is extracted, transformed, and derived from historical records.

RiC-O will remain the foundation for representing records, people, and activities, while PROV-O may provide additional detail about data lineage and the evidence supporting individual assertions.

[W3C PROV-O documentation](https://www.w3.org/TR/prov-o/)

### 4. Vital-Records Interoperability

Investigate how vital-record information is collected, registered, and exchanged across U.S. government and healthcare systems, including processes involving state registrars, the Social Security Administration, and CDC's National Center for Health Statistics.

This work will examine birth, death, and marriage registration workflows and evaluate mappings to relevant HL7 FHIR implementation guides:

- [Birth and Fetal Death Reporting (BFDR)](https://hl7.org/fhir/us/bfdr/)
- [Vital Records Death Reporting (VRDR)](https://hl7.org/fhir/us/vrdr/)

The goal is to identify common data elements, differences in definitions and value sets, and opportunities for semantic interoperability.

### 5. Historical and Archival Records

Expand beyond vital certificates to explore immigration, naturalization, and other historical federal records as additional evidence of family identities, relationships, and life events.

Potential sources include Alien Files (A-Files), naturalization Certificate Files (C-Files), and records accessible through the National Archives and Records Administration (NARA).

New information will retain references to its original archival sources to support provenance and traceability.
