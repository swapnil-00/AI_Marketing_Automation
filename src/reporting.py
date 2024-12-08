import json
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
import os

class Reporting:
    def __init__(self, config_path='config/settings.json'):
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON in config file: {config_path}")
        
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename='logs/marketing_automation.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def generate_report(self, campaigns_df: pd.DataFrame, actions: Dict[str, List[Dict]], insights: Dict[str, Any]) -> None:
        """
        Generate a comprehensive marketing automation report
        """
        try:
            # Validate campaigns_df for required columns
            required_columns = ['Spend', 'Revenue', 'ROAS', 'CTR']
            if not all(col in campaigns_df.columns for col in required_columns):
                raise ValueError(f"Missing required columns in campaigns DataFrame: {required_columns}")

            # Construct the report
            report = {
                'timestamp': datetime.now().isoformat(),
                'total_campaigns': len(campaigns_df),
                'campaign_actions': actions,
                'campaign_insights': insights,
                'performance_summary': {
                    'total_spend': campaigns_df['Spend'].sum(),
                    'total_revenue': campaigns_df['Revenue'].sum(),
                    'average_roas': campaigns_df['ROAS'].mean(),
                    'average_ctr': campaigns_df['CTR'].mean()
                }
            }

            # Save the report
            report_path = self.config.get('reporting', {}).get('report_path', 'reports/marketing_report.json')
            os.makedirs(os.path.dirname(report_path), exist_ok=True)  # Ensure directory exists

            with open(report_path, 'w') as f:
                json.dump(report, f, indent=4)

            self.logger.info(f"Report generated and saved to {report_path}")

        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            raise
