"""
Security Validation Module
==========================
Comprehensive security validation for WordPress sites including:
- HTTPS implementation and certificates
- Security headers analysis
- WordPress security best practices
- Vulnerability scanning
- Content Security Policy validation
"""

import requests
import ssl
import socket
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse, urljoin
import re
from datetime import datetime

from ..core import WordPressClient, WordPressAPIError
from ..utils import print_success, print_error, print_warning


class SecurityValidator:
    """Security validation utilities for WordPress sites."""
    
    def __init__(self, wp_client: WordPressClient = None):
        """Initialize security validator."""
        self.wp = wp_client or WordPressClient()
        self.base_url = "https://spherevista360.com"
        
        # Security headers to check
        self.security_headers = {
            'strict-transport-security': {
                'required': True,
                'description': 'HSTS - Forces HTTPS connections'
            },
            'x-content-type-options': {
                'required': True,
                'description': 'Prevents MIME type sniffing'
            },
            'x-frame-options': {
                'required': True,
                'description': 'Prevents clickjacking attacks'
            },
            'x-xss-protection': {
                'required': True,
                'description': 'Enables XSS filtering'
            },
            'content-security-policy': {
                'required': False,
                'description': 'Controls resource loading'
            },
            'referrer-policy': {
                'required': False,
                'description': 'Controls referrer information'
            }
        }
    
    def validate_site_security(self) -> Dict[str, Any]:
        """Comprehensive security validation for the entire site."""
        try:
            result = {
                'site_url': self.base_url,
                'security': {
                    'https': {'score': 0, 'issues': []},
                    'headers': {'score': 0, 'issues': []},
                    'ssl_certificate': {'score': 0, 'issues': []},
                    'wordpress_security': {'score': 0, 'issues': []},
                    'content_security': {'score': 0, 'issues': []}
                },
                'issues': [],
                'recommendations': [],
                'score': 0
            }
            
            # Validate HTTPS implementation
            result['security']['https'] = self._validate_https()
            
            # Validate security headers
            result['security']['headers'] = self._validate_security_headers()
            
            # Validate SSL certificate
            result['security']['ssl_certificate'] = self._validate_ssl_certificate()
            
            # Validate WordPress-specific security
            result['security']['wordpress_security'] = self._validate_wordpress_security()
            
            # Validate content security
            result['security']['content_security'] = self._validate_content_security()
            
            # Calculate overall score
            scores = [section['score'] for section in result['security'].values()]
            result['score'] = int(sum(scores) / len(scores)) if scores else 0
            
            # Collect all issues
            all_issues = []
            for section_name, section_data in result['security'].items():
                if section_data['issues']:
                    all_issues.extend([f"{section_name.replace('_', ' ').title()}: {issue}" for issue in section_data['issues']])
            
            result['issues'] = all_issues
            
            # Generate recommendations
            result = self._generate_security_recommendations(result)
            
            # Set status based on score
            if result['score'] >= 85:
                result['status'] = 'excellent'
                result['message'] = 'Excellent security implementation'
            elif result['score'] >= 70:
                result['status'] = 'good'
                result['message'] = 'Good security with minor improvements needed'
            elif result['score'] >= 50:
                result['status'] = 'fair'
                result['message'] = 'Fair security - several improvements recommended'
            else:
                result['status'] = 'poor'
                result['message'] = 'Poor security - immediate attention required'
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error validating site security: {str(e)}'
            }
    
    def _validate_https(self) -> Dict[str, Any]:
        """Validate HTTPS implementation and redirects."""
        analysis = {
            'https_enabled': False,
            'http_redirects': False,
            'mixed_content': 0,
            'issues': [],
            'score': 0
        }
        
        try:
            # Test HTTPS access
            https_response = requests.get(self.base_url, timeout=10, allow_redirects=True)
            if https_response.status_code == 200:
                analysis['https_enabled'] = True
                analysis['score'] += 40
                
                # Check if final URL is HTTPS
                if https_response.url.startswith('https://'):
                    analysis['score'] += 20
                else:
                    analysis['issues'].append('Site does not enforce HTTPS')
            
            # Test HTTP to HTTPS redirect
            http_url = self.base_url.replace('https://', 'http://')
            try:
                http_response = requests.get(http_url, timeout=10, allow_redirects=True)
                if http_response.url.startswith('https://'):
                    analysis['http_redirects'] = True
                    analysis['score'] += 20
                else:
                    analysis['issues'].append('HTTP does not redirect to HTTPS')
            except Exception:
                analysis['issues'].append('Unable to test HTTP redirect')
            
            # Check for mixed content (basic check)
            if analysis['https_enabled']:
                try:
                    content = https_response.text
                    http_resources = re.findall(r'src=["\']http://[^"\']+["\']', content)
                    http_resources.extend(re.findall(r'href=["\']http://[^"\']+["\']', content))
                    
                    analysis['mixed_content'] = len(http_resources)
                    if analysis['mixed_content'] > 0:
                        analysis['issues'].append(f'Found {analysis["mixed_content"]} HTTP resources on HTTPS page')
                        analysis['score'] -= min(analysis['mixed_content'] * 5, 30)
                    else:
                        analysis['score'] += 20
                        
                except Exception:
                    analysis['issues'].append('Unable to check for mixed content')
            
        except Exception as e:
            analysis['issues'].append(f'HTTPS validation failed: {str(e)}')
        
        return analysis
    
    def _validate_security_headers(self) -> Dict[str, Any]:
        """Validate security headers implementation."""
        analysis = {
            'headers_present': {},
            'missing_headers': [],
            'header_values': {},
            'issues': [],
            'score': 0
        }
        
        try:
            response = requests.get(self.base_url, timeout=10)
            headers = {k.lower(): v for k, v in response.headers.items()}
            
            total_required = sum(1 for h in self.security_headers.values() if h['required'])
            total_optional = sum(1 for h in self.security_headers.values() if not h['required'])
            present_required = 0
            present_optional = 0
            
            for header_name, header_info in self.security_headers.items():
                if header_name in headers:
                    analysis['headers_present'][header_name] = True
                    analysis['header_values'][header_name] = headers[header_name]
                    
                    if header_info['required']:
                        present_required += 1
                    else:
                        present_optional += 1
                    
                    # Validate header values
                    self._validate_header_value(header_name, headers[header_name], analysis)
                    
                else:
                    analysis['headers_present'][header_name] = False
                    analysis['missing_headers'].append(header_name)
                    
                    if header_info['required']:
                        analysis['issues'].append(f'Missing required header: {header_name}')
            
            # Calculate score
            required_score = (present_required / total_required) * 70 if total_required > 0 else 70
            optional_score = (present_optional / total_optional) * 30 if total_optional > 0 else 0
            analysis['score'] = int(required_score + optional_score)
            
        except Exception as e:
            analysis['issues'].append(f'Header validation failed: {str(e)}')
        
        return analysis
    
    def _validate_header_value(self, header_name: str, header_value: str, analysis: Dict[str, Any]) -> None:
        """Validate specific security header values."""
        if header_name == 'strict-transport-security':
            if 'max-age' not in header_value.lower():
                analysis['issues'].append('HSTS header missing max-age directive')
            elif 'max-age=0' in header_value.lower():
                analysis['issues'].append('HSTS max-age is set to 0 (disabled)')
        
        elif header_name == 'x-content-type-options':
            if header_value.lower() != 'nosniff':
                analysis['issues'].append('X-Content-Type-Options should be set to "nosniff"')
        
        elif header_name == 'x-frame-options':
            valid_values = ['deny', 'sameorigin', 'allow-from']
            if not any(val in header_value.lower() for val in valid_values):
                analysis['issues'].append('X-Frame-Options has invalid value')
        
        elif header_name == 'x-xss-protection':
            if '1' not in header_value:
                analysis['issues'].append('XSS Protection is disabled')
    
    def _validate_ssl_certificate(self) -> Dict[str, Any]:
        """Validate SSL certificate configuration."""
        analysis = {
            'certificate_valid': False,
            'certificate_expiry': None,
            'days_until_expiry': 0,
            'certificate_issuer': '',
            'issues': [],
            'score': 0
        }
        
        try:
            hostname = urlparse(self.base_url).netloc
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    analysis['certificate_valid'] = True
                    analysis['score'] += 50
                    
                    # Check certificate expiry
                    expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    analysis['certificate_expiry'] = expiry_date.isoformat()
                    
                    days_until_expiry = (expiry_date - datetime.now()).days
                    analysis['days_until_expiry'] = days_until_expiry
                    
                    if days_until_expiry < 30:
                        analysis['issues'].append(f'Certificate expires in {days_until_expiry} days')
                        analysis['score'] -= 20
                    elif days_until_expiry < 90:
                        analysis['issues'].append(f'Certificate expires in {days_until_expiry} days - consider renewal')
                        analysis['score'] -= 10
                    else:
                        analysis['score'] += 30
                    
                    # Get certificate issuer
                    issuer = cert.get('issuer', [])
                    for item in issuer:
                        if item[0][0] == 'organizationName':
                            analysis['certificate_issuer'] = item[0][1]
                            break
                    
                    analysis['score'] += 20  # Valid certificate bonus
                    
        except ssl.SSLError as e:
            analysis['issues'].append(f'SSL certificate error: {str(e)}')
        except Exception as e:
            analysis['issues'].append(f'Certificate validation failed: {str(e)}')
        
        return analysis
    
    def _validate_wordpress_security(self) -> Dict[str, Any]:
        """Validate WordPress-specific security configurations."""
        analysis = {
            'version_disclosure': False,
            'directory_listing': False,
            'sensitive_files_exposed': [],
            'admin_username': False,
            'login_protection': False,
            'issues': [],
            'score': 100
        }
        
        try:
            # Check for WordPress version disclosure
            response = requests.get(self.base_url, timeout=10)
            content = response.text.lower()
            
            if 'wp-content' in content or 'wordpress' in content:
                # Check version disclosure in meta tags
                if re.search(r'name=["\']generator["\'][^>]*wordpress', content):
                    analysis['version_disclosure'] = True
                    analysis['issues'].append('WordPress version disclosed in generator meta tag')
                    analysis['score'] -= 15
            
            # Check for sensitive file exposure
            sensitive_files = [
                '/wp-config.php',
                '/wp-config.php.bak',
                '/wp-admin/install.php',
                '/readme.html',
                '/license.txt'
            ]
            
            for file_path in sensitive_files:
                try:
                    file_response = requests.get(urljoin(self.base_url, file_path), timeout=5)
                    if file_response.status_code == 200:
                        analysis['sensitive_files_exposed'].append(file_path)
                        analysis['issues'].append(f'Sensitive file exposed: {file_path}')
                        analysis['score'] -= 10
                except Exception:
                    continue
            
            # Check directory listing
            try:
                wp_content_response = requests.get(urljoin(self.base_url, '/wp-content/'), timeout=5)
                if 'index of' in wp_content_response.text.lower():
                    analysis['directory_listing'] = True
                    analysis['issues'].append('Directory listing enabled for wp-content')
                    analysis['score'] -= 10
            except Exception:
                pass
            
            # Check for common admin usernames
            try:
                # This would require API access or more sophisticated scanning
                # For now, we'll skip this check
                pass
            except Exception:
                pass
            
        except Exception as e:
            analysis['issues'].append(f'WordPress security validation failed: {str(e)}')
        
        return analysis
    
    def _validate_content_security(self) -> Dict[str, Any]:
        """Validate content security policies and inline content."""
        analysis = {
            'csp_header': False,
            'inline_scripts': 0,
            'inline_styles': 0,
            'external_scripts': 0,
            'unsafe_content': [],
            'issues': [],
            'score': 80  # Default good score
        }
        
        try:
            response = requests.get(self.base_url, timeout=10)
            
            # Check for CSP header
            csp_header = response.headers.get('content-security-policy', '')
            if csp_header:
                analysis['csp_header'] = True
                analysis['score'] += 20
                
                # Basic CSP validation
                if 'unsafe-inline' in csp_header:
                    analysis['issues'].append('CSP allows unsafe-inline which reduces security')
                    analysis['score'] -= 10
                
                if 'unsafe-eval' in csp_header:
                    analysis['issues'].append('CSP allows unsafe-eval which reduces security')
                    analysis['score'] -= 10
            else:
                analysis['issues'].append('No Content Security Policy header found')
            
            # Analyze page content for security issues
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Count inline scripts and styles
            inline_scripts = soup.find_all('script', string=True)
            analysis['inline_scripts'] = len(inline_scripts)
            
            inline_styles = soup.find_all('style', string=True)
            analysis['inline_styles'] = len(inline_styles)
            
            # Count external scripts
            external_scripts = soup.find_all('script', src=True)
            analysis['external_scripts'] = len(external_scripts)
            
            # Check for potentially unsafe content
            for script in inline_scripts:
                if script.string and ('eval(' in script.string or 'innerHTML' in script.string):
                    analysis['unsafe_content'].append('Script using eval() or innerHTML')
            
            # Penalties for security issues
            if analysis['inline_scripts'] > 5:
                analysis['issues'].append(f'Many inline scripts ({analysis["inline_scripts"]}) - consider CSP')
                analysis['score'] -= 10
            
            if analysis['unsafe_content']:
                analysis['issues'].append(f'Found {len(analysis["unsafe_content"])} potentially unsafe content patterns')
                analysis['score'] -= 15
            
        except Exception as e:
            analysis['issues'].append(f'Content security validation failed: {str(e)}')
        
        return analysis
    
    def _generate_security_recommendations(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific security recommendations."""
        recommendations = []
        security = result['security']
        
        # HTTPS recommendations
        if not security['https']['https_enabled']:
            recommendations.append('Enable HTTPS for secure data transmission')
        
        if not security['https']['http_redirects']:
            recommendations.append('Configure HTTP to HTTPS redirects')
        
        if security['https']['mixed_content'] > 0:
            recommendations.append('Fix mixed content issues - update HTTP resources to HTTPS')
        
        # Header recommendations
        if security['headers']['missing_headers']:
            missing = ', '.join(security['headers']['missing_headers'])
            recommendations.append(f'Add missing security headers: {missing}')
        
        # Certificate recommendations
        if security['ssl_certificate']['days_until_expiry'] < 90:
            recommendations.append('Plan SSL certificate renewal')
        
        # WordPress security recommendations
        if security['wordpress_security']['version_disclosure']:
            recommendations.append('Hide WordPress version information')
        
        if security['wordpress_security']['sensitive_files_exposed']:
            recommendations.append('Protect or remove exposed sensitive files')
        
        if security['wordpress_security']['directory_listing']:
            recommendations.append('Disable directory listing')
        
        # Content security recommendations
        if not security['content_security']['csp_header']:
            recommendations.append('Implement Content Security Policy (CSP) headers')
        
        if security['content_security']['unsafe_content']:
            recommendations.append('Review and secure potentially unsafe content patterns')
        
        result['recommendations'] = recommendations
        return result