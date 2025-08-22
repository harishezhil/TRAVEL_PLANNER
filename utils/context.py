import json


class Context(dict):
    """
    Formal MCP Context.
    Required keys:
        - mcp_version: str
        - model_info: dict
        - user_input: dict
        - history: list
    Optional keys:
        - weather: list
        - events: list
        - itinerary: list
        - rag_output: str
        - llm_summary: str
        - feedback: dict
    """

    def to_json(self):
        return json.dumps(self)

    @staticmethod
    def from_json(json_str):
        return Context(json.loads(json_str))

    def validate(self):
        required = ["mcp_version", "model_info", "user_input", "history"]
        for key in required:
            if key not in self:
                raise ValueError(f"Missing required context key: {key}")
