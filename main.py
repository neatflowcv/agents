import streamlit as st
import streamlit.components.v1 as components

from agent import create_agent

st.title("Agent Chat")

# 사이드바에 알림 권한 요청 버튼
with st.sidebar:
    st.subheader("설정")
    components.html("""
    <button onclick="requestNotificationPermission()" style="
        padding: 8px 16px;
        background-color: #ff4b4b;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        margin-bottom: 8px;
    ">알림 권한 허용</button>
    <button onclick="playTestSound()" style="
        padding: 8px 16px;
        background-color: #4b4bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    ">소리 테스트</button>
    <p id="permission-status" style="font-size: 12px; color: #666;"></p>
    <script>
        function updateStatus() {
            const status = document.getElementById('permission-status');
            if (Notification.permission === 'granted') {
                status.textContent = '✓ 알림 권한이 허용되었습니다.';
                status.style.color = 'green';
            } else if (Notification.permission === 'denied') {
                status.textContent = '✗ 알림 권한이 거부되었습니다.';
                status.style.color = 'red';
            } else {
                status.textContent = '알림 권한을 허용해주세요.';
            }
        }
        function requestNotificationPermission() {
            Notification.requestPermission().then(updateStatus);
        }
        function playTestSound() {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            audioContext.resume().then(() => {
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                oscillator.frequency.value = 800;
                oscillator.type = 'sine';
                gainNode.gain.value = 0.5;
                oscillator.start();
                setTimeout(() => oscillator.stop(), 300);
            });
        }
        updateStatus();
    </script>
    """, height=120)


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

            # 소리 재생 + Desktop Notification
            components.html("""
            <script>
                // 알림음 재생 (간단한 beep)
                try {
                    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    audioContext.resume().then(() => {
                        const oscillator = audioContext.createOscillator();
                        const gainNode = audioContext.createGain();
                        oscillator.connect(gainNode);
                        gainNode.connect(audioContext.destination);
                        oscillator.frequency.value = 800;
                        oscillator.type = 'sine';
                        gainNode.gain.value = 0.3;
                        oscillator.start();
                        setTimeout(() => oscillator.stop(), 200);
                    });
                } catch (e) {
                    console.error('Audio error:', e);
                }

                // Desktop Notification (권한이 있을 때만)
                try {
                    if (Notification.permission === 'granted') {
                        new Notification('Agent', { body: '답변이 완료되었습니다.' });
                    }
                } catch (e) {
                    console.error('Notification error:', e);
                }
            </script>
            """, height=0)
