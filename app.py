from agents import main_agent
from swarm import Swarm
import streamlit as st
import os
if __name__ == '__main__':
    if 'api_key' not in st.session_state:
        api_key = st.text_input('Enter your OpenAI API key:', type='password')
        if not api_key:
            st.warning('Please enter your OpenAI API key to proceed.')
            st.stop()
        st.session_state.api_key = api_key  # Store in session state
    
    # Initialize AFTER setting API key
    os.environ['OPENAI_API_KEY'] = st.session_state.api_key
    
    swarm_client = Swarm()
    agent = main_agent

    st.image("google_calendar.png", width=150)
    st.title('Create A Google Calendar AI Agent')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role'], avatar='🤖' if message['role'] == 'assistant' else '🧑‍💻'):
            st.markdown(message['content'])

    if prompt := st.chat_input('Enter your prompt here'):
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        with st.chat_message('user', avatar='🧑‍💻'):
            st.markdown(prompt)

        with st.chat_message('ai', avatar='🤖'):
            # print('Session state message', st.session_state.messages)
            response = swarm_client.run(
                agent=agent,
                debug=True,
                # messages=[{'role': 'user', 'content': 'Show me my last 5 movie showtimes calendar events.'}],
                messages=[{'role': 'user', 'content': prompt}],
                # messages=st.session_state.messages
            )
            st.markdown(response.messages[-1]['content'])
        st.session_state.messages.append({'role': 'assistant', 'content': response.messages[-1]['content']})