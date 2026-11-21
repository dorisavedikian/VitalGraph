# VitalGraph Glossary of Terms

The RiC-O definitions below summarize the English comments in RiC-O 1.1. 

The `rico:` prefix denotes the same namespace as the default `:` prefix in the diagram. 

The `person:` prefix denotes `https://w3id.org/MON/person.owl#`, and `foaf:` denotes `http://xmlns.com/foaf/0.1/`.

## Classes

| Term | Definition / VitalGraph Use |
| --- | --- |
| [`rico:Activity`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#Activity) | An Event in which one or more Agents act for a purpose. VitalGraph uses this class for registration activities that generate certificate records. |
| [`rico:ActivityType`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#ActivityType) | Categorization of an Activity. |
| [`rico:Agent`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#Agent) | A Person, Group, Mechanism, or Position that acts in the world. |
| [`rico:Appellation`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#Appellation) | A Concept used to designate and refer to an entity. |
| [`rico:Concept`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#Concept) | An idea, unit of thought, abstract cultural object, or category. |
| [`rico:Date`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#Date) | Chronological information associated with an entity that helps identify or contextualize it. |
| [`rico:DemographicGroup`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#DemographicGroup) | Categorization of a Person or Group based on shared characteristics. |
| [`rico:Event`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#Event) | Something that happens in time and space. |
| [`rico:EventType`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#EventType) | Categorization of an Event. |
| [`rico:Name`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#Name) | An Appellation that designates an entity. In VitalGraph, a Person links to a Name node whose written form is stored with `rico:textualValue`. |
| [`rico:OccupationType`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#OccupationType) | Categorization of a profession, trade, or craft pursued by a Person in fulfilment of an Activity. |
| [`rico:Person`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#Person) | An individual human being. |
| [`rico:Place`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#Place) | A bounded, named geographic area or region. |
| [`rico:Record`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#Record) | Discrete information content fixed in a persistent, recoverable form by an Agent in the course of life or work. |
| [`rico:RecordResource`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#RecordResource) | Information produced or acquired and retained by an Agent in the course of life or work. |
| [`rico:Thing`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#Thing) | An idea, material thing, or event within the realm of human experience. |
| [`rico:Type`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#Type) | A superclass for categories that characterize entities. |

## Object Properties

| Term | Definition / VitalGraph Use |
| --- | --- |
| [`person:hasGender`](https://w3id.org/MON/person.owl?utm_source=chatgpt.com#hasGender) | MON object property from `person:Person` to `person:Sex`. In VitalGraph, use one value, `person:Male` or `person:Female`, in the named graph of the certificate that supplies it. |
| [`rico:documentedBy`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#documentedBy) | Links an Activity to a Record Resource or Instantiation it generated. In VitalGraph, it links a registration activity to its certificate record. |
| [`rico:documents`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#documents) | Links a Record Resource or Instantiation to the Activity that generated it. Inverse of `rico:documentedBy`. |
| [`rico:hasBirthDate`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#hasBirthDate) | Links a Person to their birth Date. |
| [`rico:hasBirthPlace`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#hasBirthPlace) | Links a Person to the Place where they were born. |
| [`rico:hasChild`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#hasChild) | Links a Person to one of their children. |
| [`rico:hasDeathDate`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#hasDeathDate) | Links a Person to their death Date. |
| [`rico:hasDeathPlace`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#hasDeathPlace) | Links a Person to the Place where they died. |
| [`rico:hasEventType`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#hasEventType) | Links an Event to an Event Type that categorizes it. |
| [`rico:hasOrHadDemographicGroup`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#hasOrHadDemographicGroup) | Links a Person or Group to a Demographic Group to which it belongs or belonged. |
| [`rico:hasOrHadName`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#hasOrHadName) | Links a Thing to one of its past or present Names. VitalGraph uses it from Person to Name. |
| [`rico:hasOrHadOccupationOfType`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#hasOrHadOccupationOfType) | Links a Person to an Occupation Type that categorizes or categorized their occupation. |
| [`rico:hasOrHadParticipant`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#hasOrHadParticipant) | Links an Event to a Thing that is or was involved in it. |
| [`rico:hasOrHadSpouse`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#hasOrHadSpouse) | Links two Persons who are or were married. The relationship is symmetric. |
| [`rico:hasOrHadSubject`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#hasOrHadSubject) | Links a Record Resource to a Thing that is or was its subject. VitalGraph uses it from Record to Person. |
| [`rico:isBirthPlaceOf`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#isBirthPlaceOf) | Links a Place to a Person born there. |
| [`rico:isChildOf`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#isChildOf) | Links a Person to a parent. Inverse of `rico:hasChild`. |
| [`rico:isDeathPlaceOf`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#isDeathPlaceOf) | Links a Place to a Person who died there. |
| [`rico:isEventTypeOf`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#isEventTypeOf) | Links an Event Type to an Event it categorizes. |
| [`rico:isOrWasDemographicGroupOf`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#isOrWasDemographicGroupOf) | Links a Demographic Group to a Person or Group that belongs or belonged to it. |
| [`rico:isOrWasNameOf`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#isOrWasNameOf) | Links a Name to the Thing it designates or designated. Inverse of `rico:hasOrHadName`. |
| [`rico:isOrWasOccupationTypeOf`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#isOrWasOccupationTypeOf) | Links an Occupation Type to a Person whose occupation it categorizes or categorized. |
| [`rico:isOrWasParticipantIn`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#isOrWasParticipantIn) | Links a Thing to an Event in which it participates or participated. Inverse of `rico:hasOrHadParticipant`. |
| [`rico:isOrWasSubjectOf`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#isOrWasSubjectOf) | Links a Thing to a Record Resource of which it is or was a subject. Inverse of `rico:hasOrHadSubject`. |
| [`rdfs:seeAlso`](https://www.w3.org/TR/rdf-schema/#ch_seealso) | Points to a resource that may provide additional information about the subject. In VitalGraph, it links a `rico:Place` to a reference resource. Its formal range is `rdfs:Resource`. |

## Datatype Properties

The six RiC-O properties have `rdfs:Literal` as their declared range. 
The three Person Ontology properties declare `person:Person` as their domain and `xsd:string` as their range. 
VitalGraph uses those three properties and `foaf:age` on its `rico:Person` nodes.

| Term | Definition / VitalGraph Use |
| --- | --- |
| [`foaf:age`](http://xmlns.com/foaf/0.1/age?utm_source=chatgpt.com) | Age in years, represented as an integer string. VitalGraph: Store the age reported on the certificate as an `xsd:string` in that certificate's named graph. |
| [`person:firstName`](https://w3id.org/MON/person.owl?utm_source=chatgpt.com#firstName) | A person's first name. VitalGraph: First name as recorded on the certificate. |
| [`person:lastName`](https://w3id.org/MON/person.owl?utm_source=chatgpt.com#lastName) | A person's last name. VitalGraph: Last name as recorded on the certificate. |
| [`person:maidenName`](https://w3id.org/MON/person.owl?utm_source=chatgpt.com#maidenName) | The original surname of a married woman who adopts her husband's surname. VitalGraph: Maiden surname when explicitly recorded. Keep spelling variants tied to their sources. |
| [`rico:expressedDate`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#expressedDate) | The natural-language expression of a date. VitalGraph: On `rico:Date`, store the date as written in the source. |
| [`rico:identifier`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#identifier) | A value that uniquely identifies or references an entity within a specific context. VitalGraph: On `rico:Record`, store the certificate or file number as text to preserve leading zeros. |
| [`rico:name`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#name) | A label, title, or term that distinguishes an entity. VitalGraph: Use for literal names on `rico:Place`, `rico:DemographicGroup`, and `rico:OccupationType`. |
| [`rico:normalizedDateValue`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#normalizedDateValue) | A machine-readable date expressed according to a public technical standard. VitalGraph: Optional on `rico:Date`. Store a standardized date at the precision supported by the source. |
| [`rico:textualValue`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#textualValue) | A textual expression of an Appellation or Date. Its declared domain also includes Extent. VitalGraph: On `rico:Name`, store the written form of the name. |
| [`rico:title`](https://www.ica.org/standards/RiC/ontology?utm_source=chatgpt.com#title) | An identifying name of a Record Resource, Instantiation, or Rule. VitalGraph: On `rico:Record`, store the certificate title. |

## NCIt Event Types Used in VitalGraph

VitalGraph uses these identifiers as values of `rico:hasEventType` and types them as `rico:EventType` in its graph.

| Term | Definition / VitalGraph Use |
| --- | --- |
| [Birth (`ncit:C25155`)](http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl?utm_source=chatgpt.com#C25155) | VitalGraph's intended use is the event of being born. The NCIt mapping is pending verification. |
| [Death (`ncit:C28554`)](http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl?utm_source=chatgpt.com#C28554) | The cessation of life. NCIt's preferred label is Dead, with Death as an alternative label. |
| [Marriage (`ncit:C48033`)](http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl?utm_source=chatgpt.com#C48033) | NCIt describes marriage as an institution or marital state. VitalGraph uses this identifier to categorize a marriage event. |