from abc import ABC, abstractmethod  # Define BaseScreen class (Abstract class) for all screens (Concrete classes)
from customtkinter import *  # For GUI (Main)
from tkinter import *  # For GUI
from tkinter import messagebox, filedialog  # Provide dialog boxes.
from PIL import Image  # Image handling
from datetime import datetime, timedelta  # Manage login time and expiration
import os  # File handling
import pickle  # Saving and loading user data persistently
import pygame.mixer as mixer  # Handling audio playback in the music player
import re  # Matching password and password validation
from mutagen.mp3 import MP3  # Extracts metadata (e.g. duration) from MP3 files
import time  # Tracking elapsed time
import random  # Shuffle playback in a music player


# BaseScreen: Abstract base class to ensure consistent structure for all derived screens.
class BaseScreen(ABC):

    # Initializes the shared root window and screen window.
    def __init__(self, root):
        self.root = root  # Shared root window
        self.window = None  # Will be assigned when a screen is created


    @abstractmethod
    def create_widgets(self):
        # Abstract method for creating widgets, implemented by concrete classes.
        pass


    def show(self):
        # Displays the screen and ensures the root window is visible.
        if not self.window:
            self.create_widgets()   # Create widgets if haven't been initialized
        self.window.pack(fill="both", expand=True)  # Make the frame fill the window
        self.root.deiconify()  # Show the root window


    def hide(self):
        # Hides the screen by hiding its frame and the root window.
        if self.window:
            self.window.pack_forget()  # Remove the frame from view
        self.root.withdraw()  # Hide the root window


# Login screen class (inherits from BaseScreen)
class LoginScreen(BaseScreen):
    def __init__(self, root):
        # Initializes the LoginScreen and checks if a user is already logged in.
        super().__init__(root) 
        print("LoginScreen initialized.")
        self.is_logged_in = self.load_login_state()   # Load login state from a file
        self.create_widgets()  # Create the UI elements for the login screen

    def load_login_state(self):
        # Loads the user's login state from a file, if it exists.
        try:
            with open("login_state.pkl", "rb") as file:
                return pickle.load(file)  # Return the saved login state
        except FileNotFoundError:
            return False  # Automatically logging out if the file doesn't exist

    def create_widgets(self):
        print("Creating LoginScreen widgets...")
        self.window = CTkFrame(self.root, fg_color="lightblue")  # The main frame for the login screen
        self.window.pack(fill="both", expand=True)  
        set_appearance_mode("light")  # Set light mode for the UI theme
        self.root.title("Login to Ultra")  # # Set the window title
        self.root.geometry("820x720")  # Set the window size
        self.root.iconbitmap(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\logo.ico")  # Set the application icon (absolute path)
        self.root.resizable(False, False)  # Disable resizing

        
    
        self.logo_image = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\logo.png"),size=(250, 250))  # Load the program logo

        # Load images for password visibility toggle (eye icons)
        self.eye_open = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\eye.png"), size=(20, 20))  # (absolute path)
        self.eye_close = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\eye_closed.png"), size=(20, 20))  # (absolute path)

         # Define custom fonts for labels and entries
        self.label0_font = CTkFont(family="Times New Roman", size=120, weight='bold')
        self.label1_font = CTkFont(family="Times New Roman", size=20, weight='bold')
        self.label2_font = CTkFont(family="Times New Roman", size=16, weight='bold')
        self.entry_font = CTkFont(family="Times New Roman", size=14)

         # Display the logo at the top of the screen
        self.logo_label = CTkLabel(self.window, image=self.logo_image, bg_color='lightblue', text='')
        self.logo_label.place(x=150, y=20)

         # Add heading (program name)
        self.heading_label = CTkLabel(self.window, text="Ultra", fg_color='LightBlue', font=self.label0_font, text_color='Black')
        self.heading_label.place(x=370, y=110)

        # Add input fields for username and password
        self.username_label = CTkLabel(self.window, text="Username", fg_color='LightBlue', font=self.label1_font, text_color='Black', bg_color='LightBlue')
        self.username_label.place(x=380, y=290)
        self.username_entry = CTkEntry(self.window, width=300, corner_radius=20, font=self.entry_font, placeholder_text="Username", bg_color='LightBlue')
        self.username_entry.place(x=275, y=330)

        self.password_label = CTkLabel(self.window, text="Password", fg_color='LightBlue', font=self.label1_font, text_color='Black')
        self.password_label.place(x=380, y=385)
        self.password_entry = CTkEntry(self.window, width=300, height=30, corner_radius=20, font=self.entry_font, placeholder_text="Password", show="*", bg_color='LightBlue')
        self.password_entry.place(x=275, y=425)

        
        self.password_visible = False  # Tracks whether the password is visible
        self.show_password = CTkButton(self.window, text='', image=self.eye_open, fg_color="transparent",width=6, height=1, hover_color="Grey", command= self.toggle_password_visibility, bg_color="white") 
        self.show_password.place(x=545, y=426)


        # Creates "Stay logged in" checkbox that triggers stay logged in state
        self.stay_logged_in_cb = CTkCheckBox(self.window, fg_color="Green", text="Stay logged in", bg_color='LightBlue', font=self.label2_font, corner_radius=8, hover_color="LightGreen")
        self.stay_logged_in_cb.place(x=350, y=480)

        # Creates login button that triggers the login process
        self.login_button = CTkButton(self.window, text="LOG IN", width=250, height=35, corner_radius=20, font=self.label1_font, command=self.login, bg_color='LightBlue', fg_color="RoyalBlue", hover_color="DarkBlue")
        self.login_button.place(x=300, y=535)


       # Creates a clickable label that navigates the user to the reset password screen
        self.forgot_password_label = CTkLabel(self.window, text="Forgot your password?", font=self.label2_font, text_color="blue", cursor="hand2", fg_color='LightBlue')
        self.forgot_password_label.bind("<Button-1>", lambda e: self.open_resetpassword_screen())
        self.forgot_password_label.place(x=345, y=595)


        # Creates a label asking if the user don't have an account yet
        self.DH_account_label = CTkLabel(self.window, text="Don't have an account?", font=self.label2_font, text_color="Black", fg_color='LightBlue')
        self.DH_account_label.place(x=278, y=645)


        # Creates a clickable label that navigates the user to the sign up screen
        self.sign_up_label = CTkLabel(self.window, text="Sign up for Ultra", font=self.label2_font, text_color="Blue", cursor="hand2",fg_color='LightBlue')
        self.sign_up_label.bind("<Button-1>", lambda e: self.open_signup_screen())
        self.sign_up_label.place(x=445, y=645)

        
        # Creates an exit label that allows the user to quit the program
        self.exit_label = CTkLabel(self.window, text="EXIT", font=self.label1_font, cursor="hand2",bg_color='lightblue', text_color='Red')
        self.exit_label.place(x=765, y=5)
        self.exit_label.bind("<Button-1>", lambda e: self.exit_program())


        self.load_login_info()


    
    def exit_program(self):
    
            print("Exiting the program...")  # exit process for debugging.

            with open("login_state.pkl", "wb") as file:  # Saves the state of the "Stay Logged In" checkbox to a file.
                pickle.dump(self.stay_logged_in_cb.get(), file)

            self.root.quit()   # Closes the main application window and exits the program.

    def toggle_password_visibility(self):
        if self.password_visible:
            self.password_entry.configure(show="*")   # covers the password field if currently visible.
            self.show_password.configure(image=self.eye_open)  # Changes the icon to be in hidden mode.
        else:
            self.password_entry.configure(show="")  # Reveals the password field.
            self.show_password.configure(image=self.eye_close)  # Changes the icon to be in visible mode.
        self.password_visible = not self.password_visible  # Toggles the visibility state.


    def login(self):
        username = self.username_entry.get()  # Retrieves the username from the input field.
        password = self.password_entry.get()  # Retrieves the password from the input field.
        users = self.load_user_data()  # Loads saved user data for authentication.

        if username not in users:
            # Displays an error message if the username does not exist in the saved data.
            messagebox.showerror("Login Failed", "Username not found.")
        elif users[username] != password:
            # Displays an error message if the entered password does not match the saved one.
            messagebox.showerror("Login Failed", "Incorrect password.")
        else:
            # Saves login state to a file if login is successful.
            with open("login_state.pkl", "wb") as file:
                pickle.dump({"stay_logged_in":self.stay_logged_in_cb.get(),"username": username}, file)

            if self.stay_logged_in_cb.get():
                # Optionally saves the user's credentials if they choose "Stay Logged In."
                self.save_login_info(username)
            
             # Switches to the Music Player screen, if login session successful
            self.hide()
            MusicPlayerScreen(self.root, stay_logged_in=self.stay_logged_in_cb.get(), username=username).show()


    def authenticate_user(self, username, password):
        users = self.load_user_data()  # Loads all registered users and their passwords.
        return users.get(username) == password  # Returns True if the username exists and the password matches; otherwise, False.

    
    def load_user_data(self): 
        if os.path.exists('user_data.pkl'):
            try:
                with open('user_data.pkl', 'rb') as file:
                    users = pickle.load(file)  # Deserializes user data
                    print("Loaded users:", users)  # Logs loaded data for debugging.
                    if isinstance(users, dict):
                        return users  # Returns user data if it is in the correct format.
                    else:
                        print("Error: User data is not in dictionary format.")
            except (pickle.UnpicklingError, EOFError, Exception) as e:
                # Logs errors during the data loading process.
                print(f"Error loading user data: {e}")
        
        return {}  # Returns an empty dictionary if data is unavailable or invalid.


    def save_login_info(self, username):
        users = self.load_user_data()  # Retrieves existing user data.
        password = self.password_entry.get()  # Retrieves the current password.
        users[username] = password  # Updates or adds the user's credentials to the data.
        
        
        with open('user_data.pkl', 'wb') as file:
            pickle.dump(users, file)  # Saves updated user data.
        
        
        login_time = datetime.now()  # Captures the current time of login.
        with open('login_info.pkl', 'wb') as file:
            pickle.dump((username, login_time), file) # Saves the username and login timestamp for login tracking

        print(f"Saved login info for username: {username}")  # Login operation


    def load_login_info(self):
        try:
            with open("login_state.pkl", "rb") as file:
                stay_logged_in = pickle.load(file)  # Retrieves the "Stay Logged In" state.

            if stay_logged_in:  # Proceeds only if the user activated the stay logged in
                if os.path.exists('login_info.pkl'):
                    with open('login_info.pkl', 'rb') as file:
                        data = pickle.load(file)  # Loads saved login info.
                        print("Loaded login info data:", data)  # Display loaded login data

                        
                        if isinstance(data, tuple) and len(data) == 2:
                            username, login_time = data  # Extracts username and login time.
                            if datetime.now() - login_time < timedelta(days=15):
                                self.username_entry.insert(0, username)
                                return True
                        else:
                            print("Unexpected data format in login_info.pkl:", data)
        except FileNotFoundError:
            pass # Ignores if login state file is not found.

        return False  # Returns False if login state is not valid or absent.


    def open_resetpassword_screen(self):
        self.hide()   # Hides the login screen
        ResetPasswordScreen(self.root).show()  # Initializes and shows the reset password screen.
    
    def open_signup_screen(self):
        self.hide()  # Hides the login screen
        SignUpScreen(self.root).show()  # Initializes and shows the sign up screen.



class ResetPasswordScreen(BaseScreen):
    def __init__(self, root):
        # Initializes the ResetPasswordScreen with the provided root window
        super().__init__(root)  
        print("ResetPasswordScreen initialized.")

    def create_widgets(self):
        # Creates and configures all widgets for the Reset Password screen
        print("Creating ResetPasswordScreen widgets...")


        # Main container for the screen
        self.window = CTkFrame(self.root, fg_color="lightblue")
        self.window.pack(fill="both", expand=True)  # Pack the frame to expand in both directions

        # Set appearance mode and window properties
        set_appearance_mode("light")
        self.root.title("Reset Password")  # Set fixed size for the window
        self.root.geometry("480x420")
        self.root.iconbitmap(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\logo.ico")  # Set the window icon
        self.root.resizable(False, False)  # Make the window non-resizable


        # Load images for eye icons
        self.eye_open = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\eye.png"), size=(20, 20))
        self.eye_close = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\eye_closed.png"), size=(20, 20))


        # Fonts for labels and entries
        self.label1_font = CTkFont(family="Times New Roman", size=20, weight='bold')
        self.entry_font = CTkFont(family="Times New Roman", size=14)
        self.label2_font = CTkFont(family="Times New Roman", size=14, weight='bold')

        # Username label and entry
        self.username_label = CTkLabel(self.window, text="Username", font=self.label1_font, bg_color='LightBlue')
        self.username_label.place(x= 200, y= 15)
        self.username_entry = CTkEntry(self.window, width=300, corner_radius=20, font=self.entry_font, bg_color='LightBlue', placeholder_text="Username")
        self.username_entry.place(x= 95, y= 55)

        # New password label and entry
        self.new_password_label = CTkLabel(self.window, text="New Password", font=self.label1_font, bg_color='LightBlue')
        self.new_password_label.place(x= 180, y= 110)
        self.new_password_entry = CTkEntry(self.window, width=300, height= 30, corner_radius=20, font=self.entry_font, show="*", bg_color='LightBlue', placeholder_text="New Password")
        self.new_password_entry.place(x= 95, y=160)

        # Confirm new password label and entry
        self.confirm_np_label = CTkLabel(self.window, text="Confirm New Password", font=self.label1_font, bg_color='LightBlue')
        self.confirm_np_label.place(x= 140, y= 215)
        self.confirm_np_entry = CTkEntry(self.window, width=300, height= 30, corner_radius=20, font=self.entry_font, show="*", bg_color='LightBlue', placeholder_text="Confirm New Password")
        self.confirm_np_entry.place(x= 95, y= 265)

        # Set initial state for password visibility
        self.password_visible = False

        # Button to toggle visibility for new password
        self.show_password = CTkButton(self.window, text='', image=self.eye_open, fg_color="White", hover_color="lightgray", width=6, height=1, command=self.toggle_new_password_visibility)
        self.show_password.place(x=365, y=161)

        # Button to toggle visibility for confirm new password
        self.show_confirm_password = CTkButton(self.window, text='', image=self.eye_open, fg_color="White", hover_color="lightgray", width=6, height=1, command=self.toggle_confirm_new_password_visibility)
        self.show_confirm_password.place(x=365, y=266)

        # Reset password button
        self.reset_pw_button = CTkButton(self.window, text="RESET PASSWORD", width=250,height=35, corner_radius=20, font=self.label1_font, bg_color='LightBlue', fg_color="RoyalBlue", hover_color="DarkBlue", command=self.reset_password)
        self.reset_pw_button.place(x=120, y=345)
        
        # Label to return to the login screen
        self.return_to_login_label = CTkLabel(self.window, text="Return to Login", font=self.label2_font, cursor="hand2",bg_color='lightblue', text_color='Blue')
        self.return_to_login_label.place(x=8, y=2)
        self.return_to_login_label.bind("<Button-1>", lambda e: self.Return_to_login_screen())

        # Label to exit the program
        self.exit_label = CTkLabel(self.window, text="EXIT", font=self.label2_font, cursor="hand2",bg_color='lightblue', text_color='Red')
        self.exit_label.place(x=440, y=2)
        self.exit_label.bind("<Button-1>", lambda e: self.exit_program())


        
    def exit_program(self):
        # Exits the program
        print("Exiting the program...")
        self.root.quit()

    
    def Return_to_login_screen(self):
        # Navigates back to the Login screen
        print("Return to Login screen...")
        self.hide()
        LoginScreen(self.root).show()



    def toggle_new_password_visibility(self):
        # Toggles the visibility of the new password entry
        if self.password_visible:
            self.new_password_entry.configure(show="*")  # Hide password
            self.show_password.configure(image=self.eye_open)  # Change eye icon to open
        else:
            self.new_password_entry.configure(show="")  # Show password
            self.show_password.configure(image=self.eye_close)  # Change eye icon to closed
        self.password_visible = not self.password_visible
    

    def toggle_confirm_new_password_visibility(self):
        # Toggles the visibility of the confirm new password entry
        if self.password_visible:
            self.confirm_np_entry.configure(show="*")  # Hide password
            self.show_confirm_password.configure(image=self.eye_open)  # Change eye icon to open
        else:
            self.confirm_np_entry.configure(show="")  # Show password
            self.show_confirm_password.configure(image=self.eye_close)  # Change eye icon to closed
        
       
        self.password_visible = not self.password_visible

    
    def is_valid_password(self, password, confirm_password):
        # Validates the entered password based on length, character requirements, and matching confirmation
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
            return False
        if not re.search("[A-Z]", password):
            messagebox.showerror("Error", "Password must contain at least one uppercase letter.")
            return False
        if not re.search("[a-z]", password):
            messagebox.showerror("Error", "Password must contain at least one lowercase letter.")
            return False
        if not re.search("[0-9]", password):
            messagebox.showerror("Error", "Password must contain at least one number.")
            return False
        if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            messagebox.showerror("Error", "Password must contain at least one special character.")
            return False
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return False
        return True
    

    def reset_password(self):
        # Handles the logic for resetting the password
        username = self.username_entry.get()
        new_password = self.new_password_entry.get()
        confirm_np = self.confirm_np_entry.get()
        users = self.load_user_data()
        
        if not self.is_valid_password(new_password, confirm_np):
            return  # If the password is invalid, it will return nothing
    
        if username in users:
            # Update the password if the username exists
            users[username] = new_password
            self.save_user_data(users)  # Save updated user data
            messagebox.showinfo("Success", "Password reset successfully.")
            self.hide()  # Hide the current screen
            LoginScreen(self.root).show()  # Show the login screen
        else:
            messagebox.showerror("Error", "Username not found.")  # Show error if username doesn't exist

    def load_user_data(self):
        # Loads user data from the pickle file
        if os.path.exists('user_data.pkl'):
            with open('user_data.pkl', 'rb') as file:
                return pickle.load(file)  # Return the loaded user data
        return {}  # Return an empty dictionary if the file doesn't exist

    def save_user_data(self, users):
        # Saves the updated user data to the pickle file
        with open('user_data.pkl', 'wb') as file:
            pickle.dump(users, file)  # Save the user data




class SignUpScreen(BaseScreen):
    # Inherits from BaseScreen to create the sign-up screen
    def __init__(self, root):
        super().__init__(root)  
        print("SignUpScreen initialized.")
        # Calls the parent class and prints a message

    def create_widgets(self):
        print("Creating SignUpScreen widgets...")
        # Creates the widgets for the sign-up screen
        self.window = CTkFrame(self.root, fg_color="LightYellow")
        self.window.pack(fill="both", expand=True)
        # Creates a frame for the screen with a light yellow background and fills the window 
        set_appearance_mode("light")
        # Sets the appearance mode to light
        self.root.title("Sign up to Ultra")
        self.root.geometry("820x740")
        self.root.iconbitmap(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\logo.ico")
        self.root.config(bg="lightBlue")
        self.root.resizable(False, False)
        # Sets the window title, size, icon, background color, and prevents resizing

       
    
        self.logo_image = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\logo.png"),size=(250, 250))
        self.eye_open = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\eye.png"), size=(20, 20))
        self.eye_close = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\eye_closed.png"), size=(20, 20))
        # Loads images for the logo and eye icons used for password visibility toggling


        self.label0_font = CTkFont(family="Times New Roman", size=120, weight='bold')
        self.label1_font = CTkFont(family="Times New Roman", size=20, weight='bold')
        self.label2_font = CTkFont(family="Times New Roman", size=16, weight='bold')
        self.entry_font = CTkFont(family="Times New Roman", size=14)
        # Defines different font styles for the labels and entry fields


        self.logo_label = CTkLabel(self.window, image=self.logo_image, fg_color='LightYellow', text='')
        self.logo_label.place(x=170, y=20)
        # Places the logo image at the top of the screen

        
        self.heading_label = CTkLabel(self.window, text="Ultra", fg_color='LightYellow', font=self.label0_font, text_color='Black')
        self.heading_label.place(x=370, y=110)
        # Adds the heading "Ultra" in a large, bold font

        
        self.username_label = CTkLabel(self.window, text="Username", fg_color='LightYellow', font=self.label1_font, text_color='Black')
        self.username_label.place(x=380, y=290)
        self.username_entry = CTkEntry(self.window, width=300, corner_radius=20, font=self.entry_font, placeholder_text="Username", bg_color='LightYellow')
        self.username_entry.place(x=275, y=330)
        # Creates a label and text entry for the username
        
        
        self.password_label = CTkLabel(self.window, text="Password", fg_color='LightYellow', font=self.label1_font, text_color='Black')
        self.password_label.place(x=380, y=385)
        self.password_entry = CTkEntry(self.window, width=300, height= 30, corner_radius=20, font=self.entry_font, placeholder_text="Password", show="*", bg_color='LightYellow')
        self.password_entry.place(x=275, y=425)
        # Creates a label and text entry for the password, with hidden characters for security
        
        self.confirm_password_label = CTkLabel(self.window, text="Confirm Password", fg_color='LightYellow', font=self.label1_font, text_color='Black')
        self.confirm_password_label.place(x=345, y=480)
        self.confirm_password_entry = CTkEntry(self.window, width=300, height=30, corner_radius=20, font=self.entry_font, placeholder_text="Confirm Password", show="*", bg_color='LightYellow')
        self.confirm_password_entry.place(x=275, y=520)
        


        self.password_visible = False
        self.show_password = CTkButton(self.window, text='', image=self.eye_open, fg_color="White", hover_color="lightgray", width=6, height=1, command=self.toggle_password_visibility,bg_color='White')
        self.show_password.place(x=545, y=426)
        # Adds a button to toggle the visibility of the password field, using an eye icon

        self.show_confirm_password = CTkButton(self.window, text='', image=self.eye_open, fg_color="White", hover_color="lightgray", width=6, height=1, command=self.toggle_confirm_password_visibility,bg_color='White')
        self.show_confirm_password.place(x=545, y=521)
        # Adds a button to toggle the visibility of the confirm password field, using an eye icon
       

        self.sign_up_button = CTkButton(self.window, text="SIGN UP", width=250, height=35, corner_radius=20, font=self.label1_font, command=self.signup, bg_color='LightYellow',fg_color='Gold', text_color='Black', hover_color="Yellow")
        self.sign_up_button.place(x=300, y=600)
        # Creates a sign-up button that triggers the sign-up process


        self.already_account_label = CTkLabel(self.window, text="Already have an account?", font=self.label2_font, text_color="Black", fg_color='LightYellow')
        self.already_account_label.place(x=295, y=670)
        # Creates a label asking if the user already has an account


        self.login_here_label = CTkLabel(self.window, text="Log in here", font=self.label2_font, text_color="Orange", cursor="hand2", fg_color='LightYellow')
        self.login_here_label.place(x=470, y=670)
        self.login_here_label.bind("<Button-1>", lambda e: self.open_login_screen())
        # Creates a clickable label that navigates the user to the login screen


        self.exit_label = CTkLabel(self.window, text="EXIT", font=self.label1_font, cursor="hand2",bg_color='lightyellow', text_color='Red')
        self.exit_label.place(x=765, y=5)
        self.exit_label.bind("<Button-1>", lambda e: self.exit_program())
         # Creates an exit label that allows the user to quit the program

    
    
    def exit_program(self):
        print("Exiting the program...")
        self.root.quit()
        # Exits the program when the exit label is clicked


    def open_login_screen(self):
        print("Return to Login screen...")
        self.hide()
        LoginScreen(self.root).show()
        # Hides the sign-up screen and shows the login screen

    
    def is_valid_password(self, password, confirm_password):
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
            return False
        if not re.search("[A-Z]", password):
            messagebox.showerror("Error", "Password must contain at least one uppercase letter.")
            return False
        if not re.search("[a-z]", password):
            messagebox.showerror("Error", "Password must contain at least one lowercase letter.")
            return False
        if not re.search("[0-9]", password):
            messagebox.showerror("Error", "Password must contain at least one number.")
            return False
        if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            messagebox.showerror("Error", "Password must contain at least one special character.")
            return False
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return False
        return True
        # Validates that the password is strong (contains upper and lowercase letters, numbers, special characters, etc.)


    def toggle_password_visibility(self):
        if self.password_visible:
            self.password_entry.configure(show="*")
            self.show_password.configure(image=self.eye_open)
        else:
            self.password_entry.configure(show="")
            self.show_password.configure(image=self.eye_close)
        self.password_visible = not self.password_visible
        # Toggles the visibility of the password field (show or hide password)


    def toggle_confirm_password_visibility(self):
       
        if self.password_visible:
            self.confirm_password_entry.configure(show="*")
            self.show_confirm_password.configure(image=self.eye_open)
        else:
            self.confirm_password_entry.configure(show="")
            self.show_confirm_password.configure(image=self.eye_close)
        
        
        self.password_visible = not self.password_visible
        # Toggles the visibility of the confirm password field (show or hide password)


    def load_user_data(self):
        if os.path.exists('user_data.pkl'):
            with open('user_data.pkl', 'rb') as file:
                return pickle.load(file)
        return {}
        # Loads the user data from a file if it exists, otherwise returns an empty dictionary


    def save_user_data(self, users):
        with open('user_data.pkl', 'wb') as file:
            pickle.dump(users, file)
        # Saves the user data to a file using pickle


    def signup(self):
        # Retrieves the input values from the username, password, and confirm password entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        
        # Loads the existing user data from the file
        users = self.load_user_data()


        # Checks if the password is valid and if the password and confirm password match
        if not self.is_valid_password(password, confirm_password):
            return
            # If the password is invalid, the function exits without further processing
        

        # Checks if the username already exists in the user data
        if username in users:
            # If the username already exists, show an error message
            messagebox.showerror("Error", "Username already exists.")
        else:
            # If the username is new, adds the username and password to the user data
            users[username] = password

            # Saves the updated user data back to the file
            self.save_user_data(users)
            messagebox.showinfo("Success", "Registration successful.")

            # When Registration successful, it will navigate back to login screen
            self.hide()
            LoginScreen(self.root).show()
            



class MusicPlayerScreen(BaseScreen):
    def __init__(self, root, stay_logged_in=False, username="User"):
        # Initialize the music player screen with optional stay_logged_in and username parameters
        super().__init__(root)  
        mixer.init()  # Initialize the mixer (used for audio playback)
        self.stay_logged_in = stay_logged_in
        print("MusicPlayerScreen initialized with username: {username}")
        self.username = username
        self.create_widgets()  # Call method to create UI elements

    def create_widgets(self):
        # method UI components for the music player screen
        print("Creating MusicPlayerScreen widgets...")
        self.window = CTkFrame(self.root, fg_color="LightBlue")  # Create main window frame
        self.window.pack(fill="both", expand=True)  # Pack window to expand in both directions
        set_appearance_mode("light")  # Set light appearance mode for the UI
        self.root.title("Ultra")  # Set window title
        self.root.geometry("750x770")  # Set window dimensions
        self.root.iconbitmap(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\logo.ico")  # Set window icon
        self.root.resizable(False, False)   # Disable resizing of the window


        # Load images for buttons (previous, play, pause, next, shuffle, volume, user icon)
        self.prev_image = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\prev.png"),size=(40, 40))
        self.play_image = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\play.png"), size=(50, 50))
        self.pause_image = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\pause.png"), size=(50, 50))
        self.next_image = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\next.png"), size=(40, 40))
        self.shuffle_image = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\shuffle.png"),size=(65, 65))
        self.volume_image = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\volume.png"), size=(40, 40))
        self.user_icon = CTkImage(light_image=Image.open(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj\imgs\user_icon.png"), size=(40, 40))


        # Define fonts for various labels
        self.label1_font = CTkFont(family="Times New Roman", size=20, weight= 'bold')
        self.label2_font = CTkFont(family="Times New Roman", size=16, weight= 'bold')
        self.song_font = CTkFont(family="Times New Roman", size=14)


        # Create and position UI components such as labels and buttons
        self.user_icon_label = CTkLabel(self.window, image=self.user_icon, text="", bg_color="LightBlue")
        self.user_icon_label.place(x=10, y=10)  # Place user icon label at specified position
        self.username_label = CTkLabel(self.window, text=f"{self.username}", font=self.label1_font, text_color="black", bg_color="lightBlue")
        self.username_label.place(x=55, y=18)  # Display username label


        # Create logout label and bind click event to logout method
        self.logout_label = CTkLabel(root, text="LOG OUT", font=self.label2_font, cursor="hand2", bg_color='lightblue', text_color='Red')
        self.logout_label.place(x=15, y=65)
        self.logout_label.bind("<Button-1>", lambda e: self.logout())


        # Create exit label and bind click event to exit method
        self.exit_label = CTkLabel(self.window, text="EXIT", font=self.label1_font, cursor="hand2",bg_color='lightblue', text_color='Red')
        self.exit_label.place(x=695, y=15)
        self.exit_label.bind("<Button-1>", lambda e: self.exit_program())


        # Song and status labels
        self.song_name = StringVar(value="< No song selected >")
        self.song_status = StringVar(value="< Status >")
        self.current_index =IntVar()


        self.song_name_label = CTkLabel(root, textvariable=self.song_name, font=self.label1_font, anchor="center", text_color='Black', bg_color='LightBlue')
        self.song_name_label.place(x= 275, y= 75)

        self.status_label = CTkLabel(root, textvariable=self.song_status, font=self.label2_font, text_color="Black", bg_color='LightBlue')
        self.status_label.place(x= 345, y= 125)


        # Duration labels and seek bar to control song position
        self.duration_label = CTkLabel(root, text="00:00", font=self.label2_font, text_color="Black", bg_color='LightBlue')
        self.duration_label.place(x=85, y=170)

        
        self.seek_bar = CTkSlider(root, from_=0, to=100, number_of_steps=1000, command=self.on_seek_bar_change, width=500, button_hover_color= "DarkBlue", bg_color="LightBlue")
        self.seek_bar.place(x= 126, y= 176)

        
        self.duration_frame = CTkLabel(root, text="00:00", font=self.label2_font, text_color="Black", bg_color='LightBlue')
        self.duration_frame.place(x= 630, y= 170)

        self.seek_bar.bind("<ButtonRelease-1>", lambda e: self.on_seek_bar_release(self.seek_bar.get()))


         # Playlist frame with listbox and load button
        self.playlist_frame = CTkFrame(root, width=600, height=300, corner_radius=15, bg_color="lightBlue")
        self.playlist_frame.pack(pady=10)
        self.playlist_frame.place(x=140, y=380)
        self.playlist_listbox = Listbox(self.playlist_frame, width=60, height=15, font=self.song_font, bg='RoyalBlue', fg='white', selectbackground='#4169E1', highlightthickness=0)
        self.playlist_listbox.pack(padx=30, pady=10)
        self.load_btn = CTkButton(self.playlist_frame, text="Load Songs", font= self.label2_font, fg_color= "RoyalBlue", hover_color="DarkBlue", corner_radius=20, command=lambda: self.load(self.playlist_listbox))
        self.load_btn.pack(side="bottom", pady=10)


        # Buttons for navigation (previous, play/pause, next, shuffle) and volume control
        self.prev_btn = CTkLabel(root, text="", image=self.prev_image, fg_color="lightblue")
        self.prev_btn.place(x= 260, y= 220)
        self.prev_btn.bind("<Button-1>", lambda e: self.previous_song(self.playlist_listbox, self.current_index))
        self.play_pause_btn = CTkLabel(root, text="", image= self.play_image, fg_color="lightblue")
        self.play_pause_btn.place(x= 310, y= 215)
        self.play_pause_btn.bind("<Button-1>", lambda e: self.toggle_play_pause(self.song_status, self.playlist_listbox, self.current_index))
        self.next_btn = CTkLabel(root, text="", image= self.next_image, fg_color="lightblue")
        self.next_btn.place(x= 380, y= 220)
        self.next_btn.bind("<Button-1>", lambda e: self.next_song(self.playlist_listbox, self.current_index))
        self.shuffle_btn = CTkLabel(root, image=self.shuffle_image, text="", fg_color="lightblue")
        self.shuffle_btn.place(x= 435, y= 208)
        self.shuffle_btn.bind("<Button-1>", lambda e: self.shuffle_playlist(self.playlist_listbox))


        # Volume control slider and label
        self.volume_label = CTkLabel(root, text="", image=self.volume_image, fg_color="lightblue")
        self.volume_label.place(x= 255, y= 300)
        self.volume_slider = CTkSlider(root, from_=0, to=100, number_of_steps=100, button_hover_color= "DarkBlue", bg_color="LightBlue", command=self.volume)
        self.volume_slider.set(50)
        self.volume_slider.place(x= 300, y= 313)


        # Initialize playback state variables
        self.elapsed_time = 0
        self.song_duration = 0
        self.is_paused = False
        self.paused_time = 0
        self.last_update_time = 0
        self.is_seeking = False  
        self.is_playing = False

   
            
    def exit_program(self):
        # Method to exit the program
        print("Exiting the program...")
        

        # Save login state to pickle file
        with open("login_state.pkl", "wb") as file:
            pickle.dump({"stay_logged_in": self.stay_logged_in, "username": self.username}, file)

        self.root.quit()


    def logout(self):
        """Logout and return to the login screen."""
        print("Logging out...")     # Print a message indicating the logout process has started.
        
        try:
            # Attempt to open the login state file in write-binary mode to save the new login state.
            with open(login_state_path, "wb") as file:
                # Serialize and save the login state, setting "stay_logged_in" to False and storing the current username.
                pickle.dump({"stay_logged_in": False, "username": self.username}, file)
        except Exception as e:
            print(f"Error resetting login state: {e}")
        

        # Check if the file "login_info.pkl" exists in the file system.
        if os.path.exists("login_info.pkl"):
            # If the file exists, remove it to clear any stored session information
            os.remove("login_info.pkl")


        self.hide()  # Hide current screen after logging out
        LoginScreen(self.root).show()  # Show the login screen


    def toggle_play_pause(self, status, song_list, current_index):
         # Toggle between play and pause
        try:
            if self.is_playing:
                self.pause_song(status)  # Pause song if playing
                self.play_pause_btn.configure(image=self.play_image)  
            else:
                if self.is_paused:
                    self.resume_song(status, song_list, current_index)  # Resume song if paused
                else:
                    self.play_song(song_list, status, current_index)  # Play song if not paused
                self.play_pause_btn.configure(image=self.pause_image)  # Toggle playing state
        except Exception as e:
            self.show_error(f"Error toggling play/pause: {str(e)}")


    # Method to play a song from the playlist
    def play_song(self, song_list, status, current_index):
        try:
             # Reset elapsed and paused time if the song is not paused
            if not self.is_paused:
                self.elapsed_time = 0
                self.paused_time = 0


            # Get the name of the song to be played
            song_name = song_list.get(current_index.get())


            # Check if the song directory is set, otherwise ask the user to select a directory
            if not hasattr(self, 'song_directory') or not self.song_directory:
                directory = filedialog.askdirectory(title="Select song directory")
                self.song_directory = directory  # Save the selected directory
            else:
                directory = self.song_directory  # Use the existing directory

            # Combine the directory and song name to get the full path of the song
            full_path = os.path.join(directory, song_name) 


            # Print the selected song's full path for debugging
            print(f"Selected song: {full_path}")  


            # Check if the song file exists, otherwise show an error message
            if not os.path.isfile(full_path):
                self.show_error(f"Song file not found: {full_path}")
                return

            # Get the song name without extension and shorten if it's too long
            name_without_extension = os.path.splitext(song_name)[0]
            truncated_name = truncate_song_name(name_without_extension)
            self.song_name.set(truncated_name)  # Update the song name in the UI

            
            # Stop any currently playing song and load the new one
            mixer.music.stop()
            mixer.music.load(full_path)
            mixer.music.play(start=self.paused_time)

            
            # Get the song's duration
            self.song_duration = get_song_duration(full_path)


            # Update the status to "Playing..."
            status.set("Playing...")
            self.last_update_time = time.time()   # Store the time when the song starts playing
            self.is_playing = True
            self.is_paused = False

            
            # Update the play/pause button and seek bar UI
            self.play_pause_btn.configure(image=self.pause_image)
            self.seek_bar.set(0)
            self.seek_bar.configure(to=self.song_duration)
            self.duration_frame.configure(text=f"{time.strftime('%M:%S', time.gmtime(self.song_duration))}")

            
            # Start updating the song's playback tim
            self.play_time(status, song_list, current_index)

        except Exception as e:
            # Handle any errors that occur while playing the song
            self.show_error(f"Error playing song: {str(e)}")


    # Method to pause the currently playing song
    def pause_song(self, status):
        try:
            # If a song is currently playing, pause it
            if self.is_playing:
                mixer.music.pause()
                self.is_paused = True
                self.paused_time = self.elapsed_time  # Save the time when the song was paused
                status.set("Paused")  # Update the status to "Paused"
                self.play_pause_btn.configure(image=self.play_image)  # Change button to play image
                self.is_playing = False
            else:
                # If the song is already paused, resume it
                self.resume_song(status)
        except Exception as e:
            # Handle any errors that occur while pausing the song
            self.show_error(f"Error pausing song: {str(e)}")


    # Method to resume a paused song
    def resume_song(self, status, song_list, current_index):
        try:
            # If the song is paused, resume playback from the paused time
            if self.is_paused:
                song_name = song_list.get(current_index.get())
                directory = self.song_directory  # Use the stored song directory
                full_path = os.path.join(directory, song_name)  # Get full path of the song


                 # Check if the song file exists, otherwise show an error message
                if not os.path.isfile(full_path):
                    self.show_error(f"Song file not found: {full_path}")
                    return


                # Reload and resume the song from the paused time
                mixer.music.load(full_path)
                mixer.music.play(start=self.paused_time)
                status.set("Playing...")
                self.is_paused = False
                self.last_update_time = time.time()  # Update the last update time
                self.play_time(status, song_list, current_index)  # Continue tracking playback time
                self.play_pause_btn.configure(image=self.pause_image)  # Change button to pause image
                self.is_playing = True
        except Exception as e:
            # Handle any errors that occur while resuming the song
            self.show_error(f"Error resuming song: {str(e)}")


    # Method to load songs from a selected directory into the playlist
    def load(self, listbox):
        try:
            # Ask the user to select a directory containing songs
            directory = filedialog.askdirectory(title="Open a song Directory")
            if directory:
                tracks = os.listdir(directory)  # List all files in the selected directory
                listbox.delete(0, "end")  # Clear the playlist


                # Loop through all files and add .mp3 files to the playlist
                for track in tracks:
                    if track.endswith('.mp3'):
                        song_path = os.path.join(directory, track)
                        
                        song_name = os.path.basename(song_path)  # Get the song's name 
                        listbox.insert("end", song_name)  # Add song to the playlist
                        
                print(f"Loaded songs from: {directory}")
            else:
                print("No directory selected.")  # If no directory is selected, print message
        except Exception as e:
            # Handle any errors that occur while loading songs
            self.show_error(f"Error loading songs: {str(e)}")


    # Method to adjust the volume of the song based on the slider value
    def volume(self, x):
        self.value =self.volume_slider.get()  # Get the current slider value
        mixer.music.set_volume(self.value / 100)  # Set the volume (range 0 to 1)


    # Method to track and display the current playback time of the song
    def play_time(self, status, song_list, current_index):
        if self.is_paused or self.is_seeking:
            return  # Do nothing if the song is paused or the user is seeking
        

        # Get the current playback time from the mixer
        current_time = mixer.music.get_pos() / 1000
        self.elapsed_time = self.paused_time + current_time

        # Format and display the current time and song duration
        formatted_time = time.strftime('%M:%S', time.gmtime(self.elapsed_time))
        formatted_duration = time.strftime('%M:%S', time.gmtime(self.song_duration))
        self.duration_label.configure(text=f"{formatted_time}")
        self.duration_frame.configure(text=f"{formatted_duration}")
        self.seek_bar.set(self.elapsed_time)

        
        # If the song is finished, update the status and play the next song
        if self.elapsed_time >= self.song_duration - 1:
            status.set("Finished!")
            self.next_song(song_list, current_index)
            return


         # Continue updating the playback time every second
        self.root.after(1000, self.play_time, status, song_list, current_index)


    # Method to shuffle the playlist and start playing from the first song
    def shuffle_playlist(self,playlist):
        shuffled = list(playlist.get(0, "end"))  # Get all songs from the playlist
        random.shuffle(shuffled)  # Shuffle the songs
        playlist.delete(0, "end")  # Clear the playlist
        for song in shuffled:
            playlist.insert("end", song)  # Insert shuffled songs back into the playlist

        playlist.select_clear(0, "end")
        playlist.select_set(0)  # Select the first song
        self.current_index.set(0)  # Update the current song index
        
        self.play_song(playlist, self.song_status, self.current_index)  # Start playing


    # Method to play the next song in the playlist
    def next_song(self, playlist, current_index):
        mixer.music.stop()  # Stop the current song
        self.elapsed_time = 0
        self.paused_time = 0
        self.is_playing = False


        # Move to the next song (loop back to the first song if at the end)
        next_index = (current_index.get() + 1) % playlist.size()
        playlist.select_clear(0, "end")
        playlist.select_set(next_index)
        current_index.set(next_index)
        
       
        self.seek_bar.set(0)  # Reset the seek bar
        
        self.play_song(playlist, self.song_status, current_index)  # Play the next song


    # Method to play the previous song in the playlist
    def previous_song(self, playlist, current_index):
        mixer.music.stop()  # Stop the current song
        self.elapsed_time = 0
        self.paused_time = 0
        self.is_playing = False


        # Move to the previous song (loop back to the last song if at the start)
        prev_index = (current_index.get() - 1) % playlist.size()
        playlist.select_clear(0, "end")
        playlist.select_set(prev_index)
        current_index.set(prev_index)

        
        self.seek_bar.set(0)  # Reset the seek bar
        
        self.play_song(playlist, self.song_status, current_index)  # Play the previous song


    # Method to handle changes in the seek bar value (when user drags the seek bar)
    def on_seek_bar_change(self, value):
        self.is_seeking = True  # Mark that the user is seeking (adjusting playback time)

        self.elapsed_time = value  # Set the current elapsed time to the new seek bar value
        formatted_time = time.strftime('%M:%S', time.gmtime(self.elapsed_time))  # Format the time into minutes:seconds
        self.duration_label.configure(text=f"{formatted_time}")  # Update the displayed time
        self.seek_bar.set(self.elapsed_time)  # Update the seek bar position


    # Method to handle when the user releases the seek bar (finishes seeking).
    def on_seek_bar_release(self, value):
        self.paused_time = value  # Set the paused time to the current seek bar position
        self.elapsed_time = self.paused_time  # Update the elapsed time to reflect the seek position
        mixer.music.play(start=self.paused_time)  # Play the song from the new position
        
        self.last_update_time = time.time()  # Store the current time for time calculations
        self.is_seeking = False   # Mark that the seeking process has ended
        

        # If the song was paused, resume playback.
        if self.is_paused:
            mixer.music.pause()  # Pause the music (in case the user was not playing)
            self.is_playing = False   # Show that the song is not playing
        else:
            self.play_time(self.song_status, self.playlist_listbox, self.current_index)  # Continue tracking playback time

    
    # Method to display error messages in a pop-up window.
    def show_error(self, message):
        error_window = Toplevel(self.root)  # Create a new window for the error message
        error_window.title("Error")  # Set the window title
        error_label = Label(error_window, text=message, fg="red")  # Display the error message in red
        error_label.pack(padx=20, pady=20)  # Add padding around the label
        ok_button = Button(error_window, text="OK", command=error_window.destroy)  # Button to close the error
        ok_button.pack(pady=5)  # Add padding around the button


# Set the working directory to the specified project path.
os.chdir(r"C:\Users\adiso\OneDrive\Documents\Coding\Python\Proj")
script_dir = os.path.dirname(__file__)  # Get the current directory
login_state_path = os.path.join(script_dir, "login_state.pkl")  # Define the path for login state file


# Function to load login state (whether the user should stay logged in).
def load_login_state():
    try:
        print(f"Loading login state from: {login_state_path}")  # Print the login state file path
        if os.path.exists(login_state_path):  # Check if the login state file exists
            with open(login_state_path, "rb") as file:  # Open the file in binary read mode
                login_state = pickle.load(file)  # Load the login state object

            print(f"Loaded login state: {login_state}")  # Print the loaded login state


            # Validate if the loaded login state is a dictionary.
            if isinstance(login_state, dict):
                stay_logged_in = login_state.get("stay_logged_in", False)  # Get the 'stay_logged_in' status (False)
                username = login_state.get("username", "User")  # Get the username as "User"
            else:
                raise ValueError("Invalid login state format")  # Raise an error if the format is invalid
            
            return stay_logged_in, username   # Return the login state information
        else:
            print("login_state.pkl not found, returning defaults.")  # If file not found, return default values
           
            stay_logged_in = False  # Default to not staying logged in
            username = "User"  # Default username
            save_login_state(stay_logged_in, username)  # Save the default login state
            return stay_logged_in, username

    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading login state: {e}")  # Print any errors that occur while loading the state
        stay_logged_in = False  # Default to not staying logged in
        username = "User"  # Default username
        save_login_state(stay_logged_in, username)  # Save the default login state
        return stay_logged_in, username


# Function to save the login state to a file.
def save_login_state(stay_logged_in, username):
    try:
        with open(login_state_path, "wb") as file:  # Open the file in binary write mode
            pickle.dump({"stay_logged_in": stay_logged_in, "username": username}, file)  # Save the login state
    except Exception as e:
        print(f"Error saving login state: {e}")  # Print any errors while saving the state


# Function to load songs from a selected directory.
def load_songs_from_directory():
    try:
        directory = filedialog.askdirectory(title="Open a song Directory")  # Ask the user to select a directory
        if directory:
            directory = os.path.abspath(directory)   # Convert the directory path to an absolute path
            print(f"Loading songs from: {directory}")  # Print the directory being loaded

            tracks = os.listdir(directory)  # List all files in the directory
            for track in tracks:  # Loop through each track in the directory
                if track.endswith('.mp3'):  # Only load mp3 files
                    song_path = os.path.join(directory, track)  # Construct the full song path
                    print(f"Loaded song: {song_path}")  # Print the loaded song path
    except Exception as e:
        print(f"Error loading songs: {e}")  # Print any errors that occur during song loading


# Function to truncate long song names to a specified maximum length.
def truncate_song_name(song_name, max_length=25):

    if len(song_name) > max_length:
        return song_name[:max_length] + "..."  # Shorten the name and add "..." if it's too long
    return song_name  # Return the original name if it's within the limit


# Function to get the duration of an mp3 file.
def get_song_duration(file_path):
    audio = MP3(file_path)  # Open the mp3 file using the MP3 class
    return audio.info.length  # Return the duration of the song in seconds


# Main entry for running the program
if __name__ == "__main__":
    root = CTk()  # Create the main program window
    stay_logged_in, username = load_login_state()  # Load the login state

    if stay_logged_in:  # Check if the user wants to stay logged in
        MusicPlayerScreen(root, stay_logged_in=True, username=username).show()  # Show the music player screen
    else:
        LoginScreen(root).show()  # Otherwise, show the login screen (if the there no stay logged in activated)
    
    root.mainloop()  # Start the CustomTkinter main loop to run the program
