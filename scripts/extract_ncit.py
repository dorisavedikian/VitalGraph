#!/usr/bin/env python3
"""Export the VitalGraph event vocabulary from the NCI Thesaurus EVS API."""

import argparse
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef
from rdflib.namespace import DCTERMS

CODES = ("C25155", "C28554", "C48033")
NCIT = Namespace("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#")
API = "https://api-evsrest.nci.nih.gov/api/v1/concept/ncit"
SUBSET = URIRef("https://example.org/vitalgraph/ncit-subset")


def extract(records: list, source: str) -> Graph:
    concepts = {record["code"]: record for record in records}
    if len(records) != len(CODES) or set(concepts) != set(CODES):
        raise ValueError("Expected exactly the three VitalGraph NCIt concept records.")
    versions = {record["version"] for record in records}
    if len(versions) != 1 or not all(
        record["terminology"] == "ncit" and record["active"] for record in records
    ):
        raise ValueError("Expected active NCIt concepts from a single release.")

    graph = Graph()
    graph.bind("ncit", NCIT)
    graph.add((SUBSET, RDF.type, OWL.Ontology))
    graph.add((SUBSET, DCTERMS.source, URIRef(source)))
    graph.add((SUBSET, OWL.versionInfo, Literal(versions.pop())))

    for code in CODES:
        record = concepts[code]
        definitions = [
            item["definition"] for item in record["definitions"]
            if item["source"] == "NCI" and item["code"] == "P97"
        ]
        if not record["name"] or not definitions:
            raise ValueError(f"Missing the official name or definition for {code}.")
        term = NCIT[code]
        graph.add((term, RDFS.label, Literal(record["name"])))
        for definition in definitions:
            graph.add((term, NCIT.P97, Literal(definition)))
    return graph


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Use a saved EVS JSON response.")
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parent.parent / "ontology" / "ncit-subset.ttl",
    )
    args = parser.parse_args()
    url = API + "?" + urlencode({"list": ",".join(CODES), "include": "summary"})
    try:
        if args.source:
            if args.source.resolve() == args.output.resolve():
                raise ValueError("The source and output must be different files.")
            with args.source.open(encoding="utf-8") as stream:
                records = json.load(stream)
        else:
            with urlopen(url, timeout=30) as response:
                records = json.load(response)
        graph = extract(records, url)
        graph.serialize(destination=args.output, format="turtle")
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"extract_ncit: {exc}\n")
    print(f"Exported {len(CODES)} NCIt concepts to {args.output}")


if __name__ == "__main__":
    main()
