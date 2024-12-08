import json
import logging
import pandas as pd
import os
from typing import Dict, List

class ActionExecutor:
    def __init__(self, config_path='config/settings.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename='logs/marketing_automation.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def execute_actions(self, campaigns_df: pd.DataFrame, actions: Dict[str, List[Dict]]) -> pd.DataFrame:
        """
        Execute campaign actions based on AI recommendations
        """
        try:
            # Validate campaigns_df columns
            required_columns = ['Campaign_ID', 'Spend', 'Status']
            if not all(col in campaigns_df.columns for col in required_columns):
                raise ValueError(f"Missing required columns in campaigns DataFrame: {required_columns}")

            # Validate actions structure
            if not isinstance(actions, dict):
                raise ValueError("Actions should be a dictionary with the expected format.")

            # Apply actions
            for campaign_type, campaign_list in actions.items():
                for campaign in campaign_list:
                    campaign_id = campaign['Campaign_ID']
                    mask = campaigns_df['Campaign_ID'] == campaign_id

                    if campaign_type == 'pause_campaigns':
                        campaigns_df.loc[mask, 'Status'] = 'Paused'
                    elif campaign_type == 'increase_budget':
                        # Simulate budget increase by 20%
                        campaigns_df.loc[mask, 'Spend'] *= 1.2
                    elif campaign_type == 'decrease_budget':
                        # Simulate budget decrease by 20%
                        campaigns_df.loc[mask, 'Spend'] *= 0.8

            self.logger.info("Successfully executed campaign actions")
            return campaigns_df

        except Exception as e:
            self.logger.error(f"Error executing actions: {e}")
            raise

    def save_updated_campaigns(self, campaigns_df: pd.DataFrame, filename: str = 'campaigns_updated.csv') -> None:
        """
        Save the updated campaigns DataFrame to a CSV file in the 'data/' folder.
        If the file already exists, it will be overwritten.
        """
        try:
            # Ensure 'data/' folder exists
            if not os.path.exists('data'):
                print("Creating 'data/' folder...")  # Debugging print
                os.makedirs('data')

            file_path = f'data/{filename}'

            # Save the updated DataFrame to CSV (overwrite if file exists)
            campaigns_df.to_csv(file_path, index=False)
            self.logger.info(f"Successfully saved updated campaigns to {file_path}")
            print(f"File successfully saved to {file_path}")  # Debugging print

        except Exception as e:
            self.logger.error(f"Error saving updated campaigns to CSV: {e}")
            raise

# Example usage
if __name__ == "__main__":
    executor = ActionExecutor()

    # Simulate loading campaigns data (this would normally be done in a different class)
    campaigns_df = pd.DataFrame({
        'Campaign_ID': [1, 2, 3],
        'Spend': [1000, 1500, 2000],
        'Status': ['Active', 'Active', 'Active']
    })

    # Define actions (this would come from the AI agent or decision process)
    actions = {
        'pause_campaigns': [{'Campaign_ID': 1}],
        'increase_budget': [{'Campaign_ID': 2}],
        'decrease_budget': [{'Campaign_ID': 3}]
    }

    # Execute actions
    updated_campaigns_df = executor.execute_actions(campaigns_df, actions)

    # Save updated campaigns to CSV
    executor.save_updated_campaigns(updated_campaigns_df)
