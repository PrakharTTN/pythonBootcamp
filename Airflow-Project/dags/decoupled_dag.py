"""Better version of the previous excel file manipulator, earlier tasks were tightly coupled, and the new dataframe were being returned each time, here using xcom to communicate with the process helps in reusing the df after manipulation"""

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

# File paths
excel_path = "/home/prakhar/Downloads/STICKS.xlsx"
output_pdf_path = "/home/prakhar/Downloads/report.pdf"


def load_excel(**kwargs):
    """Load the Excel file into a DataFrame."""
    df = pd.read_excel(excel_path)
    kwargs["ti"].xcom_push(key="df", value=df)


def preprocess_data(**kwargs):
    """Preprocess the DataFrame (e.g., drop null values, etc.)."""
    df = kwargs["ti"].xcom_pull(key="df", task_ids="load_excel")
    df["Date Purchased"] = pd.to_datetime(df["Date Purchased"])
    df["Quantity"] = pd.to_numeric(df["Quantity"])
    df["Purchased Price"] = pd.to_numeric(df["Purchased Price"])
    df["Current Price"] = pd.to_numeric(df["Current Price"])
    kwargs["ti"].xcom_push(key="df_cleaned", value=df)


def add_series(**kwargs):
    """Add additional columns or series to the DataFrame."""
    df = kwargs["ti"].xcom_pull(key="df_cleaned", task_ids="preprocess_data")
    df["Purchased Value"] = df["Purchased Price"] * df["Quantity"].round(2)
    df["Current Value"] = df["Current Price"] * df["Quantity"].round(2)
    df["Profit"] = df["Current Value"] - df["Purchased Value"].round(2)
    df["ROI"] = ((df["Profit"] / df["Purchased Value"]) * 100).round(2)
    df["Portfolio Percentage"] = (
        (df["Current Value"] / df["Current Value"].sum()) * 100
    ).round(2)
    kwargs["ti"].xcom_push(key="df_with_series", value=df)


def generate_plots(**kwargs):
    """Generate pie chart and bar charts based on the provided data."""
    df = kwargs["ti"].xcom_pull(key="df_with_series", task_ids="add_series")

    # Pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = plt.cm.Paired(range(len(df)))
    ax.pie(
        df["Current Value"],
        labels=df["Stock Name"],
        startangle=140,
        autopct="%1.2f%%",
        wedgeprops={"edgecolor": "black", "linewidth": 1, "linestyle": "solid"},
    )
    ax.set_title(
        "Stock Contribution in Portfolio", fontsize=16, fontweight="bold", color="black"
    )
    pie_chart_path = "/tmp/pie_chart.png"
    plt.savefig(pie_chart_path)
    plt.close()

    # Top gainers chart
    top_gainer_stocks = df.nlargest(5, "Profit")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        top_gainer_stocks["Stock Name"], top_gainer_stocks["Profit"], color=["green"]
    )
    ax.set_title("Top 5 Most Profitable Stocks")
    ax.set_xlabel("Stock Name")
    ax.set_ylabel("Profit")
    top_gainers_chart_path = "/tmp/top_gainers_chart.png"
    plt.savefig(top_gainers_chart_path)
    plt.close()

    # Top losers chart
    negative_stocks = df[df["Current Value"] < df["Purchased Value"]]
    top_loser_stocks = negative_stocks.nsmallest(5, "Profit")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_loser_stocks["Stock Name"], top_loser_stocks["Profit"], color=["red"])
    ax.set_title("Top 5 Most Losing Stocks")
    ax.set_xlabel("Stock Name")
    ax.set_ylabel("Profit")
    top_losers_chart_path = "/tmp/top_losers_chart.png"
    plt.savefig(top_losers_chart_path)
    plt.close()

    # ROI ranked chart
    rank_by_roi = df.sort_values(by="ROI", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(rank_by_roi["Stock Name"], rank_by_roi["ROI"], color="blue")
    ax.set_title("Stocks Ranked by ROI")
    ax.set_xlabel("Stock Name")
    ax.set_ylabel("ROI (%)")
    roi_ranked_chart_path = "/tmp/roi_ranked_chart.png"
    plt.savefig(roi_ranked_chart_path)
    plt.close()

    kwargs["ti"].xcom_push(
        key="chart_paths",
        value={
            "pie_chart": pie_chart_path,
            "top_gainers_chart": top_gainers_chart_path,
            "top_losers_chart": top_losers_chart_path,
            "roi_ranked_chart": roi_ranked_chart_path,
        },
    )


def create_pdf(**kwargs):
    """Create a PDF report containing the charts and data."""
    chart_paths = kwargs["ti"].xcom_pull(key="chart_paths", task_ids="generate_plots")
    df = kwargs["ti"].xcom_pull(key="df_with_series", task_ids="add_series")

    c = canvas.Canvas(output_pdf_path, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Stock Portfolio Analysis Report")

    # Add charts to the PDF
    c.drawImage(chart_paths["pie_chart"], 100, 500, width=400, height=300)
    c.drawImage(chart_paths["top_gainers_chart"], 100, 200, width=400, height=200)
    c.drawImage(chart_paths["top_losers_chart"], 100, 0, width=400, height=200)

    c.showPage()
    c.drawImage(chart_paths["roi_ranked_chart"], 100, 500, width=400, height=200)

    # Add data overview
    c.setFont("Helvetica", 12)
    c.drawString(100, 480, "Data Overview:")
    text = c.beginText(100, 460)
    for row in df.head(5).values:
        text.textLine(str(row))
    c.drawText(text)

    c.save()

    # Clean up chart images
    os.remove(chart_paths["pie_chart"])
    os.remove(chart_paths["top_gainers_chart"])
    os.remove(chart_paths["top_losers_chart"])
    os.remove(chart_paths["roi_ranked_chart"])


# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 4, 17),
    "retries": 1,
}

dag = DAG(
    "decoupled_excel_analysis",
    default_args=default_args,
    description="A DAG to process Excel data, generate plots, and create PDF reports.",
    schedule_interval=None,
    catchup=False,
)

start_task = EmptyOperator(
    task_id="start",
    dag=dag,
)

# Tasks
load_task = PythonOperator(
    task_id="load_excel",
    python_callable=load_excel,
    provide_context=True,
    dag=dag,
)

preprocess_task = PythonOperator(
    task_id="preprocess_data",
    python_callable=preprocess_data,
    provide_context=True,
    dag=dag,
)

add_series_task = PythonOperator(
    task_id="add_series",
    python_callable=add_series,
    provide_context=True,
    dag=dag,
)

generate_plots_task = PythonOperator(
    task_id="generate_plots",
    python_callable=generate_plots,
    provide_context=True,
    dag=dag,
)

create_pdf_task = PythonOperator(
    task_id="create_pdf",
    python_callable=create_pdf,
    provide_context=True,
    dag=dag,
)

end_task = EmptyOperator(
    task_id="end",
    dag=dag,
)

# Task dependencies
(
    start_task
    >> load_task
    >> preprocess_task
    >> add_series_task
    >> generate_plots_task
    >> create_pdf_task
    >> end_task
)
