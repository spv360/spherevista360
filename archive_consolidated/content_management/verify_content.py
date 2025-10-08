#!/usr/bin/env python3
"""
Content Verification Tool
Checks for duplicate posts, missing content, and content quality issues
"""

import os
import hashlib
import re
from typing import Dict, List, Set, Tuple
from collections import defaultdict

class ContentVerifier:
    def __init__(self):
        self.content_path = "/home/kddevops/projects/spherevista360/spherevista360_week1_final"
        self.expected_categories = ['Finance', 'Technology', 'Politics', 'Travel', 'World', 'Entertainment']
        
    def get_all_articles(self) -> Dict[str, List[str]]:
        """Get all articles organized by category"""
        articles = {}
        
        for category in self.expected_categories:
            category_path = os.path.join(self.content_path, category)
            if os.path.exists(category_path):
                articles[category] = []
                for file in os.listdir(category_path):
                    if file.endswith('.md'):
                        articles[category].append(file)
                articles[category].sort()
            else:
                articles[category] = []
                
        return articles
    
    def calculate_content_hash(self, file_path: str) -> str:
        """Calculate hash of file content for duplicate detection"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Normalize content (remove whitespace variations)
                normalized = re.sub(r'\s+', ' ', content.strip())
                return hashlib.md5(normalized.encode()).hexdigest()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def extract_title_from_content(self, file_path: str) -> str:
        """Extract the main title from markdown content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for first H1 heading
                h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                if h1_match:
                    return h1_match.group(1).strip()
                return "No title found"
        except Exception as e:
            return f"Error: {e}"
    
    def get_content_stats(self, file_path: str) -> Dict:
        """Get content statistics"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            stats = {
                'word_count': len(content.split()),
                'char_count': len(content),
                'line_count': len(content.splitlines()),
                'has_title': bool(re.search(r'^#\s+', content, re.MULTILINE)),
                'has_headers': bool(re.search(r'^#{2,}\s+', content, re.MULTILINE)),
                'paragraph_count': len([p for p in content.split('\n\n') if p.strip()])
            }
            
            return stats
            
        except Exception as e:
            return {'error': str(e)}
    
    def check_for_duplicates(self, articles: Dict[str, List[str]]) -> Dict:
        """Check for duplicate content across all articles"""
        duplicates = {
            'content_duplicates': [],
            'title_duplicates': [],
            'filename_duplicates': []
        }
        
        content_hashes = {}
        titles = {}
        filenames = defaultdict(list)
        
        for category, files in articles.items():
            for file in files:
                file_path = os.path.join(self.content_path, category, file)
                
                # Check content duplicates
                content_hash = self.calculate_content_hash(file_path)
                if content_hash and content_hash in content_hashes:
                    duplicates['content_duplicates'].append({
                        'file1': content_hashes[content_hash],
                        'file2': f"{category}/{file}",
                        'hash': content_hash
                    })
                else:
                    content_hashes[content_hash] = f"{category}/{file}"
                
                # Check title duplicates
                title = self.extract_title_from_content(file_path)
                if title in titles:
                    duplicates['title_duplicates'].append({
                        'title': title,
                        'file1': titles[title],
                        'file2': f"{category}/{file}"
                    })
                else:
                    titles[title] = f"{category}/{file}"
                
                # Check filename duplicates (across categories)
                base_filename = file.lower()
                filenames[base_filename].append(f"{category}/{file}")
        
        # Find filename duplicates
        for filename, locations in filenames.items():
            if len(locations) > 1:
                duplicates['filename_duplicates'].append({
                    'filename': filename,
                    'locations': locations
                })
        
        return duplicates
    
    def analyze_content_quality(self, articles: Dict[str, List[str]]) -> Dict:
        """Analyze content quality and identify potential issues"""
        quality_issues = {
            'short_articles': [],
            'missing_headers': [],
            'missing_titles': [],
            'empty_files': []
        }
        
        quality_stats = {
            'total_articles': 0,
            'total_words': 0,
            'avg_words_per_article': 0,
            'categories_with_content': 0
        }
        
        for category, files in articles.items():
            if files:
                quality_stats['categories_with_content'] += 1
                
            for file in files:
                file_path = os.path.join(self.content_path, category, file)
                stats = self.get_content_stats(file_path)
                
                if 'error' in stats:
                    continue
                    
                quality_stats['total_articles'] += 1
                quality_stats['total_words'] += stats['word_count']
                
                # Check for quality issues
                if stats['word_count'] < 100:
                    quality_issues['short_articles'].append({
                        'file': f"{category}/{file}",
                        'word_count': stats['word_count']
                    })
                
                if not stats['has_headers']:
                    quality_issues['missing_headers'].append(f"{category}/{file}")
                
                if not stats['has_title']:
                    quality_issues['missing_titles'].append(f"{category}/{file}")
                
                if stats['word_count'] == 0:
                    quality_issues['empty_files'].append(f"{category}/{file}")
        
        if quality_stats['total_articles'] > 0:
            quality_stats['avg_words_per_article'] = quality_stats['total_words'] / quality_stats['total_articles']
        
        return quality_issues, quality_stats
    
    def check_expected_content(self, articles: Dict[str, List[str]]) -> Dict:
        """Check if we have expected minimum content per category"""
        expectations = {
            'Finance': 3,      # Expect at least 3 finance articles
            'Technology': 3,   # Expect at least 3 tech articles  
            'Politics': 1,     # Expect at least 1 politics article
            'Travel': 2,       # Expect at least 2 travel articles
            'World': 2,        # Expect at least 2 world articles
            'Entertainment': 3 # Expect at least 3 entertainment articles
        }
        
        content_gaps = {
            'below_expected': [],
            'missing_categories': [],
            'over_expected': []
        }
        
        for category, expected_count in expectations.items():
            actual_count = len(articles.get(category, []))
            
            if actual_count == 0:
                content_gaps['missing_categories'].append(category)
            elif actual_count < expected_count:
                content_gaps['below_expected'].append({
                    'category': category,
                    'expected': expected_count,
                    'actual': actual_count,
                    'missing': expected_count - actual_count
                })
            elif actual_count > expected_count:
                content_gaps['over_expected'].append({
                    'category': category,
                    'expected': expected_count,
                    'actual': actual_count,
                    'extra': actual_count - expected_count
                })
        
        return content_gaps
    
    def generate_detailed_report(self, articles: Dict[str, List[str]]) -> str:
        """Generate detailed content report"""
        report_lines = []
        
        for category in self.expected_categories:
            files = articles.get(category, [])
            report_lines.append(f"\n📁 {category} ({len(files)} articles):")
            
            if not files:
                report_lines.append("   ❌ No articles found")
                continue
                
            for file in files:
                file_path = os.path.join(self.content_path, category, file)
                title = self.extract_title_from_content(file_path)
                stats = self.get_content_stats(file_path)
                
                if 'error' not in stats:
                    status_icon = "✅" if stats['word_count'] > 100 else "⚠️"
                    report_lines.append(f"   {status_icon} {file}")
                    report_lines.append(f"      Title: {title}")
                    report_lines.append(f"      Words: {stats['word_count']} | Characters: {stats['char_count']}")
                else:
                    report_lines.append(f"   ❌ {file} - Error: {stats['error']}")
        
        return "\n".join(report_lines)
    
    def run_verification(self) -> bool:
        """Run complete content verification"""
        print("🔍 Content Verification Tool")
        print("=" * 50)
        
        # Get all articles
        articles = self.get_all_articles()
        
        # Check for duplicates
        print("🔍 Checking for duplicates...")
        duplicates = self.check_for_duplicates(articles)
        
        # Analyze content quality
        print("📊 Analyzing content quality...")
        quality_issues, quality_stats = self.analyze_content_quality(articles)
        
        # Check expected content
        print("📋 Checking content expectations...")
        content_gaps = self.check_expected_content(articles)
        
        # Display results
        print("\n📊 VERIFICATION RESULTS")
        print("=" * 50)
        
        # Overall statistics
        print(f"📈 Overall Statistics:")
        print(f"   • Total Articles: {quality_stats['total_articles']}")
        print(f"   • Total Words: {quality_stats['total_words']:,}")
        print(f"   • Average Words/Article: {quality_stats['avg_words_per_article']:.0f}")
        print(f"   • Categories with Content: {quality_stats['categories_with_content']}/{len(self.expected_categories)}")
        
        # Duplicate analysis
        print(f"\n🔍 Duplicate Analysis:")
        has_duplicates = False
        
        if duplicates['content_duplicates']:
            print(f"   ❌ Content Duplicates Found: {len(duplicates['content_duplicates'])}")
            for dup in duplicates['content_duplicates']:
                print(f"      • {dup['file1']} ↔ {dup['file2']}")
            has_duplicates = True
        else:
            print(f"   ✅ No content duplicates found")
        
        if duplicates['title_duplicates']:
            print(f"   ❌ Title Duplicates Found: {len(duplicates['title_duplicates'])}")
            for dup in duplicates['title_duplicates']:
                print(f"      • '{dup['title']}' in {dup['file1']} and {dup['file2']}")
            has_duplicates = True
        else:
            print(f"   ✅ No title duplicates found")
        
        if duplicates['filename_duplicates']:
            print(f"   ⚠️ Filename Duplicates: {len(duplicates['filename_duplicates'])}")
            for dup in duplicates['filename_duplicates']:
                print(f"      • {dup['filename']}: {', '.join(dup['locations'])}")
        else:
            print(f"   ✅ No filename conflicts")
        
        # Quality issues
        print(f"\n📋 Quality Analysis:")
        has_quality_issues = False
        
        if quality_issues['short_articles']:
            print(f"   ⚠️ Short Articles (<100 words): {len(quality_issues['short_articles'])}")
            for article in quality_issues['short_articles']:
                print(f"      • {article['file']}: {article['word_count']} words")
            has_quality_issues = True
        else:
            print(f"   ✅ All articles have adequate length")
        
        if quality_issues['missing_titles']:
            print(f"   ❌ Missing Titles: {len(quality_issues['missing_titles'])}")
            for file in quality_issues['missing_titles']:
                print(f"      • {file}")
            has_quality_issues = True
        else:
            print(f"   ✅ All articles have titles")
        
        if quality_issues['empty_files']:
            print(f"   ❌ Empty Files: {len(quality_issues['empty_files'])}")
            for file in quality_issues['empty_files']:
                print(f"      • {file}")
            has_quality_issues = True
        
        # Content gaps
        print(f"\n📊 Content Coverage:")
        has_gaps = False
        
        if content_gaps['missing_categories']:
            print(f"   ❌ Missing Categories: {', '.join(content_gaps['missing_categories'])}")
            has_gaps = True
        
        if content_gaps['below_expected']:
            print(f"   ⚠️ Below Expected Content:")
            for gap in content_gaps['below_expected']:
                print(f"      • {gap['category']}: {gap['actual']}/{gap['expected']} (need {gap['missing']} more)")
            has_gaps = True
        
        if content_gaps['over_expected']:
            print(f"   ✅ Extra Content Available:")
            for extra in content_gaps['over_expected']:
                print(f"      • {extra['category']}: {extra['actual']}/{extra['expected']} (+{extra['extra']} bonus)")
        
        if not has_gaps and not content_gaps['missing_categories']:
            print(f"   ✅ All categories meet minimum requirements")
        
        # Detailed content report
        print(f"\n📁 DETAILED CONTENT REPORT")
        print("=" * 50)
        detailed_report = self.generate_detailed_report(articles)
        print(detailed_report)
        
        # Final assessment
        print(f"\n🎯 FINAL ASSESSMENT")
        print("=" * 50)
        
        if not has_duplicates and not has_quality_issues and not has_gaps:
            print("🎉 EXCELLENT: Content is clean, complete, and ready for publication!")
            status = "EXCELLENT"
        elif not has_duplicates and not has_quality_issues:
            print("✅ GOOD: Content quality is high, minor gaps in coverage")
            status = "GOOD"
        elif not has_duplicates:
            print("⚠️ FAIR: No duplicates but some quality issues need attention")
            status = "FAIR"
        else:
            print("❌ NEEDS WORK: Duplicates and quality issues require fixing")
            status = "NEEDS_WORK"
        
        print(f"\n📋 Recommended Actions:")
        if has_duplicates:
            print("1. 🔧 Remove or merge duplicate content")
        if has_quality_issues:
            print("2. ✏️ Improve short articles and fix formatting")
        if has_gaps:
            print("3. 📝 Create additional content for under-represented categories")
        if status == "EXCELLENT":
            print("1. 🚀 Content is ready for publication!")
            print("2. 📤 Proceed with WordPress upload")
        
        return status == "EXCELLENT" or status == "GOOD"

def main():
    """Main function"""
    try:
        verifier = ContentVerifier()
        success = verifier.run_verification()
        
        if success:
            print(f"\n✅ Content verification passed!")
        else:
            print(f"\n⚠️ Content verification found issues to address")
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    main()