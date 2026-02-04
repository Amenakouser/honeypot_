"""
Firebase Admin SDK initialization and configuration.

This module initializes the Firebase Admin SDK using environment variables
for secure credential management. It provides a singleton Firestore client
for use throughout the application.
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Global Firestore client
_firestore_client: Optional[firestore.Client] = None


def initialize_firebase() -> Optional[firestore.Client]:
    """
    Initialize Firebase Admin SDK with environment variables.
    
    Returns:
        Firestore client instance or None if initialization fails
    """
    global _firestore_client
    
    if _firestore_client is not None:
        return _firestore_client
    
    try:
        # Check if Firebase is already initialized
        if firebase_admin._apps:
            logger.info("Firebase already initialized")
            _firestore_client = firestore.client()
            return _firestore_client
        
        # Build service account credentials from environment variables
        firebase_config = {
            "type": os.getenv("FIREBASE_TYPE", "service_account"),
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": os.getenv("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
            "token_uri": os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
            "auth_provider_x509_cert_url": os.getenv(
                "FIREBASE_AUTH_PROVIDER_CERT_URL",
                "https://www.googleapis.com/oauth2/v1/certs"
            ),
            "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL"),
        }
        
        # Validate required fields
        required_fields = ["project_id", "private_key", "client_email"]
        missing_fields = [field for field in required_fields if not firebase_config.get(field)]
        
        if missing_fields:
            logger.warning(
                f"Firebase initialization skipped - missing environment variables: "
                f"{', '.join(missing_fields)}"
            )
            return None
        
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
        
        # Get Firestore client
        _firestore_client = firestore.client()
        
        logger.info(f"Firebase initialized successfully for project: {firebase_config['project_id']}")
        return _firestore_client
        
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        return None


def get_firestore_client() -> Optional[firestore.Client]:
    """
    Get the Firestore client instance.
    
    Returns:
        Firestore client or None if not initialized
    """
    global _firestore_client
    
    if _firestore_client is None:
        _firestore_client = initialize_firebase()
    
    return _firestore_client


def check_firebase_health() -> bool:
    """
    Check if Firebase connection is healthy.
    
    Returns:
        True if Firebase is accessible, False otherwise
    """
    try:
        client = get_firestore_client()
        if client is None:
            return False
        
        # Try to access a collection (doesn't create it if it doesn't exist)
        client.collection("health_check").limit(1).get()
        return True
        
    except Exception as e:
        logger.error(f"Firebase health check failed: {str(e)}")
        return False
