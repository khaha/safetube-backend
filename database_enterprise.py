# 🗄️ SAFETUBE ENTERPRISE DATABASE - ĐỘC NHẤT
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
import secrets
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'enterprise_users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    company_name = db.Column(db.String(200))
    password_hash = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    billing_address = db.Column(db.Text)
    phone_number = db.Column(db.String(20))
    
    # Relationships
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
    api_keys = db.relationship('APIKey', backref='user', lazy=True)
    scan_requests = db.relationship('ScanRequest', backref='user', lazy=True)
    brand_rules = db.relationship('BrandRule', backref='user', lazy=True)

class Subscription(db.Model):
    __tablename__ = 'enterprise_subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('enterprise_users.id'), nullable=False)
    plan = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='active')
    scans_remaining = db.Column(db.Integer, default=0)
    total_scans = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    stripe_subscription_id = db.Column(db.String(100))
    payment_status = db.Column(db.String(20), default='active')
    
    def is_valid(self):
        return (self.status == 'active' and 
                self.payment_status == 'active' and
                self.scans_remaining > 0 and
                self.expires_at > datetime.utcnow())

class APIKey(db.Model):
    __tablename__ = 'enterprise_api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('enterprise_users.id'), nullable=False)
    key = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    rate_limit = db.Column(db.String(20), default='100/hour')
    
    @staticmethod
    def generate_key():
        return secrets.token_urlsafe(48)

class ScanRequest(db.Model):
    __tablename__ = 'enterprise_scan_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('enterprise_users.id'), nullable=False)
    api_key_id = db.Column(db.Integer, db.ForeignKey('enterprise_api_keys.id'))
    
    # Platform Information
    platform = db.Column(db.String(20))  # youtube, tiktok, facebook, website
    content_type = db.Column(db.String(20))  # video, text, audio, image
    content_url = db.Column(db.String(500))
    content_id = db.Column(db.String(100))  # YouTube video ID, etc.
    
    # Content Information
    content_title = db.Column(db.String(500))
    content_description = db.Column(db.Text)
    content_preview = db.Column(db.Text)
    
    # Scan Results
    is_toxic = db.Column(db.Boolean)
    confidence = db.Column(db.Float)
    risk_level = db.Column(db.String(20))  # low, medium, high, critical
    categories = db.Column(db.Text)  # JSON of toxic categories
    processing_time = db.Column(db.Float)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    # Indexes for performance
    __table_args__ = (
        db.Index('idx_user_platform', 'user_id', 'platform'),
        db.Index('idx_created_at', 'created_at'),
        db.Index('idx_platform_content', 'platform', 'content_id'),
    )

class BrandRule(db.Model):
    __tablename__ = 'enterprise_brand_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('enterprise_users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    rules = db.Column(db.Text)  # JSON rules configuration
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SystemMetrics(db.Model):
    __tablename__ = 'enterprise_system_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Usage Metrics
    active_users = db.Column(db.Integer)
    total_scans_today = db.Column(db.Integer)
    total_scans_month = db.Column(db.Integer)
    
    # Platform Metrics
    youtube_scans = db.Column(db.Integer)
    tiktok_scans = db.Column(db.Integer)
    facebook_scans = db.Column(db.Integer)
    website_scans = db.Column(db.Integer)
    
    # Performance Metrics
    avg_processing_time = db.Column(db.Float)
    error_rate = db.Column(db.Float)
    cache_hit_rate = db.Column(db.Float)
    
    # System Health
    memory_usage = db.Column(db.Float)
    cpu_usage = db.Column(db.Float)
    disk_usage = db.Column(db.Float)

class APILog(db.Model):
    __tablename__ = 'enterprise_api_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    api_key_id = db.Column(db.Integer, db.ForeignKey('enterprise_api_keys.id'))
    endpoint = db.Column(db.String(100))
    method = db.Column(db.String(10))
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.Float)
    user_agent = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_api_key_date', 'api_key_id', 'created_at'),
    )