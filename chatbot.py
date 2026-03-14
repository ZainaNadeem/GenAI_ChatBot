"""
BCG GenAI Financial Chatbot
Task 2 - Rule-Based Financial Chatbot

Description:
    An AI-powered chatbot that answers natural language queries
    about financial performance of Microsoft, Tesla and Apple
    based on 10-K filings for FY2021-2023.

Supported query types:
    - Metric lookup: revenue, net income, assets, liabilities, cash flow
    - Growth trends: year-over-year change for any metric
    - Comparisons: best performing company for any metric in any year

Usage:
    python chatbot.py

Limitations:
    - Only covers Microsoft, Tesla and Apple
    - Data limited to FY2021-2023
    - Rule-based NLP — does not understand complex sentences
    - Cannot handle multiple companies in one query

Author: BCG GenAI Consulting Team
"""

import pandas as pd

# Load financial data from Task 1
from pathlib import Path
BASE_DIR = Path(__file__).parent
df = pd.read_csv(BASE_DIR / 'financial_data.csv')

print("Financial data loaded successfully")
print(f"Companies available: {list(df['Company'].unique())}")
print(f"Years available: {list(df['Fiscal Year'].unique())}")


# DATA LOOKUP FUNCTIONS
def get_metric(company, year, metric):
    """Fetch a specific metric for a company and year."""
    row = df[
        (df['Company'].str.lower() == company.lower()) &
        (df['Fiscal Year'] == int(year))
    ]
    if row.empty:
        return None
    return row[metric].values[0]


def get_all_years(company, metric):
    """Fetch a metric across all years for a company."""
    rows = df[df['Company'].str.lower() == company.lower()]
    if rows.empty:
        return None
    return dict(zip(rows['Fiscal Year'], rows[metric]))


def get_best_company(metric, year):
    """Find which company had the highest value for a metric in a given year."""
    rows = df[df['Fiscal Year'] == int(year)]
    if rows.empty:
        return None
    best_idx = rows[metric].idxmax()
    return rows.loc[best_idx, 'Company'], rows.loc[best_idx, metric]


def calculate_growth(company, metric):
    """Calculate year-over-year growth for a metric."""
    rows = df[df['Company'].str.lower() == company.lower()].sort_values('Fiscal Year')
    if len(rows) < 2:
        return None
    results = {}
    for i in range(1, len(rows)):
        prev = rows.iloc[i-1][metric]
        curr = rows.iloc[i][metric]
        year = rows.iloc[i]['Fiscal Year']
        growth = ((curr - prev) / prev) * 100
        results[int(year)] = round(growth, 2)
    return results

# QUERY UNDERSTANDING
def extract_company(text):
    """Detect which company the user is asking about."""
    text = text.lower()
    if 'microsoft' in text:
        return 'Microsoft'
    elif 'tesla' in text:
        return 'Tesla'
    elif 'apple' in text:
        return 'Apple'
    return None


def extract_year(text):
    """Detect which year the user is asking about."""
    for year in ['2021', '2022', '2023']:
        if year in text:
            return int(year)
    # If no year mentioned default to most recent
    return 2023


def extract_metric(text):
    """Detect which financial metric the user is asking about."""
    text = text.lower()
    if any(word in text for word in ['revenue', 'sales', 'income total']):
        return 'Total Revenue', 'Total Revenue'
    elif any(word in text for word in ['net income', 'profit', 'earnings']):
        return 'Net Income', 'Net Income'
    elif any(word in text for word in ['assets', 'asset']):
        return 'Total Assets', 'Total Assets'
    elif any(word in text for word in ['liabilities', 'liability', 'debt']):
        return 'Total Liabilities', 'Total Liabilities'
    elif any(word in text for word in ['cash flow', 'cfo', 'operating']):
        return 'CFO', 'Cash Flow from Operations'
    return None, None


def detect_intent(text):
    """Detect what kind of question the user is asking."""
    text = text.lower()
    if any(word in text for word in ['compare', 'vs', 'versus', 'better', 'best', 'highest', 'most', 'fastest']):
        return 'compare'
    elif any(word in text for word in ['help', 'what can', 'how do', 'questions']):
        return 'help'
    elif any(word in text for word in ['bye', 'exit', 'quit', 'goodbye']):
        return 'exit'
    elif any(word in text for word in ['growth', 'change', 'trend', 'increased', 
                                        'decreased', 'grew', 'grow', 'growing', 
                                        'over time', 'history', 'progress']):
        return 'growth'
    else:
        return 'lookup'
    
# RESPONSE BUILDER 
def build_response(user_input):
    """Build a natural language response to the user's query."""
    
    intent = detect_intent(user_input)
    company = extract_company(user_input)
    year = extract_year(user_input)
    metric_col, metric_label = extract_metric(user_input)

    # HELP 
    if intent == 'help':
        return """I can answer the following types of questions:

  📊 Metric lookup:
     "What is Microsoft's total revenue in 2023?"
     "What was Apple's net income in 2022?"
     "Show me Tesla's cash flow in 2021"

  📈 Growth trends:
     "How did Microsoft's revenue grow?"
     "Show Tesla's net income trend"

  🏆 Comparisons:
     "Which company had the highest revenue in 2023?"
     "Who was most profitable in 2022?"

  Type 'bye' to exit."""

    # EXIT 
    if intent == 'exit':
        return "exit"

    # COMPARISON 
    if intent == 'compare':
        if metric_col is None:
            metric_col = 'Total Revenue'
            metric_label = 'Total Revenue'
        best_company, best_value = get_best_company(metric_col, year)
        all_values = get_all_years_all_companies(metric_col, year)
        response = f"In FY{year}, comparing {metric_label} across all companies:\n"
        for comp, val in sorted(all_values.items(), key=lambda x: x[1], reverse=True):
            marker = " ← highest" if comp == best_company else ""
            response += f"  • {comp}: ${val:,.0f}M{marker}\n"
        return response.strip()

    # GROWTH TREND 
    if intent == 'growth':
        if company is None:
            return "Please specify a company — Microsoft, Tesla or Apple."
        if metric_col is None:
            metric_col = 'Total Revenue'
            metric_label = 'Total Revenue'
        growth = calculate_growth(company, metric_col)
        if growth is None:
            return f"Sorry, I couldn't calculate growth for {company}."
        response = f"{company} {metric_label} growth:\n"
        for yr, pct in growth.items():
            direction = "▲" if pct > 0 else "▼"
            response += f"  {direction} FY{yr}: {pct:+.1f}%\n"
        return response.strip()

    # SPECIFIC LOOKUP 
    if intent == 'lookup':
        if company is None:
            return "Please specify a company - Microsoft, Tesla or Apple."
        if metric_col is None:
            return f"I can look up: total revenue, net income, total assets, total liabilities, or cash flow. What would you like to know about {company}?"
        value = get_metric(company, year, metric_col)
        if value is None:
            return f"Sorry, I don't have {metric_label} data for {company} in FY{year}."
        return f"{company} {metric_label} in FY{year}: ${value:,.0f}M (USD Millions)"

    return "Sorry, I didn't understand that. Type 'help' to see what I can answer."

def get_all_years_all_companies(metric, year):
    """Fetch a metric for all companies in a given year."""
    rows = df[df['Fiscal Year'] == int(year)]
    return dict(zip(rows['Company'], rows[metric]))


# CONVERSATION LOOP
def run_chatbot():
    """Main conversation loop."""
    print("\n" + "="*55)
    print("  BCG GenAI — Financial Analysis Chatbot")
    print("  Data: Microsoft, Tesla, Apple | FY2021-2023")
    print("="*55)
    print("  Type 'help' to see what I can answer.")
    print("  Type 'bye' to exit.")
    print("="*55 + "\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        response = build_response(user_input)

        if response == "exit":
            print("Bot: Goodbye! Happy to help with financial analysis anytime.")
            break

        print(f"Bot: {response}\n")


# ENTRY POINT
if __name__ == "__main__":
    run_chatbot()