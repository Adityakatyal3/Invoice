# main.py
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import webbrowser
import subprocess

# File to store usernames and passwords (for demonstration purposes)
USER_CREDENTIALS_FILE = "user_credentials.txt"

class LoginPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        self.login_button = Button(text='Login', on_press=self.login)
        self.add_widget(self.username_input)
        self.add_widget(self.password_input)
        self.add_widget(self.login_button)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        # Check if the username and password match
        if self.authenticate(username, password):
            print("Authentication successful. Redirecting to the dashboard.")
            self.launch_dashboard()
        else:
            print("Authentication failed. Please try again.")

    def authenticate(self, username, password):
        # Read saved usernames and passwords from a file (for demonstration)
        try:
            with open(USER_CREDENTIALS_FILE, "r") as file:
                lines = file.readlines()
                for line in lines:
                    saved_username, saved_password = line.strip().split(",")
                    if username == saved_username and password == saved_password:
                        return True
        except FileNotFoundError:
            print("User credentials file not found.")
        return False

    def launch_dashboard(self):
        # Run the dashboard app using subprocess
        subprocess.Popen(["python", "dashboard_app.py"])

class DashboardPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.generate_invoice_button = Button(text='Generate Invoice', on_press=self.generate_invoice)
        self.customer_database_button = Button(text='Customer Database', on_press=self.prompt_for_password)
        self.add_widget(self.generate_invoice_button)
        self.add_widget(self.customer_database_button)

    def generate_invoice(self, instance):
        # Open the Google Sheets URL in the default web browser
        google_sheets_url = "https://docs.google.com/spreadsheets/d/1MrgMhh7sIXk9HN6_bMPT4JIgRcA9Dd-oOhwE4Aa2qd4/edit#gid=605647352"
        webbrowser.open(google_sheets_url)

    def prompt_for_password(self, instance):
        # Create a password input popup
        password_popup = PasswordPopup()
        password_popup.open()

    def open_customer_database(self):
        # Implement navigation or interaction with your SQLite database or Google Sheets here
        google_sheets_url = "https://docs.google.com/spreadsheets/d/1P0l7LFgV4Bm8DV7zYInWYmCL6d1q_xvB7YentPUgEJM/edit#gid=0"
        webbrowser.open(google_sheets_url)

class PasswordPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Enter Password"
        self.password_input = TextInput(hint_text="Password", password=True)
        self.confirm_button = Button(text="Confirm", on_press=self.verify_password)
        self.content = BoxLayout(orientation="vertical")
        self.content.add_widget(self.password_input)
        self.content.add_widget(self.confirm_button)

    def verify_password(self, instance):
        entered_password = self.password_input.text
        correct_password = "12345678"  # Replace with your actual password

        if entered_password == correct_password:
            self.dismiss()  # Close the popup
            App.get_running_app().root.open_customer_database()
        else:
            print("Access denied. Incorrect password.")

class MainApp(App):
    def build(self):
        return LoginPage()

if __name__ == '__main__':
    MainApp().run()
