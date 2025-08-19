#!/usr/bin/env python3
"""
Test script for agentic retrieval integration
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from backend.agentic_retrieval import agentic_retrieval_service
from backend.settings import app_settings


def test_agentic_retrieval_configuration():
    """Test if agentic retrieval is properly configured"""
    print("=== Testing Agentic Retrieval Configuration ===")
    
    # Check if agentic retrieval is enabled
    if not app_settings.agentic_retrieval:
        print("❌ Agentic retrieval is not configured")
        return False
    
    print(f"✅ Agentic retrieval is configured")
    print(f"   Enabled: {app_settings.agentic_retrieval.enabled}")
    print(f"   Agent Name: {app_settings.agentic_retrieval.agent_name}")
    print(f"   Index Name: {app_settings.agentic_retrieval.index_name}")
    print(f"   Search Endpoint: {app_settings.agentic_retrieval.search_endpoint}")
    print(f"   Reranker Threshold: {app_settings.agentic_retrieval.reranker_threshold}")
    
    return True


def test_agentic_retrieval_service():
    """Test if the agentic retrieval service is available"""
    print("\n=== Testing Agentic Retrieval Service ===")
    
    # Check if service is available
    is_available = agentic_retrieval_service.is_available()
    
    if is_available:
        print("✅ Agentic retrieval service is available")
        return True
    else:
        print("❌ Agentic retrieval service is not available")
        print("   This could be due to:")
        print("   - Invalid credentials")
        print("   - Network connectivity issues")
        print("   - Agent not found")
        print("   - Index not found")
        return False


def test_agentic_retrieval_query():
    """Test a simple agentic retrieval query"""
    print("\n=== Testing Agentic Retrieval Query ===")
    
    if not agentic_retrieval_service.is_available():
        print("❌ Skipping query test - service not available")
        return False
    
    # Test messages
    test_messages = [
        {
            "role": "user",
            "content": "What is the company's organizational structure?"
        }
    ]
    
    try:
        # Perform retrieval
        result = agentic_retrieval_service.retrieve(test_messages)
        
        if result:
            print("✅ Agentic retrieval query successful")
            print(f"   Response length: {len(result)} characters")
            print(f"   Response preview: {result[:200]}...")
            return True
        else:
            print("❌ Agentic retrieval query returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Agentic retrieval query failed: {e}")
        return False


def main():
    """Run all tests"""
    print("Agentic Retrieval Integration Test")
    print("=" * 40)
    
    # Test configuration
    config_ok = test_agentic_retrieval_configuration()
    
    # Test service availability
    service_ok = test_agentic_retrieval_service()
    
    # Test query (only if service is available)
    query_ok = False
    if service_ok:
        query_ok = test_agentic_retrieval_query()
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"Service: {'✅ PASS' if service_ok else '❌ FAIL'}")
    print(f"Query: {'✅ PASS' if query_ok else '❌ FAIL'}")
    
    if config_ok and service_ok and query_ok:
        print("\n🎉 All tests passed! Agentic retrieval is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the configuration and setup.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
