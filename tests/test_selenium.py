import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opts)


def test_homepage_loads():
    d = get_driver()
    d.get("http://web:5000/")
    assert "To-Do" in d.page_source
    d.quit()


def test_add_task():
    d = get_driver()
    d.get("http://web:5000/")

    input_box = d.find_element("id", "task-input")
    input_box.send_keys("Selenium Task")

    btn = d.find_element("css selector", "button[type='submit']")
    btn.click()

    time.sleep(2)

    assert "Selenium Task" in d.page_source
    d.quit()
