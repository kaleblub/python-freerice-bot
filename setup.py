import os

"""
setup.py must install/setup chromedriver/firefox driver to work with selenium based on user's choice
setup selenium to work right out of the box



Selenium requires a driver to interface with the chosen browser. 
Firefox, for example, requires geckodriver, 
which needs to be installed before the below examples can be run. 
Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin.

Only supports chrome driver currently...
"""
def driverChoice(choice): # 1 = chrome, 2 = firefox, other = error
	
	return 0

def prerequisites(choice, hasChrome):
	# print(f"Preparing the installation & setup of {choice}...")
	os.system("sudo apt-get update")
		
	# If system has Chrome or Firefox

	os.system("")

def installSelenium():
	print("Installing Selenium...")
	os.system("sudo pip3 install -U selenium")

def getChromeVersion():
	version = os.popen("google-chrome --version").readlines()[0].replace("Google Chrome ", "").strip().split('.')
	return (str(version[0]) + '.' + str(version[1]))

# "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_89.0.4389"
# "https://chromedriver.storage.googleapis.com/index.html?path=89.0.4389.23/"

def installChromeDriver():
	print("Installing ChromeDriver...")
	# Installs Chromedriver
	os.system(f"wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip -P /home/gaz/Downloads/")
	os.system("unzip ~/Downloads/chromedriver_linux64.zip -d ~/Downloads/")
	os.system("chmod +x ~/Downloads/chromedriver")
	# Creates some symbolic links
	os.system("sudo mv -f ~/Downloads/chromedriver /usr/local/share/chromedriver")
	os.system("sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver")
	os.system("sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver")
	os.system("sudo rm -r ~/Downloads/chromedriver_linux64.zip")

def installFirefoxDriver():
	return 0

def main():

	return 0

if __name__ == "__main__":
	installChromeDriver()