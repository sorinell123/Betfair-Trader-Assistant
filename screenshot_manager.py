import tkinter as tk
from PIL import ImageGrab, ImageTk, Image
from datetime import datetime
import os
from image_viewer import ImageViewer

class ScreenshotManager:
    def __init__(self, root, canvas, save_dir="screenshots", status_text=None):
        self.root = root
        self.canvas = canvas
        self.status_text = status_text
        self.save_dir = save_dir
        self.screenshots = []  # List to store multiple screenshots
        self.screenshot_paths = []  # List to store multiple screenshot paths
        self.tk_image = None

        # Create directory for saving screenshots if it doesn't exist
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def take_screenshot(self, selector):
        """Take a screenshot using the provided selector"""
        try:
            # Get the selection from the selector
            selection = selector.get_selection()
            
            if selection:
                x1, y1, x2, y2 = selection
                
                # Ensure selection is valid
                if x1 != x2 and y1 != y2:
                    # Capture the screen
                    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                    
                    # Generate a filename based on timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = os.path.join(self.save_dir, f"screenshot_{timestamp}.png")
                    
                    # Save the screenshot
                    screenshot.save(screenshot_path)
                    
                    # Add to the lists
                    self.screenshots.append(screenshot)
                    self.screenshot_paths.append(screenshot_path)
                    
                    # Set current screenshot for display
                    self.screenshot = screenshot
                    
                    # Display the screenshot and bind click handler
                    self.display_screenshot(bind_click=True)
                    
                    # Update status if status_text widget exists
                    if self.status_text:
                        self.status_text.config(text=f"Screenshot saved ({len(self.screenshots)} images stacked)")
                    
                    return True
            return False
                    
        except Exception as e:
            if self.status_text:
                self.status_text.config(text=f"Error taking screenshot: {str(e)}")
            return False

    def display_screenshot(self, bind_click=False):
        """Display all screenshots in a grid layout"""
        if not self.screenshots:
            return
            
        # Get canvas dimensions
        self.canvas.update_idletasks()  # Ensure dimensions are current
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 400
            canvas_height = 300

        # Clear canvas
        self.canvas.delete("all")
        
        # Calculate grid dimensions
        num_images = len(self.screenshots)
        cols = min(3, num_images)  # Maximum 3 images per row
        rows = (num_images + cols - 1) // cols
        
        # Calculate cell size
        cell_width = canvas_width // cols
        cell_height = canvas_height // rows
        
        # Keep reference to all PhotoImage objects
        self.tk_images = []
        
        for i, screenshot in enumerate(self.screenshots):
            # Calculate grid position
            row = i // cols
            col = i % cols
            
            # Get image dimensions
            img_width, img_height = screenshot.size
            
            # Calculate scale to fit in cell while maintaining aspect ratio
            scale = min(cell_width/img_width, cell_height/img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Resize and convert image
            resized_img = screenshot.resize((new_width, new_height), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(resized_img)
            self.tk_images.append(tk_image)
            
            # Calculate position to center the image in its cell
            x = col * cell_width + (cell_width - new_width) // 2
            y = row * cell_height + (cell_height - new_height) // 2
            
            # Create image on canvas
            image_item = self.canvas.create_image(
                x, y,
                image=tk_image,
                anchor="nw",
                tags=f"screenshot{i}"
            )
        
        # Add click handling if requested
        if bind_click:
            self.canvas.tag_bind("screenshot", "<Button-1>", self.open_image_viewer)
            # Add visual feedback for clickable image
            self.canvas.tag_bind("screenshot", "<Enter>", 
                lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind("screenshot", "<Leave>", 
                lambda e: self.canvas.config(cursor=""))

    def open_image_viewer(self, event=None):
        """Open the image viewer for all screenshots"""
        if self.screenshot_paths:
            ImageViewer(self.screenshot_paths)

    def get_screenshot_path(self):
        """Return the paths of all screenshots"""
        return self.screenshot_paths

    def clear_screenshots(self):
        """Clear all stacked screenshots"""
        self.screenshots = []
        self.screenshot_paths = []
        self.screenshot = None
        self.canvas.delete("all")
        if self.status_text:
            self.status_text.config(text="Screenshot stack cleared")

    def resize_if_needed(self):
        """Resize all screenshots if they exceed size limits"""
        if not self.screenshot_paths:
            return False

        try:
            for screenshot_path in self.screenshot_paths:
                # Check image size
                img_size = os.path.getsize(screenshot_path)
                if img_size > 20 * 1024 * 1024:  # 20MB
                    raise Exception("Image size exceeds 20MB limit")
                
                # Check and resize image if needed
                with Image.open(screenshot_path) as img:
                    width, height = img.size
                    if width > 3000 or height > 3000:
                        # Calculate new dimensions
                        ratio = min(3000/width, 3000/height)
                        new_width = int(width * ratio)
                        new_height = int(height * ratio)
                        
                        # Resize image
                        img = img.resize((new_width, new_height), Image.LANCZOS)
                        
                        # Save resized image
                        img.save(screenshot_path)
                        
                        if self.status_text:
                            self.status_text.config(text="Images resized to meet size requirements")
            
            return True
                    
        except Exception as e:
            if self.status_text:
                self.status_text.config(text=f"Error resizing images: {str(e)}")
            return False
