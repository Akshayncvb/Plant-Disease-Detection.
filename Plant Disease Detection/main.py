import tkinter as tk
from tkinter import messagebox, filedialog, Label, Button, Entry, Canvas
from PIL import Image, ImageTk
import os
import json

# Import the PlantDiseaseClassifier (Assuming it's implemented elsewhere)
from plant_disease_classifier import PlantDiseaseClassifier

class LoginPage:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Login Page")
        self.root.attributes('-fullscreen', True)  # Set full screen

        # Load Background Image
        self.bg_image = Image.open(r"c:\Users\na504\Downloads\plant.jpg")  # Update with correct path
        self.bg_image = self.bg_image.resize((1920, 1080))  # Resize to full screen resolution
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create Canvas for Background
        self.canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Create Login Form
        self.username_label = Label(root, text="Username:", font=("Arial", 14), bg="lightgreen")
        self.username_entry = Entry(root, font=("Arial", 14))
        self.password_label = Label(root, text="Password:", font=("Arial", 14), bg="lightgreen")
        self.password_entry = Entry(root, font=("Arial", 14), show="*")
        self.login_button = Button(root, text="Login", font=("Arial", 14), command=self.login)
        self.signup_button = Button(root, text="Sign Up", font=("Arial", 14), command=self.sign_up)

        # Place Widgets on Canvas (Centered)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        self.canvas.create_window(screen_width // 2, screen_height // 2 - 80, window=self.username_label)
        self.canvas.create_window(screen_width // 2, screen_height // 2 - 50, window=self.username_entry)
        self.canvas.create_window(screen_width // 2, screen_height // 2 - 10, window=self.password_label)
        self.canvas.create_window(screen_width // 2, screen_height // 2 + 20, window=self.password_entry)
        self.canvas.create_window(screen_width // 2 - 50, screen_height // 2 + 60, window=self.login_button)
        self.canvas.create_window(screen_width // 2 + 50, screen_height // 2 + 60, window=self.signup_button)

        # User data file path
        self.user_data_file = "users.json"
        self.on_login_success = on_login_success

        # Bind Escape key to exit full screen
        self.root.bind("<Escape>", self.exit_fullscreen)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.validate_user(username, password):
            messagebox.showinfo("Login Success", "Welcome!")
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return

        if self.add_user(username, password):
            messagebox.showinfo("Success", "Sign up successful! Please sign in.")
        else:
            messagebox.showerror("Error", "Username already exists.")

    def validate_user(self, username, password):
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, "r") as file:
                users = json.load(file)
            return username in users and users[username] == password
        return False

    def add_user(self, username, password):
        users = {}
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, "r") as file:
                users = json.load(file)

        if username in users:
            return False

        users[username] = password
        with open(self.user_data_file, "w") as file:
            json.dump(users, file)
        return True

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

class PlantDiseaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Disease Detection")
        self.root.attributes('-fullscreen', True)  # Set full screen

        # Instruction Label
        self.image_label = Label(root, text="Upload a Plant Image", font=("Arial", 16))
        self.image_label.pack(pady=20)

        # Upload Button
        self.upload_button = Button(root, text="Upload Image", command=self.upload_image, font=("Arial", 14))
        self.upload_button.pack(pady=10)

        # Image Display
        self.img_display = Label(root)
        self.img_display.pack()

        # Predict Button (Initially Disabled)
        self.predict_button = Button(root, text="Predict", command=self.predict_disease, font=("Arial", 14), state=tk.DISABLED)
        self.predict_button.pack(pady=15)

        # Label to Show Results
        self.result_label = Label(root, text="", font=("Arial", 14), fg="green", wraplength=600, justify="left")
        self.result_label.pack(pady=10)

        self.image_path = None

        # Bind Escape key to exit full screen
        self.root.bind("<Escape>", self.exit_fullscreen)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if self.image_path:
            img = Image.open(self.image_path)
            img = img.resize((300, 300))
            img = ImageTk.PhotoImage(img)
            self.img_display.config(image=img)
            self.img_display.image = img  # Keep reference
            self.predict_button.config(state=tk.NORMAL)

    def predict_disease(self):
        if not self.image_path:
            self.result_label.config(text=r"C:\Users\na504\Downloads\plant.jpg", fg="red")
            return

        classifier = PlantDiseaseClassifier()
        classifier.load_model('plant_disease_model.h5')
        result = classifier.predict(self.image_path)

        confidence = result.get('confidence', 0.0) * 100
        output_text = (
            f"🌱 Plant Type: {result.get('plant_type', 'Unknown')}\n"
            f"🦠 Disease: {result.get('disease', 'Unknown')}\n"
            f"📊 Confidence: {result.get('confidence','.2f')}%\n"
            f"🌿 Health Status: {'✅ Healthy' if result.get('is_healthy', False) else '❌ Diseased'}"
        )

        self.result_label.config(text=output_text, fg="green")
        print(output_text)

    def exit_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', False)

# Function to open main application after login
def on_login_success():
    root.withdraw()
    new_root = tk.Toplevel(root)
    PlantDiseaseGUI(new_root)

if __name__ == "__main__":
    root = tk.Tk()
    LoginPage(root, on_login_success)
    root.mainloop()
