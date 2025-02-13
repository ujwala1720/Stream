import streamlit as st
import google.generativeai as genai

# System prompt with company information
COMPANY_CONTEXT = """
You are Raven, the AI assistant for Raven Labs, an Australian-based technology company. 
Here's important company information to incorporate in your responses:

- About: Specializes in AI solutions, software development, and digital transformation services
- Founded: 2018
- Services: 
  • Custom AI Solutions Development
  • Enterprise Software Development
  • Cloud Computing Services
  • Data Analytics & Business Intelligence
  • Cybersecurity Solutions
- Contact:
  • Email: info@ravenlabs.au.com
  • Phone: +61 2 1234 5678
  • Address: Level 12, 123 Tech Street, Sydney NSW 2000, Australia
- Team: Experienced AI researchers, software engineers, and digital transformation experts
- Clients: Various industries including finance, healthcare, and government sectors

Always respond in a professional, friendly tone. Be concise but informative. 
If asked about capabilities, mention you're powered by Google's Gemini AI.
"""

def configure_gemini(api_key):
    """Configure Gemini with API key"""
    genai.configure(api_key=api_key)

def get_ai_response(prompt):
    """Get response from Gemini with company context"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        full_prompt = f"{COMPANY_CONTEXT}\n\nUser Query: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Raven Labs AI Assistant")
    
    # API key management
    if 'GEMINI_API_KEY' in st.secrets:
        api_key = st.secrets['GEMINI_API_KEY']
    else:
        api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
    
    if not api_key:
        st.warning("Please enter your Gemini API key to continue")
        st.stop()
    
    configure_gemini(api_key)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add system greeting
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm Raven, your AI assistant for Raven Labs. How can I help you today?"
        })

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        response = get_ai_response(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
