import pandas as pd

def create_user_data_frame(users_data: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(users_data)

def create_browsing_history_data_frame(browsing_data: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(browsing_data)

def create_purchase_data_frame(purchase_data: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(purchase_data)

def create_product_data_frame(product_data: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(product_data)
