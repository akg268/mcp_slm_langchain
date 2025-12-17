from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient 
from langchain_ollama import ChatOllama
from langchain.messages import AIMessage
from langchain.messages import SystemMessage, HumanMessage
from ghdata import GhData
from langchain_core.messages import AIMessage

import chainlit as cl


@cl.on_chat_start
async def main():
    mcp_client = MultiServerMCPClient({
        "myorg-mcp-server":{
            "transport":"http",
            "url":"http://localhost:8000/mcp"
        }
    })

    tools = await mcp_client.get_tools()

    slm = ChatOllama(
        model = "llama3.2",
        temperature=0,
        verbose = True,
    )
    

    agent = create_agent(model=slm,tools=tools,response_format=GhData)
    cl.user_session.set("agent", agent)


    #response=  await agent.ainvoke({"messages":messages})
    #messages = response["messages"]

    #final_ai_message = next(
    #    msg for msg in reversed(messages)
     #   if isinstance(msg, AIMessage) and msg.content
    #)

    #print(final_ai_message.content)
    #return final_ai_message.content

@cl.on_message  
async def chat(message: cl.Message):
    history = []
    msg = cl.Message(content="")
    await msg.send()
    SYS_MSG = """
    You are a GitHub issue creation agent.
    You must follow this exact process:
    1. Call find_issue_category(issue_desc)
    2. Call assign_developer(category)
    3. Call create_github_issue(title, issue_desc, category, assigned_to)
    You are NOT allowed to answer in natural language.
    You MUST call tools in order.
    Do NOT explain your reasoning.
    """
    agent = cl.user_session.get("agent")
    sys_message = SystemMessage(content =SYS_MSG)
    history.append(HumanMessage(content=message.content))
    messages = [sys_message,*history]
    response=  await agent.ainvoke({"messages":messages})
    messages = response["messages"]
    history.clear()
    final_ai_message = next(
    msg for msg in reversed(messages)
     if isinstance(msg, AIMessage) and msg.content
    )
    print(final_ai_message.content)
    await msg.stream_token(final_ai_message.content)
    #print(final_ai_message.content)
    #return final_ai_message.content
     

#if __name__ == "__main__":
#   usrMsg = """
       # I have been trying to follow your tutorials they are working great but there are infrastructure issues. create an issue for that
 #      """
 #   asyncio.run(main(usrMsg))

