import gradio as gr
from gradio import ChatMessage
from app.core import agent
from app.utils.chat_handler import stream_from_agent
from llama_index.core.workflow import Context




async def process_query(message:str, history)-> str:
    async for msg in stream_from_agent(agent, message, ctx = ctx):
        yield msg

async def main():
    app = gr.ChatInterface(
        process_query,
        chatbot = gr.Chatbot(
        label = "Agent",
          avatar_images=(
                None,
                "https://em-content.zobj.net/source/twitter/53/robot-face_1f916.png",
            ),
        ),
        examples=[
            ["Combien de clients avons-nous ?"],
            ["Le client 7 est il solvable ?"],
            ["Quelle est la plus grosse dette du client 10 et quelle est l'action immédiate à mener ?"],
        ],
        title="Client base QA bot",
    )
    app.launch(debug=True)


if __name__=="__main__":
    agent = agent.create_agent()
    ctx = Context(agent)
    import asyncio
    asyncio.run(main())