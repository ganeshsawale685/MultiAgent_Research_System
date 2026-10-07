from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint , ChatHuggingFace
from tools import web_search,scrape_url
from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(model='openai/gpt-oss-120b')

#1st Agent 

def build_search_agent(): return create_agent( model=llm, tools=[web_search], system_prompt="""You are a web research search agent. Your task is to search for relevant and reliable information using the web_search tool. Rules: - You can ONLY use the web_search tool. - Never call web_open, browser, open_url, or any other tool. - Do not try to open URLs yourself. - Use web_search to find relevant information. - Return the search results with titles, URLs, and snippets. - Do not invent information. """ )
#2nd Agent

def build_reader_agent():
    return create_agent(model=llm,tools=[scrape_url])


#Write Chain or say runnable

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic chain : for improvement

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])


critic_chain = critic_prompt | llm | StrOutputParser()

