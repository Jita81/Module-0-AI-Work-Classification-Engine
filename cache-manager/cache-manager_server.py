#!/usr/bin/env python3
"""
MCP Server Runner for cache-manager

This script starts the CacheManager MCP server with proper configuration
and error handling. It can be used directly or imported as a module.
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core import CacheManagerMCPServer
from types import CacheManagerConfig


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr),  # MCP uses stderr for logging
            logging.FileHandler(f'cache-manager_mcp.log')
        ]
    )


async def run_mcp_server():
    """Run the MCP server with proper error handling"""
    
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # AI_TODO: Load configuration from environment or config file
        config = CacheManagerConfig()
        
        # Create and initialize MCP server
        server = CacheManagerMCPServer(config)
        
        if not await server.initialize():
            logger.error("Failed to initialize MCP server")
            sys.exit(1)
        
        logger.info(f"Starting CacheManager MCP Server...")
        
        # Run the server
        await server.server.run_stdio()
        
    except KeyboardInterrupt:
        logger.info("MCP server stopped by user")
    except Exception as e:
        logger.error(f"MCP server error: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        if 'server' in locals():
            await server.cleanup()


def main():
    """Main entry point"""
    asyncio.run(run_mcp_server())


if __name__ == "__main__":
    main()
