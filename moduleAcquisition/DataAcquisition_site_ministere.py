import requests # Pour envoyer des requêtes HTTP
import re # Pour les expressions régulières
import time
from bs4 import BeautifulSoup # Afin de récupérer les données de fichiers HTML (/XML)


# headers nécessaire à l'accès du site
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}


"""
	Fonction permettant de comparer les liens à partir du href et
	de filtrer ceux des communiqués du ministère
"""
def recupLiensCommuniques(href) :
	# Filtrage des href commençant par "/Actualites/coronavirus-communiqu"
	return href and re.compile('^/Actualites/coronavirus-communiqu.*').search(href)


"""
	Fonction permettant de comparer les liens à partir du href et
	de récupérer les liens des fichiers pdf d'un communiqué donné
"""
def recupLiensPdfs(href) :
	# Filtrage du href commençant par "https://sante.sec.gouv.sn/sites/default/files/"
	# et se terminant par "pdf"
	return href and re.compile('^https://sante.sec.gouv.sn/sites/default/files/.*pdf$').search(href)


def bulletinPdfsDownload(urlHome, urlCompletePath) :

	actuPageRequest = requests.get(urlCompletePath, headers=headers) 
	  
	actuPageSoup = BeautifulSoup(actuPageRequest.content, 'lxml')
	  
	liensCommuniques = actuPageSoup.findAll(href=recupLiensCommuniques)

	urlsCommuniques = []

	for lien in liensCommuniques :
		urlsCommuniques.append(urlHome + lien['href'])

	for url in urlsCommuniques :
		bulletinPageRequest = requests.get(url, headers=headers) 
	  
		bulletinPageSoup = BeautifulSoup(bulletinPageRequest.content, 'lxml')
	  
		pdfsPaths = bulletinPageSoup.findAll(href=recupLiensPdfs)

		for pdfPath in pdfsPaths:

			lienPdf = pdfPath['href']

			nomPdf = pdfPath.text
			print(nomPdf)

			pdfPathRequest = requests.get(lienPdf, headers=headers, stream = True)
			with open(nomPdf,'wb') as pdf :
				for chunk in pdfPathRequest.iter_content(chunk_size=1024) :
					if chunk :
						pdf.write(chunk)


if __name__ == '__main__':
	urlHome = 'https://sante.sec.gouv.sn/'
	urlActualite = urlHome + 'taxonomy/term/14'

	actuPageRequest = requests.get(urlActualite, headers=headers)

	actuPagenumb = 0

	while actuPageRequest.status_code == 200 :
		bulletinPdfsDownload(urlHome, urlActualite)
		urlActualite = urlHome + 'taxonomy/term/14?page=' + str(actuPagenumb)
		actuPageRequest = requests.get(urlActualite, headers=headers)
		actuPagenumb += 1
		time.sleep(30)