import configparser
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

class SettingsManager:
    def __init__(self, config_file="config.ini"):
        self.config_file = config_file
        self.api_key = ""
        self.max_tokens = "1024"
        self.load_api_settings()

    def save_prompt(self, prompt_text, status_text):
        if not prompt_text.strip():
            messagebox.showwarning("Warning", "Please enter a prompt before saving.")
            return

        # Ask for prompt name
        prompt_name = simpledialog.askstring("Save Prompt", "Enter a name for this prompt:")
        if not prompt_name:
            return

        # Clean filename
        prompt_filename = f"{prompt_name.strip()}.txt"
        
        # Ensure prompts directory exists
        os.makedirs("prompts", exist_ok=True)
        
        # Save prompt to file
        try:
            with open(os.path.join("prompts", prompt_filename), 'w', encoding='utf-8') as f:
                f.write(prompt_text)
            status_text.config(text=f"Prompt saved as '{prompt_filename}'")
            messagebox.showinfo("Success", f"Prompt saved as '{prompt_filename}'")
        except Exception as e:
            status_text.config(text=f"Error saving prompt: {str(e)}")
            messagebox.showerror("Error", f"Failed to save prompt: {str(e)}")
    
    def get_available_prompts(self):
        """Return a list of available prompt names"""
        try:
            os.makedirs("prompts", exist_ok=True)
            files = [f[:-4] for f in os.listdir("prompts") if f.endswith('.txt')]
            return sorted(files)
        except Exception:
            return []

    def load_prompt_by_name(self, prompt_name):
        """Load a specific prompt by name"""
        if not prompt_name:
            return None
            
        try:
            with open(os.path.join("prompts", f"{prompt_name}.txt"), 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None

    def load_prompt(self, text_prompt, status_text, prompt_name=None):
        if not prompt_name:
            messagebox.showwarning("Warning", "No prompt selected.")
            return
            
        prompt_content = self.load_prompt_by_name(prompt_name)
        if prompt_content is not None:
            text_prompt.delete("1.0", tk.END)
            text_prompt.insert("1.0", prompt_content)
            status_text.config(text=f"Loaded prompt: {prompt_name}")
        else:
            messagebox.showwarning("Warning", f"Could not load prompt: {prompt_name}")

    def save_api_settings(self, api_key, max_tokens, status_text=None):
        # Save to instance variable
        self.api_key = api_key
        self.max_tokens = max_tokens
        
        # Create config parser and read existing config
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
        
        # Update API settings
        config['API'] = {
            'key': api_key,
            'max_tokens': max_tokens
        }
        
        # Preserve existing prompt if any
        if 'Prompts' not in config:
            config['Prompts'] = {}
        
        # Write to config file
        try:
            with open(self.config_file, 'w') as f:
                config.write(f)
            
            if status_text:
                status_text.config(text="API settings saved successfully")
                messagebox.showinfo("Success", "API settings saved successfully")
            return True
        except Exception as e:
            if status_text:
                status_text.config(text=f"Error saving API settings: {str(e)}")
                messagebox.showerror("Error", f"Failed to save API settings: {str(e)}")
            return False
    
    def load_api_settings(self):
        # Check if config file exists
        if not os.path.exists(self.config_file):
            return {}
        
        # Load settings from file
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file)
            
            # Load API settings
            if 'API' in config:
                self.api_key = config['API'].get('key', '')
                self.max_tokens = config['API'].get('max_tokens', '1024')
                
                return {
                    'api_key': self.api_key,
                    'max_tokens': self.max_tokens
                }
            
        except Exception as e:
            print(f"Error loading settings: {str(e)}")
        
        return {}

    def get_api_key(self):
        return self.api_key

    def get_max_tokens(self):
        return self.max_tokens
