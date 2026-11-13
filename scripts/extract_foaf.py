"""Extract the FOAF terms used by VitalGraph."""

import os
from pathlib import Path

from rdflib import Graph, Namespace, OWL, RDF, RDFS

FOAF = Namespace("http://xmlns.com/foaf/0.1/")
SOURCE = Path("/Volumes/SIROD/development/ontologies-ttl/foaf.ttl")
OUTPUT = Path("/Volumes/SIROD/development/vitalGraph/ontology/foaf-subset.ttl")


def extract_subset(source, output):
    try:
        Path.cwd()
    except FileNotFoundError:
        if not source.is_absolute() or not output.is_absolute():
            raise ValueError("The working directory is gone. Use absolute paths.")
        if not source.is_file():
            raise FileNotFoundError(f"FOAF source file not found: {source}") from None
        os.chdir(source.parent)

    if source.resolve() == output.resolve():
        raise ValueError("The source and output must be different files.")

    graph = Graph().parse(source, format="turtle")
    if (FOAF.age, RDF.type, OWL.DatatypeProperty) not in graph:
        raise ValueError("The source is missing the foaf:age datatype property.")

    subset = Graph()
    for prefix, namespace in graph.namespaces():
        subset.bind(prefix, namespace)
    subset.bind("foaf", FOAF)

    for term in (FOAF.age, *graph.objects(FOAF.age, RDFS.domain)):
        for triple in graph.triples((term, None, None)):
            subset.add(triple)

    output.parent.mkdir(parents=True, exist_ok=True)
    subset.serialize(destination=output, format="turtle")
    print(f"Extracted {len(subset)} triples to {output}")


if __name__ == "__main__":
    extract_subset(SOURCE, OUTPUT)