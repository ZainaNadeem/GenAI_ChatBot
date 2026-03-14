# BCG GenAI Financial Chatbot

A full-stack AI-powered chatbot that enables natural language queries on SEC 10-K financial filings for Microsoft, Tesla and Apple.

<img src="https://github.com/user-attachments/assets/f463b87f-9177-46d2-8d54-996183df1e8a" width="900" />



## Description

Built as part of the BCG GenAI consulting simulation, this project transforms raw SEC filing data into an interactive financial intelligence terminal. Users can query revenue, net income, cash flow, growth trends and company comparisons using plain English.



## Features

- **Natural Language Queries:** rule-based NLP engine maps plain English to financial data retrieval
- **SEC 10-K Data Pipeline:** 45 data points extracted from 9 annual filings across 3 companies
- **Growth Analysis:** year-over-year trend calculation for any metric
- **Company Comparisons:** ranks companies by any financial metric for any fiscal year
- **UI:** scrolling ticker, live data cards, financial terminal aesthetic
- **REST API:** FastAPI backend with automatic Swagger documentation at `/docs`


## Technologies

- **Python 3.11**
  - Core programming language for data pipeline, NLP logic and API
- **Pandas**
  - Data extraction, cleaning and financial metric calculations
- **Matplotlib & Seaborn**
  - Financial data visualizations and trend charts
- **FastAPI**
  - REST API backend with automatic OpenAPI documentation
- **Uvicorn**
  - ASGI server for running the FastAPI application
- **React + Vite**
  - Frontend chat interface with hot module replacement
- **IBM Plex Mono / IBM Plex Sans**
  - Typography chosen for financial terminal aesthetic


## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+

### 1. Clone the repository
```bash
git clone https://github.com/ZainaNadeem/GenAI_ChatBot.git
cd GenAI_ChatBot
```

### 2. Set up Python environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas matplotlib seaborn fastapi uvicorn python-multipart
```

### 3. Start the backend
```bash
cd backend
uvicorn main:app --reload
```
API runs at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

### 4. Start the frontend
```bash
cd frontend
npm install
npm run dev
```
UI runs at `http://localhost:5173`


## Data Sources

All financial data extracted manually from SEC EDGAR:
- [Microsoft 10-K Filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000789019&type=10-K)
- [Tesla 10-K Filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001318605&type=10-K)
- [Apple 10-K Filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=10-K)

