Here’s the full `DEVELOPMENT.md`, ready to copy and paste.

```markdown
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
- **Validation and provenance.** Check required fields, data types, and potential duplicates before import. Keep a reference to the source page and field or the sheet and row. Review flagged entries before importing the data and regenerating the RDF dataset.

### 3. Family Photographs

Add family photographs and link them to the people, places, or events they depict when those connections can be verified. Record captions, dates or approximate dates, and the source of each image where known. Use private image references for family materials.

### 4. Armenian Display Labels

Add reviewed Armenian labels using `rdfs:label` with `@hy`, starting with the people and terms visible in the graph. Test an Armenian-language question against its verified SPARQL result.

### 5. SHACL Validation

Introduce SHACL in a later phase. Run the shapes against the pilot dataset and a separate deliberately invalid example to verify that the expected violation is reported.

### 6. Provenance and Data Lineage

Extend the existing source-tracking approach by evaluating the [W3C Provenance Ontology (PROV-O)](https://www.w3.org/TR/prov-o/) to document how information is extracted, transformed, and derived from historical records.

RiC-O will remain the foundation for representing records, people, and activities, while PROV-O may provide additional detail about data lineage and the evidence supporting individual assertions.

### 7. Vital-Records Interoperability

Investigate how vital-record information is collected, registered, and exchanged across U.S. government and healthcare systems, including processes involving state registrars, the Social Security Administration, and CDC’s National Center for Health Statistics.

This work will examine birth, death, and marriage registration workflows and evaluate mappings to relevant HL7 FHIR implementation guides.

- [Birth and Fetal Death Reporting (BFDR)](https://hl7.org/fhir/us/bfdr/)
- [Vital Records Death Reporting (VRDR)](https://hl7.org/fhir/us/vrdr/)

The goal is to identify common data elements, differences in definitions and value sets, and opportunities for semantic interoperability.

### 8. Historical and Archival Records

Use the [National Archives Catalog API v2](https://catalog.archives.gov/api/v2/api-docs/) to search for records related to family members’ immigration, naturalization, and military service. Use names and known spelling variants, dates, and places to identify candidate records. Capture each result’s title, National Archives Identifier (NAID) when available, and Catalog link so the underlying record can be accessed or requested.

Potential sources include Alien Files (A-Files) held by the National Archives and Records Administration (NARA). The USCIS Genealogy Program is a separate research avenue for naturalization Certificate Files (C-Files).

Review the underlying documents and check that they refer to the right person before adding facts to the graph. Link each new assertion to its archival source and, where available, the page or field that supports it.
```