import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
import litellm
from tools import search_tool, scraper_tool

load_dotenv()
litellm.drop_params = True
os.environ["LITELLM_PROMPT_CACHING"] = "false"

# LLM
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"), 
    temperature=0
)

def run_procurement_crew(company_name, industry, budget, purpose, requirements):
    company_context = f"""
    Company Name: {company_name}
    Industry: {industry}
    Budget: ${budget}
    Purpose: {purpose}
    Requirements: {requirements}
    Important: Selected products must fit within the budget.
    """

    # Agents 
    search_agent = Agent(
        role="Product Search Specialist",
        goal="Find the best products based on company requirements.",
        backstory="You are an expert procurement specialist.",
        llm=llm, tools=[search_tool], verbose=False, allow_delegation=False, max_iter=3,
    )
    scraper_agent = Agent(
        role="Product Data Collection Specialist",
        goal="Collect detailed product information from websites.",
        backstory="You verify product information and collect structured data.",
        llm=llm, tools=[scraper_tool], verbose=False, allow_delegation=False, max_iter=3,
    )
    analysis_agent = Agent(
        role="Procurement Analysis Specialist",
        goal="Compare and rank products based on requirements and value.",
        backstory="You are an expert procurement analyst.",
        llm=llm, verbose=False, allow_delegation=False, max_iter=3,
    )
    report_agent = Agent(
        role="Procurement Report Writer",
        goal="Generate a professional HTML procurement report.",
        backstory="You create business-ready procurement reports.",
        llm=llm, verbose=False, allow_delegation=False, max_iter=3,
    )

    # Tasks
    search_task = Task(
        description=f"""Company Context: {company_context}
        Search the web using Tavily. Find the best 2 products under budget.
        For each: Product Name, Price, Key Specifications, Website URL. Be concise.""",
        expected_output="Markdown table with Product Name, Price, Specs, URL.",
        agent=search_agent,
    )
    scraping_task = Task(
        description="""Use the Product Page Scraper tool on the URLs from the previous task.
        Extract: Name, Price, RAM, Storage, Processor, Battery, Camera, Display, URL.
        If missing, write "Not found". Return structured data.""",
        expected_output="Structured list with detailed specifications.",
        agent=scraper_agent, context=[search_task],
    )
    analysis_task = Task(
        description=f"""Analyze the collected product info. Company Requirements: {company_context}
        Compare based on Price, Specs, Value for money. Rank best to worst. Be concise.""",
        expected_output="Ranked comparison table with scores and recommendation.",
        agent=analysis_agent, context=[scraping_task],
    )
    output_file = "procurement_report.html"
    report_task = Task(
        description="""Create a professional procurement report from the analysis.
        Include: Executive Summary, Company Requirements, Product Comparison,
        Recommended Product, Reasons for Selection.
        Output raw valid HTML only. No markdown fences. Use inline CSS. Be concise.""",
        expected_output="A complete HTML procurement report.",
        agent=report_agent, context=[analysis_task], output_file=output_file,
    )

    # Crew 
    crew = Crew(
        agents=[search_agent, scraper_agent, analysis_agent, report_agent],
        tasks=[search_task, scraping_task, analysis_task, report_task],
        process=Process.sequential, verbose=False, cache=False,
    )

    try:
        crew.kickoff()
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                return "The report has been successfully generated!", f.read()
        else:
            return "The report could not be found.", "<h3>No report generated</h3>"
    except Exception as e:
        return f"An error occurred: {str(e)}", f"<h3>Error: {str(e)}</h3>"