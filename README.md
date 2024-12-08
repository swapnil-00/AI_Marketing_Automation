# AI Marketing Automation

## Overview
This project implements an AI-powered marketing automation system that:
- Loads marketing campaign data
- Calculates key performance metrics
- Makes data-driven decisions to optimize campaigns
- Executes actions like pausing, increasing, or decreasing budgets
- Generates comprehensive reports

## Setup and Installation

1. Download the zip file and extract it
2. Create a virtual environment
```bash
python -m venv PrjVenv
PrjVenv/bin/activate  
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Prepare Data
- Place your `campaigns.csv` and `historical_data.csv` in the `data/` directory
- Ensure CSV files have required columns

## Running the Project
```bash
python main.py
```

## Testing
```bash
pytest tests/
```

## Project Structure
- `config/`: Configuration settings
- `data/`: Input data files
- `logs/`: Log files
- `reports/`: Generated reports
- `src/`: Core modules
- `tests/`: Unit tests

## Key Modules
- `data_loader.py`: Handles data ingestion
- `metrics_calculator.py`: Computes campaign performance metrics
- `ai_decision_agent.py`: Makes optimization decisions
- `action_executor.py`: Applies recommended actions
- `reporting.py`: Generates performance reports

## Customization
Edit `config/settings.json` to adjust optimization rules and thresholds.