import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
from termcolor import colored
import colorama
class Verbose:
	def EchoDebug(debug):
		colorama.init()
		for x in sys.argv:
			if x == "-D":
				print(colored("[Debug] ","yellow") + debug)
	def EchoWarning(warn):
		colorama.init()
		print(colored("[Warning!] ","yellow") + warn)
	def EchoError(error):
		colorama.init()
		print(colored("[Error!] ","red") + error)
	def EchoVerbose(verbose):
		colorama.init()
		for x in sys.argv:
			if x == "-V":
				print(colored("[Verbose] ","green") + verbose)
		
def get_page(link):
	driver = webdriver.Chrome()
	driver.get(link)
	time.sleep(2) #additioal secs to wait until page is loaded
	soup=BeautifulSoup(driver.page_source, 'lxml')
	driver.quit()
	return soup
def CheckForError(array):
	_len = len(array)
	if _len == 0 or _len == 1 or _len == 2 or array[0] == None:
		Verbose.EchoError("Error!")
		sys.exit()	
def Get_C_events(page):
	#jsut a debug function
	events = page.find_all("div", {"class": "c-events__item c-events__item_col"})
	CheckForError(events)
	return events
def ValidateDiv(div):
	try:
		check1 = ((((((div.find("div", {"class": "c-events__item c-events__item_game c-events-scoreboard__wrap"})).find("div", {"class": "c-events-scoreboard"})).find("div", {"class": "c-events-scoreboard__item"})).find("a", {"class": "c-events__name"})).find("span", {"class": "c-events__teams"})).find_all("div", {"class": "c-events-scoreboard__team-wrap"})[0]).find("div", {"class": "c-events__team"})
		check2 = ((((((div.find("div", {"class": "c-events__item c-events__item_game c-events-scoreboard__wrap"})).find("div", {"class": "c-events-scoreboard"})).find("div", {"class": "c-events-scoreboard__item"})).find("a", {"class": "c-events__name"})).find("span", {"class": "c-events__teams"})).find_all("div", {"class": "c-events-scoreboard__team-wrap"})[1]).find("div", {"class": "c-events__team"})
		return True
	except:
		return False
def Get_Name_of_Sport(div):
	name1 = ((((((div.find("div", {"class": "c-events__item c-events__item_game c-events-scoreboard__wrap"})).find("div", {"class": "c-events-scoreboard"})).find("div", {"class": "c-events-scoreboard__item"})).find("a", {"class": "c-events__name"})).find("span", {"class": "c-events__teams"})).find_all("div", {"class": "c-events-scoreboard__team-wrap"})[0]).find("div", {"class": "c-events__team"})
	name2 = ((((((div.find("div", {"class": "c-events__item c-events__item_game c-events-scoreboard__wrap"})).find("div", {"class": "c-events-scoreboard"})).find("div", {"class": "c-events-scoreboard__item"})).find("a", {"class": "c-events__name"})).find("span", {"class": "c-events__teams"})).find_all("div", {"class": "c-events-scoreboard__team-wrap"})[1]).find("div", {"class": "c-events__team"})
	return [name1.text, name2.text]

def Get_Coeff(div, coeff):
	bet_coeffs = ((div.find("div", {"class": "c-events__item c-events__item_game c-events-scoreboard__wrap"})).find("div", {"class": "c-bets"})).find_all("a")
	ret = ""
	if coeff == "1":
		ret = bet_coeffs[0].get("data-coef")
	if coeff == "2":
		ret = bet_coeffs[2].get("data-coef")
	if coeff == "1x":
		ret = bet_coeffs[3].get("data-coef")
	if coeff == "2x":
		ret = bet_coeffs[5].get("data-coef")
	if coeff == "x":
		ret = bet_coeffs[1].get("data-coef")
	if coeff == "12":
		ret = bet_coeffs[4].get("data-coef")
	if ret == None:
			return ""
	return ret	

def Get_Sport_Type(div, nes_sports):
		sport_type = (((div.find("div", {"class": "c-events__item c-events__item_game c-events-scoreboard__wrap"})).find("div", {"class": "c-events-scoreboard"})).find("div", {"class": "c-events-scoreboard__item"})).find("a", {"class": "c-events__name"}).get("href")
		for x in nes_sports:
			if x in sport_type:
				sport_type = x
				
		return sport_type
def Get_Event_Link(div):
	event_link = (((div.find("div", {"class": "c-events__item c-events__item_game c-events-scoreboard__wrap"})).find("div", {"class": "c-events-scoreboard"})).find("div", {"class": "c-events-scoreboard__item"})).find("a", {"class": "c-events__name"}).get("href")
	return event_link