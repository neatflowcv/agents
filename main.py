import gradio as gr

from agent import create_agent


def main():
    agent = create_agent()

    def chat(msg, history):
        """Gradio ChatInterface용 chat 함수"""
        result = agent.invoke({"messages": [("user", msg)]})
        if "messages" in result and len(result["messages"]) > 0:
            last_message = result["messages"][-1]
            if hasattr(last_message, "content"):
                return last_message.content
            if isinstance(last_message, dict) and "content" in last_message:
                return last_message["content"]
            return str(last_message)
        return str(result)

    gr.ChatInterface(chat).launch()


if __name__ == "__main__":
    main()
