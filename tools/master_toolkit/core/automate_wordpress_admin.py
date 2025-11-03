#!/usr/bin/env python3
"""
Automate WordPress Admin Configuration
Uses Selenium to configure WordPress without manual intervention
"""

import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

# Load environment variables
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_BASE_URL')
USERNAME = os.getenv('WORDPRESS_USERNAME')
ADMIN_PASSWORD = os.getenv('WORDPRESS_ADMIN_PASSWORD', os.getenv('WORDPRESS_PASSWORD'))

def setup_driver():
    """Setup Chrome driver"""
    print("🔧 Setting up browser...")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    return driver

def login_to_wordpress(driver):
    """Login to WordPress admin"""
    print(f"\n🔐 Logging in to {WORDPRESS_URL}/wp-admin...")
    
    driver.get(f"{WORDPRESS_URL}/wp-admin")
    
    # Wait for login form
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user_login"))
    )
    
    # Enter credentials
    username_field = driver.find_element(By.ID, "user_login")
    password_field = driver.find_element(By.ID, "user_pass")
    
    username_field.clear()
    username_field.send_keys(USERNAME)
    
    password_field.clear()
    password_field.send_keys(ADMIN_PASSWORD)
    
    # Submit form
    login_button = driver.find_element(By.ID, "wp-submit")
    login_button.click()
    
    # Wait for dashboard
    time.sleep(3)
    
    if "wp-admin" in driver.current_url:
        print("✅ Login successful!")
        return True
    else:
        print("❌ Login failed!")
        return False

def set_static_homepage(driver):
    """Set static homepage"""
    print("\n🏠 Configuring static homepage...")
    
    driver.get(f"{WORDPRESS_URL}/wp-admin/options-reading.php")
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "show_on_front"))
    )
    
    # Select "A static page"
    static_page_radio = driver.find_element(By.CSS_SELECTOR, "input[value='page']")
    driver.execute_script("arguments[0].click();", static_page_radio)
    
    time.sleep(1)
    
    # Select Homepage for front page
    front_page_select = Select(driver.find_element(By.ID, "page_on_front"))
    
    # Find Homepage option
    for option in front_page_select.options:
        if "Homepage" in option.text:
            front_page_select.select_by_visible_text(option.text)
            print(f"   ✓ Set front page: {option.text}")
            break
    
    # Select Blog for posts page
    posts_page_select = Select(driver.find_element(By.ID, "page_for_posts"))
    
    for option in posts_page_select.options:
        if "Blog" in option.text:
            posts_page_select.select_by_visible_text(option.text)
            print(f"   ✓ Set posts page: {option.text}")
            break
    
    # Save changes
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()
    
    time.sleep(2)
    print("✅ Homepage configured!")

def configure_menu(driver):
    """Configure navigation menu"""
    print("\n🧭 Configuring navigation menu...")
    
    driver.get(f"{WORDPRESS_URL}/wp-admin/nav-menus.php")
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "menu-to-edit"))
    )
    
    time.sleep(2)
    
    # Check if Main Menu exists, or select it
    try:
        # Try to find and select Main Menu
        menu_select = driver.find_elements(By.CSS_SELECTOR, ".menu-name-label")
        for menu_label in menu_select:
            if "Main Menu" in menu_label.text:
                menu_label.click()
                time.sleep(2)
                print("   ✓ Selected Main Menu")
                break
    except:
        print("   Creating new menu...")
    
    # Add pages to menu
    pages_to_add = ["Homepage", "About", "Services", "Contact"]
    
    # Expand pages panel
    try:
        pages_tab = driver.find_element(By.ID, "add-page")
        if "closed" in pages_tab.get_attribute("class"):
            pages_title = driver.find_element(By.CSS_SELECTOR, "#add-page .accordion-section-title")
            pages_title.click()
            time.sleep(1)
    except:
        pass
    
    # Check "View All" and add pages
    try:
        view_all_tab = driver.find_element(By.CSS_SELECTOR, "#page-all a")
        view_all_tab.click()
        time.sleep(2)
        
        # Select pages
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "#page-all .tabs-panel input[type='checkbox']")
        
        for checkbox in checkboxes:
            label = checkbox.find_element(By.XPATH, "following-sibling::label")
            page_name = label.text.strip()
            
            if any(page in page_name for page in pages_to_add):
                if not checkbox.is_selected():
                    checkbox.click()
                    print(f"   ✓ Selected: {page_name}")
        
        # Click "Add to Menu"
        add_to_menu_btn = driver.find_element(By.ID, "submit-page")
        add_to_menu_btn.click()
        time.sleep(2)
        
    except Exception as e:
        print(f"   ⚠️  Error adding pages: {e}")
    
    # Assign to Primary location
    try:
        primary_location = driver.find_element(By.CSS_SELECTOR, "input[value='primary']")
        if not primary_location.is_selected():
            primary_location.click()
            print("   ✓ Assigned to Primary location")
    except:
        pass
    
    # Save menu
    save_menu_btn = driver.find_element(By.ID, "save_menu_header")
    save_menu_btn.click()
    
    time.sleep(3)
    print("✅ Menu configured!")

def set_permalinks(driver):
    """Set permalink structure"""
    print("\n🔗 Configuring permalinks...")
    
    driver.get(f"{WORDPRESS_URL}/wp-admin/options-permalink.php")
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "selection"))
    )
    
    # Select Post name
    post_name_radio = driver.find_element(By.CSS_SELECTOR, "input[value='/%postname%/']")
    driver.execute_script("arguments[0].click();", post_name_radio)
    
    # Save changes
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()
    
    time.sleep(2)
    print("✅ Permalinks configured!")

def update_site_title(driver):
    """Update site title and tagline"""
    print("\n📝 Updating site title...")
    
    driver.get(f"{WORDPRESS_URL}/wp-admin/options-general.php")
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "blogname"))
    )
    
    # Update title
    title_field = driver.find_element(By.ID, "blogname")
    title_field.clear()
    title_field.send_keys("SphereVista360")
    
    # Update tagline
    tagline_field = driver.find_element(By.ID, "blogdescription")
    tagline_field.clear()
    tagline_field.send_keys("Your 360° View on Global Insights - Finance, Technology & Innovation")
    
    # Save changes
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()
    
    time.sleep(2)
    print("✅ Site title updated!")

def main():
    """Main automation function"""
    print("=" * 60)
    print("🤖 WordPress Admin Automation")
    print("=" * 60)
    print(f"📍 Site: {WORDPRESS_URL}")
    print(f"👤 User: {USERNAME}")
    print("=" * 60)
    
    driver = None
    
    try:
        # Setup browser
        driver = setup_driver()
        
        # Login
        if not login_to_wordpress(driver):
            print("❌ Failed to login. Check credentials.")
            return
        
        # Configure WordPress
        update_site_title(driver)
        set_static_homepage(driver)
        set_permalinks(driver)
        configure_menu(driver)
        
        print("\n" + "=" * 60)
        print("✅ AUTOMATION COMPLETE!")
        print("=" * 60)
        print(f"\n🌐 Visit your site: {WORDPRESS_URL}")
        print("   • Homepage is now the front page")
        print("   • Navigation menu is configured")
        print("   • All content is visible")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if driver:
            driver.quit()
            print("\n🔒 Browser closed")

if __name__ == "__main__":
    main()
