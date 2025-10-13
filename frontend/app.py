# Streamlit UI
import streamlit as st
import requests

# --- Configuration ---
st.set_page_config(page_title="SEDAR+ Analyst Agent", page_icon="🤖")
st.title("SEDAR+ Analyst Agent")

# FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000/query"

# --- Session State Management ---
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your financial analyst agent. How can I help you analyze the document?"}]

# --- Chat Interface ---
# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input Handling ---
if prompt := st.chat_input("Ask a question about the document..."):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- API Call to Backend ---
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare the request payload
                payload = {"question": prompt, "ticker": "TD"} # Hardcoding ticker for now
                
                # Send the request to the FastAPI backend
                response = requests.post(API_URL, json=payload)
                response.raise_for_status() # Raise an exception for bad status codes 

                # Extract the response from the API
                api_result = response.json()
                full_response = api_result.get("response", "Sorry, I encountered an error.")
                
                # Display the response and add it to session state
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except requests.exceptions.RequestException as e:
                error_message = f"Could not connect to the backend API. Please ensure it's running. Error: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})