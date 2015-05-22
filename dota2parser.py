from bs4 import BeautifulSoup
import urllib.request
import MySQLdb

db = MySQLdb.connect(user="", passwd="", db="")
c = db.cursor()
c.execute("SELECT id, name FROM heroes WHERE active=1")
heroes = c.fetchall()

for hero_id, hero_name in heroes:
	hero_url = 'https://www.dota2.com/hero/'+str(hero_name).replace(' ', '_').replace('\'', '')+'/'
	print(hero_url)
	response = urllib.request.urlopen(hero_url)
	html = response.read()
	soup = BeautifulSoup(html)
	for overviewAbilityRow in soup.find_all('div', class_='overviewAbilityRow'):
		img = overviewAbilityRow.find('img').get('src')
		name = overviewAbilityRow.find('h2').string
		description = overviewAbilityRow.find('p')
		c.execute("INSERT INTO spells (hero_id, name, description, icon) VALUES (%s, %s, %s, %s)", (hero_id, name, description, img))

db.commit()
c.close()
db.close()
