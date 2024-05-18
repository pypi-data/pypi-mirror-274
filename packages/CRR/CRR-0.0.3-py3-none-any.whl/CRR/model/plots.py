import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Plot 1: Distribution of RFM Scores

def plot_rfm_distributions(data: pd.DataFrame)-> None:
    """
    Visualizes the distribution of RFM scores across customers.

    Parameters:
        data (DataFrame): DataFrame containing 'R_Score', 'F_Score', and 'M_Score' columns.

    Description:
        This function creates histograms for Recency, Frequency, and Monetary scores, 
        providing a visual distribution which helps in understanding the spread and skewness of these scores.
    """    
    # Load the data from the given CSV file path
    

    # Set up the plotting environment
    fig, ax = plt.subplots(1, 3, figsize=(18, 6))

    # Plot for Recency Scores
    sns.histplot(data=data, x='R_Score', bins=5, kde=False, ax=ax[0])
    ax[0].set_title('Distribution of Recency Scores')
    ax[0].set_xlabel('Recency Score')
    ax[0].set_ylabel('Count')

    # Plot for Frequency Scores
    sns.histplot(data=data, x='F_Score', bins=5, kde=False, ax=ax[1])
    ax[1].set_title('Distribution of Frequency Scores')
    ax[1].set_xlabel('Frequency Score')
    ax[1].set_ylabel('Count')

    # Plot for Monetary Scores
    sns.histplot(data=data, x='M_Score', bins=5, kde=False, ax=ax[2])
    ax[2].set_title('Distribution of Monetary Scores')
    ax[2].set_xlabel('Monetary Score')
    ax[2].set_ylabel('Count')

    plt.tight_layout()
    plt.show()

# Plot 2: Distribution of RFM Scores
def cluster_p(data: pd.DataFrame) -> None:
    """
    Plot the distribution of customers across different clusters.

    Parameters:
        data (DataFrame): DataFrame containing the 'Cluster' column.

    Description:
        This function creates a count plot that shows how many customers belong to each cluster,
        helping to visualize the balance or imbalance between clusters.
    """    

    plt.figure(figsize=(10, 6))
    sns.countplot(x='Cluster', data=data)
    plt.title('Customer Distribution by Cluster')
    plt.xlabel('Cluster')
    plt.ylabel('Number of Customers')
    plt.show()


def age_dist_per_cluster(data: pd.DataFrame) -> None:
    """
    Visualizes the age distribution within each cluster.

    Parameters:
        data (DataFrame): DataFrame containing 'Cluster' and 'Age' columns.

    Description:
        This function uses a boxplot to display the spread and central tendency of age within each cluster.
    """    
    # Load the data from the given CSV file path
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Cluster', y='Age', data=data)
    plt.title('Age Distribution per Cluster')
    plt.xlabel('Cluster')
    plt.ylabel('Age')
    plt.show()


# Plot 4
def rfm_plots(data: pd.DataFrame) -> None:
    """
    Plot the relationship between Recency and Monetary values colored by Cluster.

    Parameters:
        data (DataFrame): DataFrame containing 'Recency', 'Monetary', and 'Cluster' columns.

    Description:
        This function creates a scatter plot to explore potential correlations between Recency and Monetary values,
        with points colored by cluster to highlight differences between clusters.
    """    
# Load the data
    

    # Filter out any rows with missing values in the columns you're interested in

    # Setting up the plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Recency vs Monetary
    scatter = ax.scatter(data['Recency'], data['Monetary'], c=data['Cluster'], cmap='viridis', alpha=0.6, edgecolors='w')
    ax.set_xlabel('Recency')
    ax.set_ylabel('Monetary')
    ax.set_title('Recency vs Monetary')

    # Create a legend
    legend = ax.legend(*scatter.legend_elements(), title="Clusters")
    ax.add_artist(legend)

    plt.tight_layout()
    plt.show()


def RiskLevelPlot(data: pd.DataFrame) -> None:
    """
    Displays a stacked bar plot of Churn Risk Level distribution within each cluster.

    Parameters:
        data (DataFrame): DataFrame with 'Cluster' and 'ChurnRiskLevel' columns.

    Description:
        This function aggregates data by Cluster and ChurnRiskLevel, then visualizes it in a stacked bar plot,
        providing insights into the risk distribution within each cluster.
    """    
    # Set the aesthetic style of the plots
    sns.set_style("whitegrid")
    
    # Prepare the data: sum counts for each combination of Cluster and ChurnRiskLevel
    data_count = data.groupby(['Cluster', 'ChurnRiskLevel']).size().unstack(fill_value=0)

    # Create a stacked bar plot
    plt.figure(figsize=(10, 6))
    data_count.plot(kind='bar', stacked=True, colormap='viridis', figsize=(10, 6))
    plt.xlabel('Cluster')
    plt.ylabel('Count')
    plt.title('Stacked Bar Plot of Cluster by Churn Risk Level')
    plt.xticks(rotation=45)
    plt.legend(title='Churn Risk Level', loc='upper right')
    plt.tight_layout()
    plt.show()

