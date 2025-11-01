



# 🚀 SAFETUBE ENTERPRISE MAIN APP - BẢN ĐẶC BIỆT ĐỘC NHẤT
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
from datetime import datetime
import os
import json

from config_enterprise import DevelopmentConfig
from database_enterprise import db, User, Subscription, APIKey, ScanRequest
from ai_engine_enterprise import EnterpriseAIEngine
from platform_scanners import EnterprisePlatformScanners
from subscription_system import EnterpriseSubscriptionSystem

# Setup logging
logging.basicConfig(level=DevelopmentConfig.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = DevelopmentConfig.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DevelopmentConfig.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)

# Initialize enterprise services
ai_engine = EnterpriseAIEngine(DevelopmentConfig)
platform_scanners = EnterprisePlatformScanners(DevelopmentConfig, ai_engine)
subscription_system = EnterpriseSubscriptionSystem(db)

# ==================== ENTERPRISE ROUTES ====================

@app.route('/')
def enterprise_dashboard():
    """Enterprise Dashboard"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 SafeTube Enterprise - Brand Safety Platform</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            :root {
                --primary: #2c3e50;
                --secondary: #3498db;
                --danger: #e74c3c;
                --success: #27ae60;
                --warning: #f39c12;
            }
            
            .enterprise-header {
                background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
                color: white;
                padding: 4rem 0;
                margin-bottom: 3rem;
            }
            
            .platform-card {
                background: white;
                border-radius: 15px;
                padding: 2rem;
                margin: 1rem 0;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                border-left: 5px solid var(--secondary);
                transition: transform 0.3s ease;
            }
            
            .platform-card:hover {
                transform: translateY(-5px);
            }
            
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
                padding: 1.5rem;
                margin: 0.5rem;
                text-align: center;
            }
            
            .subscription-tier {
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 2rem;
                margin: 1rem;
                text-align: center;
                transition: all 0.3s ease;
            }
            
            .subscription-tier:hover {
                border-color: var(--secondary);
                transform: scale(1.05);
            }
            
            .subscription-tier.enterprise {
                border-color: var(--secondary);
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
            }
            
            .risk-critical { background: var(--danger); color: white; }
            .risk-high { background: var(--warning); color: white; }
            .risk-medium { background: #f1c40f; color: white; }
            .risk-low { background: var(--success); color: white; }
            
            .api-demo {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 2rem;
                margin: 2rem 0;
            }
        </style>
    </head>
    <body>
        <!-- Enterprise Header -->
        <div class="enterprise-header">
            <div class="container">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <h1 class="display-3 fw-bold">
                            <i class="fas fa-shield-alt"></i> SafeTube Enterprise
                        </h1>
                        <p class="lead fs-4">AI-Powered Brand Safety Platform for YouTube, TikTok, Facebook & Websites</p>
                        <div class="mt-4">
                            <span class="badge bg-success me-2"><i class="fas fa-bolt"></i> Real-time Scanning</span>
                            <span class="badge bg-info me-2"><i class="fas fa-cloud"></i> Multi-Platform</span>
                            <span class="badge bg-warning me-2"><i class="fas fa-lock"></i> Enterprise Security</span>
                            <span class="badge bg-danger"><i class="fas fa-rocket"></i> High Performance</span>
                        </div>
                    </div>
                    <div class="col-md-4 text-end">
                        <div class="metric-card">
                            <h4><i class="fas fa-chart-line"></i> System Status</h4>
                            <div id="systemMetrics">Loading...</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="container">
            <!-- Platform Scanning -->
            <div class="row mb-5">
                <div class="col-12">
                    <h2 class="text-center mb-4">
                        <i class="fas fa-satellite-dish"></i> Multi-Platform Content Scanning
                    </h2>
                </div>
                
                <!-- YouTube Scanner -->
                <div class="col-md-6">
                    <div class="platform-card">
                        <h3><i class="fab fa-youtube text-danger"></i> YouTube Scanner</h3>
                        <p class="text-muted">Scan videos, comments, and metadata for toxic content</p>
                        
                        <div class="mb-3">
                            <label class="form-label">YouTube URL:</label>
                            <input type="text" class="form-control" id="youtubeUrl" placeholder="https://www.youtube.com/watch?v=...">
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Scan Type:</label>
                            <select class="form-control" id="youtubeScanType">
                                <option value="video">Video & Metadata</option>
                                <option value="comments">Comments Analysis</option>
                                <option value="metadata">Metadata Only</option>
                            </select>
                        </div>
                        
                        <button class="btn btn-danger w-100" onclick="scanPlatform('youtube')">
                            <i class="fas fa-search"></i> Scan YouTube Content
                        </button>
                        
                        <div id="youtubeResult" class="mt-3"></div>
                    </div>
                </div>
                
                <!-- Website Scanner -->
                <div class="col-md-6">
                    <div class="platform-card">
                        <h3><i class="fas fa-globe text-primary"></i> Website Scanner</h3>
                        <p class="text-muted">Scan website content for brand safety risks</p>
                        
                        <div class="mb-3">
                            <label class="form-label">Website URL:</label>
                            <input type="text" class="form-control" id="websiteUrl" placeholder="https://example.com">
                        </div>
                        
                        <button class="btn btn-primary w-100" onclick="scanPlatform('website')">
                            <i class="fas fa-search"></i> Scan Website Content
                        </button>
                        
                        <div id="websiteResult" class="mt-3"></div>
                    </div>
                </div>
                
                <!-- TikTok Scanner -->
                <div class="col-md-6">
                    <div class="platform-card">
                        <h3><i class="fab fa-tiktok text-dark"></i> TikTok Scanner</h3>
                        <p class="text-muted">Scan TikTok videos and content (API Required)</p>
                        
                        <div class="mb-3">
                            <label class="form-label">TikTok URL:</label>
                            <input type="text" class="form-control" id="tiktokUrl" placeholder="https://www.tiktok.com/...">
                        </div>
                        
                        <button class="btn btn-dark w-100" onclick="scanPlatform('tiktok')">
                            <i class="fas fa-search"></i> Scan TikTok Content
                        </button>
                        
                        <div id="tiktokResult" class="mt-3"></div>
                    </div>
                </div>
                
                <!-- Facebook Scanner -->
                <div class="col-md-6">
                    <div class="platform-card">
                        <h3><i class="fab fa-facebook text-primary"></i> Facebook Scanner</h3>
                        <p class="text-muted">Scan Facebook posts and content (API Required)</p>
                        
                        <div class="mb-3">
                            <label class="form-label">Facebook URL:</label>
                            <input type="text" class="form-control" id="facebookUrl" placeholder="https://www.facebook.com/...">
                        </div>
                        
                        <button class="btn btn-primary w-100" onclick="scanPlatform('facebook')">
                            <i class="fas fa-search"></i> Scan Facebook Content
                        </button>
                        
                        <div id="facebookResult" class="mt-3"></div>
                    </div>
                </div>
            </div>

            <!-- Subscription Tiers -->
            <div class="row mb-5">
                <div class="col-12">
                    <h2 class="text-center mb-4">
                        <i class="fas fa-crown"></i> Enterprise Subscription Tiers
                    </h2>
                </div>
                
                <!-- Starter Tier -->
                <div class="col-md-4">
                    <div class="subscription-tier">
                        <h3>Starter</h3>
                        <h2>$99<span class="fs-6">/month</span></h2>
                        <p>100 scans/month</p>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success"></i> YouTube + Website Scanning</li>
                            <li><i class="fas fa-check text-success"></i> Text Content Analysis</li>
                            <li><i class="fas fa-check text-success"></i> Basic Dashboard</li>
                            <li><i class="fas fa-check text-success"></i> Email Support</li>
                            <li><i class="fas fa-check text-success"></i> Offline Support</li>
                        </ul>
                        <button class="btn btn-outline-primary w-100" onclick="showSubscriptionForm('starter')">
                            Get Started
                        </button>
                    </div>
                </div>
                
                <!-- Professional Tier -->
                <div class="col-md-4">
                    <div class="subscription-tier">
                        <h3>Professional</h3>
                        <h2>$299<span class="fs-6">/month</span></h2>
                        <p>500 scans/month</p>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check text-success"></i> All Platform Scanning</li>
                            <li><i class="fas fa-check text-success"></i> Text + Video Analysis</li>
                            <li><i class="fas fa-check text-success"></i> API Access</li>
                            <li><i class="fas fa-check text-success"></i> Advanced Analytics</li>
                            <li><i class="fas fa-check text-success"></i> Priority Support</li>
                            <li><i class="fas fa-check text-success"></i> Custom Brand Rules</li>
                        </ul>
                        <button class="btn btn-primary w-100" onclick="showSubscriptionForm('professional')">
                            Upgrade Now
                        </button>
                    </div>
                </div>
                
                <!-- Enterprise Tier -->
                <div class="col-md-4">
                    <div class="subscription-tier enterprise">
                        <h3>Enterprise</h3>
                        <h2>$999<span class="fs-6">/month</span></h2>
                        <p>Unlimited Scans</p>
                        <ul class="list-unstyled">
                            <li><i class="fas fa-check"></i> All Platform Scanning</li>
                            <li><i class="fas fa-check"></i> Unlimited API Requests</li>
                            <li><i class="fas fa-check"></i> Real-time Monitoring</li>
                            <li><i class="fas fa-check"></i> Custom AI Models</li>
                            <li><i class="fas fa-check"></i> Dedicated Support</li>
                            <li><i class="fas fa-check"></i> SLA 99.9% Uptime</li>
                            <li><i class="fas fa-check"></i> White-label Solution</li>
                        </ul>
                        <button class="btn btn-light w-100" onclick="showSubscriptionForm('enterprise')">
                            Contact Sales
                        </button>
                    </div>
                </div>
            </div>

            <!-- Subscription Form -->
            <div class="row mb-5" id="subscriptionForm" style="display: none;">
                <div class="col-md-8 offset-md-2">
                    <div class="platform-card">
                        <h3><i class="fas fa-credit-card"></i> Create Enterprise Subscription</h3>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">Email Address:</label>
                                    <input type="email" class="form-control" id="subEmail" placeholder="your@company.com">
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">Company Name:</label>
                                    <input type="text" class="form-control" id="subCompany" placeholder="Your Company Inc.">
                                </div>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Select Plan:</label>
                            <select class="form-control" id="subPlan">
                                <option value="starter">Starter - $99/month</option>
                                <option value="professional">Professional - $299/month</option>
                                <option value="enterprise">Enterprise - $999/month</option>
                            </select>
                        </div>
                        
                        <button class="btn btn-success w-100" onclick="createSubscription()">
                            <i class="fas fa-rocket"></i> Create Subscription & Get API Key
                        </button>
                        
                        <div id="subscriptionResult" class="mt-3"></div>
                    </div>
                </div>
            </div>

            <!-- API Demo -->
            <div class="api-demo">
                <h3><i class="fas fa-code"></i> Enterprise API Demo</h3>
                <p>Test the SafeTube Enterprise API with your content</p>
                
                <div class="mb-3">
                    <label class="form-label">API Key (optional):</label>
                    <input type="text" class="form-control" id="apiKey" placeholder="Enter your API key">
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Text to Scan:</label>
                    <textarea class="form-control" id="demoText" rows="3" placeholder="Enter text content to scan for toxicity..."></textarea>
                </div>
                
                <button class="btn btn-info" onclick="testAPI()">
                    <i class="fas fa-vial"></i> Test API Scan
                </button>
                
                <div id="demoResult" class="mt-3"></div>
            </div>

            <!-- System Metrics -->
            <div class="row mt-5">
                <div class="col-12">
                    <div class="platform-card">
                        <h3><i class="fas fa-chart-bar"></i> Live System Metrics</h3>
                        <div class="row text-center" id="liveMetrics">
                            <!-- Metrics will be populated by JavaScript -->
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            // Platform Scanning
            function scanPlatform(platform) {
                const urlInput = document.getElementById(platform + 'Url').value;
                const scanType = document.getElementById(platform + 'ScanType')?.value || 'video';
                const apiKey = document.getElementById('apiKey').value;
                
                if (!urlInput) {
                    alert('Please enter a URL');
                    return;
                }

                const resultDiv = document.getElementById(platform + 'Result');
                resultDiv.innerHTML = '<div class="alert alert-info">🔄 Scanning... Please wait</div>';

                fetch('/api/v1/scan/platform', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        platform: platform,
                        url: urlInput,
                        scan_type: scanType,
                        api_key: apiKey
                    })
                })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        displayPlatformResult(platform, data.data);
                    } else {
                        resultDiv.innerHTML = `<div class="alert alert-danger">❌ ${data.error}</div>`;
                    }
                })
                .catch(e => {
                    resultDiv.innerHTML = `<div class="alert alert-danger">❌ Error: ${e}</div>`;
                });
            }

            function displayPlatformResult(platform, data) {
                const resultDiv = document.getElementById(platform + 'Result');
                const riskClass = `risk-${data.overall_risk}`;
                
                let resultHTML = `
                    <div class="alert ${riskClass}">
                        <h5>${data.platform.toUpperCase()} Scan Result</h5>
                        <p><strong>Overall Risk:</strong> <span class="badge bg-${data.overall_risk}">${data.overall_risk.toUpperCase()}</span></p>
                        <p><strong>URL:</strong> ${data.url}</p>
                `;
                
                // Add scan-specific results
                if (data.scans) {
                    for (const [scanType, scanData] of Object.entries(data.scans)) {
                        resultHTML += `<h6>${scanType.replace('_', ' ').toUpperCase()}</h6>`;
                        
                        if (scanData.risk_level) {
                            resultHTML += `<p>Risk: <span class="badge bg-${scanData.risk_level}">${scanData.risk_level.toUpperCase()}</span></p>`;
                        }
                        
                        if (scanData.confidence) {
                            resultHTML += `<p>Confidence: ${(scanData.confidence * 100).toFixed(1)}%</p>`;
                        }
                        
                        if (scanData.categories) {
                            resultHTML += `<p>Categories: ${scanData.categories.join(', ')}</p>`;
                        }
                    }
                }
                
                resultHTML += `</div>`;
                resultDiv.innerHTML = resultHTML;
            }

            // Subscription Management
            function showSubscriptionForm(plan) {
                document.getElementById('subscriptionForm').style.display = 'block';
                document.getElementById('subPlan').value = plan;
                document.getElementById('subscriptionResult').innerHTML = '';
                
                // Scroll to form
                document.getElementById('subscriptionForm').scrollIntoView({ behavior: 'smooth' });
            }

            function createSubscription() {
                const email = document.getElementById('subEmail').value;
                const company = document.getElementById('subCompany').value;
                const plan = document.getElementById('subPlan').value;
                
                if (!email) {
                    alert('Please enter email address');
                    return;
                }

                const resultDiv = document.getElementById('subscriptionResult');
                resultDiv.innerHTML = '<div class="alert alert-info">🔄 Creating subscription...</div>';

                fetch('/api/v1/subscription/create', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        email: email,
                        plan: plan,
                        company_name: company
                    })
                })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        resultDiv.innerHTML = `
                            <div class="alert alert-success">
                                <h5>🎉 Subscription Created Successfully!</h5>
                                <p><strong>API Key:</strong> <code>${data.api_key}</code></p>
                                <p><strong>Plan:</strong> ${data.plan_info.name}</p>
                                <p><strong>Scans Remaining:</strong> ${data.scans_remaining}</p>
                                <p><strong>Price:</strong> $${data.plan_info.price}/month</p>
                                <p class="text-muted">Save this API key for all API requests</p>
                            </div>
                        `;
                    } else {
                        resultDiv.innerHTML = `<div class="alert alert-danger">❌ ${data.error}</div>`;
                    }
                })
                .catch(e => {
                    resultDiv.innerHTML = `<div class="alert alert-danger">❌ Error: ${e}</div>`;
                });
            }

            // API Testing
            function testAPI() {
                const text = document.getElementById('demoText').value;
                const apiKey = document.getElementById('apiKey').value;
                
                if (!text) {
                    alert('Please enter text to scan');
                    return;
                }

                const resultDiv = document.getElementById('demoResult');
                resultDiv.innerHTML = '<div class="alert alert-info">🔄 Testing API...</div>';

                fetch('/api/v1/scan/text', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        text: text,
                        api_key: apiKey
                    })
                })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        const riskClass = `risk-${data.data.risk_level}`;
                        resultDiv.innerHTML = `
                            <div class="alert ${riskClass}">
                                <h5>API Scan Result</h5>
                                <p><strong>Result:</strong> ${data.data.is_toxic ? '🚨 TOXIC' : '✅ SAFE'}</p>
                                <p><strong>Risk Level:</strong> <span class="badge bg-${data.data.risk_level}">${data.data.risk_level.toUpperCase()}</span></p>
                                <p><strong>Confidence:</strong> ${(data.data.confidence * 100).toFixed(1)}%</p>
                                <p><strong>Categories:</strong> ${data.data.categories?.join(', ') || 'None'}</p>
                                <p><strong>Processing Time:</strong> ${data.data.processing_time}s</p>
                                <p><strong>Request ID:</strong> ${data.metadata.request_id}</p>
                            </div>
                        `;
                    } else {
                        resultDiv.innerHTML = `<div class="alert alert-danger">❌ ${data.error}</div>`;
                    }
                })
                .catch(e => {
                    resultDiv.innerHTML = `<div class="alert alert-danger">❌ Error: ${e}</div>`;
                });
            }

            // System Status
            function updateSystemStatus() {
                fetch('/api/v1/system/metrics')
                    .then(r => r.json())
                    .then(data => {
                        if (data.success) {
                            // Update system metrics
                            document.getElementById('systemMetrics').innerHTML = `
                                <span class="badge bg-success">AI: ${data.data.ai_models_loaded ? '✅' : '❌'}</span>
                                <span class="badge bg-info">Redis: ${data.data.redis_connected ? '✅' : '❌'}</span>
                                <span class="badge bg-primary">Status: ${data.data.status}</span>
                            `;
                            
                            // Update live metrics
                            const metricsDiv = document.getElementById('liveMetrics');
                            metricsDiv.innerHTML = `
                                <div class="col-md-3">
                                    <div class="metric-card">
                                        <h4>${data.data.total_models || 0}</h4>
                                        <p>AI Models</p>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="metric-card">
                                        <h4>${data.data.redis_connected ? '✅' : '❌'}</h4>
                                        <p>Cache Status</p>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="metric-card">
                                        <h4>${data.data.status}</h4>
                                        <p>System Status</p>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="metric-card">
                                        <h4>99.9%</h4>
                                        <p>Uptime</p>
                                    </div>
                                </div>
                            `;
                        }
                    });
            }

            // Initialize
            document.addEventListener('DOMContentLoaded', function() {
                updateSystemStatus();
                setInterval(updateSystemStatus, 30000); // Update every 30 seconds
            });
        </script>
    </body>
    </html>
    '''

# ==================== ENTERPRISE API ENDPOINTS ====================

@app.route('/api/v1/scan/text', methods=['POST'])
def api_scan_text():
    """Enterprise text scanning API"""
    try:
        start_time = datetime.utcnow()
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing text parameter',
                'error_code': 'VALIDATION_ERROR'
            }), 400
        
        text = data['text'].strip()
        api_key = data.get('api_key', '')
        
        if len(text) > 10000:
            return jsonify({
                'success': False, 
                'error': 'Text too long (max 10000 characters)',
                'error_code': 'TEXT_TOO_LONG'
            }), 400
        
        # Validate subscription if API key provided
        if api_key:
            valid, message = subscription_system.validate_subscription(api_key)
            if not valid:
                return jsonify({
                    'success': False,
                    'error': f'Subscription error: {message}',
                    'error_code': 'SUBSCRIPTION_ERROR'
                }), 402
        
        # AI processing
        result = ai_engine.scan_text_enterprise(text)
        
        # Generate request ID
        request_id = f"req_{int(datetime.utcnow().timestamp())}"
        
        return jsonify({
            'success': True,
            'data': result,
            'metadata': {
                'request_id': request_id,
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'version': 'enterprise-2.0'
            }
        })
        
    except Exception as e:
        logger.error(f"API scan error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'error_code': 'INTERNAL_ERROR'
        }), 500

@app.route('/api/v1/scan/platform', methods=['POST'])
def api_scan_platform():
    """Multi-platform content scanning API"""
    try:
        data = request.get_json()
        
        if not data or 'platform' not in data or 'url' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing platform or URL parameter',
                'error_code': 'VALIDATION_ERROR'
            }), 400
        
        platform = data['platform']
        url = data['url']
        scan_type = data.get('scan_type', 'video')
        api_key = data.get('api_key', '')
        
        # Validate subscription if API key provided
        if api_key:
            valid, message = subscription_system.validate_subscription(api_key, platform, scan_type)
            if not valid:
                return jsonify({
                    'success': False,
                    'error': f'Subscription error: {message}',
                    'error_code': 'SUBSCRIPTION_ERROR'
                }), 402
        
        # Platform-specific scanning
        if platform == 'youtube':
            result = platform_scanners.scan_youtube(url, scan_type)
        elif platform == 'tiktok':
            result = platform_scanners.scan_tiktok(url, scan_type)
        elif platform == 'facebook':
            result = platform_scanners.scan_facebook(url, scan_type)
        elif platform == 'website':
            result = platform_scanners.scan_website(url, scan_type)
        elif platform == 'instagram':
            result = platform_scanners.scan_instagram(url, scan_type)
        else:
            return jsonify({
                'success': False,
                'error': f'Unsupported platform: {platform}',
                'error_code': 'UNSUPPORTED_PLATFORM'
            }), 400
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error'],
                'error_code': 'PLATFORM_ERROR'
            }), 500
        
        return jsonify({
            'success': True,
            'data': result,
            'metadata': {
                'request_id': f"platform_{int(datetime.utcnow().timestamp())}",
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        })
        
    except Exception as e:
        logger.error(f"Platform scan error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'error_code': 'INTERNAL_ERROR'
        }), 500

@app.route('/api/v1/subscription/create', methods=['POST'])
def api_create_subscription():
    """Create enterprise subscription"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing email parameter',
                'error_code': 'VALIDATION_ERROR'
            }), 400
        
        email = data['email']
        plan = data.get('plan', 'starter')
        company_name = data.get('company_name', '')
        
        result = subscription_system.create_subscription(email, plan, company_name)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify({
                'success': False,
                'error': result['error'],
                'error_code': 'SUBSCRIPTION_CREATION_ERROR'
            }), 500
            
    except Exception as e:
        logger.error(f"Subscription creation error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'error_code': 'INTERNAL_ERROR'
        }), 500

@app.route('/api/v1/subscription/info', methods=['GET'])
def api_subscription_info():
    """Get subscription information"""
    try:
        api_key = request.args.get('api_key')
        
        if not api_key:
            return jsonify({
                'success': False,
                'error': 'Missing API key parameter',
                'error_code': 'VALIDATION_ERROR'
            }), 400
        
        info = subscription_system.get_subscription_info(api_key)
        
        if info:
            return jsonify({
                'success': True,
                'data': info
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid API key or no subscription found',
                'error_code': 'INVALID_API_KEY'
            }), 404
            
    except Exception as e:
        logger.error(f"Subscription info error: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'error_code': 'INTERNAL_ERROR'
        }), 500

@app.route('/api/v1/system/metrics')
def api_system_metrics():
    """System metrics endpoint"""
    try:
        ai_metrics = ai_engine.get_system_metrics()
        
        return jsonify({
            'success': True,
            'data': ai_metrics
        })
        
    except Exception as e:
        logger.error(f"Metrics error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== INITIALIZATION ====================

def init_database():
    """Initialize enterprise database"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create models directory
        os.makedirs('models', exist_ok=True)
        
        print("✅ Enterprise database initialized")
        print("✅ Models directory created")
# ==================== ENTERPRISE STARTUP ====================
if __name__ == '__main__':
    # Initialize database
    init_database()
    
    print("    🚀 SAFETUBE ENTERPRISE STARTING...")
    print("=" * 60)
    print("    🏢 ENTERPRISE FEATURES:")
    print("    ✅ Multi-Platform Scanning (YouTube, TikTok, Facebook, Website)")
    print("    ✅ Enterprise AI Engine with Caching")
    print("    ✅ Subscription System with API Keys")
    print("    ✅ Real-time Dashboard & Analytics")
    print("    ✅ Offline & Online Support")
    print("    ✅ High Performance & Scalability")
    print("")
    print("    💰 SUBSCRIPTION TIERS:")
    print("    Starter ($99) → Professional ($299) → Enterprise ($999)")
    print("")
    print("    🌐 ACCESS POINTS:")
    print("    📍 Dashboard: http://localhost:5000")
    print("    🔗 API Docs: Included in dashboard")
    print("    📊 Metrics: http://localhost:5000/api/v1/system/metrics")
    print("")
    print("    🎯 READY FOR ENTERPRISE DEPLOYMENT!")
    print("=" * 60)
    
    # Start server với PORT từ environment
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
