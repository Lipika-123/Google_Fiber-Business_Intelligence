# Initial Setup and Data Loading
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input/google-fiber'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

df = pd.read_csv("/kaggle/input/google-fiber/Google_Fiber.csv")
df.head()

# EXPLORATORY DATA ANALYSIS (INITIAL INVESTIGATION

df.info()
df.columns
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())
print("\nBasic Statistics:\n", df.describe())

# DATA PREPROCESSING
## Handling Date Column
# Convert date_created to datetime
df['date_created'] = pd.to_datetime(df['date_created'])

# Extract temporal features
df['year'] = df['date_created'].dt.year
df['month'] = df['date_created'].dt.month
df['quarter'] = df['date_created'].dt.quarter
df['day_of_week'] = df['date_created'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

## Handling missing value
contact_cols = [col for col in df.columns if 'contacts_n' in col]
df[contact_cols] = df[contact_cols].fillna(0)

# FEATURE ENGINEERING
contact_cols = ['contacts_n', 'contacts_n_1', 'contacts_n_2', 'contacts_n_3', 
                'contacts_n_4', 'contacts_n_5', 'contacts_n_6', 'contacts_n_7']
# Key FCR(First Contact Resolution) metrics
df['total_contacts'] = df[contact_cols].sum(axis=1)
df['is_repeat_caller'] = (df['total_contacts'] > 1).astype(int)
df['repeat_contact_count'] = df[contact_cols[1:]].sum(axis=1)  # Exclude first contact
df['fcr_success'] = (df['total_contacts'] == 1).astype(int)  # Perfect FCR
df['escalation_occurred'] = (df[['contacts_n_6', 'contacts_n_7']].sum(axis=1) > 0).astype(int)

# Contact sequence analysis
df['max_contact_sequence'] = 0
for i, col in enumerate(contact_cols):
    df.loc[df[col] > 0, 'max_contact_sequence'] = i + 1

# Time-based features for repeat patterns
df['contact_gap_days'] = np.nan
for i in range(1, 8):
    current_col = f'contacts_n_{i}' if i > 0 else 'contacts_n'
    prev_col = f'contacts_n_{i-1}' if i > 1 else 'contacts_n'
    # This would ideally come from timestamps of each contact

# REPEAT CALLER PATTERN ANALYSIS
# Overall FCR metrics
fcr_rate = df['fcr_success'].mean() * 100
repeat_rate = df['is_repeat_caller'].mean() * 100
escalation_rate = df['escalation_occurred'].mean() * 100

print(f"=== FCR PERFORMANCE ===")
print(f"First Contact Resolution Rate: {fcr_rate:.1f}%")
print(f"Repeat Caller Rate: {repeat_rate:.1f}%")
print(f"Escalation Rate: {escalation_rate:.1f}%")
print(f"Average contacts per case: {df['total_contacts'].mean():.2f}")

# Repeat caller severity analysis
repeat_cases = df[df['is_repeat_caller'] == 1]
print(f"\nRepeat cases analysis ({len(repeat_cases)} cases):")
print(f"Average repeat contacts: {repeat_cases['repeat_contact_count'].mean():.2f}")
print(f"Maximum repeat contacts: {repeat_cases['repeat_contact_count'].max()}")

# ROOT CAUSE ANALYSIS BY ISSUE TYPE AND MARKET
# FCR performance by issue type
fcr_by_type = df.groupby('new_type').agg({
    'fcr_success': 'mean',
    'is_repeat_caller': 'mean',
    'total_contacts': 'mean',
    'escalation_occurred': 'mean',
    'date_created': 'count'
}).round(3)

fcr_by_type.columns = ['fcr_rate', 'repeat_rate', 'avg_contacts', 'escalation_rate', 'case_count']
fcr_by_type = fcr_by_type.sort_values('repeat_rate', ascending=False)

print("=== WORST PERFORMING ISSUE TYPES ===")
print(fcr_by_type.head(10))

# FCR performance by market
fcr_by_market = df.groupby('new_market').agg({
    'fcr_success': 'mean',
    'is_repeat_caller': 'mean',
    'total_contacts': 'mean'
}).round(3)

fcr_by_market.columns = ['fcr_rate', 'repeat_rate', 'avg_contacts']
fcr_by_market = fcr_by_market.sort_values('repeat_rate', ascending=False)

print("\n=== WORST PERFORMING MARKETS ===")
print(fcr_by_market.head())

# VISUALIZATION FOR REPEAT CALLERS PATTERN
plt.figure(figsize=(15, 12))

# 1. FCR Rate by Issue Type
plt.subplot(3, 2, 1)
top_issues = fcr_by_type.nlargest(10, 'case_count')
plt.barh(range(len(top_issues)), top_issues['fcr_rate'])
plt.yticks(range(len(top_issues)), top_issues.index)
plt.title('FCR Rate by Issue Type (Top 10 by Volume)')
plt.xlabel('FCR Rate')

# 2. Repeat Caller Rate by Issue Type
plt.subplot(3, 2, 2)
high_repeat_issues = fcr_by_type.nlargest(10, 'repeat_rate')
plt.barh(range(len(high_repeat_issues)), high_repeat_issues['repeat_rate'])
plt.yticks(range(len(high_repeat_issues)), high_repeat_issues.index)
plt.title('Highest Repeat Caller Rates by Issue Type')
plt.xlabel('Repeat Caller Rate')

# 3. Contact Distribution
plt.subplot(3, 2, 3)
contact_distribution = df['total_contacts'].value_counts().sort_index()
plt.bar(contact_distribution.index, contact_distribution.values)
plt.title('Distribution of Total Contacts per Case')
plt.xlabel('Number of Contacts')
plt.ylabel('Number of Cases')

# 4. Escalation Analysis
plt.subplot(3, 2, 4)
escalation_by_type = fcr_by_type.nlargest(10, 'escalation_rate')
plt.barh(range(len(escalation_by_type)), escalation_by_type['escalation_rate'])
plt.yticks(range(len(escalation_by_type)), escalation_by_type.index)
plt.title('Highest Escalation Rates by Issue Type')
plt.xlabel('Escalation Rate')

# 5. Temporal Trends in Repeat Calls
plt.subplot(3, 2, 5)
monthly_trends = df.groupby(df['date_created'].dt.to_period('M')).agg({
    'fcr_success': 'mean',
    'is_repeat_caller': 'mean'
}).reset_index()
monthly_trends['date_created'] = monthly_trends['date_created'].astype(str)

x = range(len(monthly_trends))
plt.plot(x, monthly_trends['fcr_success'], label='FCR Rate', marker='o')
plt.plot(x, monthly_trends['is_repeat_caller'], label='Repeat Rate', marker='o')
plt.xticks(x, monthly_trends['date_created'], rotation=45)
plt.title('Monthly FCR and Repeat Caller Trends')
plt.legend()

# 6. Correlation Heatmap
plt.subplot(3, 2, 6)
correlation_data = df[['total_contacts', 'is_repeat_caller', 'escalation_occurred']]
sns.heatmap(correlation_data.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Correlation: Contacts vs Repeat vs Escalation')

plt.tight_layout()
plt.show()

# DEEP DIVE INTO REPEAT CALLER ROOT CAUSES
# Analyze what drives repeat calls
repeat_cases = df[df['is_repeat_caller'] == 1]

# Most common issue types among repeat callers
repeat_issue_patterns = repeat_cases['new_type'].value_counts().head(10)
print("=== MOST COMMON ISSUES AMONG REPEAT CALLERS ===")
print(repeat_issue_patterns)

# Market patterns for repeat calls
repeat_market_patterns = repeat_cases['new_market'].value_counts().head(10)
print("\n=== MARKETS WITH MOST REPEAT CALLS ===")
print(repeat_market_patterns)

# Severity analysis - cases with 3+ contacts
severe_repeat_cases = df[df['total_contacts'] >= 3]
print(f"\n=== SEVERE CASES (3+ CONTACTS): {len(severe_repeat_cases)} CASES ===")
print("Top issue types in severe cases:")
print(severe_repeat_cases['new_type'].value_counts().head(5))

# ACTIONABLE INSIGHTS AND RECOMMENDATION
# Generate actionable insights
worst_fcr_issues = fcr_by_type.nsmallest(5, 'fcr_rate')
worst_repeat_issues = fcr_by_type.nlargest(5, 'repeat_rate')
worst_escalation_issues = fcr_by_type.nlargest(5, 'escalation_rate')

print("=== ACTIONABLE RECOMMENDATIONS ===")
print("\n1. PRIORITY ISSUES FOR FCR IMPROVEMENT:")
for issue, row in worst_fcr_issues.iterrows():
    print(f"   - {issue}: FCR Rate {row['fcr_rate']*100:.1f}%, {row['case_count']} cases")

print("\n2. HIGHEST REPEAT CALL DRIVERS:")
for issue, row in worst_repeat_issues.iterrows():
    print(f"   - {issue}: Repeat Rate {row['repeat_rate']*100:.1f}%")

print("\n3. FREQUENT ESCALATION ISSUES:")
for issue, row in worst_escalation_issues.iterrows():
    print(f"   - {issue}: Escalation Rate {row['escalation_rate']*100:.1f}%")

# Calculate potential impact
total_repeat_contacts = repeat_cases['repeat_contact_count'].sum()
potential_savings = total_repeat_contacts * 0.5  # Assuming 0.5 hours saved per contact

print(f"\n4. BUSINESS IMPACT:")
print(f"   - Total repeat contacts: {total_repeat_contacts}")
print(f"   - Estimated agent hours wasted: {total_repeat_contacts * 0.5:.0f} hours")
print(f"   - Potential cost savings (est.): ${total_repeat_contacts * 25:,.0f}")

# DASHBOARD READY METRICS EXPORT
# Prepare data for dashboard
dashboard_data = {
    'overall_metrics': {
        'total_cases': len(df),
        'fcr_rate': fcr_rate,
        'repeat_rate': repeat_rate,
        'escalation_rate': escalation_rate,
        'avg_contacts': df['total_contacts'].mean()
    },
    'by_issue_type': fcr_by_type.reset_index(),
    'by_market': fcr_by_market.reset_index(),
    'repeat_caller_analysis': repeat_cases[['new_type', 'new_market', 'total_contacts', 'repeat_contact_count']],
    'temporal_trends': monthly_trends
}

# Export for dashboard
pd.DataFrame([dashboard_data['overall_metrics']]).to_csv('fcr_overall_metrics.csv', index=False)
dashboard_data['by_issue_type'].to_csv('fcr_by_issue_type.csv', index=False)
dashboard_data['by_market'].to_csv('fcr_by_market.csv', index=False)

print("\nDashboard data exported successfully!")
print("Key files created: fcr_overall_metrics.csv, fcr_by_issue_type.csv, fcr_by_market.csv")
