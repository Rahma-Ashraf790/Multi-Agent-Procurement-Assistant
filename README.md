# Multi-Agent Procurement Assistant

An AI-powered procurement assistant that automates researching, comparing, and recommending products based on a company's requirements and budget, then generates a ready-to-share HTML procurement report.

The system uses **four collaborating AI agents**, orchestrated with **CrewAI**, powered by **Groq (LLaMA 3.3 70B)**, with **Tavily** used for web search.

---

## Overview

Procurement decisions usually require manually searching the web, comparing specs across multiple product pages, and writing a recommendation report. This project automates the whole process end-to-end using a multi-agent pipeline that searches for candidate products, collects their detailed specifications, analyzes and ranks them against the company's needs, and produces a professional HTML report with a final recommendation.

---

## How It Works (Agents)

1. **Search Agent** — searches the web and finds candidate products that fit the company's budget.
2. **Scraper Agent** — visits the product pages and extracts detailed specifications (price, RAM, storage, battery, camera, etc.).
3. **Analysis Agent** — compares the products against the company's requirements and ranks them.
4. **Report Agent** — writes a professional HTML report summarizing the comparison and final recommendation.

The agents run sequentially, each one building on the previous agent's output.

---

## Tech Stack

- CrewAI — multi-agent orchestration
- Groq (LLaMA 3.3 70B) — the LLM powering the agents
- Tavily — web search API
- BeautifulSoup / requests — for scraping product pages
- Python

---

## How to Use

1. Add your Groq and Tavily API keys.
2. Update the company requirements section with your own budget, industry, and product needs.
3. Run the notebook. It will search, scrape, analyze, and generate the final report automatically.
4. The output is saved and displayed as an HTML procurement report with an executive summary, product comparison, and final recommendation.

---

## Example Output

Given a sample scenario (a $700 budget for engineer smartphones), the assistant compared two candidate phones and produced a full report including an executive summary, a ranked comparison table, and a final recommended product with the reasoning behind it.

---

## Notes & Limitations

- The number of products searched/scraped is kept small by default to control API usage and stay within rate limits.
- Scraping accuracy depends on how much structured data (meta tags) the target website provides.
- The pipeline is designed to run once per session to avoid unnecessary API calls.
