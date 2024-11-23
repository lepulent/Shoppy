import streamlit as st
from PIL import Image

APP_TITLE="Shoppy"
APP_ICON="🛒"

st.set_page_config(page_title=APP_TITLE,page_icon=APP_ICON)
st.session_state.previous=[]

img2=Image.open(r"C:\Users\Varun Sai Kanuri\Downloads\bot_3.jpg")
home=Image.open("C:\\Users\\Varun Sai Kanuri\\Downloads\\home1.png")

with st.sidebar:
    st.caption("Made with :material/favorite: by [Varun](https://www.linkedin.com/in/varun-sai-kanuri-089b34226/)")
    
home_title=f"{APP_ICON} {APP_TITLE}"
st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=4>Beta</font></span>""",unsafe_allow_html=True)
st.caption("🚀 Your Personal Shopping Agent, Built with LangGraph and Streamlit, Ready to Help 24/7")

st.write("****:violet[Shoppy]**** is your e-commerce AI Agent, designed to make online shopping more efficient and enjoyable. Assists users with product inquiries, order tracking, and support on e-commerce platforms. Built with Langgraph and Streamlit.")

st.image(home)


st.markdown("##### Ready to Get Started?")
st.markdown("""To begin your journey with ****:violet[Shoppy]****, click on the ****:blue[Guest Login]**** button below and choose to log in as yourself or as one of our guest accounts. Experience firsth and how Shoppy makes online shopping smarter and easier.""")
