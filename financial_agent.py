from dotenv import load_dotenv
load_dotenv()

from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
# from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.tavily import TavilyTools
import inspect
# from phi.tools.yfinance import YFinanceTools

# print(inspect.signature(YFinanceTools))

#web search tool
web_agent= Agent(
    name="Web search agent",
    model= Groq(id="llama-3.3-70b-versatile"),
    role="fetch latest information from the web",
    tools=[TavilyTools()],
    instructions="always provide sources references for the information you provide",
    show_tool_calls=True,
    markdown=True,
)

##financial data tool 
financial_agent=Agent(
    name="stock analysis agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools= [
        YFinanceTools(
            stock_price=True,
            analyst_recommendations= True,
            income_statements=True,
            company_news=True,
            company_info=True,
        )
    ],
    instructions=["use the tools to fetch financial data and provide analysis based on the latest information available",
                  "always cite the sources of the data you use in your analysis."],
    show_tool_calls=True,
    markdown=True,
)

## multi agent system 
financial_ai_system =Agent(
    team= [web_agent, financial_agent],
    model= Groq(id="llama-3.3-70b-versatile"),
    instructions = [
        "always provide sources references for the information.",
        "use the tools to fetch financial data and provide analysis based on the latest information available"
    ],
    show_tool_calls=True,
    markdown=True,

)

financial_ai_system.print_response(
    "What is the current stock price of meta and what are the latest news affecting its stock performance?",
    stream=False,
    )

