"""Extract the RiC-O classes and properties shown in the VitalGraph diagram."""

import argparse
import os
from collections import deque
from pathlib import Path

from rdflib import BNode, Graph, Namespace, OWL, RDF, RDFS, URIRef
from rdflib.namespace import SKOS


RICO = Namespace("https://www.ica.org/standards/RiC/ontology#")
DEFAULT_SOURCE = Path("/Volumes/SIROD/development/ontologies-ttl/RiC-O_1-1.ttl")
DEFAULT_OUTPUT = Path(__file__).with_name("RiC-O_1-1-subset.ttl")

CLASS_NAMES = """
Thing RecordResource Record Agent Person Event Concept Type EventType
Place Date OccupationType ActivityType DemographicGroup
Activity Appellation Name
""".split()

OBJECT_PROPERTY_NAMES = """
hasOrHadSubject isOrWasSubjectOf
documentedBy documents
hasOrHadName isOrWasNameOf
hasOrHadParticipant isOrWasParticipantIn
hasEventType isEventTypeOf
hasBirthPlace isBirthPlaceOf hasDeathPlace isDeathPlaceOf
hasBirthDate hasDeathDate
hasChild isChildOf hasOrHadSpouse
hasOrHadOccupationOfType isOrWasOccupationTypeOf
hasOrHadDemographicGroup isOrWasDemographicGroupOf
""".split()


DATATYPE_PROPERTY_NAMES = """
expressedDate identifier name normalizedDateValue textualValue title
""".split()


def selected_classes(ontology):
    """Include named RiC-O superclasses of the selected classes."""
    classes = {RICO[name] for name in CLASS_NAMES}
    pending = deque(classes)
    while pending:
        for parent in ontology.objects(pending.popleft(), RDFS.subClassOf):
            if isinstance(parent, URIRef) and str(parent).startswith(str(RICO)):
                if parent not in classes:
                    classes.add(parent)
                    pending.append(parent)
    return classes


def extract(ontology, classes, properties):
    """Copy definitions and referenced blank nodes, skipping excluded annotations."""
    result = Graph()
    for prefix, namespace in ontology.namespaces():
        if prefix and str(namespace) != str(RICO):
            result.bind(prefix, namespace)
    result.bind("", RICO, replace=True)

    pending = deque(sorted(classes | properties))
    visited = set()
    while pending:
        subject = pending.popleft()
        if subject in visited:
            continue
        visited.add(subject)
        for predicate, value in ontology.predicate_objects(subject):
            if predicate in (SKOS.changeNote, RICO.RiCCMCorrespondingComponent):
                continue
            result.add((subject, predicate, value))
            if isinstance(value, BNode):
                pending.append(value)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    try:
        Path.cwd()
    except FileNotFoundError:
        if not args.source.is_absolute() or not args.output.is_absolute():
            parser.error("The working directory is gone. Change directories or use absolute paths.")
        if not args.source.is_file():
            parser.error(f"RiC-O source file not found: {args.source}")
        # RDFLib's Turtle parser needs a working directory even for absolute paths.
        os.chdir(args.source.parent)

    source = args.source.resolve()
    output = args.output.resolve()
    if source == output:
        parser.error("The source and output must be different files.")

    ontology = Graph().parse(source, format="turtle")
    classes = selected_classes(ontology)
    objects = {RICO[name] for name in OBJECT_PROPERTY_NAMES}
    datatypes = {RICO[name] for name in DATATYPE_PROPERTY_NAMES}
    for terms, expected_type in (
        (classes, OWL.Class),
        (objects, OWL.ObjectProperty),
        (datatypes, OWL.DatatypeProperty),
    ):
        missing = sorted(str(term) for term in terms if (term, RDF.type, expected_type) not in ontology)
        if missing:
            parser.error("Missing or incorrectly typed RiC-O terms: " + ", ".join(missing))

    result = extract(ontology, classes, objects | datatypes)
    result.serialize(destination=str(output), format="turtle")
    print(f"Extracted {len(classes)} classes and {len(objects)} object properties, "
          f"and {len(datatypes)} datatype properties "
          f"({len(result):,} triples) to {args.output}")


if __name__ == "__main__":
    main()
