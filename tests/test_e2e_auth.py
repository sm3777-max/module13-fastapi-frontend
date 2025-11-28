import pytest
from playwright.sync_api import Page, expect
import random
import time
import requests 

# Helper function to generate unique user data
def get_random_user():
    rand_id = random.randint(100000, 999999) 
    return {
        "email": f"e2e_{rand_id}@test.com",
        "username": f"e2e_user_{rand_id}",
        "password": "securepass"
    }

# --- WAIT FOR SERVER FIXTURE (CRITICAL) ---

def wait_for_app_startup(url, timeout=25):
    """Polls the given URL until it returns a 200 status."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Check the root endpoint health
            response = requests.get(url)
            if response.status_code == 200:
                print("\n[INFO] Server is UP!")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    raise TimeoutError(f"Server did not start up at {url} within {timeout} seconds.")

@pytest.fixture(scope="session", autouse=True)
def wait_for_server_start(base_url):
    """Fixture that runs once per session to wait for the app service."""
    # FINAL FIX: Hardcode the target for the polling function to prevent MissingSchema error.
    wait_for_app_startup("http://localhost:8000/") 

# --- TEST 1: REGISTRATION (POSITIVE) ---
def test_frontend_register(page: Page, base_url):
    user = get_random_user()
    
    # 1. Go to register page
    page.goto(f"{base_url}/static/register.html")
    
    # 2. Fill form
    page.fill("#email", user["email"])
    page.fill("#username", user["username"])
    page.fill("#password", user["password"])
    
    # 3. Submit
    page.click("button[type=submit]")
    
    # 4. Check for success message
    message = page.locator("#message")
    expect(message).to_contain_text("Registration Successful", timeout=15000)

# --- TEST 2: LOGIN (POSITIVE) ---
def test_frontend_login(page: Page, base_url):
    # 1. Create a user FIRST (relies on successful register test run)
    user = get_random_user()
    
    # Register them via the UI
    page.goto(f"{base_url}/static/register.html")
    page.fill("#email", user["email"])
    page.fill("#username", user["username"])
    page.fill("#password", user["password"])
    page.click("button[type=submit]")
    expect(page.locator("#message")).to_contain_text("Registration Successful", timeout=15000)
    
    # 2. Now go to Login page
    page.goto(f"{base_url}/static/login.html")
    
    # 3. Fill form with the user we just made
    page.fill("#username", user["email"]) 
    page.fill("#password", user["password"])
    page.click("button[type=submit]")
    
    # 4. Check Success
    message = page.locator("#message")
    expect(message).to_contain_text("Login Successful", timeout=15000)

# --- TEST 3: LOGIN (NEGATIVE) ---
def test_frontend_login_fail(page: Page, base_url):
    # 1. Go to login page
    page.goto(f"{base_url}/static/login.html")
    
    # 2. Fill with definitely wrong data
    page.fill("#username", "nonexistent@user.com")
    page.fill("#password", "wrongpass")
    page.click("button[type=submit]")
    
    # 3. Check for error message
    message = page.locator("#message")
    expect(message).to_contain_text("Invalid credentials", timeout=15000)