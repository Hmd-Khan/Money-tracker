# Import necessary libraries
import pandas as pd
import streamlit as st
import csv
from datetime import datetime
import matplotlib.pyplot as plt

# A class to handle CSV file operations
class CSV:
    """
    A class to handle CSV file operations such as initializing the file,
    adding new entries, and retrieving transactions within a date range.
    """
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d.%m.%Y"

    @classmethod
    def initialize_csv(cls):
        """
        Initializes the CSV file if it does not exist.
        """
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        """
        Adds a new transaction entry to the CSV file.
        """
        new_entry = {
            "date": date.strftime(cls.FORMAT),
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """
        Retrieves transactions from the CSV file within a specified date range.
        """
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]
        return filtered_df

def plot_transactions(df):
    """
    Plots income and expenses over time.
    """
    if df.empty:
        return

    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")["amount"]
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")["amount"]
        .sum()
        .reindex(df.index, fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(income_df.index, income_df, label="Income", color="g")
    ax.plot(expense_df.index, expense_df, label="Expense", color="r")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount")
    ax.set_title("Income and Expenses Over Time")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

def plot_expense_analysis(df):
    """
    Plots a pie chart of expenses by category.
    """
    if df.empty:
        return

    expense_df = df[df["category"] == "Expense"]
    if expense_df.empty:
        st.write("No expenses to analyze.")
        return

    expense_by_category = expense_df.groupby("description")["amount"].sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    expense_by_category.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90)
    ax.set_ylabel("")
    ax.set_title("Expense Analysis by Category")
    st.pyplot(fig)

def main():
    """
    The main function that runs the Streamlit application.
    """
    st.set_page_config(page_title="Finance Tracker", layout="wide")
    st.title("Finance Tracker")

    # Initialize the CSV file
    CSV.initialize_csv()

    # Sidebar for adding new transactions
    st.sidebar.header("Add a New Transaction")
    date = st.sidebar.date_input("Date", datetime.today())
    amount = st.sidebar.number_input("Amount", min_value=0.01, step=0.01)
    category = st.sidebar.selectbox("Category", ["Income", "Expense"])
    description = st.sidebar.text_input("Description")

    if st.sidebar.button("Add Transaction"):
        CSV.add_entry(date, amount, category, description)
        st.sidebar.success("Transaction added successfully!")

    # Main content for viewing transactions
    st.header("View Transactions")
    start_date = st.date_input("Start Date", datetime.today().replace(day=1))
    end_date = st.date_input("End Date", datetime.today())

    if start_date > end_date:
        st.error("Error: Start date cannot be after end date.")
    else:
        df = CSV.get_transactions(start_date, end_date)
        if df.empty:
            st.write("No transactions found in the selected date range.")
        else:
            st.write(f"Transactions from {start_date.strftime('%d.%m.%Y')} to {end_date.strftime('%d.%m.%Y')}")
            st.dataframe(df)

            # Calculate and display summary
            total_income = df[df["category"] == "Income"]["amount"].sum()
            total_expense = df[df["category"] == "Expense"]["amount"].sum()
            net_savings = total_income - total_expense

            st.subheader("Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"${total_income:,.2f}")
            col2.metric("Total Expense", f"${total_expense:,.2f}")
            col3.metric("Net Savings", f"${net_savings:,.2f}")

            # Display plots
            st.subheader("Transaction Plot")
            plot_transactions(df.copy())

            st.subheader("Expense Analysis")
            plot_expense_analysis(df.copy())

if __name__ == "__main__":
    main()
