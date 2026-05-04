import tkinter as tk
from tkinter import Menu
import subprocess
import webbrowser

class DesktopPet:
    def __init__(self):
        self.window = tk.Tk()
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.geometry("120x120+500+400")
        self.window.wm_attributes('-transparentcolor', 'white')
        
        self.canvas = tk.Canvas(self.window, width=120, height=120, bg='white', highlightthickness=0)
        self.canvas.pack()
        
        self.pet_type = 'blob'
        self.dx = 3
        self.dy = 3
        self.moving = False
        
        # Speech bubble
        self.bubble_bg = None
        self.bubble_text = None
        
        self.draw_pet()
        
        # Initialize menu
        self.menu = Menu(self.window, tearoff=False)
        self.build_menu()
        
        self.canvas.bind("<Button-3>", self.show_menu)
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        
        self.animate()
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
        """Show a speech bubble with a message for 3 seconds"""
        # Delete old bubble
        if self.bubble_bg:
            self.canvas.delete(self.bubble_bg)
        if self.bubble_text:
            self.canvas.delete(self.bubble_text)
        
        # Calculate bubble size
        bubble_width = len(message) * 7 + 20
        x1 = 60 - bubble_width // 2
        x2 = 60 + bubble_width // 2
        
        # Background bubble (white with black outline)
        self.bubble_bg = self.canvas.create_oval(x1, -5, x2, 25, fill='white', outline='black', width=1)
        
        # Text - black, simple font
        self.bubble_text = self.canvas.create_text(
            60, 10, 
            text=message, 
            font=('Arial', 10), 
            fill='black',
            anchor='center'
        )
        
        # Remove after 3 seconds
        self.window.after(3000, self.clear_bubble)
    
    def clear_bubble(self):
        if self.bubble_bg:
            self.canvas.delete(self.bubble_bg)
            self.bubble_bg = None
        if self.bubble_text:
            self.canvas.delete(self.bubble_text)
            self.bubble_text = None
    
    def say_hi(self):
        self.show_speech("Hi!")
    
    def open_calculator(self):
        try:
            subprocess.Popen("calc.exe")
            self.show_speech("Opening calculator")
        except:
            self.show_speech("Oops, no calculator")
    
    def open_notepad(self):
        try:
            subprocess.Popen("notepad.exe")
            self.show_speech("Opening notepad")
        except:
            self.show_speech("Oops, no notepad")
    
    def open_browser(self):
        webbrowser.open("https://www.google.com")
        self.show_speech("Opening browser")
    
    def change_pet(self, pet_type):
        self.pet_type = pet_type
        self.draw_pet()
    
    def build_menu(self):
        self.menu.delete(0, tk.END)
        
        # Move/Stop option
        if self.moving:
            self.menu.add_command(label="Stop", command=self.stop_moving)
        else:
            self.menu.add_command(label="Move", command=self.start_moving)
        
        # Change Pet submenu
        change_menu = Menu(self.menu, tearoff=False)
        change_menu.add_command(label="Blob (default)", command=lambda: self.change_pet('blob'))
        change_menu.add_command(label="Dog", command=lambda: self.change_pet('dog'))
        change_menu.add_command(label="Cat", command=lambda: self.change_pet('cat'))
        change_menu.add_command(label="Cube", command=lambda: self.change_pet('cube'))
        self.menu.add_cascade(label="Change Pet", menu=change_menu)
        
        # More Options submenu
        more_menu = Menu(self.menu, tearoff=False)
        more_menu.add_command(label="Say Hi", command=self.say_hi)
        more_menu.add_command(label="Open Calculator", command=self.open_calculator)
        more_menu.add_command(label="Open Notepad", command=self.open_notepad)
        more_menu.add_command(label="Open Browser", command=self.open_browser)
        self.menu.add_cascade(label="More Options", menu=more_menu)
        
        self.menu.add_separator()
        self.menu.add_command(label="Close", command=self.close_pet)
    
    def show_menu(self, event):
        self.build_menu()
        self.menu.post(event.x_root, event.y_root)
    
    def start_moving(self):
        self.moving = True
        self.build_menu()
    
    def stop_moving(self):
        self.moving = False
        self.build_menu()
    
    def close_pet(self):
        self.window.quit()
        self.window.destroy()
    
    def animate(self):
        if self.moving:
            x = self.window.winfo_x()
            y = self.window.winfo_y()
            screen_w = self.window.winfo_screenwidth()
            screen_h = self.window.winfo_screenheight()
            
            if x <= 0 or x + 120 >= screen_w:
                self.dx = -self.dx
            if y <= 0 or y + 120 >= screen_h:
                self.dy = -self.dy
            
            self.window.geometry(f"+{x + self.dx}+{y + self.dy}")
        
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