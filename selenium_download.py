from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Used for sleep command
import time

# Chrome flags
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1366x768")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--ignore-certificate-errors")

# Insecure certs - currently doesn't work without
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['acceptSslCerts'] = True
capabilities['acceptInsecureCerts'] = True

# Create temporary place to download files (currently not using this)
#downloadDirectory = tempfile.mkdtemp()

# Set directory and disable images as it's headless
prefs = { "download.default_directory" : '/home/selenium' ,
	  "profile.managed_default_content_settings.images" : 2 }
chrome_options.add_experimental_option("prefs",prefs)

# Location of chromedriver
chrome_driver = '/usr/local/bin/chromedriver'

# Launch the browser
driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=capabilities, executable_path=chrome_driver)

# Add missing support for chrome "send_command" to get headless downloads working
driver.command_executor._commands["send_command"] = (
		"POST",
	 	'/session/$sessionId/chromium/send_command'
	)
params = {
	'cmd': 'Page.setDownloadBehavior',
	'params': {
	   'behavior': 'allow',
	   'downloadPath': "/home/selenium"
		}
	}
driver.execute("send_command", params)

# Instructions

driver.get('https://*WEB-DOMAIN-HERE*/')

time.sleep(2)

# Login to website
driver.find_element_by_id("inputUsername").send_keys("*USERNAME*")
driver.find_element_by_id("inputPassword").send_keys("*PASSWORD*")
driver.find_element_by_css_selector("button.btn.update").click()

time.sleep(2)

# Navigate to downloads page
driver.get('https://*WEB-DOMAIN-HERE*/licenses')

# Click on a download button to download file
driver.find_element_by_css_selector('button.btn.btn-default.license-download-button').click()

time.sleep(2)

# Grabbing a screenshot to check state
driver.get_screenshot_as_file('screenshot.png')

# Close session
driver.quit()
