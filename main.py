import tkinter as tk
from gui import ScreenshotAIApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotAIApp(root)
    
    # Update canvas size when window resizes
    def on_resize(event):
        if hasattr(app, 'screenshot_manager') and app.screenshot_manager:
            app.screenshot_manager.display_screenshot()
    
    root.bind("<Configure>", on_resize)
    
    root.mainloop()
