from promptflow import tool
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from promptflow.connections import AzureOpenAIConnection, CognitiveSearchConnection
from promptflow.tracing import trace


@trace
@tool
def retrieve_documents(
    query: str,
    search_connection: CognitiveSearchConnection,
    index_name: str,
    top_k: int = 3
) -> str:
    """
    Retrieve documents from Azure AI Search based on the query.
    """
    if not query:
        return ""

    try:
        # Initialize the SearchClient
        search_client = SearchClient(
            endpoint=search_connection.api_base,
            index_name=index_name,
            credential=AzureKeyCredential(search_connection.api_key)
        )

        # Perform the search
        # Note: This uses simple text search. For vector/hybrid, you'd generate embeddings first.
        results = search_client.search(search_text=query, top=top_k)

        # Process results
        docs = []
        for result in results:
            # Assuming 'content' is the main field. Adjust based on your index schema.
            # We also try to fetch 'title' or 'sourcepage' for better context if available.
            content = result.get('content') or result.get('text') or str(result)
            source = result.get('sourcepage') or result.get('title') or ""
            if source:
                docs.append(f"Source: {source}\nContent: {content}")
            else:
                docs.append(content)

        return "\n\n".join(docs)

    except Exception as e:
        return f"Error retrieving documents: {str(e)}"