from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

class Sawyer_Scraper:

    def __init__(self):
        self.home_URL = "https://www.hisawyer.com"
        self.browser = webdriver.Firefox()

    def get_url(self):
        return self.browser.current_url

    def go_to_url(self, target_url):
        self.browser.get(target_url)

    def login(self, username, password):

        self.browser.get(self.home_URL + "/auth/log-in")
        self.email = self.browser.find_element_by_name("email")
        self.email.send_keys(username)
        self.password = self.browser.find_element_by_name("password")
        self.password.send_keys(password)
        self.next = self.browser.find_element_by_class_name("mkt-standalone-MuiButton-label")
        self.next.click()
        time.sleep(5)
        self.browser.get(self.home_URL + "/portal/weekly_calendar")
        self.browser.get(self.home_URL + "/portal/schedules/other")

    def scrape(self, filename):
        self.filename = filename + ".txt"
        self.camp_name = self.browser.find_element_by_xpath("//*[@class='portal-navbar-title-container']").text
        self.html = self.browser.page_source
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.all = self.soup.find_all("div",{"class": "portal-list-content class-summary"})[1]
        self.attendees = self.all.find_all("div",{"class": "portal-list-row"})
        self.attendees.pop(0)
        self.all_parents = []

        for self.item in self.attendees:
            self.parent = self.item.find_all("div", {"class": "portal-list-content"})[1]
            self.parent = self.parent.find("a")
            self.all_parents.append(self.parent.attrs['href'])

        with open(self.filename, 'w') as self.output_file:
            for self.parent in self.all_parents:
                self.browser.get(self.home_URL + self.parent)
                self.name = self.browser.find_element_by_xpath("//*[@class='member-name padding-left-20']").text
                self.output_file.write("Parent Name : " + self.name +  ', ')
                self.phone = self.browser.find_element_by_xpath("//*[contains(text(), 'Phone')]/following-sibling::div").text
                self.output_file.write(self.phone + '\n')
                self.secondary_contact = self.browser.find_element_by_xpath("//*[contains(text(), 'Secondary Contact')]/following-sibling::div").text
                self.output_file.write("Secondary Contact: " + self.secondary_contact + '\n')
                self.emergency_contact_name = self.browser.find_element_by_xpath("//*[contains(text(), 'Emergency Contact Information')]/ancestor::div[@class='row']/following-sibling::div").text
                self.output_file.write("Emergency Contact: " + self.emergency_contact_name + ', ')
                self.emergency_contact_number = self.browser.find_element_by_xpath("//*[contains(text(), 'Emergency Contact Number')]/ancestor::div[@class='row']/following-sibling::div").text
                self.output_file.write(self.emergency_contact_number + ", ")
                self.emergency_contact_relationship = self.browser.find_element_by_xpath("//*[contains(text(), 'Emergency Contact Relationship')]/ancestor::div[@class='row']/following-sibling::div").text
                self.output_file.write(self.emergency_contact_relationship + '\n')
                self.alternative_person = self.browser.find_element_by_xpath("//*[contains(text(), 'Is there anyone else OTHER than the listed parents')]/ancestor::div[@class='row']/following-sibling::div").text
                self.output_file.write("Alternative Pickup: " + self.alternative_person + '\n')
                self.insurance_name = self.browser.find_element_by_xpath("//*[contains(text(), 'Insurance Company Name')]/ancestor::div[@class='row']/following-sibling::div").text
                self.output_file.write("Insurance: " + self.insurance_name + ", ")
                self.insurance_id = self.browser.find_element_by_xpath("//*[contains(text(), 'Policy or Certificate Number')]/ancestor::div[@class='row']/following-sibling::div").text
                self.output_file.write(self.insurance_id + '\n')
                self.hospital = self.browser.find_element_by_xpath("//*[contains(text(), 'Preferred Hospital')]/ancestor::div[@class='row']/following-sibling::div").text
                self.output_file.write("Preferred Hospital : " +  self.hospital + '\n')

        self.browser.get(self.home_URL + "/portal/schedules/other")
        return "success"

    def close(self):
        self.browser.quit()
