#!/usr/bin/env python3
"""Extract the RDFS terms used by the VitalGraph application profile."""

import argparse
from pathlib import Path

from rdflib import Graph, RDFS

SOURCE = Path("/Volumes/SIROD/development/ontologies-ttl/rdfs.ttl")
OUTPUT = Path("/Volumes/SIROD/development/vitalGraph/ontology/rdfs-subset.ttl")
TERMS = (RDFS.seeAlso, RDFS.Resource, RDFS.Literal)


def extract_subset(source: Path, output: Path) -> int:
    if source.resolve() == output.resolve() or (
        output.exists() and source.samefile(output)
    ):
        raise ValueError("The source and output must be different files.")

    graph = Graph().parse(source, format="turtle")
    subset = Graph()
    for prefix, namespace in graph.namespaces():
        subset.bind(prefix, namespace)

    for term in TERMS:
        triples = list(graph.triples((term, None, None)))
        if not triples:
            raise ValueError(f"Missing source definition for {term}")
        for triple in triples:
            subset.add(triple)

    for predicate in (RDFS.domain, RDFS.range):
        if set(subset.objects(RDFS.seeAlso, predicate)) != {RDFS.Resource}:
            raise ValueError(f"Expected {predicate} of rdfs:seeAlso to be rdfs:Resource")

    subset.serialize(destination=output, format="turtle")
    return len(subset)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        count = extract_subset(args.source, args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"extract_rdfs: {exc}\n")
    print(f"Extracted {count} triples to {args.output}")


if __name__ == "__main__":
    main()
