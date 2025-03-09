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
    id_vars=['Year', 'Term', 'Term Date'],
    value_vars=['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled'],
    var_name='Department',
    value_name='Department Enrolled'
)

# Create a Streamlit dashboard
st.title("University Admissions and Satisfaction Dashboard")

# Create a sidebar with filters
st.sidebar.header("Filters")
selected_years = st.sidebar.multiselect("Select Year", melted_df['Year'].unique())
selected_terms = st.sidebar.multiselect("Select Term", melted_df['Term'].unique())

# Filter the data based on selected years and terms
filtered_df = melted_df.copy()
if selected_years:
    filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]
if selected_terms:
    filtered_df = filtered_df[filtered_df['Term'].isin(selected_terms)]

# Display the overall retention rate as a metric
st.metric("Overall Retention Rate", f"{overall_retention_rate:.2f}%")

# Plot the retention rate trend over time
retention_trend = filtered_df.groupby('Term Date')['Retention Rate (%)'].mean().reset_index()
fig_retention = px.line(retention_trend, x='Term Date', y='Retention Rate (%)', title="Retention Rate Over Time")
st.plotly_chart(fig_retention)

# Plot the student satisfaction trend over time
satisfaction_trend = filtered_df.groupby('Term Date')['Student Satisfaction (%)'].mean().reset_index()
fig_satisfaction = px.line(satisfaction_trend, x='Term Date', y='Student Satisfaction (%)', title="Student Satisfaction Over Time")
st.plotly_chart(fig_satisfaction)

# Plot the enrollment breakdown by department
enrollment_department = filtered_df.groupby('Department')['Department Enrolled'].sum().reset_index()
fig_enrollment_department = px.bar(enrollment_department, x='Department', y='Department Enrolled', title="Enrollment by Department")
st.plotly_chart(fig_enrollment_department)

# Compare the Spring and Fall trends
spring_fall_comparison = filtered_df.groupby(['Year', 'Term'])['Department Enrolled'].mean().reset_index()
fig_spring_fall = px.bar(spring_fall_comparison, x='Year', y='Department Enrolled', color='Term', barmode='group', title="Spring vs. Fall Enrollment")
st.plotly_chart(fig_spring_fall)

# Compare the trends between departments, retention rates, and satisfaction levels
dept_comparison = filtered_df.groupby('Department')[['Retention Rate (%)', 'Student Satisfaction (%)']].mean().reset_index()
fig_dept_comparison = px.scatter(dept_comparison, x='Retention Rate (%)', y='Student Satisfaction (%)', color='Department', title="Retention vs. Satisfaction by Department")
st.plotly_chart(fig_dept_comparison)
