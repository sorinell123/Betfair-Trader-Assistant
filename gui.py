import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import keyboard
import os

from screenshot_manager import ScreenshotManager
from settings_manager import SettingsManager
from trading_analyzer import TradingAnalyzer
from screenshot_selector import ScreenshotSelector
from api_client import ClaudeAPIClient

class ScreenshotAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Betfair Trader Assistant")
        self.root.geometry("900x700")
        
        # Initialize managers
        self.settings_manager = SettingsManager()
        self.trading_analyzer = TradingAnalyzer(root)
        
        # Set up variables
        self.max_tokens_var = tk.StringVar(value=self.settings_manager.get_max_tokens())
        self.api_endpoint = "https://api.anthropic.com/v1/messages"
        
        # Create the UI
        self.setup_ui()
        
        # Initialize screenshot manager after canvas creation
        self.screenshot_manager = ScreenshotManager(root, self.canvas, status_text=self.status_text)
        
        # Start keyboard listener in a separate thread
        self.keyboard_thread = threading.Thread(target=self.start_keyboard_listener, daemon=True)
        self.keyboard_thread.start()
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame for screenshot display and controls
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left frame for screenshot
        left_frame = tk.Frame(top_frame, bd=2, relief=tk.SUNKEN)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Screenshot canvas
        self.canvas = tk.Canvas(left_frame, bg="lightgray")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_text(200, 150, text="Press Ctrl+Z to capture screenshot", fill="black", font=("Arial", 14))
        
        # Right frame for text input and buttons
        right_frame = tk.Frame(top_frame, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        
        # Text prompt label
        prompt_label = tk.Label(right_frame, text="Enter your prompt:")
        prompt_label.pack(anchor="w", pady=(0, 5))
        
        # Text prompt input and buttons
        prompt_frame = tk.Frame(right_frame)
        prompt_frame.pack(fill=tk.X, pady=(0, 10))

        # Prompt selection dropdown
        prompt_select_frame = tk.Frame(prompt_frame)
        prompt_select_frame.pack(fill=tk.X, pady=(0, 5))
        
        prompt_select_label = tk.Label(prompt_select_frame, text="Select Prompt:")
        prompt_select_label.pack(side=tk.LEFT)
        
        self.prompt_dropdown = ttk.Combobox(prompt_select_frame, state="readonly")
        self.prompt_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.prompt_dropdown.bind('<<ComboboxSelected>>', self.on_prompt_selected)
        self.update_prompt_dropdown()
        
        # Text prompt input
        self.text_prompt = scrolledtext.ScrolledText(prompt_frame, height=10)
        self.text_prompt.pack(fill=tk.X, pady=(0, 5))
        
        # Save prompt button
        save_prompt_frame = tk.Frame(prompt_frame)
        save_prompt_frame.pack(fill=tk.X)
        
        self.save_prompt_btn = tk.Button(save_prompt_frame, text="Save Prompt", 
                                       command=self.save_prompt)
        self.save_prompt_btn.pack(side=tk.LEFT)
        
        # Status label
        status_label = tk.Label(right_frame, text="Status:")
        status_label.pack(anchor="w")
        
        self.status_text = tk.Label(right_frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor="w")
        self.status_text.pack(fill=tk.X, pady=(0, 10))
        
        # API Settings frame
        api_settings_frame = tk.LabelFrame(right_frame, text="Claude API Settings")
        api_settings_frame.pack(fill=tk.X, pady=10)
        
        # Model info
        model_label = tk.Label(api_settings_frame, text="Model:")
        model_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        model_value = tk.Label(api_settings_frame, text="claude-3-7-sonnet-20250219")
        model_value.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # API Key field
        api_key_label = tk.Label(api_settings_frame, text="API Key:")
        api_key_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.api_key_entry = tk.Entry(api_settings_frame, show="*", width=30)
        self.api_key_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        if self.settings_manager.get_api_key():
            self.api_key_entry.insert(0, self.settings_manager.get_api_key())
            
        # Max tokens field
        max_tokens_label = tk.Label(api_settings_frame, text="Max Tokens:")
        max_tokens_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        self.max_tokens_entry = tk.Entry(api_settings_frame, textvariable=self.max_tokens_var, width=10)
        self.max_tokens_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # API Endpoint field
        endpoint_label = tk.Label(api_settings_frame, text="API Endpoint:")
        endpoint_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        
        endpoint_value = tk.Label(api_settings_frame, text=self.api_endpoint)
        endpoint_value.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Toggle show/hide API key
        self.show_key_var = tk.BooleanVar(value=False)
        show_key_cb = tk.Checkbutton(api_settings_frame, text="Show Key", 
                                     variable=self.show_key_var, 
                                     command=self.toggle_api_key_visibility)
        show_key_cb.grid(row=0, column=2, padx=5, pady=5)
        
        # Save API settings button
        save_api_btn = tk.Button(api_settings_frame, text="Save API Settings", 
                                command=lambda: self.settings_manager.save_api_settings(
                                    self.api_key_entry.get().strip(),
                                    self.max_tokens_var.get(),
                                    self.status_text))
        save_api_btn.grid(row=2, column=1, padx=5, pady=5, sticky="e")
        
        # Configure grid weights
        api_settings_frame.columnconfigure(1, weight=1)
        
        # Keyboard shortcuts info
        shortcuts_frame = tk.LabelFrame(right_frame, text="Keyboard Shortcuts")
        shortcuts_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(shortcuts_frame, text="Ctrl+Z: Capture screenshot", anchor="w").pack(fill=tk.X)
        tk.Label(shortcuts_frame, text="Ctrl+X: Send to AI", anchor="w").pack(fill=tk.X)
        
        # Buttons
        buttons_frame = tk.Frame(right_frame)
        buttons_frame.pack(fill=tk.X)
        
        self.capture_btn = tk.Button(buttons_frame, text="Capture Screenshot", command=self.take_screenshot)
        self.capture_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_stack_btn = tk.Button(buttons_frame, text="Clear Stack", command=self.clear_stack)
        self.clear_stack_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.send_btn = tk.Button(buttons_frame, text="Send to AI", command=self.send_to_ai)
        self.send_btn.pack(side=tk.LEFT)
        
        # Bottom frame for AI response
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        response_label = tk.Label(bottom_frame, text="AI Response:")
        response_label.pack(anchor="w")
        
        self.ai_response = scrolledtext.ScrolledText(bottom_frame)
        self.ai_response.pack(fill=tk.BOTH, expand=True)
    
    def start_keyboard_listener(self):
        # Register keyboard shortcuts
        keyboard.add_hotkey('ctrl+z', self.take_screenshot)  # Will now auto-stack images
        keyboard.add_hotkey('ctrl+x', self.send_to_ai)
        keyboard.add_hotkey('ctrl+c', self.clear_stack)  # Add shortcut for clearing stack
        keyboard.wait()
    
    def take_screenshot(self):
        # Minimize the window
        self.root.iconify()
        # Take screenshot after a small delay to allow UI to hide
        self.root.after(500, self._capture_screenshot)
    
    def _capture_screenshot(self):
        try:
            # Create selector window
            selector = ScreenshotSelector()
            
            # Take screenshot using screenshot manager
            if not self.screenshot_manager.take_screenshot(selector):
                self.status_text.config(text="Screenshot cancelled or failed")
            
            # Restore the window
            self.root.deiconify()
            
        except Exception as e:
            self.status_text.config(text=f"Error taking screenshot: {str(e)}")
            self.root.deiconify()
    
    def clear_stack(self):
        """Clear the screenshot stack"""
        self.screenshot_manager.clear_screenshots()

    def send_to_ai(self):
        screenshot_paths = self.screenshot_manager.get_screenshot_path()
        if not screenshot_paths:
            self.status_text.config(text="No screenshots available. Capture one first.")
            return
        
        prompt_text = self.text_prompt.get("1.0", tk.END).strip()
        if not prompt_text:
            self.status_text.config(text="Please enter a text prompt.")
            return
        
        self.status_text.config(text="Sending to AI...")
        
        # Create a thread to avoid blocking the UI
        threading.Thread(target=self._process_ai_request, args=(prompt_text,), daemon=True).start()
    
    def _process_ai_request(self, prompt_text):
        try:
            api_key = self.settings_manager.get_api_key()
            if api_key and self.api_endpoint:
                try:
                    self.root.after(0, self.status_text.config, {"text": "Sending to AI API..."})
                    
                    # Resize image if needed
                    self.screenshot_manager.resize_if_needed()
                    
                    # Create Claude API client
                    client = ClaudeAPIClient(api_key)
                    
                    # Send request using the client
                    try:
                        response = client.create_message(
                            text_prompt=prompt_text,
                            image_paths=self.screenshot_manager.get_screenshot_path(),
                            max_tokens=int(self.max_tokens_var.get()),
                            status_callback=lambda msg: self.root.after(0, self.status_text.config, {"text": msg})
                        )
                        
                        # Extract response text
                        if "content" in response and len(response["content"]) > 0:
                            ai_result = response["content"][0]["text"]
                        else:
                            ai_result = "Error: No content in response"
                            
                    except Exception as e:
                        error_msg = str(e)
                        if hasattr(e, 'response') and e.response is not None:
                            try:
                                error_data = e.response.json()
                                error_msg = error_data.get("error", {}).get("message", str(e))
                            except:
                                error_msg = e.response.text

                        ai_result = (
                            f"API Error:\n\n"
                            f"{error_msg}\n\n"
                            "Possible solutions:\n"
                            "1. Verify your API key is correct\n"
                            "2. Check if you have sufficient API credits\n"
                            "3. Ensure you're using a valid Claude API key from Anthropic\n"
                            "4. The API service might be temporarily unavailable\n\n"
                            "For more help, visit: https://docs.anthropic.com/"
                        )
                    
                    self.root.after(0, self.status_text.config, {"text": "Received AI response"})
                
                except Exception as e:
                    ai_result = f"API Error: {str(e)}\n\n"
                    ai_result += "Please check your API settings and internet connection."
                    self.root.after(0, self.status_text.config, {"text": f"API Error: {str(e)}"})
            
            else:
                # No API settings, use placeholder response
                paths = self.screenshot_manager.get_screenshot_path()
                paths_str = "\n".join(paths)
                ai_result = f"I've analyzed your screenshots at:\n{paths_str}\n\n"
                ai_result += f"Your prompt was: '{prompt_text}'\n\n"
                ai_result += "This is a placeholder AI response. To get actual AI responses, you need to:\n"
                ai_result += "1. Enter your Claude API Key in the API Settings section\n"
                ai_result += "2. Click 'Save API Settings'\n"
                ai_result += "3. Try sending to AI again\n\n"
                ai_result += "Make sure you have a valid Claude API key from Anthropic."
            
            # Update the UI in a thread-safe way
            self.root.after(0, self._update_ai_response, ai_result)
            
        except Exception as e:
            self.root.after(0, self.status_text.config, {"text": f"Error: {str(e)}"})

    def _update_ai_response(self, text):
        # Clear and update the response text widget
        self.ai_response.delete("1.0", tk.END)
        self.ai_response.insert("1.0", text)
        
        # Check for trading recommendation and show popup if found
        trade_info = self.trading_analyzer.parse_trading_recommendation(text)
        if trade_info:
            self.trading_analyzer.show_trade_popup(trade_info)
    
    def toggle_api_key_visibility(self):
        # Toggle between showing and hiding the API key
        if self.show_key_var.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="*")
    
    def update_prompt_dropdown(self):
        """Update the prompt dropdown with available prompts"""
        available_prompts = self.settings_manager.get_available_prompts()
        self.prompt_dropdown['values'] = available_prompts
        if available_prompts:
            self.prompt_dropdown.set(available_prompts[0])
        else:
            self.prompt_dropdown.set('')

    def save_prompt(self):
        """Save the current prompt and update dropdown"""
        self.settings_manager.save_prompt(
            self.text_prompt.get("1.0", tk.END).strip(),
            self.status_text
        )
        self.update_prompt_dropdown()

    def on_prompt_selected(self, event=None):
        """Handle prompt selection from dropdown"""
        selected_prompt = self.prompt_dropdown.get()
        self.settings_manager.load_prompt(
            self.text_prompt,
            self.status_text,
            selected_prompt
        )
