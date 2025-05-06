import tkinter as tk

class TradingAnalyzer:
    def __init__(self, root):
        self.root = root

    def parse_trading_recommendation(self, response_text):
        """Parse trading information from the AI response with the new format"""
        try:
            # Clean up the response text first - remove any leading asterisks and whitespace
            response_text = response_text.lstrip('* \n\t\r').strip()
            
            # Initialize dictionary for trading info
            trade_info = {}
            
            # Trading fields to look for with their possible variations, including markdown
            trading_fields = {
                "Action": ["Action:", "TRADING RECOMMENDATION:", "***Action:", "**Action:", "*Action:"],
                "Entry Zone": ["Entry Zone:", "Entry:", "***Entry Zone:", "**Entry Zone:", "*Entry Zone:"],
                "Stop Loss": ["Stop Loss:", "SL:", "***Stop Loss:", "**Stop Loss:", "*Stop Loss:",
                            "***SL:", "**SL:", "*SL:"],
                "Target Profit": ["Target Profit:", "TP:", "***Target Profit:", "**Target Profit:", "*Target Profit:",
                                "***TP:", "**TP:", "*TP:"],
                "Exit Timing": ["Exit Timing:", "Exit:", "***Exit Timing:", "**Exit Timing:", "*Exit Timing:",
                              "***Exit:", "**Exit:", "*Exit:"],
                "Confidence Score": ["Confidence Score:", "Confidence:", "***Confidence Score:", "**Confidence Score:",
                                   "*Confidence Score:", "***Confidence:", "**Confidence:", "*Confidence:"]
            }
            
            # Split response into lines and process each line
            lines = response_text.split('\n')
            for line in lines:
                # Remove leading/trailing whitespace and asterisks
                line = line.strip().lstrip('*').strip()
                # Check each field's possible variations
                for field_key, field_variations in trading_fields.items():
                    if any(field in line for field in field_variations):
                        if ":" in line:
                            # Split at the first occurrence of : for better handling
                            parts = line.split(":", 1)
                            value = parts[1].strip()
                            
                            # Clean up the value - remove all markdown and formatting
                            value = value.strip('*').replace("**", "").replace("***", "").strip()
                            
                            # Special handling for confidence score
                            if field_key == "Confidence Score":
                                try:
                                    # Extract numeric value
                                    score = int(''.join(filter(str.isdigit, value)))
                                    if 1 <= score <= 100:
                                        trade_info[field_key] = score
                                except ValueError:
                                    continue
                            else:
                                trade_info[field_key] = value
            
            # Only return if we have the required fields and confidence score is >= 60
            required_fields = ["Action", "Entry Zone", "Stop Loss", "Target Profit", "Exit Timing", "Confidence Score"]
            if (all(field in trade_info for field in required_fields) and
                isinstance(trade_info.get("Confidence Score"), int) and
                trade_info["Confidence Score"] >= 60):
                return trade_info
                    
        except Exception as e:
            print(f"Error parsing trading info: {str(e)}")
        return None

    def show_trade_popup(self, trade_info):
        """Display a popup with the detailed trading recommendation"""
        popup = tk.Toplevel(self.root)
        popup.title("Trading Recommendation")
        popup.geometry("500x400")
        popup.attributes('-topmost', True)
        
        # Configure popup
        popup.configure(bg='#f0f0f0')
        popup.grab_set()  # Make popup modal
        
        # Center popup on screen
        popup.geometry("+%d+%d" % (
            self.root.winfo_x() + (self.root.winfo_width() // 2 - 250),
            self.root.winfo_y() + (self.root.winfo_height() // 2 - 200)
        ))
        
        # Create main frame
        frame = tk.Frame(popup, bg='#f0f0f0', padx=25, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add title with border
        title_frame = tk.Frame(frame, bg='#f0f0f0', pady=10)
        title_frame.pack(fill=tk.X)
        title_frame.configure(highlightbackground="#cccccc", highlightthickness=1)
        
        title = tk.Label(title_frame, text="TRADING RECOMMENDATION", 
                        font=("Arial", 14, "bold"),
                        bg='#f0f0f0', fg='#333333')
        title.pack(pady=5)
        
        # Add trading information with improved styling
        fields = [
            ("Action", "Action"),
            ("Entry Zone", "Entry Zone"),
            ("Stop Loss", "Stop Loss"),
            ("Target Profit", "Target Profit"),
            ("Exit Timing", "Exit Timing"),
            ("Confidence Score", "Confidence")
        ]
        
        # Create a frame for the content with a light border
        content_frame = tk.Frame(frame, bg='#f0f0f0', padx=15, pady=10)
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        
        for field_key, display_name in fields:
            value = trade_info.get(field_key, "N/A")
            info_frame = tk.Frame(content_frame, bg='#f0f0f0')
            info_frame.pack(fill=tk.X, pady=5)
            
            label = tk.Label(info_frame, text=f"{display_name}:", 
                           font=("Arial", 10, "bold"),
                           width=15, anchor='w',
                           bg='#f0f0f0', fg='#444444')
            label.pack(side=tk.LEFT)
            
            # Special handling for confidence score
            if field_key == "Confidence Score":
                score = int(value) if isinstance(value, int) else 0
                # Color coding based on confidence score
                if score >= 90:
                    bg_color = '#90EE90'  # Light green for exceptional
                elif score >= 80:
                    bg_color = '#98FB98'  # Pale green for strong
                elif score >= 70:
                    bg_color = '#FFFF99'  # Light yellow for good
                else:
                    bg_color = '#FFB366'  # Light orange for reasonable
                
                value = f"{score} - " + (
                    "Exceptional" if score >= 90 else
                    "Strong" if score >= 80 else
                    "Good" if score >= 70 else
                    "Reasonable"
                )
                
                value_label = tk.Label(info_frame, text=value,
                                     font=("Arial", 10),
                                     bg=bg_color, padx=5, pady=2)
            else:
                value_label = tk.Label(info_frame, text=str(value),
                                     font=("Arial", 10),
                                     bg='#f0f0f0', fg='#333333')
            
            value_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Add OK button with improved styling
        ok_button = tk.Button(frame, text="OK", command=popup.destroy,
                            width=10, bg='#4a90e2', fg='white',
                            font=("Arial", 10, "bold"),
                            relief=tk.FLAT)
        ok_button.pack(pady=(20, 0))
        
        # Handle window close button
        popup.protocol("WM_DELETE_WINDOW", popup.destroy)
        
        # Play notification sound
        self.root.bell()
