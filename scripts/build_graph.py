#!/usr/bin/env python3
"""Build a VitalGraph TriG dataset and Armenian instance-label template from CSV."""
import argparse
import csv
import re
from pathlib import Path
from tempfile import NamedTemporaryFile
from rdflib import Dataset, Graph, Literal, Namespace, RDF, RDFS, URIRef, XSD
from rdflib.plugins.serializers.turtle import SUBJECT, TurtleSerializer

VG = Namespace("https://example.org/vitalgraph/")
RICO = Namespace("https://www.ica.org/standards/RiC/ontology#")
PERSON = Namespace("https://w3id.org/MON/person.owl#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
NCIT = Namespace("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#")

SCHEMAS = {
    "persons": "person_id,name_id,preferred_name",
    "records": "record_id,record_type,event_id,activity_id,title,identifier",
    "record_persons": "record_id,person_id,role,first_name,last_name,maiden_name,gender,age",
    "record_relationships": "record_id,subject_person_id,predicate,object_person_id",
    "record_attributes": "record_id,person_id,attribute_id,attribute_type,expressed_value,normalized_value,see_also_url",
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
GENDERS = {"Female": PERSON.Female, "Male": PERSON.Male,"female": PERSON.Female, "male": PERSON.Male, "F": PERSON.Female, "M": PERSON.Male,  "f": PERSON.Female, "m": PERSON.Male}
PERSON_FIELDS = {
    "first_name": PERSON.firstName,
    "last_name": PERSON.lastName,
    "maiden_name": PERSON.maidenName,
    "age": FOAF.age,
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
    """Read one CSV table and yield its source location and row dictionary.

    Accept UTF-8 input with an optional byte-order mark. Require exactly the
    schema's columns in any order and preserve cell text as recorded. Skip
    empty rows and reject malformed headers, row lengths, CSV, or encoding.

    Args:
        directory: Path containing the five input CSV files.
        table: Table name from SCHEMAS, without the .csv extension.

    Yields:
        A (location, row) pair containing the file and line reference and a
        dictionary mapping column names to their recorded strings.

    Raises:
        ValueError: The CSV structure or text encoding is invalid.
        OSError: The input file cannot be opened or read.
    """
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
    """Resolve a validated identifier to an RDF resource IRI.

    Expand bare local IDs and vg: IDs under the VitalGraph namespace. Accept
    absolute HTTP(S) IRIs matching ABSOLUTE_ID without expansion.

    Args:
        value: Identifier string from a CSV cell.
        field: Column name to include in validation errors.
        location: Source file and line reference for error reporting.

    Returns:
        An rdflib.URIRef identifying the resource.

    Raises:
        ValueError: The identifier does not match an accepted form.
    """
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
    """Return the mapping value for an allowed CSV option.

    Args:
        value: Exact option string supplied in the CSV.
        choices: Mapping of accepted strings to their configured values.
        field: Column name to include in validation errors.
        location: Source file and line reference for error reporting.

    Raises:
        ValueError: The option is absent from choices.
    """
    if value not in choices:
        raise ValueError(f"{location}: {field} must be one of {', '.join(choices)}")
    return choices[value]


def add_literal(graph, subject, predicate, value, datatype=None):
    """Add a nonempty recorded value as an RDF literal to graph.

    Use the optional RDF datatype and disable RDFLib literal normalization
    to preserve the supplied lexical form. An empty string adds no triple.
    Mutate graph in place and return None.
    """
    if value != "":
        graph.add((subject, predicate, Literal(value, datatype=datatype, normalize=False)))


def link(graph, subject, predicate, obj, inverse):
    """Add a resource link and, when supplied, its explicit inverse.

    Add (subject, predicate, obj) to graph. If inverse is not None, also add
    (obj, inverse, subject). Mutate graph in place and return None.
    """
    graph.add((subject, predicate, obj))
    if inverse is not None:
        graph.add((obj, inverse, subject))


def build_graph(directory):
    """Build a dataset from the five validated CSV tables in directory.

    Read persons, records, record_persons, record_relationships, and
    record_attributes in that order. Put person identities, preferred names,
    record metadata, registration activities, event types, subject links,
    and event participation in the default graph.

    Store recorded person fields, gender, family relationships, and attribute
    nodes in named graphs identified by their source record IRIs. Also store
    marriage participation in the corresponding record graph. Add supported
    inverse links explicitly and bind the namespaces used by the dataset.

    Validate identifiers, references, supported option values, duplicate
    declarations, and attribute values before returning the dataset.

    Args:
        directory: Path containing the five CSV files defined by SCHEMAS.

    Returns:
        An rdflib.Dataset containing the default graph and record graphs.

    Raises:
        ValueError: CSV data fails one of the implemented validation checks.
        OSError: An input file cannot be opened or read.
    """
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
        """Register a node's kind and source location, checking for collisions.

        Allow reuse only when shared is True and the registered kind matches.
        Mutate the enclosing identifier registry. Raise ValueError with both
        source locations when a declaration conflicts with an existing one.
        """
        previous = ids.get(node)
        if previous is None:
            ids[node] = (kind, location)
        elif not shared or previous[0] != kind:
            raise ValueError(f"{location}: {node} already declared as {previous[0]} at {previous[1]}")

    def reference(value, field, registry, location):
        """Resolve an identifier and require its presence in a registry.

        Return the resolved URIRef when it is known. Raise ValueError with
        the field and source location for an invalid or unknown identifier.
        """
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
        url = row["see_also_url"]
        if url:
            if not ABSOLUTE_ID.fullmatch(url):
                raise ValueError(f"{where}: see_also_url must be a full HTTP(S) URL")
            graph.add((attribute, RDFS.seeAlso, URIRef(url)))

    for record in records:
        graph = dataset.graph(record)
        if not graph:
            graph.add((record, RDF.type, RICO.Record))
    return dataset


def build_instance_labels(dataset, output):
    """Add Armenian label placeholders for instance resources in the dataset.

    Read existing labels from output when present and preserve their values,
    including labels for resources no longer in the CSVs. Include typed people,
    names, records, events, registration activities, and attribute resources
    across all graphs. Event-type concepts are covered by ontology labels.
    Return a Graph without modifying the dataset or writing a file.
    """
    labels = Graph()
    if output.exists():
        labels.parse(output, format="turtle")
    for prefix, namespace in dataset.namespaces():
        labels.bind(prefix, namespace)

    instances = {
        subject
        for subject, _, rdf_type, _ in dataset.quads((None, RDF.type, None, None))
        if isinstance(subject, URIRef) and rdf_type != RICO.EventType
    }
    for instance in sorted(instances):
        armenian = [
            value for value in labels.objects(instance, RDFS.label)
            if isinstance(value, Literal) and value.language
            and value.language.lower().split("-")[0] == "hy"
        ]
        if any(str(value) for value in armenian):
            labels.remove((instance, RDFS.label, Literal("", lang="hy")))
        elif not armenian:
            labels.add((instance, RDFS.label, Literal("", lang="hy")))
    return labels


def instance_label_context(dataset):
    """Return deduplicated recorded-property and value comments for each IRI.

    Preserve literal wording for translation reference. Repeated copies of
    the same property and value across certificates yield one comment.
    Person entries include recorded first-name, last-name, and maiden-name values.
    Certificate identifiers are excluded from translation comments.
    Entries without an eligible recorded value receive no hint comment.
    """
    manager = dataset.namespace_manager
    people = {
        subject for subject, _, _, _ in dataset.quads((None, RDF.type, RICO.Person, None))
    }
    context = {}
    for subject, predicate, value, _ in dataset.quads((None, None, None, None)):
        if not isinstance(subject, URIRef) or not isinstance(value, Literal):
            continue
        if predicate == RICO.identifier:
            continue
        if subject in people and predicate not in (
            PERSON.firstName, PERSON.lastName, PERSON.maidenName
        ):
            continue
        comment = f"Recorded {manager.normalizeUri(predicate)}: {str(value)!r}"
        context.setdefault(subject, set()).add(comment)

    return {subject: sorted(comments) for subject, comments in context.items()}


class InstanceLabelSerializer(TurtleSerializer):
    """Write ordinary Turtle with generated source comments before each entry."""

    def __init__(self, graph, context):
        super().__init__(graph)
        self.context = context

    def preprocess(self):
        """Declare the prefixes used by both labels and source comments."""
        super().preprocess()
        for prefix, namespace in self.store.namespaces():
            if prefix in {"vg", "rico", "person", "foaf", "rdfs", "ncit"}:
                self.addNamespace(prefix, namespace)

    def s_default(self, subject):
        """Keep each comment immediately above its matching resource statement."""
        self.write("\n" + self.indent())
        for comment in self.context.get(subject, ()):
            for line in comment.splitlines():
                self.write("# " + line + "\n" + self.indent())
        self.path(subject, SUBJECT)
        self.predicateList(subject)
        self.write(" .")
        return True


def write_rdf_outputs(outputs, label_context=None):
    """Stage RDF files before replacing outputs, restoring them on failure.

    Each item is a (graph, destination Path, RDF format) tuple. Serialize all
    files first, then replace the destinations. If a replacement fails,
    restore already replaced files from their previous contents. Destination
    directories must exist. Remove temporary files on completion or failure.
    When label_context is supplied, add those source comments to Turtle output.
    """
    staged = []
    replaced = []
    try:
        for graph, output, rdf_format in outputs:
            previous = output.read_bytes() if output.exists() else None
            with NamedTemporaryFile(
                dir=output.parent, prefix=".vitalgraph-", delete=False
            ) as temp:
                temporary = Path(temp.name)
            staged.append((temporary, output, previous))
            if rdf_format == "turtle" and label_context is not None:
                with temporary.open("wb") as stream:
                    InstanceLabelSerializer(graph, label_context).serialize(
                        stream, encoding="utf-8"
                    )
            else:
                graph.serialize(
                    destination=str(temporary), format=rdf_format, encoding="utf-8"
                )
        try:
            for temporary, output, previous in staged:
                temporary.replace(output)
                replaced.append((temporary, output, previous))
        except OSError:
            for temporary, output, previous in reversed(replaced):
                if previous is None:
                    output.unlink()
                else:
                    temporary.write_bytes(previous)
                    temporary.replace(output)
            raise
    finally:
        for temporary, _, _ in staged:
            temporary.unlink(missing_ok=True)


def write_trig(dataset, output):
    """Serialize a dataset as UTF-8 TriG and atomically replace output.

    Keep the existing single-output entry point available to callers.
    The output directory must already exist.
    """
    write_rdf_outputs(((dataset, output, "trig"),))


def main():
    """Build the dataset and write TriG plus an Armenian instance-label file.

    Default to data-compiled/data and
    data-compiled/data_instances/vg-instance-data.trig relative to the
    script's grandparent directory. Write data-labels-hy.ttl beside the
    TriG output unless --labels-output is specified. Retain existing
    translations on rebuild. Reject output paths that resolve to,
    or identify the same file as, any input CSV. Report handled input and
    filesystem errors with exit status 1; print the output path and total
    number of quads on success.
    """
    root = Path(__file__).resolve().parent.parent / "data-compiled"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=root / "data_csv")
    parser.add_argument("--output", type=Path, default=root / "data_instances" / "vg-instance-data.trig")
    parser.add_argument(
        "--labels-output", type=Path,
        help="Armenian instance labels. Defaults to data-labels-hy.ttl beside --output.",
    )
    args = parser.parse_args()
    try:
        output = args.output.resolve()
        labels_output = (
            args.labels_output or output.with_name("data-labels-hy.ttl")
        ).resolve()
        if output == labels_output or (
            output.exists() and labels_output.exists() and output.samefile(labels_output)
        ):
            raise ValueError("the TriG and labels output paths must differ")
        for destination in (output, labels_output):
            for table in SCHEMAS:
                source = args.data_dir / f"{table}.csv"
                if destination == source.resolve() or (
                    destination.exists() and source.exists() and destination.samefile(source)
                ):
                    raise ValueError("output paths must differ from all five input paths")
        dataset = build_graph(args.data_dir)
        triple_count = sum(1 for _ in dataset.quads((None, None, None, None)))
        if triple_count == 0:
            raise ValueError(
                f"No RDF statements generated from {args.data_dir.resolve()}. "
                "The input CSVs contain no data rows. Select populated CSVs with --data-dir. "
                "Existing output files have been preserved."
            )
        labels = build_instance_labels(dataset, labels_output)
        write_rdf_outputs((
            (dataset, output, "trig"),
            (labels, labels_output, "turtle"),
        ), label_context=instance_label_context(dataset))
    except (OSError, ValueError, SyntaxError) as exc:
        parser.exit(1, f"VitalGraph: {exc}\n")
    print(f"Wrote {output}")
    print(f"Wrote Armenian instance labels to {labels_output}")
    print(f"RDF triples across all graphs: {triple_count:,}")


if __name__ == "__main__":
    main()
