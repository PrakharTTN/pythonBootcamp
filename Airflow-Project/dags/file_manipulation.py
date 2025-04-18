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


def load_excel():
    """Load the Excel file into a DataFrame."""
    df = pd.read_excel(excel_path)
    return df


def preprocess_data(df):
    """Preprocess the DataFrame (e.g., drop null values, etc.)."""
    df["Date Purchased"] = pd.to_datetime(df["Date Purchased"])
    df["Quantity"] = pd.to_numeric(df["Quantity"])
    df["Purchased Price"] = pd.to_numeric(df["Purchased Price"])
    df["Current Price"] = pd.to_numeric(df["Current Price"])
    return df


def add_series(df):
    """Add additional columns or series to the DataFrame."""
    df["Purchased Value"] = df["Purchased Price"] * df["Quantity"].round(2)
    df["Current Value"] = df["Current Price"] * df["Quantity"].round(2)
    df["Profit"] = df["Current Value"] - df["Purchased Value"].round(2)
    df["ROI"] = ((df["Profit"] / df["Purchased Value"]) * 100).round(2)
    df["Portfolio Percentage"] = (
        (df["Current Value"] / df["Current Value"].sum()) * 100
    ).round(2)
    return df


def generate_plots(df):
    """Generate pie chart and bar charts based on the provided data."""

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

    rank_by_roi = df.sort_values(by="ROI", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(rank_by_roi["Stock Name"], rank_by_roi["ROI"], color="blue")
    ax.set_title("Stocks Ranked by ROI")
    ax.set_xlabel("Stock Name")
    ax.set_ylabel("ROI (%)")
    roi_ranked_chart_path = "/tmp/roi_ranked_chart.png"
    plt.savefig(roi_ranked_chart_path)
    plt.close()

    return (
        pie_chart_path,
        top_gainers_chart_path,
        top_losers_chart_path,
        roi_ranked_chart_path,
    )


def create_pdf(
    pie_chart_path,
    top_gainers_chart_path,
    top_losers_chart_path,
    roi_ranked_chart_path,
    df,
):
    """Create a PDF report containing the charts and data."""
    c = canvas.Canvas(output_pdf_path, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Stock Portfolio Analysis Report")

    c.drawImage(pie_chart_path, 100, 500, width=400, height=300)

    c.drawImage(top_gainers_chart_path, 100, 200, width=400, height=200)

    c.drawImage(top_losers_chart_path, 100, 0, width=400, height=200)

    c.showPage()
    c.drawImage(roi_ranked_chart_path, 100, 500, width=400, height=200)

    c.setFont("Helvetica", 12)
    c.drawString(100, 480, "Data Overview:")
    text = c.beginText(100, 460)
    for row in df.head(5).values:
        text.textLine(str(row))
    c.drawText(text)

    c.save()

    os.remove(pie_chart_path)
    os.remove(top_gainers_chart_path)
    os.remove(top_losers_chart_path)
    os.remove(roi_ranked_chart_path)


def process_excel(**kwargs):
    """Main function to process the Excel file."""
    df = load_excel()
    df_cleaned = preprocess_data(df)
    df_with_series = add_series(df_cleaned)
    (
        pie_chart_path,
        top_gainers_chart_path,
        top_losers_chart_path,
        roi_ranked_chart_path,
    ) = generate_plots(df_with_series)
    create_pdf(
        pie_chart_path,
        top_gainers_chart_path,
        top_losers_chart_path,
        roi_ranked_chart_path,
        df_with_series,
    )


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 4, 17),
    "retries": 1,
}


dag = DAG(
    "excel_data_analysis",
    default_args=default_args,
    description="A DAG to process Excel data, generate plots, and create PDF reports.",
    schedule_interval=None,
    catchup=False,
)

start_task = EmptyOperator(
    task_id="start",
    dag=dag,
)

process_task = PythonOperator(
    task_id="process_excel_task",
    python_callable=process_excel,
    provide_context=True,
    dag=dag,
)
end_task = EmptyOperator(
    task_id="end",
    dag=dag,
)
(start_task >> process_task >> end_task)
