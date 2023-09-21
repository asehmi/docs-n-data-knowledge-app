MESSAGES = [{
    "role": "user",
    "content": "Help me understand following by describing as a detailed knowledge graph: {user_input}"
}]

FUNCTION_CALL = {"name": "knowledge_graph"}

FUNCTIONS = [{
    "name": "knowledge_graph",
    "description":
        "Generate a knowledge graph with entities and relationships. "
        "Use the colors to help differentiate between different node or edge types/categories. "
        "Always provide light pastel colors that work well with black font.",
    "parameters": {
        "type": "object",
        "properties": {
            "metadata": {
                "type": "object",
                "properties": {
                    "createdDate": {"type": "string"},
                    "lastUpdated": {"type": "string"},
                    "description": {"type": "string"}
                }
            },
            "nodes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "label": {"type": "string"},
                        "type": {"type": "string"},
                        # Added color property
                        "color": {"type": "string"},
                        "properties": {
                            "type": "object",
                            "description": "Additional attributes for the node"
                        }
                    },
                    "required": [
                        "id",
                        "label",
                        "type",
                        "color",
                    ]  # Added color to required
                },
            },
            "edges": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "from": {"type": "string"},
                        "to": {"type": "string"},
                        "relationship": {"type": "string"},
                        "direction": {"type": "string"},
                        # Added color property
                        "color": {"type": "string"},
                        "properties": {
                            "type": "object",
                            "description": "Additional attributes for the edge"
                        }
                    },
                    "required": [
                        "from",
                        "to",
                        "relationship",
                        "color"
                    ]  # Added color to required
                },
            },
        },
        "required": ["nodes", "edges"]
    },
}]

