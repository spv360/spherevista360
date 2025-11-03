#!/usr/bin/env python3
"""
Add stock ticker to WordPress site using custom code injection
"""

# Stock ticker HTML with inline styles (no position:fixed issues)
TICKER_CODE = """
<!-- Stock Ticker Injection Script -->
<script>
(function() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTicker);
    } else {
        initTicker();
    }
    
    function initTicker() {
        // Create ticker element
        var tickerHTML = `
<div id="spherevista-stock-ticker" style="background: #1a1a2e; color: white; padding: 10px 0; overflow: hidden; border-bottom: 2px solid #0f3460; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); position: relative; z-index: 50;">
    <div style="max-width: 100%; overflow: hidden;">
        <div class="ticker-scroll" style="display: flex; animation: tickerScroll 30s linear infinite;">
            <div style="display: flex; gap: 50px; padding: 0 20px; white-space: nowrap; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">SPY</span>
                    <span style="font-weight: 600; color: #ffffff;">$452.34</span>
                    <span style="color: #00ff88; font-weight: 600;">+0.54%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">QQQ</span>
                    <span style="font-weight: 600; color: #ffffff;">$382.67</span>
                    <span style="color: #ff4757; font-weight: 600;">-0.32%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">AAPL</span>
                    <span style="font-weight: 600; color: #ffffff;">$182.45</span>
                    <span style="color: #00ff88; font-weight: 600;">+1.79%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">MSFT</span>
                    <span style="font-weight: 600; color: #ffffff;">$378.85</span>
                    <span style="color: #00ff88; font-weight: 600;">+0.52%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">GOOGL</span>
                    <span style="font-weight: 600; color: #ffffff;">$139.67</span>
                    <span style="color: #ff4757; font-weight: 600;">-0.63%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">AMZN</span>
                    <span style="font-weight: 600; color: #ffffff;">$145.23</span>
                    <span style="color: #00ff88; font-weight: 600;">+1.01%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">TSLA</span>
                    <span style="font-weight: 600; color: #ffffff;">$242.18</span>
                    <span style="color: #00ff88; font-weight: 600;">+2.40%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">META</span>
                    <span style="font-weight: 600; color: #ffffff;">$478.92</span>
                    <span style="color: #ff4757; font-weight: 600;">-0.49%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 5px; padding: 4px 12px; background: rgba(255,255,255,0.1); border-radius: 12px; font-size: 12px; font-weight: 600;">
                    <span>🔴</span>
                    <span>Market Closed</span>
                </div>
            </div>
            <div style="display: flex; gap: 50px; padding: 0 20px; white-space: nowrap; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">SPY</span>
                    <span style="font-weight: 600; color: #ffffff;">$452.34</span>
                    <span style="color: #00ff88; font-weight: 600;">+0.54%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">QQQ</span>
                    <span style="font-weight: 600; color: #ffffff;">$382.67</span>
                    <span style="color: #ff4757; font-weight: 600;">-0.32%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">AAPL</span>
                    <span style="font-weight: 600; color: #ffffff;">$182.45</span>
                    <span style="color: #00ff88; font-weight: 600;">+1.79%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">MSFT</span>
                    <span style="font-weight: 600; color: #ffffff;">$378.85</span>
                    <span style="color: #00ff88; font-weight: 600;">+0.52%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">GOOGL</span>
                    <span style="font-weight: 600; color: #ffffff;">$139.67</span>
                    <span style="color: #ff4757; font-weight: 600;">-0.63%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">AMZN</span>
                    <span style="font-weight: 600; color: #ffffff;">$145.23</span>
                    <span style="color: #00ff88; font-weight: 600;">+1.01%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">TSLA</span>
                    <span style="font-weight: 600; color: #ffffff;">$242.18</span>
                    <span style="color: #00ff88; font-weight: 600;">+2.40%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 500;">
                    <span style="font-weight: 700; font-size: 15px; color: #00d4ff; letter-spacing: 0.5px;">META</span>
                    <span style="font-weight: 600; color: #ffffff;">$478.92</span>
                    <span style="color: #ff4757; font-weight: 600;">-0.49%</span>
                </div>
                <div style="display: inline-flex; align-items: center; gap: 5px; padding: 4px 12px; background: rgba(255,255,255,0.1); border-radius: 12px; font-size: 12px; font-weight: 600;">
                    <span>🔴</span>
                    <span>Market Closed</span>
                </div>
            </div>
        </div>
    </div>
</div>
<style>
@keyframes tickerScroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
</style>
        `;
        
        // Find the body element and prepend ticker
        var body = document.body;
        if (body && body.firstChild) {
            var tempDiv = document.createElement('div');
            tempDiv.innerHTML = tickerHTML;
            var tickerElement = tempDiv.firstChild;
            body.insertBefore(tickerElement, body.firstChild);
            
            // Add some top padding to body to push content down
            document.body.style.paddingTop = '0px';
        }
    }
})();
</script>
"""

def add_ticker_to_header():
    """Add stock ticker via WordPress Custom Code in header"""
    
    # We'll add this to the homepage via wp_head hook
    # Using WordPress Code Snippets or theme customizer
    
    print("📊 Stock Ticker Code Generated")
    print("=" * 60)
    print("\nTo add the stock ticker to your site:")
    print("\n1. Go to WordPress Admin > Appearance > Customize")
    print("2. Navigate to 'Additional CSS' or 'Custom Code'")
    print("3. Or install 'Code Snippets' plugin")
    print("4. Add the following code to inject in <head> section:")
    print("\n" + "=" * 60)
    print(TICKER_CODE)
    print("=" * 60)
    
    # Save to file
    with open('stock_ticker_code.html', 'w') as f:
        f.write(TICKER_CODE)
    
    print("\n✅ Code also saved to: stock_ticker_code.html")
    print("\nThis will inject the ticker at the very top of every page!")

if __name__ == '__main__':
    add_ticker_to_header()
