#!/usr/bin/env python3
"""
Setup script for agentic retrieval configuration
"""

import os
import sys
from pathlib import Path


def get_user_input(prompt, default=None, required=False):
    """Get user input with optional default value"""
    while True:
        if default:
            user_input = input(f"{prompt} (default: {default}): ").strip()
            if not user_input:
                user_input = default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        if user_input or not required:
            return user_input
        else:
            print("This field is required. Please provide a value.")


def create_env_file():
    """Create or update .env file with agentic retrieval configuration"""
    env_file = Path(".env")
    
    # Check if .env file exists
    existing_vars = {}
    if env_file.exists():
        print("Found existing .env file. Reading current configuration...")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    existing_vars[key] = value
    
    print("\n=== Agentic Retrieval Configuration ===")
    print("This script will help you configure agentic retrieval for your AI RFP application.")
    print("You'll need the following information:")
    print("- Azure AI Search endpoint")
    print("- Knowledge agent name")
    print("- Search index name")
    print("- Azure OpenAI configuration")
    print()
    
    # Get agentic retrieval configuration
    print("Agentic Retrieval Settings:")
    enabled = get_user_input("Enable agentic retrieval?", "true").lower() == "true"
    
    if enabled:
        search_endpoint = get_user_input(
            "Azure AI Search endpoint", 
            existing_vars.get("AGENTIC_RETRIEVAL_SEARCH_ENDPOINT", ""),
            required=True
        )
        
        search_key = get_user_input(
            "Azure AI Search API key (optional if using managed identity)",
            existing_vars.get("AGENTIC_RETRIEVAL_SEARCH_KEY", "")
        )
        
        agent_name = get_user_input(
            "Knowledge agent name",
            existing_vars.get("AGENTIC_RETRIEVAL_AGENT_NAME", "rfp-agent")
        )
        
        index_name = get_user_input(
            "Search index name",
            existing_vars.get("AGENTIC_RETRIEVAL_INDEX_NAME", ""),
            required=True
        )
        
        reranker_threshold = get_user_input(
            "Reranker threshold",
            existing_vars.get("AGENTIC_RETRIEVAL_RERANKER_THRESHOLD", "2.5")
        )
        
        system_message = get_user_input(
            "System message for the agent",
            existing_vars.get("AGENTIC_RETRIEVAL_SYSTEM_MESSAGE", 
                "A Q&A agent that can answer questions about RFP's (requests for proposals) for the Foundever company. If you do not have the answer, respond with 'I don't know'.")
        )
        
        # Get Azure OpenAI configuration if not already set
        print("\nAzure OpenAI Configuration:")
        print("(These are required for agentic retrieval to work)")
        
        openai_endpoint = get_user_input(
            "Azure OpenAI endpoint",
            existing_vars.get("AZURE_OPENAI_ENDPOINT", ""),
            required=True
        )
        
        openai_model = get_user_input(
            "Azure OpenAI model deployment name",
            existing_vars.get("AZURE_OPENAI_MODEL", ""),
            required=True
        )
        
        openai_key = get_user_input(
            "Azure OpenAI API key (optional if using managed identity)",
            existing_vars.get("AZURE_OPENAI_KEY", "")
        )
        
        openai_api_version = get_user_input(
            "Azure OpenAI API version",
            existing_vars.get("AZURE_OPENAI_API_VERSION", "2025-03-01-preview")
        )
        
        embedding_deployment = get_user_input(
            "Azure OpenAI embedding deployment name",
            existing_vars.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
        )
        
        embedding_model = get_user_input(
            "Azure OpenAI embedding model",
            existing_vars.get("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
        )
        
        # Update existing variables
        existing_vars.update({
            "AGENTIC_RETRIEVAL_ENABLED": str(enabled).lower(),
            "AGENTIC_RETRIEVAL_SEARCH_ENDPOINT": search_endpoint,
            "AGENTIC_RETRIEVAL_AGENT_NAME": agent_name,
            "AGENTIC_RETRIEVAL_INDEX_NAME": index_name,
            "AGENTIC_RETRIEVAL_RERANKER_THRESHOLD": reranker_threshold,
            "AGENTIC_RETRIEVAL_SYSTEM_MESSAGE": f'"{system_message}"',
            "AZURE_OPENAI_ENDPOINT": openai_endpoint,
            "AZURE_OPENAI_MODEL": openai_model,
            "AZURE_OPENAI_API_VERSION": openai_api_version,
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT": embedding_deployment,
            "AZURE_OPENAI_EMBEDDING_MODEL": embedding_model,
        })
        
        # Add optional keys if provided
        if search_key:
            existing_vars["AGENTIC_RETRIEVAL_SEARCH_KEY"] = search_key
        if openai_key:
            existing_vars["AZURE_OPENAI_KEY"] = openai_key
    else:
        # Disable agentic retrieval
        existing_vars["AGENTIC_RETRIEVAL_ENABLED"] = "false"
    
    # Write the .env file
    print(f"\nWriting configuration to {env_file}...")
    with open(env_file, 'w') as f:
        f.write("# Agentic Retrieval Configuration\n")
        f.write("# Generated by setup_agentic_retrieval.py\n\n")
        
        for key, value in sorted(existing_vars.items()):
            f.write(f"{key}={value}\n")
    
    print(f"✅ Configuration saved to {env_file}")
    
    if enabled:
        print("\nNext steps:")
        print("1. Ensure your Azure AI Search service has a knowledge agent configured")
        print("2. Verify your search index has semantic configuration and vector search enabled")
        print("3. Test the configuration by running: python test_agentic_retrieval.py")
        print("4. Start your application: python start.cmd")
    else:
        print("\nAgentic retrieval has been disabled.")
        print("To enable it later, run this script again or manually edit the .env file.")


def main():
    """Main function"""
    print("Agentic Retrieval Setup Script")
    print("=" * 40)
    
    try:
        create_env_file()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during setup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
