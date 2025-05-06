# Betfair Trader Assistant

A desktop application designed to assist Betfair traders by capturing and analyzing betting exchange screenshots using AI technology. The application helps identify profitable trading opportunities and provides detailed market analysis.

## Features

- **Screenshot Capture**: Easily capture betting exchange screenshots with Ctrl+Z
- **Multiple Screenshot Support**: Stack multiple screenshots for comprehensive analysis
- **AI-Powered Analysis**: Get detailed market analysis including:
  - Current price identification
  - Directional predictions
  - Price/volume graph analysis
  - Market context evaluation
- **Trading Recommendations**: Receive specific trading suggestions with:
  - Entry price points
  - Stop loss levels
  - Target profit levels
- **Customizable Prompts**: Save and load different analysis prompts
- **User-Friendly Interface**: Clean GUI with keyboard shortcuts

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/betfair-trader-assistant.git
cd betfair-trader-assistant
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Copy the configuration template and set up your configuration:
```bash
cp config.ini.template config.ini
```

5. Edit `config.ini` with your settings

## Configuration

1. Open `config.ini` and configure:
   - API settings
   - Maximum tokens for responses
   - Other custom settings

## Usage

### Starting the Application

Run the application:
```bash
python main.py
```

### Keyboard Shortcuts

- `Ctrl+Z`: Capture screenshot
- `Ctrl+X`: Send to AI for analysis
- `Ctrl+C`: Clear screenshot stack

### Basic Workflow

1. When you see a trading opportunity:
   - Press `Ctrl+Z` to capture the screen
   - Select the area to capture using your mouse
   - Repeat for multiple screenshots if needed

2. Select or enter your analysis prompt

3. Press `Ctrl+X` to get AI analysis

4. Review the trading recommendation in the popup window

### Working with Prompts

- Save frequently used prompts using the "Save Prompt" button
- Load saved prompts from the dropdown menu
- Customize prompts for different race types or betting scenarios

## Project Structure

```
betfair-trader-assistant/
├── main.py              # Application entry point
├── gui.py              # Main GUI implementation
├── api_client.py       # API client implementation
├── screenshot_manager.py    # Screenshot handling
├── settings_manager.py     # Configuration management
├── trading_analyzer.py     # Trading analysis logic
├── screenshot_selector.py  # Screenshot area selector
├── config.ini          # Configuration file
└── prompts/           # Stored analysis prompts
    ├── FLAT TURF SPRINT HANDICAPS (5-6f).txt
    ├── NATIONAL HUNT RACES.txt
    └── ...
```

## Dependencies

- Python 3.8+
- tkinter
- keyboard
- Pillow (PIL)
- requests

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
