# VitalGraph Development Roadmap

VitalGraph is being developed incrementally, starting with an RDF knowledge graph built from family birth, marriage, and death certificates. The initial pilot reuses established ontologies, converts certificate transcriptions from CSV to RDF, and uses GraphDB to visualize the dataset and run SPARQL queries. It also tests the Family Knowledge agent’s ability to answer natural-language questions and cite the certificates that support its answers.

For background and project scope, see the [README](README.md).

## Planned Development

### 1. Certificate Entry and Additional Fields

Expand the model and CSV tables to capture additional details from the certificates, including residences, medical information such as cause of death, and burial details such as cemetery, location, and date. 

### 2. Automated Data Intake

Build an import step that maps scanned PDFs and tabular sources into the existing VitalGraph CSV tables. Review extracted values against the source documents before generating RDF, and flag uncertain or unreadable entries.

### 3. Armenian Display Labels

- Test the **Family Knowledge** agent in GraphDB’s **Talk to Your Graph** with English and Armenian questions, checking that it retrieves the correct people, relationships, and supporting certificate evidence.

### 4. Application Profile and Validation

Evaluate [DCTAP](https://www.dublincore.org/specifications/dctap/primer/) as a tabular way to maintain VitalGraph’s application profile. Define SHACL shapes to check required links, resource types, literal datatypes, and allowed values. Test whether DCTAP can support generating and maintaining those shapes using [TAP2SHACL](https://codeberg.org/philbarker/TAP2SHACL)

Compare [pySHACL](https://github.com/rdflib/pyshacl) to [GraphDB's SHACL](https://graphdb.ontotext.com/documentation/11.5/shacl-validation.html#) validation to determine which bettter supports default graph and certificate specific named graphs, ease of integration and correctness of validation reports. Test both with known valid and invalid graphs.

Once the validation rules are finalized, I’ll update the UML and other [diagrams](diagrams) to show the corresponding cardinality and value constraints.

### 5. Provenance

Extend the existing certificate-level named graphs with details about who entered or reviewed the data and when. 

### 6. Historical and Archival Records

Use the [National Archives Catalog API v2](https://catalog.archives.gov/api/v2/api-docs/) to search for records related to family members’ immigration, naturalization, and military service. Use names and known spelling variants, dates, and places to identify candidate records. Capture each result’s National Archives Identifier (NAID) when available, and Catalog link so the underlying record can be accessed or requested.

Potential sources include Alien Files (A-Files) held by the National Archives and Records Administration (NARA). 

The USCIS Genealogy Program is a separate research avenue for naturalization Certificate Files (C-Files).

### Family Records in Syria and Lebanon

Investigate records concerning my father and paternal grandparents, including my father’s birth in Syria and subsequent move to Lebanon. The aim is to try to document their identities, family relationships, places of residence, and migration history, while preserving the names and other details recorded by each source.

#### Starting References

- [Syrian civil-document guide](https://travel.state.gov/content/travel/en/us-visas/Visa-Reciprocity-and-Civil-Documents-by-Country/Syria.html)
- [Lebanese Embassy](https://lebanonembassyus.org)
- [Armenian Prelacy of Lebanon certificate services](https://armprelacylb.org)

### 7. Vital-Records Interoperability

Investigate how vital-record information is collected, registered, and exchanged across U.S. government and healthcare systems, including processes involving state registrars, the Social Security Administration, and CDC’s National Center for Health Statistics.

Explore how VitalGraph’s birth and death certificate fields map to the corresponding HL7 FHIR vital-records reporting guides.

- [Birth and Fetal Death Reporting (BFDR)](https://hl7.org/fhir/us/bfdr/)
- [Vital Records Death Reporting (VRDR)](https://hl7.org/fhir/us/vrdr/)