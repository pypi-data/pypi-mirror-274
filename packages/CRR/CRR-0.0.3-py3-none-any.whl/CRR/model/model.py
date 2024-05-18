import pandas as pd
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
import numpy as np

def get_rfm(customers_df: pd.DataFrame, products_df: pd.DataFrame, orders_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Recency, Frequency, and Monetary values for each customer and assign RFM scores.
    
    Parameters:
        customers_df (DataFrame): Contains customer data with at least 'CustomerID'.
        products_df (DataFrame): Contains product data with at least 'ProductID'.
        orders_df (DataFrame): Contains order data with 'OrderDate', 'CustomerID', 'ProductID', 'Price', and 'Quantity'.

    Returns:
        DataFrame: A DataFrame with each customer's RFM scores and metrics, merged with the customer information.
    """
    
   
    orders_df['OrderDate'] = pd.to_datetime(orders_df['OrderDate'], errors='coerce')
    orders_df.dropna(subset=['OrderDate'], inplace=True)  # Handle missing dates

    orders_df = orders_df.merge(customers_df, on="CustomerID", how='inner')
    orders_df = orders_df.merge(products_df, on="ProductID", how='inner')

    
    orders_df['TotalPrice'] = orders_df['Price'] * orders_df['Quantity']

    
    current_date = datetime.now()
    rfm_table = orders_df.groupby('CustomerID').agg({
        'OrderDate': lambda x: (current_date - x.max()).days,
        'OrderID': 'count',
        'TotalPrice': 'sum'
    }).rename(columns={'OrderDate': 'Recency', 'OrderID': 'Frequency', 'TotalPrice': 'Monetary'})

    
    rfm_table['R_Score'] = pd.qcut(rfm_table['Recency'], 4, labels=range(4, 0, -1))
    rfm_table['F_Score'] = pd.qcut(rfm_table['Frequency'].rank(method='first'), 4, labels=range(1, 5))
    rfm_table['M_Score'] = pd.qcut(rfm_table['Monetary'].rank(method='first'), 4, labels=range(1, 5))
    rfm_table['RFM_Score'] = rfm_table['R_Score'].astype(str) + rfm_table['F_Score'].astype(str) + rfm_table['M_Score'].astype(str)

    
    customer_rfm = customers_df.merge(rfm_table, on='CustomerID', how='inner')
    return customer_rfm
    




def get_clusters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply K-Means clustering to customer data based on RFM metrics and save the results.

    Parameters:
        df (DataFrame): Customer data with RFM metrics.

    Returns:
        DataFrame: Updated customer data including cluster assignments.
    """

    imputer = SimpleImputer(strategy='mean')
    rfm = df[['Recency', 'Frequency', 'Monetary']]
    rfm_imputed = imputer.fit_transform(rfm)

    # Standardize the data
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_imputed)

    for k in range(3, 7):
        kmeans = KMeans(n_clusters=k, random_state=1)
        df['Cluster'] = kmeans.fit_predict(rfm_scaled)
        cluster_summary = df.groupby('Cluster').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': ['mean', 'count']
        }).round(2)
        print(f"Cluster Summary for {k} Clusters:")
        print(cluster_summary)
        print("\n")

    
    k_selected = 5 
    kmeans = KMeans(n_clusters=k_selected, random_state=1)
    df['Cluster'] = kmeans.fit_predict(rfm_scaled)
    df = df[['CustomerID','Recency','Frequency','Monetary','R_Score','F_Score','M_Score','RFM_Score','Cluster']]
    df.to_csv("data/Customer_RFM_Clusters.csv", index=False)
    return df

def classify_churn_risk(rfm_table: pd.DataFrame) -> pd.DataFrame:
    """
    Classify customers into churn risk levels based on their RFM scores.

    Parameters:
        rfm_table (DataFrame): Data with RFM scores.

    Returns:
        DataFrame: Data updated with a 'ChurnRiskLevel' column.
    """    
    
    conditions = [
        (rfm_table['R_Score'] <= 2) & (rfm_table['F_Score'] <= 2) & (rfm_table['M_Score'] <= 2),
        (rfm_table['R_Score'] >= 3)
    ]
    # Labels for risk levels
    values = ['High Risk', 'Low Risk']
    default_value = 'Medium Risk'
    
    # Create a new column for churn risk level
    rfm_table['ChurnRiskLevel'] = np.select(conditions, values, default=default_value)
    rfm_table.to_csv('data/Modeling.csv', index = False)
    return rfm_table


def churn_rate_by_risk_level(rfm_table: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate churn rates by risk level based on customer churn risk classification.

    Parameters:
        rfm_table (DataFrame): Data with churn risk levels.

    Returns:
        DataFrame: Churn rate percentages by churn risk level.
    """    
    
    risk_level_summary = rfm_table.groupby('ChurnRiskLevel').agg({
        'CustomerID': 'count'
    }).rename(columns={'CustomerID': 'Count'})
    total_customers = rfm_table['CustomerID'].count()
    risk_level_summary['ChurnRate'] = (risk_level_summary['Count'] / total_customers) * 100
    risk_level_summary['ChurnRate'] = risk_level_summary['ChurnRate'].round(2)
    
    risk_level_summary[['ChurnRate']].to_csv("data/ChurnRate.csv")
    return risk_level_summary[['ChurnRate']]