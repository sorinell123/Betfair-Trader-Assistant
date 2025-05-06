# How to Use Betfair Trader Assistant

This guide will walk you through using the Betfair Trader Assistant effectively, from initial setup to advanced features.

## Quick Start Guide

### First-Time Setup

1. Install the application:
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/betfair-trader-assistant.git
   cd betfair-trader-assistant

   # Set up virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

2. Configure the application:
   - Copy `config.ini.template` to `config.ini`
   - Add your API key in the config file
   - Set your preferred max tokens

3. Launch the application:
   ```bash
   python main.py
   ```

### Basic Usage Workflow

1. **Capture Screenshots**
   - Press `Ctrl+Z` to start capture
   - Select the area containing the betting exchange interface
   - The window will minimize automatically during capture
   - You can capture multiple screenshots for analysis

2. **Choose or Enter a Prompt**
   - Select a pre-made prompt from the dropdown
   - Or enter your own analysis prompt
   - Save frequently used prompts with the "Save Prompt" button

3. **Get Analysis**
   - Press `Ctrl+X` to send screenshots for analysis
   - Wait for the AI response
   - Review the trading recommendation popup

4. **Clear Screenshots**
   - Press `Ctrl+C` to clear the screenshot stack
   - Start fresh with new captures

## Detailed Instructions

### Screenshot Capture Process

1. **Preparation**
   - Have the betting exchange page ready
   - Position it where you want to capture
   - Ensure all relevant information is visible

2. **Capturing**
   - Press `Ctrl+Z`
   - The application window will minimize
   - Click and drag to select the area
   - Release to capture
   - Window will restore automatically

3. **Multiple Screenshots**
   - Capture additional screenshots as needed
   - They'll be stacked for analysis
   - Useful for capturing different timeframes
   - Or different aspects of the market

### Working with Prompts

1. **Pre-made Prompts**
   The application comes with specialized prompts for different race types:
   - ALL-WEATHER HANDICAPS
   - FLAT TURF SPRINT HANDICAPS
   - NATIONAL HUNT RACES
   - And more...

2. **Using Prompts**
   - Select from the dropdown menu
   - Prompt will load in the text area
   - Modify as needed for your specific case
   - Click "Save Prompt" to store new versions

3. **Creating Custom Prompts**
   - Write your analysis requirements
   - Include specific aspects you want analyzed
   - Save for future use
   - Access them from the dropdown later

### Understanding Analysis Results

The AI analysis provides structured information:

1. **Current Price Analysis**
   - Identifies exact trading prices
   - Shows price movement trends
   - Highlights support/resistance levels
   - Notes significant money flow

2. **Directional Predictions**
   - Predicts likely price movements
   - Based on momentum indicators
   - Considers volume distribution
   - Analyzes steaming/drifting patterns

3. **Trading Recommendations**
   Format:
   ```
   Action: BACK or LAY
   Entry price: Specific odds
   Stop loss: Support/resistance level
   Target profit: Projected exit point
   Confidence: HIGH/MEDIUM
   ```

## Tips and Best Practices

### Optimal Screenshot Timing

1. **Market Activity**
   - Capture during significant price movements
   - Include volume spikes
   - Show clear trend formations
   - Catch key support/resistance tests

2. **Information Quality**
   - Ensure price ladder is clearly visible
   - Include volume information
   - Capture relevant time periods
   - Show multiple runners if relevant

### Prompt Customization

1. **Race-Specific Analysis**
   - Use specialized prompts for race types
   - Modify based on market conditions
   - Add specific concerns or focus areas
   - Include time-relevant factors

2. **Market Context**
   - Include overround requirements
   - Specify volume thresholds
   - Note time-to-post importance
   - Highlight specific patterns to watch

### Trading Recommendation Usage

1. **Implementation**
   - Always verify the analysis
   - Use recommended entry points as guides
   - Respect stop losses
   - Monitor target levels

2. **Risk Management**
   - Don't trade without stop losses
   - Follow confidence ratings
   - Use appropriate stake sizes
   - Monitor market changes

## Troubleshooting

### Common Issues

1. **Screenshot Capture Problems**
   - Ensure proper screen resolution
   - Check for window overlap
   - Verify selection area is valid
   - Restart application if persistent

2. **Analysis Delays**
   - Check internet connection
   - Verify API key is valid
   - Reduce screenshot size if needed
   - Check API status

3. **Prompt Issues**
   - Ensure prompt is loaded
   - Check for proper formatting
   - Verify saved prompts directory
   - Reset to default if needed

## Keyboard Shortcuts Reference

| Shortcut | Action |
|----------|--------|
| `Ctrl+Z` | Capture screenshot |
| `Ctrl+X` | Send to AI for analysis |
| `Ctrl+C` | Clear screenshot stack |

Remember: The key to successful trading is combining the AI analysis with your own judgment and risk management strategy.
