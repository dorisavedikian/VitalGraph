#!/usr/bin/env python3
"""Build a VitalGraph TriG dataset from five UTF-8 CSV files."""
import argparse
import csv
import re
from pathlib import Path
from tempfile import NamedTemporaryFile

from rdflib import Dataset, Literal, Namespace, RDF, RDFS, URIRef, XSD

VG = Namespace("https://example.org/vitalgraph/")
RICO = Namespace("https://www.ica.org/standards/RiC/ontology#")
PERSON = Namespace("https://w3id.org/MON/person.owl#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
NCIT = Namespace("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#")

SCHEMAS = {
    "persons": "person_id,name_id,preferred_name,identity_status",
    "records": "record_id,record_type,event_id,activity_id,title,identifier",
    "record_persons": "record_id,person_id,role,first_name,last_name,maiden_name,gender,age,gender_as_written",
    "record_relationships": "record_id,subject_person_id,predicate,object_person_id",
    "record_attributes": "record_id,person_id,attribute_id,attribute_type,expressed_value,normalized_value",
}

EVENT_TYPES = {
    "birth": ("C25155", "Birth"),
    "marriage": ("C48033", "Marriage"),
    "death": ("C28554", "Dead"),
}
ROLES = {
    "subject": (True, False),
    "participant": (False, True),
    "subject_participant": (True, True),
    "mentioned": (False, False),
}
GENDERS = {"Female": PERSON.Female, "Male": PERSON.Male}
PERSON_FIELDS = {
    "first_name": PERSON.firstName,
    "last_name": PERSON.lastName,
    "maiden_name": PERSON.maidenName,
    "age": FOAF.age,
    "gender_as_written": VG.recordedGender,
}
RELATIONSHIPS = {
    "child_of": (RICO.isChildOf, RICO.hasChild),
    "parent_of": (RICO.hasChild, RICO.isChildOf),
    "spouse_of": (RICO.hasOrHadSpouse, RICO.hasOrHadSpouse),
}
ATTRIBUTES = {
    "birth_date": (RICO.Date, RICO.hasBirthDate, None),
    "death_date": (RICO.Date, RICO.hasDeathDate, None),
    "birth_place": (RICO.Place, RICO.hasBirthPlace, RICO.isBirthPlaceOf),
    "death_place": (RICO.Place, RICO.hasDeathPlace, RICO.isDeathPlaceOf),
    "demographic_group": (RICO.DemographicGroup, RICO.hasOrHadDemographicGroup,
                          RICO.isOrWasDemographicGroupOf),
    "occupation": (RICO.OccupationType, RICO.hasOrHadOccupationOfType,
                   RICO.isOrWasOccupationTypeOf),
}
LOCAL_ID = re.compile(r"[A-Za-z0-9_][A-Za-z0-9._~-]*")
ABSOLUTE_ID = re.compile(r"https?://(?=[^/?#])[^\s<>\x00-\x1f{}|^\x60\\\x22]*")


def read_rows(directory, table):
    path = directory / f"{table}.csv"
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source, strict=True)
        columns = SCHEMAS[table].split(",")
        try:
            header = next(reader, [])
            if len(header) != len(columns) or set(header) != set(columns):
                raise ValueError(f"{path}: expected columns {','.join(columns)}")
            for cells in reader:
                location = f"{path}:{reader.line_num}"
                if not cells:
                    continue
                if len(cells) != len(columns):
                    raise ValueError(f"{location}: expected {len(columns)} fields, got {len(cells)}")
                if any(cells):
                    yield location, dict(zip(header, cells))
        except (csv.Error, UnicodeError) as exc:
            raise ValueError(f"{path}:{reader.line_num}: {exc}") from exc


def resource(value, field, location):
    if value.startswith("vg:"):
        value = value[3:]
        if LOCAL_ID.fullmatch(value):
            return VG[value]
    elif LOCAL_ID.fullmatch(value):
        return VG[value]
    elif ABSOLUTE_ID.fullmatch(value):
        return URIRef(value)
    raise ValueError(f"{location}: {field} needs a local ID, vg: ID, or absolute HTTP(S) IRI")


def option(value, choices, field, location):
    if value not in choices:
        raise ValueError(f"{location}: {field} must be one of {', '.join(choices)}")
    return choices[value]


def add_literal(graph, subject, predicate, value, datatype=None):
    if value != "":
        graph.add((subject, predicate, Literal(value, datatype=datatype, normalize=False)))


def link(graph, subject, predicate, obj, inverse):
    graph.add((subject, predicate, obj))
    if inverse is not None:
        graph.add((obj, inverse, subject))


def build_graph(directory):
    dataset = Dataset()
    default = dataset.default_graph
    for prefix, namespace in (("vg", VG), ("rico", RICO), ("person", PERSON),
                              ("foaf", FOAF), ("ncit", NCIT), ("xsd", XSD),
                              ("rdfs", RDFS)):
        dataset.bind(prefix, namespace)

    ids = {NCIT[code]: ("event type", "certificate template")
           for code, _ in EVENT_TYPES.values()}
    ids[default.identifier] = ("default graph", "RDFLib")
    people = set()
    records = {}
    appearances = {}
    relationships = {}

    def declare(node, kind, location, shared=False):
        previous = ids.get(node)
        if previous is None:
            ids[node] = (kind, location)
        elif not shared or previous[0] != kind:
            raise ValueError(f"{location}: {node} already declared as {previous[0]} at {previous[1]}")

    def reference(value, field, registry, location):
        node = resource(value, field, location)
        if node not in registry:
            raise ValueError(f"{location}: unknown {field} {value!r}")
        return node

    for where, row in read_rows(directory, "persons"):
        person = resource(row["person_id"], "person_id", where)
        declare(person, "person", where)
        people.add(person)
        default.add((person, RDF.type, RICO.Person))
        if row["name_id"]:
            name = resource(row["name_id"], "name_id", where)
            declare(name, "name", where)
            default.add((name, RDF.type, RICO.Name))
            link(default, person, RICO.hasOrHadName, name, RICO.isOrWasNameOf)
            add_literal(default, name, RICO.textualValue, row["preferred_name"])
        elif row["preferred_name"]:
            raise ValueError(f"{where}: preferred_name requires name_id")

    for where, row in read_rows(directory, "records"):
        record = resource(row["record_id"], "record_id", where)
        event = resource(row["event_id"], "event_id", where)
        activity = resource(row["activity_id"], "activity_id", where)
        record_type = row["record_type"]
        code, label = option(record_type, EVENT_TYPES, "record_type", where)
        declare(record, "record", where)
        declare(event, f"{record_type} event", where, shared=True)
        declare(activity, "registration activity", where, shared=True)
        records[record] = (event, record_type)
        event_type = NCIT[code]
        for node, rdf_type in ((record, RICO.Record), (event, RICO.Event),
                               (activity, RICO.Activity), (event_type, RICO.EventType)):
            default.add((node, RDF.type, rdf_type))
        default.add((event_type, RDFS.label, Literal(label, lang="en")))
        link(default, event, RICO.hasEventType, event_type, RICO.isEventTypeOf)
        link(default, record, RICO.documents, activity, RICO.documentedBy)
        add_literal(default, record, RICO.title, row["title"])
        add_literal(default, record, RICO.identifier, row["identifier"])

    for where, row in read_rows(directory, "record_persons"):
        record = reference(row["record_id"], "record_id", records, where)
        person = reference(row["person_id"], "person_id", people, where)
        key = (record, person)
        if key in appearances:
            raise ValueError(f"{where}: duplicate appearance, first declared at {appearances[key]}")
        appearances[key] = where
        graph = dataset.graph(record)
        subject, participant = option(row["role"], ROLES, "role", where)
        event, record_type = records[record]
        if subject:
            link(default, record, RICO.hasOrHadSubject, person, RICO.isOrWasSubjectOf)
        if participant:
            link(default, event, RICO.hasOrHadParticipant, person, RICO.isOrWasParticipantIn)
            if record_type == "marriage":
                graph.add((event, RICO.hasOrHadParticipant, person))
        if not subject and not participant:
            graph.add((person, RDF.type, RICO.Person))
        for field, predicate in PERSON_FIELDS.items():
            add_literal(graph, person, predicate, row[field], XSD.string)
        if row["gender"]:
            gender = option(row["gender"], GENDERS, "gender", where)
            graph.add((person, PERSON.hasGender, gender))

    for where, row in read_rows(directory, "record_relationships"):
        record = reference(row["record_id"], "record_id", records, where)
        subject = reference(row["subject_person_id"], "subject_person_id", people, where)
        obj = reference(row["object_person_id"], "object_person_id", people, where)
        forward, inverse = option(row["predicate"], RELATIONSHIPS, "predicate", where)
        if subject == obj:
            raise ValueError(f"{where}: a family relationship requires two different people")
        key = (record, frozenset(((subject, forward, obj), (obj, inverse, subject))))
        if key in relationships:
            raise ValueError(f"{where}: duplicate relationship, first declared at {relationships[key]}")
        relationships[key] = where
        link(dataset.graph(record), subject, forward, obj, inverse)

    for where, row in read_rows(directory, "record_attributes"):
        record = reference(row["record_id"], "record_id", records, where)
        person = reference(row["person_id"], "person_id", people, where)
        attribute = resource(row["attribute_id"], "attribute_id", where)
        rdf_type, forward, inverse = option(row["attribute_type"], ATTRIBUTES, "attribute_type", where)
        declare(attribute, "attribute", where)
        expressed, normalized = row["expressed_value"], row["normalized_value"]
        if normalized and rdf_type != RICO.Date:
            raise ValueError(f"{where}: normalized_value applies only to date attributes")
        if expressed == "" and normalized == "":
            raise ValueError(f"{where}: provide an expressed_value or a normalized date")
        graph = dataset.graph(record)
        graph.add((attribute, RDF.type, rdf_type))
        link(graph, person, forward, attribute, inverse)
        if rdf_type == RICO.Date:
            add_literal(graph, attribute, RICO.expressedDate, expressed)
            add_literal(graph, attribute, RICO.normalizedDateValue, normalized)
        else:
            add_literal(graph, attribute, RICO.name, expressed)

    for record in records:
        graph = dataset.graph(record)
        if not graph:
            graph.add((record, RDF.type, RICO.Record))
    return dataset


def write_trig(dataset, output):
    # A failed build leaves any existing output intact.
    with NamedTemporaryFile(dir=output.parent, prefix=".vitalgraph-", delete=False) as temp:
        temporary = Path(temp.name)
    try:
        dataset.serialize(destination=str(temporary), format="trig", encoding="utf-8")
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=root / "data")
    parser.add_argument("--output", type=Path, default=root / "vitalgraph.trig")
    args = parser.parse_args()
    try:
        output = args.output.resolve()
        for table in SCHEMAS:
            source = args.data_dir / f"{table}.csv"
            if output == source.resolve() or (output.exists() and source.exists() and output.samefile(source)):
                raise ValueError("the output path must differ from all five input paths")
        dataset = build_graph(args.data_dir)
        write_trig(dataset, output)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"VitalGraph: {exc}\n")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
