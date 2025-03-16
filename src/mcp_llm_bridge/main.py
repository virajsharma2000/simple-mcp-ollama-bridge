# src/mcp_llm_bridge/main.py
import os
import asyncio
from dotenv import load_dotenv
from mcp import StdioServerParameters
from mcp_llm_bridge.config import BridgeConfig, LLMConfig
from mcp_llm_bridge.bridge import BridgeManager
import colorlog
import logging

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s%(reset)s:     %(cyan)s%(name)s%(reset)s - %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
))

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

async def main():
    # Load environment variables
    load_dotenv()

    # Configure bridge
    config = BridgeConfig(
        mcp_server_params=StdioServerParameters(
            command="uv",
            # CHANGE THIS = it needs to be an absolute directory!
            args=["--directory", "/home/yash/llms/mcp/mc-server-fetch/servers/src/fetch", "run", "mcp-server-fetch"],
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
        system_prompt="You are a helpful assistant that can use tools to help answer questions."
    )
    
    logger.info(f"Starting bridge with model: {config.llm_config.model}")
    
    
    # Use bridge with context manager
    async with BridgeManager(config) as bridge:
        while True:
            try:
                user_input = input("\nEnter your prompt (or 'quit' to exit): ")
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                    
                response = await bridge.process_message(user_input)
                print(f"\nResponse: {response}")
                
            except KeyboardInterrupt:
                logger.info("\nExiting...")
                break
            except Exception as e:
                logger.error(f"\nError occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())