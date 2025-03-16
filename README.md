# MCP LLM Bridge

A bridge connecting Model Context Protocol (MCP) servers to OpenAI-compatible LLMs like Ollama
Read more about MCP by Anthropic here:

- [Resources](https://modelcontextprotocol.io/docs/concepts/resources)
- [Prompts](https://modelcontextprotocol.io/docs/concepts/prompts)
- [Tools](https://modelcontextprotocol.io/docs/concepts/tools)
- [Sampling](https://modelcontextprotocol.io/docs/concepts/sampling)


## Quick Start

```bash
# Install
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/bartolli/mcp-llm-bridge.git
cd mcp-llm-bridge
uv venv
source .venv/bin/activate
uv pip install -e .


Note: reactivate the environment if needed to use the keys in `.env`: `source .venv/bin/activate`

Then configure the bridge in [src/mcp_llm_bridge/main.py](src/mcp_llm_bridge/main.py)

```python
 mcp_server_params=StdioServerParameters(
            command="uv",
            # CHANGE THIS = it needs to be an absolute directory! add the mcp fetch server at the directory (clone from https://github.com/modelcontextprotocol/servers/)
            args=["--directory", "~/llms/mcp/mc-server-fetch/servers/src/fetch", "run", "mcp-server-fetch"],
            env=None
        ),
        # llm_config=LLMConfig(
        #     api_key=os.getenv("OPENAI_API_KEY"),
        #     model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        #     base_url=None
        # ),
        llm_config=LLMConfig(
            api_key="ollama",  # Can be any string for local testing
            model="llama3.2",
            base_url="http://localhost:11434/v1"  # Point to your local model's endpoint
        ),
)
```

### Additional Endpoint Support

The bridge also works with any endpoint implementing the OpenAI API specification:

#### Ollama

```python
llm_config=LLMConfig(
    api_key="not-needed",
    model="mistral-nemo:12b-instruct-2407-q8_0",
    base_url="http://localhost:11434/v1"
)
```


## License

[MIT](LICENSE.md)

## Contributing

PRs welcome.
