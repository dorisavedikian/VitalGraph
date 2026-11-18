# VitalGraph Development Roadmap

VitalGraph is being developed incrementally, starting with an RDF knowledge graph built from family birth, marriage, and death certificates. The initial pilot reuses established ontologies, converts certificate transcriptions from CSV to RDF, and uses GraphDB to visualize the dataset and run SPARQL queries. It also tests the Family Knowledge agent’s ability to answer natural-language questions and cite the certificates that support its answers.

For background and project scope, see the [README](README.md).

## Planned Development

### 1. Certificate Entry and Additional Fields

Transcribe the eight remaining family certificates, enter them in the CSV tables, and regenerate the RDF dataset. Preserve names and other details as recorded on each certificate, including spelling variants.

Expand the model and CSV tables to capture additional details from the certificates, including residences, medical information such as cause of death, and burial details such as cemetery, location, and date. Link each detail to its source certificate and, where available, the field where it appears. Keep residences distinct from places of birth, marriage, death, or burial.

### 2. Automated Data Intake

Build an import step that maps scanned PDFs and tabular sources into the existing VitalGraph CSV tables so they can feed the current CSV-to-RDF generator.

- **Scanned PDFs.** Read certificate scans and map the information into the existing CSV tables. Flag hard-to-read text or unclear field matches so they can be checked against the original certificate.
- **Spreadsheets and CSV files.** Define reusable mappings from source columns to the existing table fields. Preserve original values alongside normalized values when both are needed.

### 3. Armenian Display Labels

Add reviewed Armenian labels using `rdfs:label` with `@hy`, starting with the people and terms visible in the graph. Test an Armenian-language question against its verified SPARQL result.

### 4. Application Profile and Validation

Evaluate DCTAP as a spreadsheet-based way to maintain VitalGraph’s application profile and generate SHACL shapes. Compare it with writing a small set of SHACL shapes directly before adopting it.

### 5. Historical and Archival Records

Use the [National Archives Catalog API v2](https://catalog.archives.gov/api/v2/api-docs/) to search for records related to family members’ immigration, naturalization, and military service. Use names and known spelling variants, dates, and places to identify candidate records. Capture each result’s title, National Archives Identifier (NAID) when available, and Catalog link so the underlying record can be accessed or requested.

Potential sources include Alien Files (A-Files) held by the National Archives and Records Administration (NARA). The USCIS Genealogy Program is a separate research avenue for naturalization Certificate Files (C-Files).

Review the underlying documents and check that they refer to the right person before adding facts to the graph. Link each new assertion to its archival source and, where available, the page or field that supports it.

### Family Records in Syria and Lebanon

Investigate records concerning my father and paternal grandparents, including my father’s birth in Syria and subsequent move to Lebanon. The aim is to document their identities, family relationships, places of residence, and migration history, while preserving the names and other details recorded by each source.

#### Starting References

- [Syrian civil-document guide](https://travel.state.gov/content/travel/en/us-visas/Visa-Reciprocity-and-Civil-Documents-by-Country/Syria.html)
- [Lebanese Embassy civil-document request guidance](https://lebanonembassyus.org/consular-services/other/)
- [Armenian Prelacy of Lebanon certificate services](https://armprelacylb.org/azk-arachnortaran/services/hasdadakirner/)

### 6. Vital-Records Interoperability

Investigate how vital-record information is collected, registered, and exchanged across U.S. government and healthcare systems, including processes involving state registrars, the Social Security Administration, and CDC’s National Center for Health Statistics.

Explore how VitalGraph’s birth and death certificate fields map to the corresponding HL7 FHIR vital-records reporting guides.

- [Birth and Fetal Death Reporting (BFDR)](https://hl7.org/fhir/us/bfdr/)
- [Vital Records Death Reporting (VRDR)](https://hl7.org/fhir/us/vrdr/)