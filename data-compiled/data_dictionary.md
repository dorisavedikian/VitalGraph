# VitalGraph CSV data dictionary

The script reads the five CSVs in `data/` and writes TriG to `data-compiled/data_instances/vg-instance-data.trig` by default. Use `--data-dir` and `--output` to select different paths. The header-only templates produce a valid empty dataset. Fill the templates with your transcriptions and rerun to rebuild the file. 

Save the CSVs as UTF-8 and keep every header. Use text cell formatting when entering dates, ages, and identifiers in a spreadsheet so the spreadsheet preserves spelling, precision, and leading zeros. CSV quoting supports commas, quotes, and embedded line breaks. Empty optional fields produce no corresponding triple. Nonempty text is copied exactly as supplied, including whitespace and line breaks.

## Model and identifiers

The birth, marriage, and death mappings follow a certificate template, which uses placeholders for unfilled fields. The generator uses their terms and URI patterns and starts with empty input files.

| Prefix | Namespace |
| --- | --- |
| `vg:` | `https://example.org/vitalgraph/` |
| `rico:` | `https://www.ica.org/standards/RiC/ontology#` |
| `person:` | `https://w3id.org/MON/person.owl#` |
| `foaf:` | `http://xmlns.com/foaf/0.1/` |
| `ncit:` | `http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#` |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` |
| `rdf:` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` |

ID fields accept a local ID such as `person-001`, the equivalent `vg:person-001`, or an existing full HTTP(S) IRI. Local IDs start with an ASCII letter, digit, or underscore and may continue with those characters or `.`, `~`, and `-`. IDs and controlled values are case-sensitive. Retain established IDs across builds. Use the same person ID across certificates only when you have chosen that identity. Use distinct IDs for unresolved identities even when the names match. The generator creates no person IDs, name matches, or identity equivalence links.

The default graph holds the person registry and certificate metadata, including subject and participant links. Each named graph uses its certificate record IRI and holds that certificate's transcribed values, relationship evidence, and attribute nodes. Marriage event participation is also repeated in the marriage certificate graph to match the template. For a certificate with no named-graph evidence yet, the generator repeats its `rdf:type rico:Record` triple in the named graph so the graph survives TriG serialization. A `mentioned` appearance places that person's type in the named graph, as the template does for parents.

## persons.csv

One row per persistent person.

| Field | Required | RDF mapping or use |
| --- | --- | --- |
| `person_id` | Yes | Subject IRI of `rdf:type rico:Person` in the default graph. Unique. |
| `name_id` | With `preferred_name` | Unique IRI typed `rico:Name`. Connects Person → Name with `rico:hasOrHadName` and Name → Person with `rico:isOrWasNameOf`. |
| `preferred_name` | No | `rico:textualValue` on the Name resource. Enter the name you have chosen for the registry. |

## records.csv

One row per certificate.

| Field | Required | RDF mapping or use |
| --- | --- | --- |
| `record_id` | Yes | Unique `rico:Record` IRI in the default graph and identifier of its named graph. |
| `record_type` | Yes | `birth`, `marriage`, or `death`. Selects the template's `rico:EventType` IRI and English label. |
| `event_id` | Yes | `rico:Event` IRI. The Event links to its type with `rico:hasEventType` and receives the inverse `rico:isEventTypeOf`. |
| `activity_id` | Yes | `rico:Activity` IRI for registration. Connects Record → Activity via `rico:documents` and Activity → Record via `rico:documentedBy`. |
| `title` | No | `rico:title` on the Record. |
| `identifier` | No | `rico:identifier` on the Record. Enter the historical certificate or file number as text. |

To reproduce the event IRIs in your pasted template, enter `birth-001`, `marriage-001`, and `death-001` in the corresponding `event_id` cells. The generator uses those values for event declarations, participant links, and event-type links.

Event and activity IDs may repeat if you explicitly identify the same event or registration in multiple rows. A reused event ID must keep the same record type. All other resource declarations must use distinct IRIs, including across resource types. The template's NCIt mappings are preserved as configured, including the glossary's pending verification for Birth.

| Record type | Event type and label |
| --- | --- |
| `birth` | `ncit:C25155`, `"Birth"@en` |
| `marriage` | `ncit:C48033`, `"Marriage"@en` |
| `death` | `ncit:C28554`, `"Dead"@en` |

## record_persons.csv

One row per certificate and person pair. Subject and participant roles reflect your explicit choices.

| Field | Required | RDF mapping or use |
| --- | --- | --- |
| `record_id` | Yes | Existing `records.csv` ID. Selects the named graph and associated Event. |
| `person_id` | Yes | Existing `persons.csv` ID. Subject of the certificate-specific fields. |
| `role` | Yes | `subject` adds the Record–Person pair `rico:hasOrHadSubject` / `rico:isOrWasSubjectOf`. `participant` adds the Event–Person pair `rico:hasOrHadParticipant` / `rico:isOrWasParticipantIn`. `subject_participant` adds both pairs. `mentioned` adds the Person type in the named graph. |
| `first_name` | No | `person:firstName` as `xsd:string`. |
| `last_name` | No | `person:lastName` as `xsd:string`. |
| `maiden_name` | No | `person:maidenName` as `xsd:string`. |
| `gender` | No | Enter `Female` or `F` for `person:Female`, or `Male` or `M` for `person:Male`, only if explicitly mapped by you. Emits `person:hasGender`. |
| `age` | No | `foaf:age` as `xsd:string`, including qualifiers or units if present. |

## record_relationships.csv

One row per relationship asserted by a certificate. The generator writes both directions shown in the template. Enter each relationship once. Its inverse or reversed symmetric spelling would be a duplicate.

| Field | Required | RDF mapping or use |
| --- | --- | --- |
| `record_id` | Yes | Existing record ID. Selects the certificate graph. |
| `subject_person_id` | Yes | Existing person ID. Starting point of the selected predicate. |
| `predicate` | Yes | `child_of` emits `rico:isChildOf` / `rico:hasChild`. `parent_of` emits `rico:hasChild` / `rico:isChildOf`. `spouse_of` emits `rico:hasOrHadSpouse` in both directions. |
| `object_person_id` | Yes | Existing person ID. Endpoint of the selected predicate. Must differ from the subject. |

## record_attributes.csv

One row per attribute resource as recorded on a particular certificate.

| Field | Required | RDF mapping or use |
| --- | --- | --- |
| `record_id` | Yes | Existing record ID. Selects the certificate graph. |
| `person_id` | Yes | Existing person ID. Subject of the outgoing attribute link. |
| `attribute_id` | Yes | Unique IRI for this evidence resource. Keep the established IRI if there is one. |
| `attribute_type` | Yes | Selects the resource class and links from the table below. |
| `expressed_value` | Yes unless a normalized date is supplied | Exact source wording. Uses `rico:expressedDate` on dates and `rico:name` on other attributes. |
| `normalized_value` | No | Date attributes only. Adds `rico:normalizedDateValue` as supplied. The generator does not calculate or validate date normalization. |
| `see_also_url` | No (header required) | Enter a full HTTP(S) URL. Adds `rdfs:seeAlso` from the attribute resource to the URL as an IRI in the certificate’s named graph. Leave blank to omit the link. The formal range is `rdfs:Resource`. |

The generator accepts `see_also_url` for every attribute type. For a `birth_place` or `death_place` row, it links the `rico:Place` resource to a reference. Keep the place name as written on the certificate in `expressed_value`.

| Attribute type | Class | Person → resource | Resource → Person |
| --- | --- | --- | --- |
| `birth_date` | `rico:Date` | `rico:hasBirthDate` | |
| `death_date` | `rico:Date` | `rico:hasDeathDate` | |
| `birth_place` | `rico:Place` | `rico:hasBirthPlace` | `rico:isBirthPlaceOf` |
| `death_place` | `rico:Place` | `rico:hasDeathPlace` | `rico:isDeathPlaceOf` |
| `demographic_group` | `rico:DemographicGroup` | `rico:hasOrHadDemographicGroup` | `rico:isOrWasDemographicGroupOf` |
| `occupation` | `rico:OccupationType` | `rico:hasOrHadOccupationOfType` | `rico:isOrWasOccupationTypeOf` |

Relationship and attribute rows can refer directly to a registered person. Add a `record_persons.csv` row when the certificate also supplies personal fields or an explicit appearance role.
