import os
import sys

from application.exception import BackorderException
from application.util.utililty import load_object

import pandas as pd


class BackorderData:

    def __init__(self,
                    national_inv:float,
                    lead_time:float,
                    in_transit_qty:float,
                    forecast_3_m:float,
                    forecast_6_m:float,
                    forecast_9_m:float,
                    sales_1_m:float,
                    sales_3_m:float,
                    sales_6_m:float,
                    sales_9_m:float,
                    min_bank:float,
                    pieces_past_due:float,
                    Perf_6_Month_Avg:float,
                    Perf_12_Month_Avg:float,
                    Local_Bo_Qty:float,
                    Potential_Issue:str,
                    Deck_Risk:str,
                    OE_Constraint:str,
                    PPAP_Risk:str,
                    Stop_Auto_Buy:str,
                    Rev_Stop:str,
                    went_on_backorder:str = None
                 ):
        try:
            
            self.national_inv = national_inv
            self.lead_time = lead_time
            self.in_transit_qty = in_transit_qty
            self.forecast_3_m = forecast_3_m
            self.forecast_6_m = forecast_6_m
            self.forecast_9_m = forecast_9_m
            self.sales_1_m = sales_1_m
            self.sales_3_m = sales_3_m
            self.sales_6_m = sales_6_m
            self.sales_9_m = sales_9_m
            self.min_bank = min_bank
            self.pieces_past_due = pieces_past_due
            self.Perf_6_Month_Avg = Perf_6_Month_Avg
            self.Perf_12_Month_Avg = Perf_12_Month_Avg
            self.Local_Bo_Qty = Local_Bo_Qty
            self.Potential_Issue = Potential_Issue
            self.Deck_Risk = Deck_Risk
            self.OE_Constraint = OE_Constraint
            self.PPAP_Risk = PPAP_Risk
            self.Stop_Auto_Buy = Stop_Auto_Buy
            self.Rev_Stop = Rev_Stop
            self.went_on_backorder = went_on_backorder
        except Exception as e:
            raise BackorderException(e, sys) from e

    def get_backorder_input_data_frame(self):

        try:
            housing_input_dict = self.get_backorder_data_as_dict()
            return pd.DataFrame(housing_input_dict)
        except Exception as e:
            raise BackorderException(e, sys) from e

    def get_backorder_data_as_dict(self):
        try:
            input_data = {
                "national_inv":[self.national_inv],
                "lead_time":[self.lead_time],
                "in_transit_qty":[self.in_transit_qty],
                "forecast_3_m":[self.forecast_3_m],
                "forecast_6_m":[self.forecast_6_m],
                "forecast_9_m":[self.forecast_9_m],
                "sales_1_m":[self.sales_1_m],
                "sales_3_m":[self.sales_3_m],
                "sales_6_m":[self.sales_6_m],
                "sales_9_m":[self.sales_9_m],
                "min_bank":[self.min_bank],
                "pieces_past_due":[self.pieces_past_due],
                "Perf_6_Month_Avg":[self.Perf_6_Month_Avg],
                "Perf_12_Month_Avg":[self.Perf_12_Month_Avg],
                "Local_Bo_Qty":[self.Local_Bo_Qty],
                "Potential_Issue":[self.Potential_Issue],
                "Deck_Risk":[self.Deck_Risk],
                "OE_Constraint":[self.OE_Constraint],
                "PPAP_Risk":[self.PPAP_Risk],
                "Stop_Auto_Buy":[self.Stop_Auto_Buy],
                "Rev_Stop":[self.Rev_Stop],
                "went_on_backorder":[self.went_on_backorder]}


            return input_data
        except Exception as e:
            raise BackorderException(e, sys)


class BackOrderPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise BackorderException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            print(latest_model_path)
            return latest_model_path
        except Exception as e:
            raise BackorderException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            value = model.predict(X)
            return value
        except Exception as e:
            raise BackorderException(e, sys) from e