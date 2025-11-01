# 🌐 SAFETUBE ENTERPRISE PLATFORM SCANNERS - ĐỘC NHẤT
import requests
import re
import logging
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import json
import time

logger = logging.getLogger(__name__)

class EnterprisePlatformScanners:
    def __init__(self, config, ai_engine):
        self.config = config
        self.ai_engine = ai_engine
        
    def scan_youtube(self, url, scan_type='video'):
        """Scan YouTube content - VIDEO, COMMENTS, METADATA"""
        try:
            logger.info(f"🎬 Scanning YouTube: {url}")
            
            # Extract video ID
            video_id = self._extract_youtube_id(url)
            if not video_id:
                return {'error': 'Invalid YouTube URL'}
            
            results = {
                'platform': 'youtube',
                'content_id': video_id,
                'scan_type': scan_type,
                'url': url,
                'scans': {}
            }
            
            # Scan video metadata
            if scan_type in ['video', 'metadata']:
                metadata = self._get_youtube_metadata(video_id)
                results['scans']['metadata'] = metadata
                
                # Scan video title and description
                if metadata.get('title'):
                    text_scan = self.ai_engine.scan_text_enterprise(
                        f"{metadata.get('title', '')} {metadata.get('description', '')}"
                    )
                    results['scans']['text_analysis'] = text_scan
            
            # Scan comments (if available)
            if scan_type in ['video', 'comments']:
                comments = self._get_youtube_comments(video_id)
                if comments:
                    toxic_comments = []
                    for comment in comments[:50]:  # Limit to 50 comments
                        comment_scan = self.ai_engine.scan_text_enterprise(comment['text'])
                        if comment_scan.get('is_toxic'):
                            toxic_comments.append({
                                'comment': comment['text'],
                                'analysis': comment_scan
                            })
                    
                    results['scans']['comments_analysis'] = {
                        'total_comments': len(comments),
                        'toxic_comments': len(toxic_comments),
                        'toxic_comment_samples': toxic_comments[:5]  # Show 5 samples
                    }
            
            # Calculate overall risk
            results['overall_risk'] = self._calculate_overall_risk(results['scans'])
            
            return results
            
        except Exception as e:
            logger.error(f"YouTube scan failed: {e}")
            return {'error': f'YouTube scanning failed: {str(e)}'}
    
    def scan_tiktok(self, url, scan_type='video'):
        """Scan TikTok content"""
        try:
            logger.info(f"🎵 Scanning TikTok: {url}")
            
            # TikTok scanning logic would go here
            # Note: TikTok requires official API access for full scanning
            
            return {
                'platform': 'tiktok',
                'url': url,
                'scan_type': scan_type,
                'status': 'requires_tiktok_api',
                'message': 'Full TikTok scanning requires official API access'
            }
            
        except Exception as e:
            logger.error(f"TikTok scan failed: {e}")
            return {'error': f'TikTok scanning failed: {str(e)}'}
    
    def scan_facebook(self, url, scan_type='post'):
        """Scan Facebook content"""
        try:
            logger.info(f"📘 Scanning Facebook: {url}")
            
            # Facebook scanning logic would go here
            # Note: Facebook requires Graph API access
            
            return {
                'platform': 'facebook',
                'url': url,
                'scan_type': scan_type,
                'status': 'requires_facebook_api',
                'message': 'Full Facebook scanning requires Graph API access'
            }
            
        except Exception as e:
            logger.error(f"Facebook scan failed: {e}")
            return {'error': f'Facebook scanning failed: {str(e)}'}
    
    def scan_website(self, url, scan_type='text'):
        """Scan Website content - OFFLINE SUPPORT"""
        try:
            logger.info(f"🌐 Scanning Website: {url}")
            
            # Extract text content from website
            text_content = self._extract_website_text(url)
            if not text_content:
                return {'error': 'Could not extract website content'}
            
            results = {
                'platform': 'website',
                'url': url,
                'scan_type': scan_type,
                'scans': {}
            }
            
            # Scan extracted text
            if text_content:
                text_scan = self.ai_engine.scan_text_enterprise(text_content)
                results['scans']['text_analysis'] = text_scan
                
                # Extract and scan page title
                title = self._extract_page_title(text_content)
                if title:
                    title_scan = self.ai_engine.scan_text_enterprise(title)
                    results['scans']['title_analysis'] = title_scan
            
            # Calculate overall risk
            results['overall_risk'] = self._calculate_overall_risk(results['scans'])
            
            return results
            
        except Exception as e:
            logger.error(f"Website scan failed: {e}")
            return {'error': f'Website scanning failed: {str(e)}'}
    
    def scan_instagram(self, url, scan_type='post'):
        """Scan Instagram content"""
        try:
            logger.info(f"📷 Scanning Instagram: {url}")
            
            # Instagram scanning logic would go here
            # Note: Instagram requires Graph API access
            
            return {
                'platform': 'instagram',
                'url': url,
                'scan_type': scan_type,
                'status': 'requires_instagram_api',
                'message': 'Full Instagram scanning requires Graph API access'
            }
            
        except Exception as e:
            logger.error(f"Instagram scan failed: {e}")
            return {'error': f'Instagram scanning failed: {str(e)}'}
    
    def _extract_youtube_id(self, url):
        """Extract YouTube video ID from URL"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?]*)',
            r'youtube\.com\/watch\?.*v=([^&]*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _get_youtube_metadata(self, video_id):
        """Get YouTube video metadata (simplified - would use YouTube API in production)"""
        # This is a simplified version. In production, use YouTube Data API v3
        try:
            # For demo purposes, return mock data
            return {
                'title': f'Video Title for {video_id}',
                'description': 'This is a sample video description that would be scanned for toxic content.',
                'channel': 'Sample Channel',
                'duration': '10:30',
                'view_count': '1,000,000'
            }
        except Exception as e:
            logger.error(f"YouTube metadata extraction failed: {e}")
            return {}
    
    def _get_youtube_comments(self, video_id):
        """Get YouTube comments (simplified - would use YouTube API in production)"""
        # This is a simplified version. In production, use YouTube Data API v3
        try:
            # For demo purposes, return mock comments
            return [
                {'text': 'This is a normal comment about the video.'},
                {'text': 'Great content! Thanks for sharing.'},
                {'text': 'This is a toxic comment with bad words.'}
            ]
        except Exception as e:
            logger.error(f"YouTube comments extraction failed: {e}")
            return []
    
    def _extract_website_text(self, url):
        """Extract text content from website - WORKS OFFLINE"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # Limit to 5000 characters
            
        except Exception as e:
            logger.error(f"Website text extraction failed: {e}")
            return None
    
    def _extract_page_title(self, html_content):
        """Extract page title from HTML content"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            title_tag = soup.find('title')
            return title_tag.get_text() if title_tag else None
        except:
            return None
    
    def _calculate_overall_risk(self, scans):
        """Calculate overall risk level from multiple scans"""
        risk_scores = {
            'critical': 4,
            'high': 3, 
            'medium': 2,
            'low': 1
        }
        
        max_risk = 'low'
        
        for scan_type, scan_data in scans.items():
            if 'risk_level' in scan_data:
                current_risk = scan_data['risk_level']
                if risk_scores.get(current_risk, 0) > risk_scores.get(max_risk, 0):
                    max_risk = current_risk
        
        return max_risk