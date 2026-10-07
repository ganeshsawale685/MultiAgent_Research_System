from agents import build_reader_agent,build_search_agent,writer_chain,critic_chain
from rich import print

def run_research_pipeline(topic : str)->dict:

    state ={}

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages":[("user",f"Find recent,reliable and detailed information about : {topic}")]
    })

    state['search_result'] = search_result['messages'][-1].content

    # step 2 --reader agent

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_result'][:800]}"
        )]
    })

    state['reader_result'] = reader_result['messages'][-1].content

    # print(state['reader_result'])

    # Step 3 write chain

    research_combined = (
        f'Search Results : \n {state["search_result"]} \n \n '
        f'Detailed Scraped content :\n {state['reader_result']}' 
    )

    state["report"] =writer_chain.invoke({
        "topic" : topic,
        "research":research_combined
    })

    print("\n Final Report \n ",state['report'])


    # Critic Report 


    state['feedback']=critic_chain.invoke({
        "report":state['report'][:8000]
    })

   
    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)