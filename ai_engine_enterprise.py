# 🤖 SAFETUBE ENTERPRISE AI ENGINE - ĐỘC NHẤT
import torch
import redis
import json
import time
import logging
import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from functools import lru_cache
from datetime import datetime
import threading

logger = logging.getLogger(__name__)

class EnterpriseAIEngine:
    def __init__(self, config):
        self.config = config
        self.redis_client = None
        self._init_redis()
        
        # AI Models
        self.text_models = {}
        self.video_models = {}
        self.audio_models = {}
        
        # Load models in background
        self._load_models_async()
    
    def _init_redis(self):
        """Initialize Redis for caching"""
        try:
            self.redis_client = redis.from_url(self.config.REDIS_URL)
            self.redis_client.ping()
            logger.info("✅ Redis connected for enterprise caching")
        except:
            logger.warning("⚠️ Redis not available - using memory cache")
            self.redis_client = None
    
    def _load_models_async(self):
        """Load AI models in background thread"""
        def load_models():
            logger.info("🚀 Loading Enterprise AI Models...")
            
            # Text Models
            self._load_text_models()
            
            # Video Models (YOLO for violence detection)
            self._load_video_models()
            
            logger.info("🎯 Enterprise AI Engine ready!")
        
        thread = threading.Thread(target=load_models)
        thread.daemon = True
        thread.start()
    
    def _load_text_models(self):
        """Load text classification models"""
        try:
            # Vietnamese Toxic Content Detection
            self.text_models['vietnamese_toxic'] = {
                'tokenizer': AutoTokenizer.from_pretrained("vinai/phobert-base"),
                'model': AutoModelForSequenceClassification.from_pretrained("vinai/phobert-base", num_labels=2)
            }
            self.text_models['vietnamese_toxic']['model'].eval()
            logger.info("✅ Vietnamese toxic model loaded")
            
        except Exception as e:
            logger.error(f"❌ Text model loading failed: {e}")
    
    def _load_video_models(self):
        """Load video analysis models"""
        try:
            from ultralytics import YOLO
            self.video_models['violence'] = YOLO('yolov8n.pt')
            logger.info("✅ Video violence model loaded")
        except Exception as e:
            logger.error(f"❌ Video model loading failed: {e}")
    
    def scan_text_enterprise(self, text, language='vi', categories=None):
        """Enterprise-grade text scanning"""
        start_time = time.time()
        
        try:
            # Cache check
            cache_key = f"text_scan:{hash(text)}:{language}"
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                cached_result['cached'] = True
                return cached_result
            
            # AI Processing based on language
            if language == 'vi':
                result = self._scan_vietnamese_text(text, categories)
            else:
                result = self._scan_english_text(text, categories)
            
            result.update({
                'processing_time': time.time() - start_time,
                'model_version': 'enterprise-2.0',
                'cached': False,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Cache result
            self._cache_result(cache_key, result, ttl=300)  # 5 minutes
            
            return result
            
        except Exception as e:
            logger.error(f"Text scan failed: {e}")
            return self._fallback_scan(text, start_time)
    
    def _scan_vietnamese_text(self, text, categories):
        """Scan Vietnamese text with PhoBERT"""
        if 'vietnamese_toxic' not in self.text_models:
            return self._fallback_scan(text, 0)
        
        model_info = self.text_models['vietnamese_toxic']
        inputs = model_info['tokenizer'](
            text, 
            return_tensors="pt", 
            truncation=True, 
            max_length=256,
            padding=True
        )
        
        with torch.no_grad():
            outputs = model_info['model'](**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            pred = torch.argmax(probs, dim=-1).item()
            confidence = probs[0][pred].item()
        
        # Enhanced category detection
        detected_categories = self._detect_toxic_categories(text)
        risk_level = self._calculate_risk_level(confidence, detected_categories)
        
        return {
            'is_toxic': bool(pred),
            'confidence': confidence,
            'risk_level': risk_level,
            'categories': detected_categories,
            'language': 'vi'
        }
    
    def _scan_english_text(self, text, categories):
        """Scan English text (placeholder for multilingual support)"""
        # Simple keyword-based detection for English
        toxic_keywords_en = [
            'kill', 'murder', 'violence', 'gun', 'weapon', 'attack',
            'sex', 'porn', 'nude', 'xxx', 'adult', 'nsfw',
            'hate', 'racist', 'discrimination', 'attack'
        ]
        
        is_toxic = any(keyword in text.lower() for keyword in toxic_keywords_en)
        confidence = 0.8 if is_toxic else 0.7
        
        detected_categories = self._detect_toxic_categories(text)
        risk_level = self._calculate_risk_level(confidence, detected_categories)
        
        return {
            'is_toxic': is_toxic,
            'confidence': confidence,
            'risk_level': risk_level,
            'categories': detected_categories,
            'language': 'en'
        }
    
    def _detect_toxic_categories(self, text):
        """Detect specific toxic categories"""
        text_lower = text.lower()
        categories = []
        
        # Violence detection
        violence_keywords = ['đánh nhau', 'chém giết', 'bạo lực', 'máu me', 'súng', 'dao']
        if any(keyword in text_lower for keyword in violence_keywords):
            categories.append('violence')
        
        # Sexual content
        sexual_keywords = ['sex', 'khiêu dâm', 'nude', '18+', 'hentai', 'xxx']
        if any(keyword in text_lower for keyword in sexual_keywords):
            categories.append('sexual')
        
        # Hate speech
        hate_keywords = ['chửi', 'ngu', 'đần', 'cặc', 'địt', 'xúc phạm']
        if any(keyword in text_lower for keyword in hate_keywords):
            categories.append('hate_speech')
        
        # Fake news
        fake_keywords = ['tin giả', 'bịa đặt', 'lừa đảo', 'scam']
        if any(keyword in text_lower for keyword in fake_keywords):
            categories.append('fake_news')
        
        return categories
    
    def _calculate_risk_level(self, confidence, categories):
        """Calculate risk level based on confidence and categories"""
        if confidence > 0.9 or 'violence' in categories:
            return 'critical'
        elif confidence > 0.7 or 'sexual' in categories:
            return 'high'
        elif confidence > 0.5:
            return 'medium'
        else:
            return 'low'
    
    def scan_video_enterprise(self, video_path, platform='youtube'):
        """Enterprise-grade video scanning"""
        start_time = time.time()
        
        try:
            if 'violence' not in self.video_models:
                return {'error': 'Video model not available'}
            
            import cv2
            
            cap = cv2.VideoCapture(video_path)
            violence_detections = []
            frame_count = 0
            
            # Optimized frame sampling
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = max(1, int(fps / 6))  # 6 FPS for balance
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    results = self.video_models['violence'](frame, verbose=False)
                    
                    for result in results:
                        for box in result.boxes:
                            class_id = int(box.cls[0])
                            class_name = self.video_models['violence'].names[class_id]
                            confidence = float(box.conf[0])
                            
                            # Detect dangerous objects
                            if class_name in ['knife', 'gun', 'pistol', 'weapon'] and confidence > 0.5:
                                violence_detections.append({
                                    'frame': frame_count,
                                    'object': class_name,
                                    'confidence': confidence,
                                    'timestamp': frame_count / fps
                                })
                
                frame_count += 1
            
            cap.release()
            
            risk_level = 'critical' if len(violence_detections) > 0 else 'low'
            
            return {
                'violence_detections': violence_detections,
                'total_frames_processed': frame_count,
                'risk_level': risk_level,
                'processing_time': time.time() - start_time,
                'is_unsafe': len(violence_detections) > 0
            }
            
        except Exception as e:
            logger.error(f"Video scan failed: {e}")
            return {'error': f'Video processing failed: {str(e)}'}
    
    def _fallback_scan(self, text, start_time):
        """Fallback scanning when AI fails"""
        toxic_keywords = [
            'đánh nhau', 'chém giết', 'bạo lực', 'máu me',
            'sex', 'khiêu dâm', 'nude', '18+', 'hentai',
            'chửi', 'ngu', 'địt', 'đụ', 'cặc'
        ]
        
        is_toxic = any(keyword in text.lower() for keyword in toxic_keywords)
        confidence = 0.85 if is_toxic else 0.75
        categories = self._detect_toxic_categories(text)
        risk_level = self._calculate_risk_level(confidence, categories)
        
        return {
            'text': text,
            'is_toxic': is_toxic,
            'confidence': confidence,
            'risk_level': risk_level,
            'categories': categories,
            'processing_time': time.time() - start_time,
            'model_version': 'fallback',
            'cached': False
        }
    
    def _get_cached_result(self, cache_key):
        """Get cached result from Redis"""
        if not self.redis_client:
            return None
        
        try:
            cached = self.redis_client.get(cache_key)
            return json.loads(cached) if cached else None
        except:
            return None
    
    def _cache_result(self, cache_key, result, ttl=300):
        """Cache result in Redis"""
        if not self.redis_client:
            return
        
        try:
            self.redis_client.setex(cache_key, ttl, json.dumps(result))
        except:
            pass
    
    def get_system_metrics(self):
        """Get AI engine metrics"""
        return {
            'text_models_loaded': len(self.text_models) > 0,
            'video_models_loaded': len(self.video_models) > 0,
            'redis_connected': self.redis_client is not None,
            'total_models': len(self.text_models) + len(self.video_models),
            'status': 'operational'
        }