#! /usr/bin/python

## Author maallen87@gmail.com 
import time

import sys

import smtplib

import requests

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from email.MIMEMultipart import MIMEMultipart

from email.MIMEText import MIMEText

from selenium.common.exceptions import NoSuchElementException



USER_EMAIL = raw_input("Enter email address used to login to portal: ")

USER_PASSWORD = raw_input("Enter password for portal: ")

NUM_OF_TICKETS_REQUIRED = raw_input("Enter the number of tickets (1-4) required: ")

MATCH_PAGE = raw_input("Enter the web address for the specific match you require tickets: ")

NUM_OF_TICKETS_REQUIRED.strip()



def areTicketsAvailable():

	if "Waiting Room" in driver.title:

		return False

	bodyText = driver.find_element_by_id("main_content_resale_item").text

	if "There are currently no tickets being resold" in bodyText:

		return False

	else:

		return True



def enterPortal():

	while "Waiting Room" in driver.title:

		print "In waiting room, please enter captcha details and enter portal..."

		time.sleep(5)

	print "Entered portal! Monitoring requested page for ", NUM_OF_TICKETS_REQUIRED, " tickets."



def login():

	bodyText = driver.find_element_by_tag_name("body").text

	if "Password" in bodyText:

		elem = driver.find_element_by_name("login")

		elem.send_keys(USER_EMAIL)

		elem = driver.find_element_by_name("password")

		elem.send_keys(USER_PASSWORD)

		elem = driver.find_element_by_id("continue_button")

		elem.click()



def waitForTickets():

	while not areTicketsAvailable():

		driver.refresh()

		if "Waiting Room" in driver.title:

			enterPortal()

		if driver.find_element_by_id("warningTimeoutWRButton").is_displayed():

			driver.find_element_by_id("warningTimeoutWRButton").click()

		if driver.find_element_by_id("ajaxErrorDialog").is_displayed():

			driver.refresh()

		time.sleep(1)



def addTicketsToBasket():

	print "Tickets found!! Attempting to add to basket..."

	for option in driver.find_elements_by_tag_name('option'):

		if option.text == NUM_OF_TICKETS_REQUIRED:

			if option.is_displayed():

				option.click()

				print "Selected ", NUM_OF_TICKETS_REQUIRED," tickets"

				break

	driver.find_element_by_id("book").click()



def areTicketsInBasket():

	try:

		if "added to your shopping basket" in driver.find_element_by_id("added_message_content").text:

			print "Tickets in basket!!"

			return True		

	except NoSuchElementException:

		pass

	return False



def notify():

	print "Sending notifications..."

	r = requests.post(## ENTER IFTTT MAKER WEB POST REQUEST ADDRESS HERE ##)

	print "IFTTT notification sent!"

	fromaddr = << ENTER FROM EMAIL HERE >>

	toaddr = << ENTER TO EMAIL HERE >>

	msg = MIMEMultipart()

	msg['From'] = fromaddr

	msg['To'] = toaddr

	msg['Subject'] = "EURO 2016 tickets in basket"

	 

	body = "Login to EURO 2016 resale platform as tickets are in account for purchase!"

	msg.attach(MIMEText(body, 'plain'))

	 

	server = smtplib.SMTP('smtp.gmail.com', 587)

	server.starttls()

	server.login(fromaddr, << PUT YOUR GMAIL PASSWORD HERE >>)

	text = msg.as_string()

	server.sendmail(fromaddr, toaddr, text)

	server.quit()

	print "Email sent."



def goToMatchPage():

	driver.get(MATCH_PAGE)



def startMonitoring():

	goToMatchPage();

	enterPortal()

	if "UEFA EURO 2016" or "Items selection" in driver.title:

		login()

		waitForTickets()

		addTicketsToBasket()

		if areTicketsInBasket():

			notify()

		else:

			startMonitoring()

	else:

		startMonitoring()



driver = webdriver.Firefox()

startMonitoring()