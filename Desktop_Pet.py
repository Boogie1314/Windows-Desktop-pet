import tkinter as tk
from tkinter import Menu
import subprocess
import webbrowser
import platform
import sys
import os

class DesktopPet:
    def __init__(self):
        self.window = tk.Tk()
        
        # Remove window decorations
        self.window.overrideredirect(True)
        
        # Make window stay on top (works better on macOS)
        self.window.attributes('-topmost', True)
        
        # For macOS - use alpha transparency instead of color keying
        if platform.system() == 'Darwin':
            # This gives actual transparency on macOS
            self.window.wm_attributes('-alpha', 0.95)
            # Use a transparent background for canvas
            self.canvas = tk.Canvas(self.window, width=120, height=120, 
                                   bg='systemTransparent', highlightthickness=0)
        else:
            self.canvas = tk.Canvas(self.window, width=120, height=120, 
                                   bg='white', highlightthickness=0)
            self.window.wm_attributes('-transparentcolor', 'white')
        
        self.canvas.pack()
        
        # Window properties
        self.window.geometry("120x120+500+400")
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        
        self.pet_type = 'blob'
        self.dx = 3
        self.dy = 3
        self.moving = False
        
        # Speech bubble
        self.bubble_bg = None
        self.bubble_text = None
        self.bubble_message = None
        
        self.draw_pet()
        
        # Menu setup
        self.menu = Menu(self.window, tearoff=False)
        self.build_menu()
        
        # Bind mouse events
        self.canvas.bind("<Button-3>", self.show_menu)
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        
        # Start animation
        self.animate()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.close_pet)
        
        self.window.mainloop()
    
    def draw_pet(self):
        self.canvas.delete("all")
        
        if self.pet_type == 'blob':
            self.canvas.create_oval(20, 20, 100, 100, fill='lightblue', outline='darkblue', width=2)
            self.canvas.create_oval(45, 45, 55, 55, fill='black')
            self.canvas.create_oval(65, 45, 75, 55, fill='black')
            self.canvas.create_arc(50, 65, 70, 80, start=0, extent=-180, style=tk.ARC, width=2)
        elif self.pet_type == 'dog':
            self.canvas.create_oval(25, 35, 95, 95, fill='#D2A679', outline='#8B5A2B', width=2)
            self.canvas.create_oval(30, 20, 55, 50, fill='#D2A679', outline='#8B5A2B', width=2)
            self.canvas.create_oval(65, 20, 90, 50, fill='#D2A679', outline='#8B5A2B', width=2)
            self.canvas.create_oval(45, 50, 55, 60, fill='black')
            self.canvas.create_oval(65, 50, 75, 60, fill='black')
            self.canvas.create_oval(52, 70, 68, 78, fill='black')
            self.canvas.create_arc(55, 75, 65, 85, start=0, extent=180, fill='pink', width=1)
        elif self.pet_type == 'cat':
            self.canvas.create_oval(25, 35, 95, 95, fill='#808080', outline='#4A4A4A', width=2)
            self.canvas.create_polygon(30, 25, 50, 40, 40, 15, fill='#808080', outline='#4A4A4A')
            self.canvas.create_polygon(90, 25, 70, 40, 80, 15, fill='#808080', outline='#4A4A4A')
            self.canvas.create_oval(40, 50, 50, 60, fill='#FFFF00')
            self.canvas.create_oval(70, 50, 80, 60, fill='#FFFF00')
            self.canvas.create_oval(45, 53, 47, 57, fill='black')
            self.canvas.create_oval(73, 53, 75, 57, fill='black')
            self.canvas.create_oval(55, 68, 65, 75, fill='pink')
            self.canvas.create_line(20, 65, 38, 67, fill='black', width=1)
            self.canvas.create_line(20, 72, 38, 72, fill='black', width=1)
            self.canvas.create_line(82, 67, 100, 65, fill='black', width=1)
            self.canvas.create_line(82, 72, 100, 70, fill='black', width=1)
        elif self.pet_type == 'cube':
            self.canvas.create_rectangle(25, 25, 95, 95, fill='#9B59B6', outline='#6C3483', width=3)
            self.canvas.create_rectangle(40, 40, 80, 80, fill='#BB8FCE', outline='#6C3483', width=1)
            self.canvas.create_text(60, 60, text='■', font=('Arial', 20), fill='white')
    
    def show_speech(self, message):
        """Show a speech bubble with a message"""
        # Clear old bubble
        if self.bubble_bg:
            self.canvas.delete(self.bubble_bg)
        if self.bubble_text:
            self.canvas.delete(self.bubble_text)
        
        # Calculate bubble dimensions
        bubble_width = len(message) * 8 + 30
        x1 = 60 - (bubble_width // 2)
        x2 = 60 + (bubble_width // 2)
        
        # Draw speech bubble
        self.bubble_bg = self.canvas.create_oval(x1, -5, x2, 28, 
                                                 fill='white', outline='black', width=2)
        self.bubble_text = self.canvas.create_text(60, 12, text=message, 
                                                   font=('Arial', 10, 'bold'), 
                                                   fill='black', anchor='center')
        
        # Auto-clear after 3 seconds
        self.window.after(3000, self.clear_bubble)
    
    def clear_bubble(self):
        if self.bubble_bg:
            self.canvas.delete(self.bubble_bg)
            self.bubble_bg = None
        if self.bubble_text:
            self.canvas.delete(self.bubble_text)
            self.bubble_text = None
    
    def say_hi(self):
        self.show_speech("Hi there! 👋")
    
    def open_calculator(self):
        try:
            if platform.system() == 'Darwin':
                subprocess.Popen(["open", "-a", "Calculator"])
                self.show_speech("Opening Calculator")
            elif platform.system() == 'Windows':
                subprocess.Popen("calc.exe")
                self.show_speech("Opening Calculator")
            else:
                subprocess.Popen(["gnome-calculator"])
                self.show_speech("Opening Calculator")
        except:
            self.show_speech("Can't open calculator 😢")
    
    def open_notepad(self):
        try:
            if platform.system() == 'Darwin':
                subprocess.Popen(["open", "-a", "TextEdit"])
                self.show_speech("Opening TextEdit")
            elif platform.system() == 'Windows':
                subprocess.Popen("notepad.exe")
                self.show_speech("Opening Notepad")
            else:
                subprocess.Popen(["gedit"])
                self.show_speech("Opening Text Editor")
        except:
            self.show_speech("Can't open editor 😢")
    
    def open_browser(self):
        webbrowser.open("https://www.google.com")
        self.show_speech("Opening Browser 🌐")
    
    def change_pet(self, pet_type):
        self.pet_type = pet_type
        self.draw_pet()
        self.show_speech(f"Changed to {pet_type}!")
    
    def build_menu(self):
        self.menu.delete(0, tk.END)
        
        # Movement toggle
        if self.moving:
            self.menu.add_command(label="⏸️ Stop Moving", command=self.stop_moving)
        else:
            self.menu.add_command(label="▶️ Start Moving", command=self.start_moving)
        
        self.menu.add_separator()
        
        # Change Pet submenu
        change_menu = Menu(self.menu, tearoff=False)
        change_menu.add_command(label="🔵 Blob", command=lambda: self.change_pet('blob'))
        change_menu.add_command(label="🐕 Dog", command=lambda: self.change_pet('dog'))
        change_menu.add_command(label="🐈 Cat", command=lambda: self.change_pet('cat'))
        change_menu.add_command(label="🧊 Cube", command=lambda: self.change_pet('cube'))
        self.menu.add_cascade(label="🎨 Change Pet", menu=change_menu)
        
        # Actions submenu
        actions_menu = Menu(self.menu, tearoff=False)
        actions_menu.add_command(label="💬 Say Hi", command=self.say_hi)
        actions_menu.add_command(label="🧮 Open Calculator", command=self.open_calculator)
        actions_menu.add_command(label="📝 Open Text Editor", command=self.open_notepad)
        actions_menu.add_command(label="🌐 Open Browser", command=self.open_browser)
        self.menu.add_cascade(label="⚡ Actions", menu=actions_menu)
        
        self.menu.add_separator()
        self.menu.add_command(label="❌ Close Pet", command=self.close_pet)
    
    def show_menu(self, event):
        self.build_menu()
        self.menu.post(event.x_root, event.y_root)
    
    def start_moving(self):
        self.moving = True
        self.build_menu()
        # Update the menu display
        self.menu.update()
    
    def stop_moving(self):
        self.moving = False
        self.build_menu()
        self.menu.update()
    
    def close_pet(self):
        self.window.quit()
        self.window.destroy()
        sys.exit(0)
    
    def animate(self):
        if self.moving:
            # Get current position
            x = self.window.winfo_x()
            y = self.window.winfo_y()
            
            # Get screen dimensions
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            
            # Bounce off edges
            if x <= 0 or x + 120 >= screen_width:
                self.dx = -self.dx
            if y <= 0 or y + 120 >= screen_height:
                self.dy = -self.dy
            
            # Update position
            new_x = x + self.dx
            new_y = y + self.dy
            
            # Keep within bounds
            new_x = max(0, min(new_x, screen_width - 120))
            new_y = max(0, min(new_y, screen_height - 120))
            
            self.window.geometry(f"+{new_x}+{new_y}")
        
        self.window.after(50, self.animate)
    
    def start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y
    
    def on_drag(self, event):
        x = self.window.winfo_x() + event.x - self.drag_x
        y = self.window.winfo_y() + event.y - self.drag_y
        self.window.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    DesktopPet()
