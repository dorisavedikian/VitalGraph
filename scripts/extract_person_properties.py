from pathlib import Path

from rdflib import BNode, Graph, Namespace, OWL, RDF, RDFS, URIRef
from rdflib.collection import Collection


PERSON = Namespace("https://w3id.org/MON/person.owl#")

SELECTED_PROPERTIES = [
    PERSON.firstName,
    PERSON.lastName,
    PERSON.maidenName,
    PERSON.hasGender,
]

GENDER_VALUES = {PERSON.Female, PERSON.Male}

SOURCE = Path("/Volumes/SIROD/development/ontologies-ttl/person.ttl")
OUTPUT = Path("ontology/person-subset.ttl")


def extract_subset(source, output):
    graph = Graph().parse(source, format="turtle")
    subset = Graph()

    for prefix, namespace in graph.namespaces():
        subset.bind(prefix, namespace)

    visited = set()

    def copy_definition(subject):
        """Copy a resource definition and its referenced blank nodes."""
        if subject in visited:
            return

        visited.add(subject)
        for predicate, obj in graph.predicate_objects(subject):
            subset.add((subject, predicate, obj))
            if isinstance(obj, BNode):
                copy_definition(obj)

    for prop in SELECTED_PROPERTIES:
        if not list(graph.predicate_objects(prop)):
            print(f"WARNING: Definition not found: {prop}")
            continue

        copy_definition(prop)

        for relation in (RDFS.domain, RDFS.range):
            for obj in graph.objects(prop, relation):
                if isinstance(obj, URIRef) and obj.startswith(str(PERSON)):
                    for predicate in (RDF.type, RDFS.label, RDFS.comment):
                        for value in graph.objects(obj, predicate):
                            subset.add((obj, predicate, value))

    # Copy the gender values used as individuals of person:Sex.
    for value in sorted(GENDER_VALUES):
        if (value, RDF.type, PERSON.Sex) not in graph:
            raise ValueError(f"Missing MON sex individual: {value}")
        for predicate in (RDF.type, RDFS.label):
            for obj in graph.objects(value, predicate):
                subset.add((value, predicate, obj))

    # Preserve MON's declaration that these two individuals are distinct.
    for axiom in graph.subjects(RDF.type, OWL.AllDifferent):
        for members in graph.objects(axiom, OWL.distinctMembers):
            if set(Collection(graph, members)) == GENDER_VALUES:
                copy_definition(axiom)

    output.parent.mkdir(parents=True, exist_ok=True)
    subset.serialize(destination=output, format="turtle")

    print(f"Extracted {len(subset)} triples")
    print(f"Saved to: {output}")


if __name__ == "__main__":
    extract_subset(SOURCE, OUTPUT)
