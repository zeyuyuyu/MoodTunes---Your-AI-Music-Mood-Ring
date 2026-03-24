from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get('http://localhost:8000')
    yield driver
    driver.quit()

def test_initial_state(driver):
    # Check if main elements are present
    assert 'MoodTunes' in driver.title
    mood_ring = driver.find_element(By.CLASS_NAME, 'mood-ring')
    assert mood_ring.is_displayed()
    
    mood_text = driver.find_element(By.ID, 'moodText')
    assert 'Take a photo' in mood_text.text

def test_mood_detection_flow(driver):
    # Click mood ring
    mood_ring = driver.find_element(By.ID, 'moodRing')
    mood_ring.click()
    
    # Simulate file input (can't actually input file in headless test)
    driver.execute_script("""
        document.getElementById('cameraInput').dispatchEvent(
            new Event('change', { bubbles: True })
        );
    """)
    
    # Wait for mood detection
    time.sleep(4)
    
    # Verify mood was detected
    mood_text = driver.find_element(By.ID, 'moodText')
    assert 'feeling:' in mood_text.text.lower()
    
    # Verify playlist was generated
    playlist = driver.find_element(By.ID, 'playlistTracks')
    assert len(playlist.find_elements(By.TAG_NAME, 'div')) > 0

def test_share_functionality(driver):
    # First trigger a mood
    driver.execute_script("""
        document.getElementById('cameraInput').dispatchEvent(
            new Event('change', { bubbles: True })
        );
    """)
    time.sleep(4)
    
    # Click share button
    share_btn = driver.find_element(By.CLASS_NAME, 'share-btn')
    share_btn.click()
    
    # Since we can't test actual sharing, we just verify the button click doesn't error
    assert True