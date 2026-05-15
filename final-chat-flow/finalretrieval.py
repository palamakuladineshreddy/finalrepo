from promptflow import tool
from promptflow.connections import CognitiveSearchConnection

@tool
def retrieve_documents(
    query: str,
    search_connection: CognitiveSearchConnection,
    index_name: str,
    top_k: int = 3
) -> str:
    """
    Retrieve documents from Azure AI Search based on the user query.
    """

    # ✅ Prevent execution during tool metadata generation
    if query is None:
        return ""

    if not query.strip():
        return ""

    try:
        # ✅ Import INSIDE function (critical fix)
        from azure.core.credentials import AzureKeyCredential
        from azure.search.documents import SearchClient

        search_client = SearchClient(
            endpoint=search_connection.api_base,
            index_name=index_name,
            credential=AzureKeyCredential(search_connection.api_key)
        )

        # ✅ Force evaluation immediately
        results = list(
            search_client.search(
                search_text=query,
                top=top_k
            )
        )

        docs = []

        for result in results:
            content = ""
            source = ""

            if isinstance(result, dict):
                content = result.get("content") or result.get("text") or ""
                source = result.get("sourcepage") or result.get("title") or ""
            else:
                content = str(result)

            if source:
                docs.append(f"Source: {source}\nContent: {content}")
            else:
                docs.append(content)

        return "\n\n".join(docs)

    except Exception as e:
        return f"Error retrieving documents: {str(e)}"