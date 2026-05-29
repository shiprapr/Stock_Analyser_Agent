from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.tavily import TavilyTools


# Create agent
financial_ai_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),

    tools=[
        TavilyTools(),

        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            income_statements=True,
            company_news=True,
            company_info=True,
        )
    ],

    instructions=[
        "Use Tavily for latest news and web information.",
        "Use YFinanceTools for financial data.",
        "Always provide sources."
    ],

    markdown=True,
)


# Streamlit UI
st.set_page_config(
    page_title="AI Stock Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Stock Analyzer")
st.write("Ask anything about stocks, companies, financials, and latest market news.")

# User input
query = st.text_input(
    "Enter your question:",
    placeholder="Example: What is the current stock price of Meta and latest news?"
)

# Button
if st.button("Analyze"):

    if query:

        with st.spinner("Analyzing stock data..."):

            try:
                response = financial_ai_agent.run(query)

                st.markdown(response.content)

            except Exception as e:
                st.error(f"Error: {str(e)}")