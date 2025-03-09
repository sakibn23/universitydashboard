import streamlit as st
import plotly.express as px
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('university_student_dashboard_data.csv')

# Create a dictionary to map terms to month names
term_month_year_map = {
    'Spring': 'May',
    'Fall': 'November'
}

# Create `Term Date` column using the mapping
term_date_df = df.copy()
term_date_df['Term Date'] = term_date_df['Year'].astype(str) + '-' + term_date_df['Term'].map(term_month_year_map)
term_date_df['Term Date'] = pd.to_datetime(term_date_df['Term Date'], format='%Y-%B')

# Calculate overall retention rate
overall_retention_rate = (df['Enrolled'].sum() / df['Admitted'].sum()) * 100

# Reshape the dataframe to combine the enrollment data for all departments into a single column
melted_df = term_date_df.melt(
    id_vars=['Year', 'Term', 'Term Date', 'Retention Rate (%)
