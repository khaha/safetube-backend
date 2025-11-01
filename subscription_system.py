# 💰 SAFETUBE ENTERPRISE SUBSCRIPTION SYSTEM - ĐỘC NHẤT
import json
import hashlib
import datetime
from pathlib import Path
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EnterpriseSubscriptionSystem:
    def __init__(self, db):
        self.db = db
        self.subscription_plans = {
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
                "scans": 99999,  # Effectively unlimited
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
    
    def create_subscription(self, email, plan="starter", company_name=""):
        """Create new enterprise subscription"""
        try:
            from database_enterprise import User, Subscription, APIKey
            
            # Create user
            user = User(
                email=email,
                company_name=company_name,
                created_at=datetime.utcnow()
            )
            self.db.session.add(user)
            self.db.session.flush()  # Get user ID
            
            # Create subscription
            subscription = Subscription(
                user_id=user.id,
                plan=plan,
                scans_remaining=self.subscription_plans[plan]["scans"],
                expires_at=datetime.utcnow() + timedelta(days=30),
                payment_status='active'
            )
            self.db.session.add(subscription)
            
            # Create API key
            api_key = APIKey(
                user_id=user.id,
                key=self._generate_api_key(),
                name='Primary API Key',
                rate_limit=self.subscription_plans[plan]["rate_limit"]
            )
            self.db.session.add(api_key)
            
            self.db.session.commit()
            
            logger.info(f"✅ Subscription created for {email} - Plan: {plan}")
            
            return {
                'success': True,
                'user_id': user.id,
                'api_key': api_key.key,
                'plan': plan,
                'plan_info': self.subscription_plans[plan],
                'scans_remaining': subscription.scans_remaining
            }
            
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"❌ Subscription creation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def validate_subscription(self, api_key, platform=None, scan_type='text'):
        """Validate subscription and deduct scan"""
        try:
            from database_enterprise import APIKey, Subscription
            
            # Find API key
            api_key_obj = APIKey.query.filter_by(key=api_key, is_active=True).first()
            if not api_key_obj:
                return False, "Invalid API key"
            
            # Find active subscription
            subscription = Subscription.query.filter_by(
                user_id=api_key_obj.user_id, 
                status='active',
                payment_status='active'
            ).first()
            
            if not subscription:
                return False, "No active subscription"
            
            # Check if platform is allowed
            if platform and platform not in self.subscription_plans[subscription.plan]["platforms"]:
                return False, f"Platform {platform} not allowed in {subscription.plan} plan"
            
            # Check scans remaining
            if subscription.scans_remaining <= 0:
                return False, "No scans remaining"
            
            # Deduct scan
            subscription.scans_remaining -= 1
            subscription.total_scans += 1
            api_key_obj.last_used = datetime.utcnow()
            
            self.db.session.commit()
            
            return True, "Valid subscription"
            
        except Exception as e:
            logger.error(f"Subscription validation failed: {e}")
            return False, f"Validation error: {str(e)}"
    
    def get_subscription_info(self, api_key):
        """Get subscription information"""
        try:
            from database_enterprise import APIKey, Subscription, User
            
            api_key_obj = APIKey.query.filter_by(key=api_key).first()
            if not api_key_obj:
                return None
            
            subscription = Subscription.query.filter_by(user_id=api_key_obj.user_id).first()
            user = User.query.get(api_key_obj.user_id)
            
            if not subscription:
                return None
            
            return {
                'user': {
                    'email': user.email,
                    'company_name': user.company_name
                },
                'subscription': {
                    'plan': subscription.plan,
                    'status': subscription.status,
                    'scans_remaining': subscription.scans_remaining,
                    'total_scans': subscription.total_scans,
                    'expires_at': subscription.expires_at.isoformat()
                },
                'plan_info': self.subscription_plans[subscription.plan]
            }
            
        except Exception as e:
            logger.error(f"Get subscription info failed: {e}")
            return None
    
    def upgrade_subscription(self, api_key, new_plan):
        """Upgrade subscription plan"""
        try:
            from database_enterprise import APIKey, Subscription
            
            api_key_obj = APIKey.query.filter_by(key=api_key).first()
            if not api_key_obj:
                return {'success': False, 'error': 'Invalid API key'}
            
            subscription = Subscription.query.filter_by(user_id=api_key_obj.user_id).first()
            if not subscription:
                return {'success': False, 'error': 'No subscription found'}
            
            # Calculate additional scans
            current_plan_scans = self.subscription_plans[subscription.plan]["scans"]
            new_plan_scans = self.subscription_plans[new_plan]["scans"]
            additional_scans = new_plan_scans - current_plan_scans
            
            # Update subscription
            subscription.plan = new_plan
            subscription.scans_remaining += additional_scans
            
            # Update API key rate limit
            api_key_obj.rate_limit = self.subscription_plans[new_plan]["rate_limit"]
            
            self.db.session.commit()
            
            return {
                'success': True,
                'new_plan': new_plan,
                'scans_remaining': subscription.scans_remaining,
                'rate_limit': api_key_obj.rate_limit
            }
            
        except Exception as e:
            self.db.session.rollback()
            logger.error(f"Subscription upgrade failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_usage_analytics(self, api_key, days=30):
        """Get usage analytics for subscription"""
        try:
            from database_enterprise import APIKey, ScanRequest
            from datetime import datetime, timedelta
            
            api_key_obj = APIKey.query.filter_by(key=api_key).first()
            if not api_key_obj:
                return None
            
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Get scan requests for the period
            scans = ScanRequest.query.filter(
                ScanRequest.user_id == api_key_obj.user_id,
                ScanRequest.created_at >= start_date
            ).all()
            
            # Calculate analytics
            platform_usage = {}
            risk_distribution = {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            }
            
            for scan in scans:
                # Platform usage
                platform = scan.platform or 'unknown'
                platform_usage[platform] = platform_usage.get(platform, 0) + 1
                
                # Risk distribution
                risk_level = scan.risk_level or 'low'
                risk_distribution[risk_level] = risk_distribution.get(risk_level, 0) + 1
            
            return {
                'total_scans': len(scans),
                'platform_usage': platform_usage,
                'risk_distribution': risk_distribution,
                'period_days': days
            }
            
        except Exception as e:
            logger.error(f"Usage analytics failed: {e}")
            return None
    
    def _generate_api_key(self):
        """Generate secure API key"""
        import secrets
        return f"st_{secrets.token_urlsafe(48)}"