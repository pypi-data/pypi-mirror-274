import sys
from rag_cli.embedder import run_embedder
from rag_cli.vector_store import run_vector_store
from rag_cli.cli import cli, list_of_floats


def main():
    args = cli()

    if args.command in ["embed"]:
        # If the file argument is not provided, read from stdin
        if args.file == sys.stdin:
            run_embedder(text=sys.stdin.read(), ollama_url=args.ollama_url)
        else:
            run_embedder(file=args.file, ollama_url=args.ollama_url)
    elif args.command in ["vector-store"]:
        embedding_input = args.embedding.read().strip()
        embedding = list_of_floats(embedding_input)

        run_vector_store(
            qdrant_url=args.qdrant_url,
            collection_name=args.collection_name,
            embedding=embedding,
            data=args.data,
        )


if __name__ == "__main__":
    main()
