# Finance Tracker

A simple and interactive finance tracker application built with Streamlit.

## Description

This application allows you to track your income and expenses. You can add new transactions, view a summary of your financial activity within a specified date range, and visualize your income and expenses over time with a line chart and a pie chart for expense analysis.

## Features

- Add new income and expense transactions.
- View transactions within a selected date range.
- See a summary of total income, total expenses, and net savings.
- Visualize income and expenses over time with a line chart.
- Analyze expenses by category with a pie chart.

## Project Structure

- `main.py`: The main application file containing the Streamlit UI and all the application logic.
- `finance_data.csv`: The CSV file where all the transaction data is stored.
- `README.md`: This file.

## Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib

## Setup and Usage

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/finance-tracker.git
    cd finance-tracker
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**

    ```bash
    streamlit run main.py
    ```

    The application will open in your web browser.
