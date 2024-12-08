import pandas as pd
import json
import logging
from typing import Dict, Any

class DataLoader:
    def __init__(self, config_path='config/settings.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        logging.basicConfig(
            filename='logs/marketing_automation.log',
            level=getattr(logging, self.config['logging']['log_level'])
        )
        self.logger = logging.getLogger(__name__)

    def load_campaigns(self) -> pd.DataFrame:
        """
        Load campaign data from CSV
        """
        try:
            campaigns_path = self.config['data_paths']['campaigns']
            campaigns_df = pd.read_csv(campaigns_path)
            
            # Validate required columns
            required_columns = [
                'Campaign_ID', 'Impressions', 'Clicks', 'Conversions', 
                'Spend', 'Revenue', 'Status'
            ]
            
            for col in required_columns:
                if col not in campaigns_df.columns:
                    raise ValueError(f"Missing required column: {col}")
            
            self.logger.info(f"Successfully loaded {len(campaigns_df)} campaigns")
            return campaigns_df
        
        except Exception as e:
            self.logger.error(f"Error loading campaigns: {e}")
            raise

    def load_historical_data(self) -> pd.DataFrame:
        """
        Load historical campaign data from CSV
        """
        try:
            historical_path = self.config['data_paths']['historical_data']
            historical_df = pd.read_csv(historical_path)
            
            self.logger.info(f"Successfully loaded {len(historical_df)} historical records")
            return historical_df
        
        except Exception as e:
            self.logger.error(f"Error loading historical data: {e}")
            raise