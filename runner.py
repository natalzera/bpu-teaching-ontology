"""
Modified query runner by Gabriel Natal Coutinho - 12543461

Usage:
- Original way
    python runner.py graph.ttl query.rq

- load data into named graphs:
    python runner.py \\
        --graph ./kommune-navn.ttl http://data.lenka.no/dumps/kommune-navn.ttl \\
        --graph ./kommunesentre-geonames.ttl http://data.lenka.no/dumps/kommunesentre-geonames.ttl \\
        --graph ./about.rdf http://sws.geonames.org/6453350/about.rdf \\
        query.rq

- load extra data into the default graph:
    python runner.py --data ./extra.ttl query.rq

- run a SPARQL Update instead of a query:
    python runner.py --update query.rq

**All of the above can be combined**
"""

import sys
import argparse
from pyoxigraph import (
    Store, QuerySolutions, QueryBoolean, QueryTriples, RdfFormat, NamedNode
)


def print_table(headers, rows):
    widths = [max(len(str(h)), *(len(str(r[i])) for r in rows)) if rows else len(str(h))
              for i, h in enumerate(headers)]
    def fmt(cells):
        return " | ".join(str(c).ljust(w) for c, w in zip(cells, widths))
    print(fmt(headers))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(fmt(r))


def load_data(store, path, graph_iri=None):
    to_graph = NamedNode(graph_iri) if graph_iri else None
    store.load(path=path, to_graph=to_graph)


def run_query(store, query_text):
    result = store.query(query_text)

    if isinstance(result, QuerySolutions):
        headers = [str(v) for v in result.variables]
        rows = [[s[v] for v in result.variables] for s in result]
        print_table(headers, rows)
    elif isinstance(result, QueryTriples):
        serialized = result.serialize(format=RdfFormat.TURTLE)
        if isinstance(serialized, bytes):
            serialized = serialized.decode("utf-8")
        print(serialized, end="")
    elif isinstance(result, QueryBoolean):
        print("Result: YES" if bool(result) else "Result: NO")
    else:
        print(f"Unsupported query result type: {type(result).__name__}")


def run_update(store, update_text):
    store.update(update_text)
    print("Update applied successfully.")
    print("Current size of store: ", len(list(store)))


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Load RDF data into an Oxigraph store (optionally into "
                     "named graphs) and run a SPARQL query or update "
                     "against it."
    )
    parser.add_argument(
        "-g", "--graph",
        nargs=2,
        metavar=("PATH", "IRI"),
        action="append",
        default=[],
        dest="named_graphs",
        help="Load PATH into the named graph identified by IRI "
             "(e.g. its original source URL). May be repeated."
    )
    parser.add_argument(
        "-d", "--data",
        metavar="PATH",
        action="append",
        default=[],
        dest="default_graph_files",
        help="Load PATH into the store's default graph. May be repeated."
    )
    parser.add_argument(
        "-u", "--update",
        action="store_true",
        help="Treat the statement file as a SPARQL Update statement "
             "(INSERT DATA / DELETE / DELETE-WHERE / ...) instead of a "
             "SPARQL query."
    )
    parser.add_argument("pos1", nargs="?", metavar="GRAPH_FILE_or_STATEMENT_FILE")
    parser.add_argument("pos2", nargs="?", metavar="STATEMENT_FILE")

    args = parser.parse_args(argv)

    if args.pos2 is not None:
        args.legacy_graph_file = args.pos1
        args.statement_file = args.pos2
    elif args.pos1 is not None:
        args.legacy_graph_file = None
        args.statement_file = args.pos1
    else:
        parser.error("a statement file (query or update) is required")

    return args


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)

    store = Store()

    if args.legacy_graph_file:
        load_data(store, args.legacy_graph_file)

    for path in args.default_graph_files:
        load_data(store, path)

    for path, iri in args.named_graphs:
        load_data(store, path, graph_iri=iri)

    with open(args.statement_file) as f:
        statement_text = f.read()

    if args.update:
        run_update(store, statement_text)
    else:
        run_query(store, statement_text)


if __name__ == "__main__":
    main()
