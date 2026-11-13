# VitalGraph Development Roadmap

VitalGraph is being developed incrementally, beginning with an RDF knowledge graph constructed from family birth, marriage, and death certificates. Initial development focuses on ontology reuse, data integration, SHACL validation, and SPARQL querying.

The following areas outline opportunities to extend the project beyond its initial proof of concept. For background and project scope, see the [README](README.md).

## Planned Development

### 1. Provenance and Data Lineage

Extend the existing source-tracking approach by evaluating the W3C Provenance Ontology (PROV-O) to document how information is extracted, transformed, and derived from historical records.

RiC-O will remain the foundation for representing records, people, and activities, while PROV-O may provide additional detail about data lineage and the evidence supporting individual assertions.

[W3C PROV-O documentation](https://www.w3.org/TR/prov-o/)

### 2. Natural-Language Knowledge Graph Queries

Explore integrating the OpenAI API with SPARQL to support natural-language questions about family history.

Responses will be grounded in authorized knowledge graph data, reference supporting records, and distinguish documented facts from inferred relationships or unresolved identity matches.

### 3. Vital-Records Interoperability

Investigate how vital-record information is collected, registered, and exchanged across U.S. government and healthcare systems, including processes involving state registrars, the Social Security Administration, and CDC's National Center for Health Statistics.

This work will examine birth, death, and marriage registration workflows and evaluate mappings to relevant HL7 FHIR implementation guides:

- [Birth and Fetal Death Reporting (BFDR)](https://hl7.org/fhir/us/bfdr/)
- [Vital Records Death Reporting (VRDR)](https://hl7.org/fhir/us/vrdr/)

The goal is to identify common data elements, differences in definitions and value sets, and opportunities for semantic interoperability.

### 4. Historical and Archival Records

Expand beyond vital certificates to explore immigration, naturalization, and other historical federal records as additional evidence of family identities, relationships, and life events.

Potential sources include Alien Files (A-Files), naturalization Certificate Files (C-Files), and records accessible through the National Archives and Records Administration (NARA).

New information will retain references to its original archival sources to support provenance and traceability.
