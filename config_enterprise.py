




# 🏢 SAFETUBE ENTERPRISE - CONFIG ĐỘC NHẤT
import os
from pathlib import Path
import logging
from datetime import timedelta

class Config:
    # Base Configuration
    BASE_DIR = Path(__file__).parent
    SECRET_KEY = os.getenv('SECRET_KEY', 'safetube-enterprise-super-secret-2024')
    
    # Database - SQLite for offline, PostgreSQL for online
    DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/safetube_enterprise.db')
    
    # Redis for caching and performance
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # AI Models Paths
    TEXT_MODEL_PATH = BASE_DIR / "models" / "toxic_model"
    VIDEO_MODEL_PATH = BASE_DIR / "models" / "yolo_violence.pt"
    AUDIO_MODEL_PATH = BASE_DIR / "models" / "whisper"
    
    # Platform API Keys - DÙNG KEY CỦA MÀY
    YOUTUBE_API_KEY = "AIzaSyDOcHc1jv2TVm2_tZHPUHc_ZWLZp6Bs4Ik"
    TIKTOK_CLIENT_KEY = "awm9ieja6jy218ed"
    TIKTOK_CLIENT_SECRET = "gpVBWuLbRqStlQi2LcgB2R3nNVIJyle5"
    FB_USER_TOKEN = "EAAL24MloZCa8BP2fZAQjk8XlVmOZBMsEzjcYrK3lSomZA4ytoBmrQTbZCrZCCYZAGVznyTmewZCFsQan9zXMG2hQj85U8mr7yWzj1r2VzrHdocE5ulMZBwKEFkaSiPav0ho5ZBQzGf2sTxRPOkpEZB0QOnqLmAOC8sIUZBSMIVjJalfqUNfQxpZClJlTC4bx5ERJX55HevrZB2wGENO7tKdpuVDl3LYj0f2e06cD7JUZCrFqpLZBklEEtnfdkgipDP3A0MkbJuUKZBpyAhp4uGB5iRQnHyIN4yYZAGmqX0cATX7YyQz5bPcxCt1rd0sLemDjgUpg7Q6x1ZACbTl1HJqaM02jeZBO1H9oNWrHgwZDZD"
    
    # VnCoreNLP for Vietnamese NLP
    VNCORENLP_HOST = "http://127.0.0.1:54053"
    
    # Security & Performance
    CORS_ORIGINS = ["https://safetube.ai", "http://localhost:3000", "*"]
    RATE_LIMIT_STORAGE_URL = REDIS_URL
    MODEL_CACHE_SIZE = 1000
    REQUEST_TIMEOUT = 60
    
    # Monitoring & Logging
    LOG_LEVEL = logging.INFO
    ENABLE_METRICS = True
    
    # Platform Configuration
    PLATFORMS = {
        "youtube": {
            "name": "YouTube",
            "scan_types": ["video", "comments", "metadata"],
            "api_required": True,
            "offline_support": True
        },
        "tiktok": {
            "name": "TikTok", 
            "scan_types": ["video", "comments", "metadata"],
            "api_required": True,
            "offline_support": True
        },
        "facebook": {
            "name": "Facebook",
            "scan_types": ["post", "comments", "video"],
            "api_required": True,
            "offline_support": True
        },
        "website": {
            "name": "Website",
            "scan_types": ["text", "images"],
            "api_required": False,
            "offline_support": True
        },
        "instagram": {
            "name": "Instagram",
            "scan_types": ["post", "comments", "images"],
            "api_required": True,
            "offline_support": True
        }
    }
    
    # Subscription Plans - ENTERPRISE GRADE
    SUBSCRIPTION_PLANS = {
        "starter": {
            "name": "Starter",
            "price": 99,
            "scans": 100,
            "rate_limit": "50/hour",
            "platforms": ["youtube", "website"],
            "features": [
                "Text Content Scanning",
                "Basic YouTube Integration", 
                "Email Support",
                "Basic Dashboard"
            ],
            "offline_support": True
        },
        "professional": {
            "name": "Professional",
            "price": 299,
            "scans": 500,
            "rate_limit": "200/hour", 
            "platforms": ["youtube", "tiktok", "facebook", "website"],
            "features": [
                "Text + Video Content Scanning",
                "Multi-Platform Support",
                "API Access",
                "Advanced Analytics",
                "Priority Support",
                "Custom Brand Rules"
            ],
            "offline_support": True
        },
        "enterprise": {
            "name": "Enterprise", 
            "price": 999,
            "scans": "Unlimited",
            "rate_limit": "1000/hour",
            "platforms": ["youtube", "tiktok", "facebook", "website", "instagram"],
            "features": [
                "All Platform Scanning",
                "Unlimited API Requests", 
                "Real-time Monitoring",
                "Custom AI Models",
                "Dedicated Support",
                "SLA 99.9% Uptime",
                "White-label Solution",
                "On-premise Deployment"
            ],
            "offline_support": True
        }
    }

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.WARNING

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///test_safetube.db'
import os
from pathlib import Path
import logging
from datetime import timedelta

class Config:
    # Base Configuration
    BASE_DIR = Path(__file__).parent
    SECRET_KEY = os.getenv('SECRET_KEY', 'safetube-enterprise-super-secret-2024')
    
    # Database - SQLite for offline, PostgreSQL for online
    DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/safetube_enterprise.db')
    
    # Redis for caching and performance
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # AI Models Paths
    TEXT_MODEL_PATH = BASE_DIR / "models" / "toxic_model"
    VIDEO_MODEL_PATH = BASE_DIR / "models" / "yolo_violence.pt"
    AUDIO_MODEL_PATH = BASE_DIR / "models" / "whisper"
    
    # Platform API Keys - DÙNG KEY CỦA MÀY
    YOUTUBE_API_KEY = "AIzaSyDOcHc1jv2TVm2_tZHPUHc_ZWLZp6Bs4Ik"
    TIKTOK_CLIENT_KEY = "awm9ieja6jy218ed"
    TIKTOK_CLIENT_SECRET = "gpVBWuLbRqStlQi2LcgB2R3nNVIJyle5"
    FB_USER_TOKEN = "EAAL24MloZCa8BP2fZAQjk8XlVmOZBMsEzjcYrK3lSomZA4ytoBmrQTbZCrZCCYZAGVznyTmewZCFsQan9zXMG2hQj85U8mr7yWzj1r2VzrHdocE5ulMZBwKEFkaSiPav0ho5ZBQzGf2sTxRPOkpEZB0QOnqLmAOC8sIUZBSMIVjJalfqUNfQxpZClJlTC4bx5ERJX55HevrZB2wGENO7tKdpuVDl3LYj0f2e06cD7JUZCrFqpLZBklEEtnfdkgipDP3A0MkbJuUKZBpyAhp4uGB5iRQnHyIN4yYZAGmqX0cATX7YyQz5bPcxCt1rd0sLemDjgUpg7Q6x1ZACbTl1HJqaM02jeZBO1H9oNWrHgwZDZD"
    
    # VnCoreNLP for Vietnamese NLP
    VNCORENLP_HOST = "http://127.0.0.1:54053"
    
    # Security & Performance
    CORS_ORIGINS = ["https://safetube.ai", "http://localhost:3000", "*"]
    RATE_LIMIT_STORAGE_URL = REDIS_URL
    MODEL_CACHE_SIZE = 1000
    REQUEST_TIMEOUT = 60
    
    # Monitoring & Logging
    LOG_LEVEL = logging.INFO
    ENABLE_METRICS = True
    
    # Platform Configuration
    PLATFORMS = {
        "youtube": {
            "name": "YouTube",
            "scan_types": ["video", "comments", "metadata"],
            "api_required": True,
            "offline_support": True
        },
        "tiktok": {
            "name": "TikTok", 
            "scan_types": ["video", "comments", "metadata"],
            "api_required": True,
            "offline_support": True
        },
        "facebook": {
            "name": "Facebook",
            "scan_types": ["post", "comments", "video"],
            "api_required": True,
            "offline_support": True
        },
        "website": {
            "name": "Website",
            "scan_types": ["text", "images"],
            "api_required": False,
            "offline_support": True
        },
        "instagram": {
            "name": "Instagram",
            "scan_types": ["post", "comments", "images"],
            "api_required": True,
            "offline_support": True
        }
    }
    
    # Subscription Plans - ENTERPRISE GRADE
    SUBSCRIPTION_PLANS = {
        "starter": {
            "name": "Starter",
            "price": 99,
            "scans": 100,
            "rate_limit": "50/hour",
            "platforms": ["youtube", "website"],
            "features": [
                "Text Content Scanning",
                "Basic YouTube Integration", 
                "Email Support",
                "Basic Dashboard"
            ],
            "offline_support": True
        },
        "professional": {
            "name": "Professional",
            "price": 299,
            "scans": 500,
            "rate_limit": "200/hour", 
            "platforms": ["youtube", "tiktok", "facebook", "website"],
            "features": [
                "Text + Video Content Scanning",
                "Multi-Platform Support",
                "API Access",
                "Advanced Analytics",
                "Priority Support",
                "Custom Brand Rules"
            ],
            "offline_support": True
        },
        "enterprise": {
            "name": "Enterprise", 
            "price": 999,
            "scans": "Unlimited",
            "rate_limit": "1000/hour",
            "platforms": ["youtube", "tiktok", "facebook", "website", "instagram"],
            "features": [
                "All Platform Scanning",
                "Unlimited API Requests", 
                "Real-time Monitoring",
                "Custom AI Models",
                "Dedicated Support",
                "SLA 99.9% Uptime",
                "White-label Solution",
                "On-premise Deployment"
            ],
            "offline_support": True
        }
    }

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.WARNING

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = 'sqlite:///test_safetube.db'
