from tkinter import *
from hi_sawyer_backend import Sawyer_Scraper

scraper_object = Sawyer_Scraper()

class Hi_Saywer:

    def __init__(self, scraper):
        self.scraper = scraper
        self.login_status = False

        self.l1 = Label(window, text = 'Username')
        self.l1.grid(row = 0, column = 0)

        self.l2 = Label(window, text = 'Password')
        self.l2.grid(row = 0, column = 2)

        self.l4 = Label(window, text = 'File Name')
        self.l4.grid(row = 2, column = 0)

        self.b1 = Button(window, text = 'Login', width = 12, command = self.login)
        self.b1.grid(row = 1, column = 0, columnspan = 2)

        self.b2 = Button(window, text = 'Go!', width = 12, command = self.get_data)
        self.b2.grid(row = 3, column = 0, columnspan = 2)

        self.b3 = Button(window, text = 'Exit', width = 12, command = self.stop)
        self.b3.grid(row = 5, column = 0, columnspan = 2)

        self.username = StringVar()
        self.user_field = Entry(window, width = 30, textvariable = self.username)
        self.user_field.grid(row = 0, column = 1)

        self.password = StringVar()
        self.pass_field = Entry(window, width = 30, textvariable = self.password)
        self.pass_field.grid(row = 0, column = 3)

        self.file_name = StringVar()
        self.file_field = Entry(window, width = 30, textvariable = self.file_name)
        self.file_field.grid(row = 2, column = 1)

        self.text_box = Text(window, height = 3, width = 60)
        self.text_box.grid(row = 4, column = 0, columnspan = 4)
        self.text_box.insert(END, "Please enter your username and password for hisawyer.com and click Login")

    def login(self):
        if self.login_status == True:
            self.text_box.delete(1.0, END)
            self.text_box.insert(END, "You are already logged in. Navigate to desired camp page, enter the name of the file you want your data saved under and click GO!")
            return
        self.scraper.login(self.username.get(), self.password.get())
        if self.scraper.get_url() != "https://www.hisawyer.com/portal/schedules/other":
            self.scraper.go_to_url("https://www.hisawyer.com/auth/log-in")
            self.text_box.delete(1.0, END)
            self.text_box.insert(END, "Login Failed Please Try Again")
        else:
            self.login_status = True
            self.text_box.delete(1.0, END)
            self.text_box.insert(END, "Login Complete! Navigate to desired camp page, enter the name of the file you want your data saved under and click GO!")

    def get_data(self):
        if self.login_status == False:
            self.text_box.delete(1.0, END)
            self.text_box.insert(END, "Please Login first")
            return
        complete = self.scraper.scrape(self.file_name.get())
        if complete == "success":
            self.text_box.delete(1.0, END)
            self.text_box.insert(END, "Success! Information saved to " + self.file_name.get())

    def stop(self):
        self.scraper.stop()
        window.destroy()

window = Tk()

window.wm_title("Sawyer")

program_window = Hi_Saywer(scraper_object)

window.mainloop()
