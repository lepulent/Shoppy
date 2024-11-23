import streamlit as st


APP_TITLE="Shoppy"
APP_ICON="🛒"
PAGE_TITLE="FAQs"
PAGE_ICON="❓"

st.set_page_config(page_title=PAGE_TITLE,page_icon=PAGE_ICON)

with st.sidebar:
    st.caption("Made with :material/favorite: by [Varun](https://www.linkedin.com/in/varun-sai-kanuri-089b34226/)")

st.markdown("#### FAQs")
with st.expander("What is 🛒 Shoppy?", expanded=False):
    st.markdown("""Shoppy is an intelligent assistant that caters to various aspects of the shopping journey, including:

****Product Inquiries****: Get detailed information about products, check availability, and discover related items effortlessly.

****Order Status Updates****: Stay informed about the progress of your orders, from confirmation to delivery.

****Product Recommendations****: Receive personalized product suggestions tailored to your preferences and previous activities.

****Order Management****: Display all orders associated with an account, place new orders based on specific product names, and cancel existing orders—all through a simple chat interface.""")


with st.expander("How to Get Started with Shoppy?"):
    st.markdown("""
Getting started with Shoppy is simple and welcoming, even if you don’t have an account. Here’s how it works:

****Login Options****: You can log in as a guest. For guest access, we provide a selection of predefined user accounts that allow you to explore Shoppy's capabilities.

****Guest Experience****: When logged in as a guest, you can ask product-related questions, browse items by category, and check the order history of the account you’re logged into. This feature is perfect for trying out Shoppy’s functions and understanding how it can assist with real-world shopping scenarios.

****Interacting with Shoppy****: Simply type your queries into the chat, and Shoppy will respond with relevant answers or actions. Whether it’s checking product availability, placing an order, or managing existing orders, Shoppy has you covered.""")

with st.expander("What is an Google API Key 🔑 and why do I need one?"):
    st.markdown("An Google API key is a unique credential that allows you to interact with Google's Gemini models. Shoppy uses the Gemini model to provide seamless support by understanding customer queries through text, and context for accurate product recommendations and order assistance.")

with st.expander("How can I get an Google API Key 🔑?"):
    st.markdown("You can obtain an Google API Key by creating one on the Google AI Studio website: https://aistudio.google.com/app/apikey")

with st.expander("Why do I need to enter my Google API key each time I use the app?"):
    st.markdown("For security reasons, your actual Google Key is not stored on our servers. Our application only uses it during the duration of your sessions to interact with Gemini.")

with st.expander("Does Shoppy cost money 💸?"):
    st.markdown("Shoppy itself is free to use, but since it relies on the Gemini 1.5-flash model via your Google API key, there is a free tier available for limited usage. If you exceed the free tier limits, additional charges may apply based on Google's API pricing.")

with st.expander("💡 What are some example prompts I can use to interact with Shoppy?"):
    st.markdown("""
    
    1. Show me a list of all my orders.
    
    2. Can you suggest some popular products in Electronics?
    
    3. I’d like to order 2 units of the iPhone 15.
    
    4. What’s the status of my order with ID 1003?
    
    5. Please cancel my order with ID 1005.
    
    **Note:** Product Categories available are Electronics, Books and Fashion
    
    """)
    
with st.expander("What language models do you support?"):
    st.markdown("""Shoppy currently supports the ***Gemini-1.5-flash*** language model for delivering efficient and accurate assistance.""")
