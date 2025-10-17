"""
Output Formatters
================
Formatting utilities for consistent output display.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class ResultFormatter:
    """Format operation results for display."""
    
    @staticmethod
    def format_validation_result(result: Dict[str, Any], title: str = "Validation Result") -> str:
        """Format validation result for display."""
        output = []
        output.append(f"\n📊 {title}")
        output.append("-" * 40)
        
        success_rate = result.get('success_rate', 0)
        output.append(f"Success Rate: {ResultFormatter._format_percentage(success_rate)}")
        
        if 'total_checked' in result:
            output.append(f"Total Checked: {result['total_checked']}")
        
        if 'issues_found' in result:
            output.append(f"Issues Found: {result['issues_found']}")
        
        if 'fixed' in result:
            output.append(f"Fixed: {result['fixed']}")
        
        # Show specific issues
        if 'issues' in result and result['issues']:
            output.append("\n🔍 Issues:")
            for issue in result['issues']:
                output.append(f"  • {issue}")
        
        # Show fixes
        if 'fixes' in result and result['fixes']:
            output.append("\n✅ Fixes Applied:")
            for fix in result['fixes']:
                output.append(f"  • {fix}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_post_summary(post: Dict[str, Any]) -> str:
        """Format post summary for display."""
        title = post.get('title', {}).get('rendered', 'Untitled')
        post_id = post.get('id', 'Unknown')
        status = post.get('status', 'Unknown')
        
        # Get publish date
        date_str = post.get('date', '')
        if date_str:
            try:
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except:
                formatted_date = date_str[:10]
        else:
            formatted_date = 'Unknown'
        
        return f"📝 [{post_id}] {title} ({status}, {formatted_date})"
    
    @staticmethod
    def format_operation_summary(operation: str, results: Dict[str, Any]) -> str:
        """Format operation summary."""
        output = []
        output.append(f"\n🎯 {operation} Summary")
        output.append("=" * 50)
        
        # Basic stats
        if 'total_processed' in results:
            output.append(f"Total Processed: {results['total_processed']}")
        
        if 'successful' in results:
            output.append(f"Successful: {results['successful']}")
        
        if 'failed' in results:
            output.append(f"Failed: {results['failed']}")
        
        if 'errors' in results and results['errors']:
            output.append(f"\n❌ Errors Encountered:")
            for error in results['errors'][:5]:  # Show max 5 errors
                output.append(f"  • {error}")
            if len(results['errors']) > 5:
                output.append(f"  ... and {len(results['errors']) - 5} more")
        
        # Calculate success rate
        total = results.get('total_processed', 0)
        successful = results.get('successful', 0)
        if total > 0:
            success_rate = (successful / total) * 100
            output.append(f"\nOverall Success Rate: {ResultFormatter._format_percentage(success_rate)}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_progress(current: int, total: int, item_name: str = "item") -> str:
        """Format progress indicator."""
        if total == 0:
            return f"⏳ Processing {item_name}s..."
        
        percentage = (current / total) * 100
        progress_bar = "█" * int(percentage // 5) + "░" * (20 - int(percentage // 5))
        return f"⏳ Progress: [{progress_bar}] {current}/{total} {item_name}s ({percentage:.1f}%)"
    
    @staticmethod
    def _format_percentage(value: float) -> str:
        """Format percentage with color coding."""
        if value >= 90:
            return f"🟢 {value:.1f}%"
        elif value >= 70:
            return f"🟡 {value:.1f}%"
        else:
            return f"🔴 {value:.1f}%"


class TableFormatter:
    """Format data in table format."""
    
    @staticmethod
    def format_table(data: List[Dict], headers: List[str], max_width: int = 80) -> str:
        """Format data as a simple table."""
        if not data:
            return "No data to display"
        
        # Calculate column widths
        col_widths = {}
        for header in headers:
            col_widths[header] = len(header)
        
        for row in data:
            for header in headers:
                value = str(row.get(header, ''))
                col_widths[header] = max(col_widths[header], len(value))
        
        # Limit column widths
        max_col_width = max_width // len(headers) - 3
        for header in headers:
            col_widths[header] = min(col_widths[header], max_col_width)
        
        # Build table
        output = []
        
        # Header
        header_row = " | ".join(header.ljust(col_widths[header]) for header in headers)
        output.append(header_row)
        output.append("-" * len(header_row))
        
        # Data rows
        for row in data:
            data_row = []
            for header in headers:
                value = str(row.get(header, ''))
                if len(value) > col_widths[header]:
                    value = value[:col_widths[header]-3] + "..."
                data_row.append(value.ljust(col_widths[header]))
            output.append(" | ".join(data_row))
        
        return "\n".join(output)