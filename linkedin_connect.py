import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

def linkedin_auto_connect(username, password, max_connections=40):
    # Configure Chrome options to act more human-like
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    
    # Random user agent to appear more like a normal browser
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    
    # Initialize the browser with webdriver_manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        # Login to LinkedIn
        driver.get("https://www.linkedin.com/login")
        time.sleep(2 + random.uniform(0.5, 1.5))  # Random delay
        
        # Login process
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        
        # Type username like a human
        for char in username:
            username_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.3))
        
        time.sleep(random.uniform(0.5, 1.0))
        
        password_field = driver.find_element(By.ID, "password")
        
        # Type password like a human
        for char in password:
            password_field.send_keys(char)
            time.sleep(random.uniform(0.05, 0.3))
        
        time.sleep(random.uniform(0.5, 1.0))
        
        # Uncheck "Keep me logged in" checkbox if it's checked
        try:
            remember_me_checkbox = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "rememberMeOptIn-checkbox"))
            )
            
            # Check if it's already checked
            if remember_me_checkbox.is_selected():
                # Find the label and click it to uncheck
                remember_me_label = driver.find_element(By.XPATH, "//label[@for='rememberMeOptIn-checkbox']")
                remember_me_label.click()
                print("Unchecked 'Keep me logged in'")
                time.sleep(random.uniform(0.5, 1.0))
        except Exception as e:
            print(f"Couldn't find or interact with 'Keep me logged in' checkbox: {e}")
        
        # Click login
        password_field.send_keys(Keys.RETURN)
        time.sleep(5 + random.uniform(1, 2))  # Wait for login
        
        # Automatically navigate to My Network section
        print("Navigating to My Network page...")
        driver.get("https://www.linkedin.com/mynetwork/grow/")
        time.sleep(4 + random.uniform(1, 2))  # Wait for page to load
        
        connections_sent = 0
        fails = 0
        
        while connections_sent < max_connections:
            # Scroll down to load more profiles
            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2 + random.uniform(0.5, 1.5))
            
            # Check if we've hit the bottom of the page
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # Try a few more times with different scrolling techniques
                for _ in range(3):
                    driver.execute_script("window.scrollBy(0, window.innerHeight);")
                    time.sleep(1 + random.uniform(0.5, 1))
                    driver.execute_script("window.scrollBy(0, -300);")
                    time.sleep(0.5)
                    driver.execute_script("window.scrollBy(0, 300);")
                    
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height != last_height:
                        break
            
            # Find all Connect buttons - specifically on the My Network page
            try:
                # On My Network page, the connect buttons often have a specific structure
                connect_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Connect') or (contains(., 'Connect') and not(contains(., 'connections')))]")
                
                # Filter out already connected or pending buttons
                valid_buttons = []
                for button in connect_buttons:
                    try:
                        button_text = button.text.strip()
                        if "Connect" in button_text and "Following" not in button_text and "Pending" not in button_text:
                            valid_buttons.append(button)
                    except:
                        continue
                
            except Exception as e:
                print(f"Error finding connect buttons: {e}")
                continue
            
            if not valid_buttons:
                print("No valid connect buttons found on this scroll. Scrolling more...")
                continue
            
            print(f"Found {len(valid_buttons)} valid connect buttons")
            
            # Process each Connect button
            for button in valid_buttons:
                if connections_sent >= max_connections:
                    print(f"Reached maximum connection limit ({max_connections}). Stopping.")
                    break
                
                try:
                    # Scroll the button into view
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
                    time.sleep(1 + random.uniform(0.5, 1))
                    
                    # Click the Connect button
                    try:
                        button.click()
                    except ElementClickInterceptedException:
                        # If click intercepted, try with JavaScript
                        driver.execute_script("arguments[0].click();", button)
                    
                    time.sleep(1 + random.uniform(0.5, 1))
                    
                    # Handle the connection modal
                    try:
                        # Look for the Send button in the modal
                        send_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send now' or text()='Send' or contains(@aria-label, 'Send invitation')]"))
                        )
                        time.sleep(random.uniform(0.3, 0.7))
                        send_button.click()
                        connections_sent += 1
                        print(f"Connection request sent: {connections_sent}/{max_connections}")
                        time.sleep(2 + random.uniform(0.5, 1.5))  # Wait for the modal to close
                        
                    except TimeoutException:
                        # No modal appeared, check if connection was sent anyway
                        try:
                            # Check if the button changed to "Pending"
                            # First check original button
                            try:
                                if "Pending" in button.text.strip():
                                    connections_sent += 1
                                    print(f"Connection request sent (button changed to Pending): {connections_sent}/{max_connections}")
                                    continue
                            except:
                                pass
                                
                            # Then check for any pending buttons in the area
                            pending_check = WebDriverWait(driver, 2).until(
                                EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Pending')]"))
                            )
                            connections_sent += 1
                            print(f"Connection request sent (no modal): {connections_sent}/{max_connections}")
                        except:
                            fails += 1
                            print(f"Failed to send connection (no modal): {fails}")
                        
                    except Exception as e:
                        fails += 1
                        print(f"Failed to send connection (modal error): {fails} - {str(e)[:50]}")
                        
                except Exception as e:
                    fails += 1
                    print(f"Error processing button: {e}. Failures: {fails}")
                    continue
                
                # Random delay between connections to appear more human-like
                time.sleep(3 + random.uniform(1, 3))
        
        print(f"\nFinished sending connection requests!")
        print(f"Successful connections sent: {connections_sent}")
        print(f"Failed attempts: {fails}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Script completed. Browser will close in 5 seconds.")
        for i in range(5, 0, -1):
            print(f"Closing browser in {i}...")
            time.sleep(1)
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    
    LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    
    max_conn = 40

    linkedin_auto_connect(LINKEDIN_USERNAME, LINKEDIN_PASSWORD, max_connections=max_conn)