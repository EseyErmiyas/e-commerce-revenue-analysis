# E-Commerce Commercial Performance Analysis

# Overview

This project analyses e-commerce data to evaluate commercial performance, revenue trends, and marketing channel effectiveness. 

The goal is to understand how revenue is generated over time, identify key acquisition channels, and highlight areas where volatility and data limitations affect business insight.

The analysis focuses on core KPIs, time-based revenue trends, and marketing channel contribution, using Python (Pandas & Matplotlib) to produce clear, repeatable outputs.

# Key Insights
    # Monthly Revenue Trend
    charts/monthly_revenue.png

    # Revenue by Marketing Channel
    charts/monthly_revenue_by_channel.png

# Data Assumptions
    One row represents one completed order
    Orders without a valid price or purchase timestamp are excluded
    Missing marketing attribution is retained and labelled as unknown to preserve valid transactions

# Summary insight:
The dataset contains over 20,000 completed orders, generating $3.76M in revenue. Customers typically place just over one order each, indicating limited repeat purchasing and a largely transactional customer base.

# Revenue Trends Over Time
Revenue was analysed at multiple time frames. Daily revenue proved highly volatile and offered limited insight, so monthly aggregation was used as the primary trend indicator.

# Key observations:
    Monthly revenue shows an overall upward trajectory
    Performance is highly volatile, with significant spikes in specific periods
    Growth appears to be event-driven, rather than consistent or predictable month-to-month

This suggests that revenue performance is influenced by intermittent campaigns, promotions, or external factors rather than steady underlying demand.

# Marketing Channel Performance
# Key insights:
    Direct traffic dominates both order volume and revenue, indicating strong brand-led demand.
    Affiliate traffic produces the highest average order value, suggesting higher-intent customers despite lower volume.
    Email drives meaningful volume but with a lower average order value.
    A small but notable share of orders is attributed to unknown, highlighting incomplete marketing attribution and limiting full channel performance visibility.

# Channel Performance Over Time
Monthly revenue was further analysed by marketing channel using a stacked bar chart. This highlights how channel contribution shifts across periods and reinforces the finding that overall growth is driven by channel-specific spikes, rather than consistent performance across all acquisition sources.

# Tools & Techniques
    Python: Pandas, Matplotlib
    Data Cleaning: Deduplication, null handling, outlier removal (IQR method).
    Analysis: KPI calculation, time-series aggregation, channel performance analysis.
    Visualisation: Monthly revenue trends and stacked channel contribution charts.

# Key Takeaways
    Revenue growth exists but is volatile and event-driven.
    Business performance is heavily concentrated in a small number of channels.
    Channel quality varies significantly, as shown by differences in average order value.
    Incomplete attribution data limits full marketing effectiveness analysis.