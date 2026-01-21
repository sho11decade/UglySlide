"""
Configuration and setup utilities for DasaMaker
"""

import os
from pathlib import Path


class Config:
    """Application configuration"""
    
    # File upload settings
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {'pptx'}
    UPLOAD_FOLDER = str(Path(__file__).parent / 'uploads')
    # Optional cleanup TTL (minutes) for periodic sweeper of old files
    CLEANUP_TTL_MINUTES = 60
    
    # Flask settings
    DEBUG = False
    TESTING = False
    # Expose Flask's MAX_CONTENT_LENGTH via our file size setting
    @property
    def MAX_CONTENT_LENGTH(self) -> int:
        return self.MAX_FILE_SIZE
    
    # Application metadata
    APP_NAME = "DasaMaker"
    APP_VERSION = "0.1.0"
    
    @staticmethod
    def get_upload_folder() -> str:
        """Get upload folder path"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        return Config.UPLOAD_FOLDER


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    UPLOAD_FOLDER = str(Path(__file__).parent / 'test_uploads')


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
