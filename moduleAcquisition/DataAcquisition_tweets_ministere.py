import requests # Pour envoyer des requêtes HTTP
import re # Pour les expressions régulières
import time
from bs4 import BeautifulSoup # Afin de récupérer les données de fichiers HTML (/XML)
"""
	Afin d'exécuter, contrôler un navigateur (ici Chrome)
	=> Accès à Twitter et récupération de données
"""
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome


######################################Variables Globales#########################################

dates = set() # Ajoute la date de chaque tweet récupéré


###########################################Fonctions##############################################

"""
	-> Prend en paramètre un tweet (ici, contenant un communiqué) 
	-> Stocke sa date
	-> Récupère le communiqué 
	-> Le stocke sous format .jpeg et lui attribue un nom
"""
def get_tweet_bulletin(card) :

	#date
	datetime = card.find_element_by_xpath('./div[2]/div[1]//a/time').get_attribute('datetime')
	date = re.search('(.*)T', datetime)
	if date :
		date = date.group(1)

	if date in dates :
		return

	dates.add(date)

	#images communiqués
	try :
		time.sleep(5)
		bulletinImgs = card.find_elements_by_xpath('./div[2]/div[2]/div[2]//a')
	except NoSuchElementException :
		return
	else :
		j = 0

		# while (j < len(bulletinImgs)) :
		while ((j < 1) if (len(bulletinImgs) < 2) else (j < 2)) :
			time.sleep(5)
			try :
				bulletinImgLink = card.find_element_by_xpath('./div[2]/div[2]/div[2]//a['+str(j+1)+']//img').get_attribute('src')
			except NoSuchElementException :
				return
			else :
				bulletinImgLink = re.sub(r'900x900', 'medium', bulletinImgLink)
				bulletinImgLink = re.sub(r'small', 'large', bulletinImgLink)
				print(bulletinImgLink)

				bulletinImgRequest = requests.get(bulletinImgLink)

				
				fileName = "communique_" + date + "_" + str(j) + ".jpg"
				print(fileName)

				with open(fileName,'wb') as img :
					img.write(bulletinImgRequest.content)

				j+=1


if __name__ == '__main__' :
	
	theUrl = 'https://twitter.com/MinisteredelaS1'

	driver = Chrome(executable_path = "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe")

	driver.get(theUrl)

	last_position = driver.execute_script('return window.pageYOffset;')

	last_scrollHeight = driver.execute_script("""return Math.max(
												  document.body.scrollHeight, document.documentElement.scrollHeight,
												  document.body.offsetHeight, document.documentElement.offsetHeight,
												  document.body.clientHeight, document.documentElement.clientHeight
												);""")

	keep = []

	dates_size_init = len(dates)

	attempt = 0

	tweets = 0

	scrolling = True

	while scrolling :
		time.sleep(10)
		cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')

		for card in cards :
			tweets += 1
			time.sleep(5)
			try :
				checkpoint = card.find_element_by_xpath('./div[2]/div[2]/div[1]//span')
			except NoSuchElementException :
				if card :
					keep.append(card)
			else :
				if (card) and (re.search('Communiqu', checkpoint.text)) :
					get_tweet_bulletin(card)

		scroll_attempt = 0

		while True :

			scrollHeight = driver.execute_script("""return Math.max(
												  document.body.scrollHeight, document.documentElement.scrollHeight,
												  document.body.offsetHeight, document.documentElement.offsetHeight,
												  document.body.clientHeight, document.documentElement.clientHeight
												);""")

			if tweets == 856 :
				scrolling = False
				break
			elif len(dates) == dates_size_init :
				attempt += 1
				if attempt >= 3 :
					driver.execute_script('window.scrollTo(0,' + str(last_position + 4000) + ');')
					last_position += 4000
					attempt = 0
					break
				else :
					break
			else :
				if last_scrollHeight < scrollHeight :
					last_scrollHeight = scrollHeight
					break
				else :
					driver.execute_script('window.scrollTo(0,' + str(last_position + 4000) + ');')
					last_position += 4000
					break