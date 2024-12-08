import pandas as pd
import numpy as np
import logging
from typing import Dict, Any
import json
import os

class MetricsCalculator:
    def __init__(self, config_path='config/settings.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Set up logger to save to 'logs/marketing_automation.log'
        logging.basicConfig(
            filename='logs/marketing_automation.log',  # Set the log file path here
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def calculate_metrics(self, campaigns_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate key performance metrics for campaigns
        """
        try:
            # Check for required columns
            required_columns = {'Clicks', 'Impressions', 'Revenue', 'Spend', 'Conversions'}
            if not required_columns.issubset(campaigns_df.columns):
                missing_columns = required_columns - set(campaigns_df.columns)
                raise ValueError(f"Missing required columns in campaign data: {missing_columns}")
            
            # Calculate Click-Through Rate (CTR)
            campaigns_df['CTR'] = campaigns_df['Clicks'] / campaigns_df['Impressions']
            
            # Calculate Return on Ad Spend (ROAS)
            campaigns_df['ROAS'] = campaigns_df.apply(
                lambda x: x['Revenue'] / x['Spend'] if x['Spend'] > 0 else 0, axis=1
            )
            
            # Calculate Cost Per Acquisition (CPA)
            campaigns_df['CPA'] = campaigns_df.apply(
                lambda x: x['Spend'] / x['Conversions'] if x['Conversions'] > 0 else 0, axis=1
            )
            
            self.logger.info("Successfully calculated campaign metrics")
            return campaigns_df
        
        except Exception as e:
            self.logger.error(f"Error calculating metrics: {e}")
            raise

    def analyze_trends(self, historical_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze trends from historical data
        """
        try:
            # Check for required columns
            required_columns = {'Campaign_ID', 'Conversions', 'ROAS'}
            if not required_columns.issubset(historical_df.columns):
                missing_columns = required_columns - set(historical_df.columns)
                raise ValueError(f"Missing required columns in historical data: {missing_columns}")
            
            # Group by campaign and calculate week-over-week changes
            weekly_trends = historical_df.groupby('Campaign_ID').agg({
                'Conversions': 'mean',
                'ROAS': 'mean'
            })
            
            insights = {
                'avg_conversions': weekly_trends['Conversions'].mean(),
                'avg_roas': weekly_trends['ROAS'].mean(),
                'top_performing_campaigns': weekly_trends.nlargest(3, 'ROAS').index.tolist()
            }
            
            self.logger.info("Successfully analyzed campaign trends")
            return insights
        
        except Exception as e:
            self.logger.error(f"Error analyzing trends: {e}")
            raise
