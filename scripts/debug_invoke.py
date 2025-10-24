import traceback
import importlib.util
from pathlib import Path

# Load the project's app.py by absolute path to avoid name conflicts with other packages
APP_PATH = Path(r"e:\LLMOPS-AIOPS-PROJECTS\flipkart-product-recommender\app.py").resolve()


def load_create_app():
    spec = importlib.util.spec_from_file_location("local_app", str(APP_PATH))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.create_app


def main():
    # Build the vector store and RAG chain directly (same as create_app) so we can call invoke
    from flipkart.data_ingestion import DataIngestor
    from flipkart.rag_chain import RAGChainBuilder

    try:
        print('Ingesting data (this may take a moment)')
        vector_store = DataIngestor().ingest(load_existing=True)
        rag_chain = RAGChainBuilder(vector_store=vector_store).build_chain()

        print('rag_chain repr:', repr(rag_chain))
        # Try to print input schema and its fields if present
        try:
            schema = rag_chain.get_input_schema()
            print('Input schema class:', schema)
            try:
                fields = getattr(schema, '__fields__', None)
                if fields:
                    print('Schema fields:')
                    for k, v in fields.items():
                        print(' -', k, ':', v.type_)
            except Exception:
                pass
        except Exception:
            pass

        # Try invocation as a plain string
        try:
            print('\nTrying invoke with plain string input...')
            res1 = rag_chain.invoke(
                "is this phone good?",
                config={"configurable": {"session_id": "debug-session"}},
            )
            print('Result (string):', res1)
        except Exception:
            print('Exception for string input:')
            traceback.print_exc()

        # Try invocation with dict input under 'input' key
        try:
            print('\nTrying invoke with dict input...')
            res2 = rag_chain.invoke(
                {"input": "is this phone good?"},
                config={"configurable": {"session_id": "debug-session"}},
            )
            print('Result (dict):', res2)
        except Exception:
            print('Exception for dict input:')
            traceback.print_exc()
    except Exception:
        print('Exception raised during rag_chain.invoke:')
        traceback.print_exc()


if __name__ == '__main__':
    main()
