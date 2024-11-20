import plotly.express as px

def create_heatmap_chart(df):
    fig = px.imshow(
        df.pivot_table(index='appointment_category', columns='experience_category', values='doctor_count',
                         fill_value=0),
        labels=dict(x="Doctor Experience (years)", y="Appointment Count Category"),
        color_continuous_scale='Viridis',
        title="Number of Doctors by Experience and Appointment Count"
    )

    fig.update_layout(
        xaxis_title="Doctor Experience (years)",
        yaxis_title="Appointment Count Category",
        coloraxis_colorbar=dict(title="Number of Doctors"),
        template="plotly_white",
        xaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3],
            ticktext=["0-5 years", "5-10 years", "10-15 years", "15+ years"]
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3, 4],
            ticktext=["0-5", "5-10", "10-20", "20-30", "30+"],
        )
    )

    return fig

def describe_to_table_heat(df):
    if df.empty:
        return []

    description = df.describe()

    description_reset = description.reset_index()

    description_reset.columns = ['Statistic'] + list(description.columns)

    table_data = description_reset.to_dict('records')

    return table_data