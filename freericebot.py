import os
import time
import signal
from math import sqrt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

''' ____GOALS TO HIT____
	Randomize account creation ? Can't because 
		Then keep account information for logins and getting totals and stuff
		(I should test if they can find out if the accounts are bots though)
	Search for better methods of scraping and web automation

	
	Make different options to run(ex: multiplication, english vocab, different languages, etc)
	Make option for how many rounds to play, loop through
		Give output of counter for correct vs wrong answers
	For the English Grammar option
		Open https://www.thesaurus.com/
			Or install a thesaurus module?
			Search mainWord
		Check/Save 4 choices from freerice  (<div class="card-button">)
		See if any of 4 choices are in mainWord synonyms   
			<span class="css-133coio etbu2a32">
			
			
		| Fix This Error Message |
		V						 V
		Traceback (most recent call last):
  	File "freericebot.py", line 85, in <module>
    get_question()
  File "freericebot.py", line 30, in get_question
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "card-title")))
  File "/usr/local/lib/python3.7/dist-packages/selenium/webdriver/support/wait.py", line 80, in until
    raise TimeoutException(message, screen, stacktrace)
selenium.common.exceptions.TimeoutException: Message:

'''

''' Starts freerice.com and takes argument of which game to play and opens chosen game '''
def freericeGameStartup(driver):  # Argument of (chosen_category)
	driver.implicitly_wait(30)
	driver.get("https://freerice.com/profile-login")  # driver.get(chosen_category)
	driver.implicitly_wait(30)  # Waits up to 30 seconds for page to load

'''Using FR_USERNAME, FR_PASSWORD, and FR_BDAY sign into freerice'''
def freericeSignIn(driver, config):
	dateInput = driver.find_element_by_css_selector('input[type="text"]')
	saveButton = driver.find_element_by_css_selector('button[class="box-button box-button-filled-green age-screen-save-button"]')
	
	driver.execute_script(f"document.getElementsByTagName('input')[1].setAttribute('value', {config[2]})")



	# ActionChains(driver).move_to_element(dateInput).click()
	# for i in range(len(dateInput.text)):
	# 	dateInput.sendKeys("")
	# 	dateInput.sendKeys(Keys.BACKSPACE)
	# dateInput.send_keys(config[2])


''' Updates 'totalRice.txt' '''
def totalRice_update():
	f = open("/home/kaleblub/Desktop/python/freerice/rice", 'r')
	fullFile = f.read()
	f.seek(0, os.SEEK_SET)
	lineList = f.readlines()
	allTotal = str(int(lineList[-1]) + grains)
	fullFile = fullFile.replace(lineList[-1], allTotal)
	f.close()
	f = open("/home/kaleblub/Desktop/python/freerice/rice", 'w')
	f.write(fullFile)
	f.close()


''' Get Question and Answer Buttons '''
def get_question(driver):
	global question, answer1, answer2, answer3, answer4  # Making variables usable throughout program.
	driver.get(driver.current_url)
	wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "card-title")))
	driver.implicitly_wait(30)  # Waits up to 30 seconds for page to load

	question = driver.find_element_by_class_name("card-title")
	wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "card-button")))
	answer1 = driver.find_elements_by_class_name("card-button")[0]
	answer2 = driver.find_elements_by_class_name("card-button")[1]
	answer3 = driver.find_elements_by_class_name("card-button")[2]
	answer4 = driver.find_elements_by_class_name("card-button")[3]


''' Checks the solved problem with the four answers and clicks the match '''
def answer_checker(solution, driver):
	if solution == answer1.text:
		driver.execute_script("arguments[0].click();", answer1)  # Clicks button 1
		# print(i, "out of", times, "Correct!")
	elif solution == answer2.text:
		driver.execute_script("arguments[0].click();", answer2)  # Clicks button 2
		# print(i, "out of", times, "Correct!")
	elif solution == answer3.text:
		driver.execute_script("arguments[0].click();", answer3)  # Clicks button 3
		# print(i, "out of", times, "Correct!")
	elif solution == answer4.text:
		driver.execute_script("arguments[0].click();", answer4)  # Clicks button 4
		# print(i, "out of", times, "Correct!")
	else:
		driver.execute_script("arguments[0].click();", answer1)  # Randomize click when match can't be found
		# print("Can't Choose Answer, Default To Answer #1")

"""Checks for account info in config.py file, if it's not there, 
	prompts user to create account and input details in terminal"""
def checkForAccount():
	try:
		from config import FR_USERNAME, FR_PASSWORD, FR_BDAY
	except ImportError as IE:
		import getpass
		print("! You do not have an account yet, \nplease head to 'https://freerice.com/profile-register'\nand fill in the relevent information below to be stored in a config file...")
		FR_USERNAME = input("Username/Email: ")
		FR_PASSWORD = getpass.getpass("Password: ")
		FR_BDAY = input("\n\n\nLastly, what is your birthday? \n*Please input as <month>/<day>/<year>\n: ")
		f = open("config.py", "w+")
		f.write(f"FR_USERNAME = '{FR_USERNAME}'\n")
		f.write(f"FR_PASSWORD = '{FR_PASSWORD}'\n")
		f.write(f"FR_BDAY = '{FR_BDAY}'\n")
		f.close()
		print("\n\n\n\nUser details saved in config.py\nPlease run the program again...\nShutdown.\n\n\n\n\n\n")
	return [FR_USERNAME, FR_PASSWORD, FR_BDAY]

def main():
	# Before starting, check if there are account details in config.py
	accountDetails = checkForAccount() # list

	# Choose which category to choose from and play
	print("What FreeRice Game Should I Play?")
	print("Multiplication Tables = 'mt'  |  Basic Math Pre-Algebra = 'bm'  |  Vocabulary = 'v'")
	game = input(": ")
	# Choose how many times to play that category
	times = input("How Many Times Should I Play The Game? ")

	chromedriver = "chromedriver"
	driver = webdriver.Chrome(chromedriver)  # Opens a Chrome page
	wait = WebDriverWait(driver, 50)
	# driver.implicitly_wait(30)
	# driver.get("https://beta.freerice.com/categories/basic-math-pre-algebra")
	# driver.implicitly_wait(30)  # Waits up to 30 seconds for page to load

	# Timer to see how long playing the game takes
	startTime = time.time()
	freericeGameStartup(driver)
	freericeSignIn(driver, accountDetails)

	''' Click 'OK' On Cookies Button '''
	cookies_button = driver.find_elements_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/button")[0]
	cookies_button.click()
	driver.implicitly_wait(30)  # Waits up to 30 seconds for page to load

	correct_counter = 0

	''' MULTIPLICATION TABLE OPTION '''
	if times == '':
		while True:
			try:
				get_question(driver)
				solution = eval(question.text.rstrip('=').replace('x', '*'))
				print(question.text, "=", solution)
				print(answer1.text, answer2.text, answer3.text, answer4.text)
				answer_checker(str(solution))
				print("\n")
				correct_counter = correct_counter + 1
				print(correct_counter)
				print("\n")
			except KeyboardInterrupt:
				pass
			except TimeoutException:
				print("Loading took too long!")
				driver.quit()
				pass
	else:
		for i in range(1, int(times)+1):
			try:
				get_question(driver)
				solution = eval(question.text.rstrip('=').replace('x', '*'))
				print(question.text, "=", solution)
				print(answer1.text, answer2.text, answer3.text, answer4.text)
				answer_checker(str(solution), driver)
				print("\n")
				correct_counter = correct_counter + 1
				print(correct_counter)
				print("\n")
			except KeyboardInterrupt:
				pass
			except TimeoutException:
				print("Loading took too long!")
				pass

	driver.quit()
	# driver.get(driver.current_url)
	grains = correct_counter * 10  # driver.find_element_by_class_name("rice-counter__value").text
	totalTime = (time.time() - startTime) / 60
	print("I played", correct_counter, "games and earned", grains, "grains of rice in", totalTime, "minutes!")
	totalRice_update()

if __name__ == "__main__":
	main()

''' 
77010
	BASIC MATH PRE-ALGEBRA OPTION
	for i in range(1, times+1):
		get_question()
		if "rounded" in question.text:  # For rounding questions
			solution = round(float((question.text).replace("rounded ", "").replace(" =", "")))
		elif "square root " in question.text:  # For square root questions
			solution = int(sqrt(int((question.text).replace("square root ", "").replace(" =", ""))))
		elif "%" in question.text:  # For calculating percentage	.82 = 0.82		50% = 0.5
			solution = int((question.text).rstrip('= %')) / 100  #18% 80% 82% 28% | 2/3 1/3 2/5 1/2
		else:
			solution = eval((question.text).rstrip('=').replace('x', '*').replace("^", "**"))
	
		if '/' in question.text:  # For Division
			solution = int(solution)  # Also needs to calculate to decimal
			#  5 / 13 + 7 / 13 = 0
			#  9 / 13, 12 / 13, 11 / 13, 10 / 13
		print(question.text, solution)
		print(answer1.text, answer2.text, answer3.text, answer4.text)
		answer_checker(str(solution))
		print("")
	
	
	
	ENGLISH VOCAB OPTION
	Save main_window
	main_window = driver.window_handles[0]
	
	Word to search for synonyms
	mainWord = driver.find_element_by_class_name("card-title")
	print((mainWord.text).rstrip(" means:"))
	
	Opens new tab in chrome and goes to 'thesaurus.com'
	driver.execute_script("window.open('https://www.thesaurus.com/');")
	driver.switch_to_window(driver.window_handles[1])
	driver.implicitly_wait(5)
	
	Thesaurus Searchbar Find and input 'mainWord'
	thes_searchbar = driver.find_element_by_id("searchbar_input")
	thes_searchbar.send_keys((mainWord.text).rstrip(" means:"))
		Search Submit Find and Click
	search_submit = driver.find_element_by_id("search-submit")[0]
	search_submit.click()
	
	
	MENU NAVIGATION
	|	|	|	|	|
	V	V	V	V	V
	
	# Click Menu Button
	wait.until(EC.element_to_be_clickable((By.ID, 'Path_7605')))
	driver.find_elements_by_id("Path_7605")[0].click()
	driver.implicitly_wait(5)
	
	# Click Categories Button
	driver.find_elements_by_class_name("side-drawer-menu-item")[1].click()
	driver.implicitly_wait(5)
	
	# Click Basic Math
	driver.find_elements_by_class_name("category-image--basic-math-pre-algebra")[0].click()
'''

