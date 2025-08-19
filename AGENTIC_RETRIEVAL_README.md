# Agentic Retrieval Integration

This document explains how to set up and use the agentic retrieval feature in the AI RFP Agentic web application.

## Overview

Agentic retrieval uses Azure AI Search knowledge agents to provide more intelligent search capabilities. The knowledge agent can:

1. Analyze conversation history to understand information needs
2. Break down complex queries into focused subqueries
3. Run simultaneous searches against text fields and vector embeddings
4. Use semantic ranking to rerank results
5. Merge results into a unified response

## Prerequisites

Before enabling agentic retrieval, ensure you have:

1. **Azure AI Search Service** with a knowledge agent configured
2. **Azure OpenAI Service** with appropriate models deployed
3. **Search Index** with semantic configuration and vector search enabled
4. **Knowledge Agent** created in Azure AI Search

## Configuration

### Environment Variables

Add the following environment variables to your `.env` file:

```bash
# Enable agentic retrieval
AGENTIC_RETRIEVAL_ENABLED=true

# Azure AI Search configuration
AGENTIC_RETRIEVAL_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AGENTIC_RETRIEVAL_SEARCH_KEY=your-search-api-key  # Optional if using managed identity
AGENTIC_RETRIEVAL_AGENT_NAME=rfp-agent
AGENTIC_RETRIEVAL_INDEX_NAME=ai-rfp-project-agentic-index
AGENTIC_RETRIEVAL_RERANKER_THRESHOLD=2.5

# System message for the agent
AGENTIC_RETRIEVAL_SYSTEM_MESSAGE="A Q&A agent that can answer questions about RFP's (requests for proposals) for the Foundever company. If you do not have the answer, respond with 'I don't know'."

# Azure OpenAI configuration (required)
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com/
AZURE_OPENAI_MODEL=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2025-03-01-preview
AZURE_OPENAI_KEY=your-openai-api-key  # Optional if using managed identity
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-3-large
```

### Azure AI Search Index Requirements

Your search index must meet the following requirements for agentic retrieval:

1. **Semantic Configuration**: Must have a `default_configuration_name`
2. **Vector Search**: Must be enabled with appropriate vector fields
3. **Content Fields**: Must have searchable content fields
4. **Metadata Fields**: Should include title, URL, and filepath fields

Example index schema:
```json
{
  "name": "ai-rfp-project-agentic-index",
  "fields": [
    {
      "name": "chunk_id",
      "type": "Edm.String",
      "key": true,
      "searchable": true,
      "filterable": true,
      "retrievable": true,
      "stored": true,
      "sortable": true,
      "facetable": true,
      "analyzer_name": "keyword"
    },
    {
      "name": "content",
      "type": "Edm.String",
      "searchable": true,
      "retrievable": true,
      "stored": true
    },
    {
      "name": "title",
      "type": "Edm.String",
      "searchable": true,
      "retrievable": true,
      "stored": true
    },
    {
      "name": "url",
      "type": "Edm.String",
      "retrievable": true,
      "stored": true
    },
    {
      "name": "filepath",
      "type": "Edm.String",
      "retrievable": true,
      "stored": true
    },
    {
      "name": "content_embedding_text_3_large",
      "type": "Collection(Edm.Single)",
      "stored": true,
      "vector_search_dimensions": 3072,
      "vector_search_profile_name": "hnsw_text_3_large"
    }
  ],
  "vector_search": {
    "profiles": [
      {
        "name": "hnsw_text_3_large",
        "algorithm_configuration_name": "alg",
        "vectorizer_name": "azure_openai_text_3_large"
      }
    ],
    "algorithms": [
      {
        "name": "alg",
        "kind": "hnsw"
      }
    ],
    "vectorizers": [
      {
        "vectorizer_name": "azure_openai_text_3_large",
        "parameters": {
          "resource_url": "https://your-openai-resource.openai.azure.com/",
          "deployment_name": "text-embedding-3-large",
          "model_name": "text-embedding-3-large",
          "api_key": "your-api-key"
        }
      }
    ]
  },
  "semantic_search": {
    "default_configuration_name": "semantic_config",
    "configurations": [
      {
        "name": "semantic_config",
        "prioritized_fields": {
          "content_fields": [
            {
              "field_name": "content"
            }
          ]
        }
      }
    ]
  }
}
```

## Knowledge Agent Setup

### Creating a Knowledge Agent

1. **Navigate to Azure AI Search** in the Azure portal
2. **Go to Knowledge Agents** section
3. **Create a new knowledge agent** with the following configuration:

```json
{
  "name": "rfp-agent",
  "models": [
    {
      "azure_open_ai_parameters": {
        "resource_url": "https://your-openai-resource.openai.azure.com/",
        "deployment_name": "gpt-4o-mini",
        "model_name": "gpt-4o-mini"
      }
    }
  ],
  "target_indexes": [
    {
      "index_name": "ai-rfp-project-agentic-index",
      "default_reranker_threshold": 2.5
    }
  ]
}
```

## How It Works

### Conversation Flow

1. **User sends a message** to the chat interface
2. **Agentic retrieval is triggered** if enabled and available
3. **Knowledge agent analyzes** the conversation history and user query
4. **Subqueries are generated** and executed against the search index
5. **Results are semantically ranked** and merged
6. **Retrieved content is added** as context to the user's message
7. **Azure OpenAI generates** the final response using the enhanced context

### API Endpoints

#### Check Agentic Retrieval Status
```http
GET /agentic_retrieval/status
```

Response:
```json
{
  "enabled": true,
  "available": true,
  "status": "available",
  "agent_name": "rfp-agent",
  "index_name": "ai-rfp-project-agentic-index",
  "message": "Agentic retrieval is available"
}
```

#### Frontend Settings
The frontend settings include agentic retrieval status:
```json
{
  "agentic_retrieval_enabled": true,
  "auth_enabled": true,
  "feedback_enabled": true,
  "ui": { ... },
  "sanitize_answer": false,
  "oyd_enabled": null
}
```

## Troubleshooting

### Common Issues

1. **Agentic retrieval not available**
   - Check if the knowledge agent exists in Azure AI Search
   - Verify the agent name matches the configuration
   - Ensure the search index is properly configured

2. **Authentication errors**
   - Verify API keys are correct
   - Check managed identity permissions if using system-assigned identity
   - Ensure the service has access to both Azure AI Search and Azure OpenAI

3. **No retrieval results**
   - Check if the search index contains relevant documents
   - Verify the reranker threshold is appropriate
   - Review the system message for relevance

### Logging

Enable debug logging to troubleshoot issues:

```bash
DEBUG=true
```

Look for logs related to:
- `AgenticRetrievalService`
- `KnowledgeAgentRetrievalClient`
- Agentic retrieval initialization and requests

## Performance Considerations

1. **Latency**: Agentic retrieval adds additional processing time
2. **Cost**: Each retrieval request consumes Azure AI Search and Azure OpenAI tokens
3. **Rate Limits**: Be aware of Azure AI Search and Azure OpenAI rate limits
4. **Caching**: Consider implementing caching for frequently requested information

## Security

1. **API Keys**: Store API keys securely using environment variables or Azure Key Vault
2. **Managed Identity**: Use managed identity when possible for better security
3. **Network Security**: Ensure proper network security rules for Azure services
4. **Access Control**: Implement appropriate access controls for the knowledge agent

## Monitoring

Monitor the following metrics:
- Agentic retrieval success/failure rates
- Response times
- Token consumption
- Error rates and types

Use Azure Application Insights or similar monitoring tools to track performance and usage.
