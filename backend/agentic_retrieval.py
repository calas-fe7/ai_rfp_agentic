import logging
import json
from typing import List, Dict, Any, Optional
from azure.search.documents.agent import KnowledgeAgentRetrievalClient
from azure.search.documents.agent.models import (
    KnowledgeAgentRetrievalRequest, 
    KnowledgeAgentMessage, 
    KnowledgeAgentMessageTextContent, 
    KnowledgeAgentIndexParams
)
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from backend.settings import app_settings


class AgenticRetrievalService:
    """Service for handling agentic retrieval using Azure AI Search knowledge agents"""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the knowledge agent retrieval client"""
        if not app_settings.agentic_retrieval or not app_settings.agentic_retrieval.enabled:
            logging.debug("Agentic retrieval not enabled")
            return
        
        try:
            # Get credentials
            if app_settings.agentic_retrieval.search_key:
                credential = AzureKeyCredential(app_settings.agentic_retrieval.search_key)
            else:
                credential = DefaultAzureCredential()
            
            # Initialize the client
            self.client = KnowledgeAgentRetrievalClient(
                endpoint=app_settings.agentic_retrieval.search_endpoint,
                agent_name=app_settings.agentic_retrieval.agent_name,
                credential=credential
            )
            logging.info(f"Agentic retrieval client initialized for agent: {app_settings.agentic_retrieval.agent_name}")
            
        except Exception as e:
            logging.error(f"Failed to initialize agentic retrieval client: {e}")
            self.client = None
    
    def is_available(self) -> bool:
        """Check if agentic retrieval is available"""
        return self.client is not None
    
    def retrieve(self, messages: List[Dict[str, Any]]) -> Optional[str]:
        """
        Perform agentic retrieval using the knowledge agent
        
        Args:
            messages: List of conversation messages
            
        Returns:
            Retrieved content as string, or None if retrieval failed
        """
        if not self.is_available():
            logging.warning("Agentic retrieval not available")
            return None
        
        try:
            # Convert messages to the format expected by the agent
            agent_messages = []
            for msg in messages:
                if msg.get("role") != "system":  # Skip system messages
                    agent_messages.append(
                        KnowledgeAgentMessage(
                            role=msg["role"],
                            content=[KnowledgeAgentMessageTextContent(text=msg["content"])]
                        )
                    )
            
            # Create retrieval request
            retrieval_request = KnowledgeAgentRetrievalRequest(
                messages=agent_messages,
                target_index_params=[
                    KnowledgeAgentIndexParams(
                        index_name=app_settings.agentic_retrieval.index_name,
                        reranker_threshold=app_settings.agentic_retrieval.reranker_threshold
                    )
                ]
            )
            
            # Perform retrieval
            retrieval_result = self.client.retrieve(retrieval_request)
            
            # Extract the response content
            if retrieval_result.response and len(retrieval_result.response) > 0:
                response_content = retrieval_result.response[0].content[0].text
                logging.debug(f"Agentic retrieval successful, content length: {len(response_content)}")
                return response_content
            else:
                logging.warning("No response content from agentic retrieval")
                return None
                
        except Exception as e:
            logging.error(f"Error during agentic retrieval: {e}")
            return None
    
    def get_retrieval_activity(self, retrieval_result) -> List[Dict[str, Any]]:
        """Get activity information from retrieval result"""
        if hasattr(retrieval_result, 'activity'):
            return [activity.as_dict() for activity in retrieval_result.activity]
        return []
    
    def get_retrieval_references(self, retrieval_result) -> List[Dict[str, Any]]:
        """Get reference information from retrieval result"""
        if hasattr(retrieval_result, 'references'):
            return [reference.as_dict() for reference in retrieval_result.references]
        return []


# Global instance
agentic_retrieval_service = AgenticRetrievalService()
