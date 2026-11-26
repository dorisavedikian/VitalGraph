#!/usr/bin/env python3
"""Generate English reference labels and Armenian placeholders from ontology subsets."""

import argparse
from pathlib import Path
from tempfile import NamedTemporaryFile

from rdflib import Graph, Literal, OWL, RDF, RDFS, URIRef
from rdflib.plugins.serializers.turtle import TurtleSerializer

TERM_TYPES = {
    OWL.Class,
    RDFS.Class,
    OWL.ObjectProperty,
    OWL.DatatypeProperty,
    OWL.AnnotationProperty,
    OWL.NamedIndividual,
    RDF.Property,
}
# These display terms may be referenced without definitions in the subsets.
DISPLAY_LABELS = {
    RDF.type: Literal('type', lang='en'),
    RDFS.label: Literal('label', lang='en'),
    RDFS.subClassOf: Literal('subClassOf', lang='en'),
}


class EnglishFirstTurtleSerializer(TurtleSerializer):
    """Place English and untagged reference labels before Armenian labels."""

    def sortProperties(self, properties):
        """Preserve RDFLib's predicate order and reorder only label values."""
        predicates = super().sortProperties(properties)
        if RDFS.label in properties:
            properties[RDFS.label].sort(key=lambda value: (
                0 if isinstance(value, Literal) and (
                    not value.language or value.language.lower().split('-')[0] == 'en'
                ) else 1,
                str(value),
            ))
        return predicates


def main():
    """Refresh source English labels and preserve existing Armenian translations.

    Copy English-tagged and untagged labels with their original wording and
    datatypes. Use standard English fallbacks for the three additional schema
    terms when their labels are absent from the subsets. Add an empty @hy
    placeholder only when the term has no Armenian label.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ontology-dir", type=Path,
        default=Path(__file__).resolve().parent.parent / 'ontology',
        help='Directory containing *subset.ttl files.',
    )
    parser.add_argument(
        '--output', type=Path,
        help='Labels file to create or extend. Defaults to ontology-dir/labels-hy.ttl.',
    )
    args = parser.parse_args()
    output = args.output or args.ontology_dir / 'labels-hy.ttl'
    sources = sorted(args.ontology_dir.glob('*subset.ttl'))
    if not sources:
        parser.error(f'No *subset.ttl files found in {args.ontology_dir}')
    if any(output.resolve() == source.resolve() for source in sources):
        parser.error('The labels output must differ from every input subset.')

    definitions = Graph()
    for source in sources:
        definitions.parse(source, format='turtle')

    terms = set(DISPLAY_LABELS)
    for subject in set(definitions.subjects()):
        if not isinstance(subject, URIRef):
            continue
        types = set(definitions.objects(subject, RDF.type))
        if OWL.Ontology in types:
            continue
        if types & TERM_TYPES or any(definitions.objects(subject, RDFS.label)):
            terms.add(subject)

    labels = Graph()
    if output.exists():
        labels.parse(output, format='turtle')
    # Use explicit prefixes in the Turtle header, including on repeated runs.
    for prefix, namespace in (
        ('foaf', 'http://xmlns.com/foaf/0.1/'),
        ('ncit', 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#'),
        ('person', 'https://w3id.org/MON/person.owl#'),
        ('rdf', str(RDF)),
        ('rdfs', str(RDFS)),
        ('rico', 'https://www.ica.org/standards/RiC/ontology#'),
    ):
        labels.bind(prefix, URIRef(namespace), override=True, replace=True)

    added = 0
    english_count = 0
    for term in sorted(terms):
        english = {
            value for value in definitions.objects(term, RDFS.label)
            if isinstance(value, Literal) and str(value) and (
                not value.language or value.language.lower().split('-')[0] == 'en'
            )
        }
        if not english and term in DISPLAY_LABELS:
            english.add(DISPLAY_LABELS[term])
        if english:
            for value in list(labels.objects(term, RDFS.label)):
                if isinstance(value, Literal) and (
                    not value.language or value.language.lower().split('-')[0] == 'en'
                ):
                    labels.remove((term, RDFS.label, value))
            for value in english:
                labels.add((term, RDFS.label, value))
            english_count += len(english)
        armenian = [
            value for value in labels.objects(term, RDFS.label)
            if isinstance(value, Literal)
            and value.language
            and value.language.lower().split('-')[0] == 'hy'
        ]
        if any(str(value) for value in armenian):
            labels.remove((term, RDFS.label, Literal('', lang='hy')))
        elif not armenian:
            labels.add((term, RDFS.label, Literal('', lang='hy')))
            added += 1

    output.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=output.parent, prefix='.labels-hy-', delete=False) as temp:
        temporary = Path(temp.name)
    try:
        with temporary.open('wb') as stream:
            EnglishFirstTurtleSerializer(labels).serialize(stream, encoding='utf-8')
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    print(f'Read {len(sources)} subsets; found {len(terms)} named terms.')
    print(f'Included {english_count} English reference labels.')
    print(f'Added {added} Armenian label placeholders to {output}')


if __name__ == '__main__':
    main()
