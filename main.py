import streamlit as st

from agent import create_agent

st.title("Agent Chat")


@st.cache_resource
def get_agent():
    return create_agent()


agent = get_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        final_content = ""

        with st.status("처리 중...", expanded=True) as status:
            for event in agent.stream({"messages": [("user", prompt)]}):
                # 에이전트가 도구 호출을 결정했을 때
                if "agent" in event:
                    messages = event["agent"]["messages"]
                    for m in messages:
                        if hasattr(m, "tool_calls") and m.tool_calls:
                            for tc in m.tool_calls:
                                tool_name = tc["name"]
                                tool_args = tc.get("args", {})
                                args_str = ", ".join(
                                    f"{k}={v!r}" for k, v in tool_args.items()
                                )
                                st.write(f"🔍 `{tool_name}({args_str})` 실행 중...")
                        elif hasattr(m, "content") and m.content:
                            final_content = m.content

                # 도구 실행 완료
                if "tools" in event:
                    messages = event["tools"]["messages"]
                    for m in messages:
                        tool_name = getattr(m, "name", "도구")
                        st.write(f"✓ `{tool_name}` 완료")

            status.update(label="완료", state="complete")

        if final_content:
            st.markdown(final_content)
            st.session_state.messages.append(
                {"role": "assistant", "content": final_content}
            )
