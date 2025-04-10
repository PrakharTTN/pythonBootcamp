from django.shortcuts import render
from django.http import HttpResponse
from .forms import PortfolioForm
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import redirect
from django.contrib import messages


def analyze_file(file_path):

    # Pre-process
    try:
        df = pd.read_excel(file_path)
        df["Date Purchased"] = pd.to_datetime(df["Date Purchased"])
        df["Quantity"] = pd.to_numeric(df["Quantity"])
        df["Purchased Price"] = pd.to_numeric(df["Purchased Price"])
        df["Current Price"] = pd.to_numeric(df["Current Price"])
        df.dropna(subset=["Purchased Price", "Current Price", "Quantity"], inplace=True)

        df["Purchased Value"] = df["Purchased Price"] * df["Quantity"]
        df["Current Value"] = df["Current Price"] * df["Quantity"]
        df["Profit"] = df["Current Value"] - df["Purchased Value"]
        df["ROI"] = ((df["Profit"] / df["Purchased Value"]) * 100).round(2)
        df["Portfolio Percentage"] = (
            (df["Current Value"] / df["Current Value"].sum()) * 100
        ).round(2)
        return df

    except:
        return None


def portfolio_view(request):

    if request.method == "POST" and request.FILES["portfolio_file"]:
        file = request.FILES["portfolio_file"]
        file_path = "uploaded_file.xlsx"
        with open(file_path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        df = analyze_file(file_path)
        if df is None:
            messages.error(
                request, "🚨 Bad Data Detected! Please Use Correct Format 🚨"
            )
            # return render(request, "upload_file.html", context=context)
            return redirect("portfolio:portfolio_upload")

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(
            df["Current Value"],
            labels=df["Stock Name"],
            startangle=140,
            autopct="%1.2f%%",
            wedgeprops={"edgecolor": "black", "linewidth": 1, "linestyle": "solid"},
        )
        ax.set_title(
            "Stock Contribution in Portfolio",
            fontsize=16,
            fontweight="bold",
            color="black",
        )

        pie_buffer = BytesIO()
        plt.savefig(pie_buffer, format="png")
        pie_buffer.seek(0)
        pie_chart_base64 = base64.b64encode(pie_buffer.read()).decode()

        top_gainer_stocks = df.nlargest(5, "Profit")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(
            top_gainer_stocks["Stock Name"], top_gainer_stocks["Profit"], color="green"
        )
        ax.set_title("Top 5 Most Profitable Stocks")
        ax.set_xlabel("Stock Name")
        ax.set_ylabel("Profit")

        bar_buffer = BytesIO()
        plt.savefig(bar_buffer, format="png")
        bar_buffer.seek(0)
        bar_chart_base64 = base64.b64encode(bar_buffer.read()).decode()

        negative_stocks = df[(df["Current Value"] < df["Purchased Value"])]
        top_loser_stocks = negative_stocks.nsmallest(5, "Profit")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(top_loser_stocks["Stock Name"], top_loser_stocks["Profit"], color="red")
        ax.set_title("Top 5 Most Losing Stocks")
        ax.set_xlabel("Stock Name")
        ax.set_ylabel("Profit")

        loser_buffer = BytesIO()
        plt.savefig(loser_buffer, format="png")
        loser_buffer.seek(0)
        loser_chart_base64 = base64.b64encode(loser_buffer.read()).decode()

        rank_by_roi = df.sort_values(by="ROI", ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(rank_by_roi["Stock Name"], rank_by_roi["ROI"], color="blue")
        ax.set_title("Stocks Ranked by ROI")
        ax.set_xlabel("Stock Name")
        ax.set_ylabel("ROI (%)")

        roi_buffer = BytesIO()
        plt.savefig(roi_buffer, format="png")
        roi_buffer.seek(0)
        roi_chart_base64 = base64.b64encode(roi_buffer.read()).decode()

        portfolio_summary = {
            "Total_Portfolio_Value": df["Current Value"].sum().round(2),
            "Total_Portfolio_Profit": df["Profit"].sum().round(2),
            "Portfolio_Return": (
                (df["Profit"].sum() / df["Purchased Value"].sum()) * 100
            ).round(2),
            "Top 5_Profitable_Stocks": top_gainer_stocks[
                ["Stock Name", "Profit"]
            ].to_html(classes="table table-striped"),
            "Top_5_Losing_Stocks": top_loser_stocks[["Stock Name", "Profit"]].to_html(
                classes="table table-striped"
            ),
        }

        return render(
            request,
            "portfolio_results.html",
            {
                "portfolio_summary": portfolio_summary,
                "pie_chart_base64": pie_chart_base64,
                "bar_chart_base64": bar_chart_base64,
                "loser_chart_base64": loser_chart_base64,
                "roi_chart_base64": roi_chart_base64,
                "df": df.sort_values(
                    by="Portfolio Percentage", ascending=False, ignore_index=True
                ).to_html(classes="table table-striped"),
            },
        )

    return render(request, "upload_file.html")
