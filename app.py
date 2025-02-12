import streamlit as st
import google.generativeai as genai

# Configure Gemini with direct API key
GEMINI_API_KEY = "paste gemini api key"  # 
genai.configure(api_key=GEMINI_API_KEY)

# Company information database
COMPANY_INFO = {
    "about": "Raven Labs is an Australian-based technology company specializing in AI solutions, software development, and digital transformation services.",
    "services": [
        "Custom AI Solutions Development",
        "Enterprise Software Development",
        "Cloud Computing Services",
        "Data Analytics & Business Intelligence",
        "Cybersecurity Solutions"
    ],
    "contact": {
        "email": "info@ravenlabs.au.com",
        "phone": "+61 2 1234 5678",
        "address": "Level 12, 123 Tech Street, Sydney NSW 2000, Australia"
    },
    "team": "Our team consists of experienced AI researchers, software engineers, and digital transformation experts.",
    "foundation": "Established in 2018",
    "clients": "We serve clients across various industries including finance, healthcare, and government sectors."
}

def get_company_response(query):
    """Handle company-specific queries"""
    query = query.lower()
    
    if 'about' in query:
        return COMPANY_INFO['about']
    elif 'services' in query:
        return "Our services include:\n- " + "\n- ".join(COMPANY_INFO['services'])
    elif 'contact' in query or 'address' in query or 'email' in query:
        contact = COMPANY_INFO['contact']
        return f"Contact us at:\nEmail: {contact['email']}\nPhone: {contact['phone']}\nAddress: {contact['address']}"
    elif 'team' in query:
        return COMPANY_INFO['team']
    elif 'found' in query or 'start' in query:
        return COMPANY_INFO['foundation']
    elif 'client' in query:
        return COMPANY_INFO['clients']
    return None

def get_general_response(prompt):
    """Get response from Gemini"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Raven Labs AI Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Accept user input
    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        company_response = get_company_response(prompt)
        response = company_response if company_response else get_general_response(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
