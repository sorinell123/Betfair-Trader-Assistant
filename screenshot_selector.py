import tkinter as tk
from ctypes import windll

class ScreenshotSelector:
    def __init__(self):
        self.root = tk.Tk()
        # Get DPI scaling factor
        try:
            self.scale_factor = windll.shcore.GetScaleFactorForDevice(0) / 100
        except:
            self.scale_factor = 1.0  # Default to 1.0 if unable to get scaling factor
        
        self.root.attributes('-alpha', 0.3)  # Semi-transparent
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        
        # Set up canvas for drawing selection rectangle
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.configure(cursor="cross")
        
        # Variables for selection
        self.start_x = None
        self.start_y = None
        self.start_screen_x = None
        self.start_screen_y = None
        self.current_rect = None
        self.selection = None
        
        # Bind mouse events
        self.canvas.bind('<Button-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        
        # Bind escape key to cancel
        self.root.bind('<Escape>', lambda e: self.root.quit())
    
    def get_abs_coordinates(self, event):
        """Convert window-relative coordinates to screen coordinates"""
        # Get the root window position
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        
        # Calculate absolute coordinates
        abs_x = root_x + event.x
        abs_y = root_y + event.y
        
        # Apply DPI scaling
        return (int(abs_x * self.scale_factor), 
                int(abs_y * self.scale_factor))
    
    def on_press(self, event):
        # Store both canvas and screen coordinates
        self.start_x = event.x
        self.start_y = event.y
        self.start_screen_x, self.start_screen_y = self.get_abs_coordinates(event)
        
    def on_drag(self, event):
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        
        # Draw rectangle using canvas coordinates for display
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline='red', width=2
        )
    
    def on_release(self, event):
        if self.start_screen_x is not None and self.start_screen_y is not None:
            # Get end screen coordinates
            end_screen_x, end_screen_y = self.get_abs_coordinates(event)
            
            # Calculate final coordinates
            x1 = min(self.start_screen_x, end_screen_x)
            y1 = min(self.start_screen_y, end_screen_y)
            x2 = max(self.start_screen_x, end_screen_x)
            y2 = max(self.start_screen_y, end_screen_y)
            
            # Store selection coordinates
            self.selection = (x1, y1, x2, y2)
            self.root.quit()
    
    def get_selection(self):
        self.root.mainloop()
        selection = self.selection
        self.root.destroy()
        return selection
