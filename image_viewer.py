import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, image_paths):
        if isinstance(image_paths, str):
            image_paths = [image_paths]  # Convert single path to list
            
        self.root = tk.Toplevel()
        self.root.title("Image Viewer")
        
        # Set minimum window size to avoid zero dimensions
        self.root.minsize(400, 300)
        
        # Store image paths and initialize variables
        self.image_paths = image_paths
        self.zoom_levels = {path: 1.0 for path in image_paths}
        self.original_images = {}
        self.current_images = {}
        self.photo_images = {}
        
        self.setup_ui()
        
        # Wait for window to be ready
        self.root.update_idletasks()
        
        # Set window state to zoomed (maximized) after UI setup
        self.root.state('zoomed')
        self.root.focus_set()
        
        # Load images after window is ready
        self.load_images()
        self.setup_bindings()
    
    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        # Create a tab for each image
        self.tabs = {}
        self.canvases = {}
        
        for path in self.image_paths:
            # Create frame for tab
            frame = ttk.Frame(self.notebook)
            self.tabs[path] = frame
            
            # Add tab with image name
            tab_name = path.split('/')[-1]  # Get filename from path
            self.notebook.add(frame, text=tab_name)
            
            # Create canvas with scrollbars for each tab
            canvas = tk.Canvas(frame, highlightthickness=0)
            scrollbar_y = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
            
            # Configure canvas scrolling
            canvas.configure(
                xscrollcommand=scrollbar_x.set,
                yscrollcommand=scrollbar_y.set
            )
            
            # Pack scrollbars and canvas
            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x.pack(side="bottom", fill="x")
            canvas.pack(side="left", fill="both", expand=True)
            
            self.canvases[path] = canvas
            
            # Add reset zoom button for each tab
            reset_btn = tk.Button(frame, text="Reset Zoom", 
                                command=lambda p=path: self.reset_zoom(p))
            reset_btn.place(relx=0.02, rely=0.02)
    
    def load_images(self):
        for path in self.image_paths:
            # Load and store original image
            self.original_images[path] = Image.open(path)
            self.update_image(path)
    
    def setup_bindings(self):
        # Bind events for each canvas
        for path, canvas in self.canvases.items():
            # Mouse wheel for zooming
            canvas.bind("<MouseWheel>", 
                      lambda e, p=path: self.handle_zoom(e, p))  # Windows
            canvas.bind("<Button-4>", 
                      lambda e, p=path: self.handle_zoom(e, p))  # Linux scroll up
            canvas.bind("<Button-5>", 
                      lambda e, p=path: self.handle_zoom(e, p))  # Linux scroll down
            
            # Pan bindings
            canvas.bind("<ButtonPress-1>", self.start_pan)
            canvas.bind("<B1-Motion>", self.handle_pan)
        
        # Close on Escape
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        # Update image on window resize
        self.root.bind("<Configure>", self.on_resize)
    
    def update_image(self, path):
        if not self.original_images.get(path):
            return
            
        canvas = self.canvases[path]
        original_image = self.original_images[path]
            
        # Get current window size with minimum values
        win_width = max(400, canvas.winfo_width())
        win_height = max(300, canvas.winfo_height())
        
        # Get original image size
        img_width, img_height = original_image.size
        
        # Calculate new size maintaining aspect ratio and applying zoom
        scale = min(win_width/img_width, win_height/img_height) * self.zoom_levels[path]
        new_width = max(1, int(img_width * scale))
        new_height = max(1, int(img_height * scale))
        
        # Resize image
        self.current_images[path] = original_image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )
        
        # Convert to PhotoImage and store reference
        self.photo_images[path] = ImageTk.PhotoImage(self.current_images[path])
        
        # Update canvas
        canvas.delete("all")
        canvas.create_image(
            win_width//2, 
            win_height//2,
            image=self.photo_images[path],
            anchor="center",
            tags="image"
        )
        
        # Update scrollregion to match new image size
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def handle_zoom(self, event, path):
        if event.num == 5 or event.delta < 0:  # Zoom out
            self.zoom_levels[path] = max(0.1, self.zoom_levels[path] - 0.1)
        else:  # Zoom in
            self.zoom_levels[path] = min(5.0, self.zoom_levels[path] + 0.1)
        
        self.update_image(path)
    
    def start_pan(self, event):
        canvas = event.widget
        canvas.scan_mark(event.x, event.y)
        
    def handle_pan(self, event):
        canvas = event.widget
        canvas.scan_dragto(event.x, event.y, gain=1)
    
    def reset_zoom(self, path):
        self.zoom_levels[path] = 1.0
        self.update_image(path)
        
    def on_resize(self, event):
        # Only handle window resize events
        if event.widget == self.root:
            # Update current tab's image
            current_tab = self.notebook.select()
            for path, tab in self.tabs.items():
                if str(tab) == str(current_tab):
                    self.update_image(path)
                    break
