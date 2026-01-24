### E-Commerce Data Analysis

## Data Assumptions:
# One row = one completed order
# All prices are in USD
# Orders without price or timestamp are invalid

## Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

## Load data from the excel file and inspect the data.
raw_df = pd.read_excel('data/gamezone-orders-data.xlsx')
df = raw_df.copy()
#df.shape
#df.columns
#df.head()
#df.info()

## Data Cleaning 

## Exact duplicate rows were identified and removed. 
# df.duplicated().sum()
# df = df.drop_duplicates()

## Duplicates based on the 'ORDER_ID' column were also dropped. 
df['ORDER_ID'].duplicated().sum()
df[df['ORDER_ID'].duplicated(keep=False)][['ORDER_ID', 'ACCOUNT_CREATION_METHOD', 'USD_PRICE']]
df = df.drop_duplicates(subset='ORDER_ID')


## After identifying the missing data, I dropped the rows that had null values in either the 'USD_PRICE' or 'COUNTRY_CODE' columns. I then filled the missing values in the 'MARKETING_CHANNEL' & 'ACCOUNT_CREATION_METHOD' rows with 'unknown'.

# print(df.isna().sum())
df = df.dropna(subset=['USD_PRICE', 'COUNTRY_CODE'])
df = df.fillna('unknown')

## Extreme outliers were omitted. A histogram was used to understand the skew. 
Q1 = df['USD_PRICE'].quantile(0.25)
Q3 = df['USD_PRICE'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

#df2 = df[df['USD_PRICE'] > upper]
#x = df2['USD_PRICE'].value_counts().sort_index()
#plt.hist(df2['USD_PRICE'], bins=50)
#plt.xlabel("Price (USD)")
#plt.title("Game Zone Price Distribution")
#plt.ylabel("Number of Orders")
#plt.show()

df = df[(df['USD_PRICE'] >= lower) & (df['USD_PRICE'] <= upper)]

## Corrected the Data Type for the 'PURCHASE_TS' column.
df['PURCHASE_TS'] = pd.to_datetime(df['PURCHASE_TS'], errors='coerce')
df = df.dropna(subset=['PURCHASE_TS'])

## Final Checks
# df.isna().sum()
# df.duplicated().sum()
# df['ORDER_ID'].duplicated().sum()

#df.info()

clean_df = df.copy()

## Cleaned Data Overview

clean_data_overview = pd.DataFrame({
    "metric":[
        "rows",
        "duplicate_orders",
        "null_price",
        "null_purchase_ts",
        "unknown_marketing_channel"
    ],

    "value": [
        clean_df.shape[0],
        clean_df['ORDER_ID'].duplicated().sum(),
        clean_df['USD_PRICE'].isna().sum(),
        clean_df['PURCHASE_TS'].isna().sum(),
        (clean_df['MARKETING_CHANNEL'] == 'unknown').sum()
    ]
})

# print(clean_data_overview)

### Analysis of Cleaned Data
## KPI Metrics

kpis = pd.DataFrame({
    "metric": [
        "Total Orders",
        "Total Revenue (USD)",
        "Average Order Value (USD)",
        "Unique Customers",
        "Orders per Customer"
    ],
    "value": [
        clean_df['ORDER_ID'].nunique(),
        clean_df['USD_PRICE'].sum(),
        clean_df['USD_PRICE'].mean(),
        clean_df['USER_ID'].nunique(),
        clean_df['ORDER_ID'].nunique() / clean_df['USER_ID'].nunique()
    ]
})

kpis['value'] = kpis['value'].map('{:,.2f}'.format)

print(kpis)

## Revenue trends over time
clean_df['purchase_date'] = clean_df['PURCHASE_TS'].dt.date
clean_df['purchase_month'] = clean_df['PURCHASE_TS'].dt.to_period('M')
clean_df['purchase_year'] = clean_df['PURCHASE_TS'].dt.to_period('Y')

yearly_revenue = (
    clean_df
    .groupby('purchase_year')['USD_PRICE']
    .sum()
    .reset_index()
)

yearly_revenue['purchase_year'] = yearly_revenue['purchase_year'].astype(str)
plt.figure(figsize=(10,5))
plt.bar(yearly_revenue['purchase_year'], yearly_revenue['USD_PRICE'])
plt.title("Yearly Revenue Over Time")
plt.xlabel("Date")
plt.ylabel("Revenue (USD)")
plt.tight_layout()

plt.savefig("charts/yearly_revenue.png")
plt.close()

monthly_revenue = (
    clean_df
    .groupby('purchase_month')['USD_PRICE']
    .sum()
    .reset_index()
)

monthly_revenue['purchase_month'] = monthly_revenue['purchase_month'].astype(str)
plt.figure(figsize=(10,5))
plt.plot(monthly_revenue['purchase_month'], monthly_revenue['USD_PRICE'], marker='o')
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (USD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/monthly_revenue.png")
plt.close()


## Channel Summary

channel_summary = (
    clean_df
    .groupby('MARKETING_CHANNEL')
    .agg(
        orders=('ORDER_ID', 'count'),
        revenue=('USD_PRICE', 'sum'),
        avg_order_value=('USD_PRICE', 'mean')
    )
    .sort_values('revenue', ascending=False)
)

print(channel_summary)

monthly_revenue_by_channel = (
    clean_df
    .groupby(['purchase_month', 'MARKETING_CHANNEL'])['USD_PRICE']
    .sum()
    .reset_index()
)

monthly_revenue_by_channel_pivot=(
    monthly_revenue_by_channel.pivot(
        index='purchase_month',
        columns='MARKETING_CHANNEL',
        values='USD_PRICE'
    )
    .fillna(0)
)

monthly_revenue_by_channel_pivot.index = (
    monthly_revenue_by_channel_pivot.index.astype(str)
)
plt.figure(figsize=(20,6))

monthly_revenue_by_channel_pivot.plot(
    kind='bar',
    stacked=True
)

plt.title("Monthly Revenue by Marketing Channel")
plt.xlabel("Month")
plt.ylabel("Revenue (USD)")
plt.xticks(rotation=45)
plt.legend(
    title="Marketing Channel",
    loc="upper left"
)
plt.tight_layout()

plt.savefig("charts/monthly_revenue_by_channel.png")
plt.close()
