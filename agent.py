from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient 
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain.messages import AIMessage
from langchain.messages import SystemMessage, HumanMessage
from ghdata import GhData
from langchain_core.messages import AIMessage
from langchain_mcp_adapters.callbacks import Callbacks, CallbackContext
import json

import chainlit as cl


async def on_progress(
    progress: float,
    total: float | None,
    message: str | None,
    context: CallbackContext,
):
    """Handle progress updates from MCP servers."""
    percent = (progress / total * 100) if total else progress
    tool_info = f" ({context.tool_name})" if context.tool_name else ""
    print(f"[{context.server_name}{tool_info}] Progress: {percent:.1f}% - {message}")

@cl.on_chat_start
async def main():
    mcp_client = MultiServerMCPClient(
        {
        "myorg-mcp-server":{
            "transport":"http",
            "url":"http://localhost:8000/mcp"
        }
    },
    callbacks=Callbacks(on_progress=on_progress)
    
    )

    tools = await mcp_client.get_tools()

    slm = ChatOllama(
        model = "llama3.2",
        temperature=0,
        verbose = True,
    )

    #gpt = ChatOpenAI(model="gpt-4o-mini",
      #              temperature=0.1 )
    

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
    1. Given user input find the suitable title and issue description
    2. Call create_github_issue(title, issue_desc)
    You are NOT allowed to answer in natural language.
    You MUST call tools in order.
    Do NOT explain your reasoning.
    Respond ONLY after the tool completes
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
    deser_json = json.loads(final_ai_message.content)
    output_template = f"""
    Title : {deser_json['title']} \n
    Description: {deser_json['issue_desc']}  \n
    Category:{deser_json['category']}  \n
    Assigned to: {deser_json['assigned_to']}  \n
    """
    print(f"final message:: {output_template}")
    await msg.stream_token(output_template)
    #print(final_ai_message.content)
    #return final_ai_message.content
     

#if __name__ == "__main__":
#   usrMsg = """
       # I have been trying to follow your tutorials they are working great but there are infrastructure issues. create an issue for that
 #      """
 #   asyncio.run(main(usrMsg))

