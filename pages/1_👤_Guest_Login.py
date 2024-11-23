import streamlit as st
from PIL import Image
import time

APP_TITLE="Shoppy"
APP_ICON="🛒"
PAGE_TITLE="Guest Login"
PAGE_ICON="👤"

st.set_page_config(page_title=PAGE_TITLE,page_icon=PAGE_ICON)
profile_image_left_url=r"images/user_5.jpg"
profile_image_right_url=r"images/men_5.jpg"
profile_image_left=Image.open(profile_image_left_url)
img1=profile_image_left.resize((250, 300), Image.ANTIALIAS)
profile_image_right=Image.open(profile_image_right_url)
img2=profile_image_right.resize((250, 300), Image.ANTIALIAS)

st.markdown(f"""# {'Guest Login'}""",unsafe_allow_html=True)
# st.caption("🚀 Your Personal Shopping Assistant, Built with LangGraph and Streamlit, Ready to Help 24/7")

with st.sidebar:
    st.caption("Made with :material/favorite: by [Varun](https://www.linkedin.com/in/varun-sai-kanuri-089b34226/)")
    
st.markdown("""

Welcome to the Guest Login Page! Here, you can explore and experience all the powerful features of Shoppy without needing to create an account. We offer two guest profiles for you to log in with, so you can see firsthand how Shoppy assists with product inquiries, order management, and more. Choose one of the profiles below and start interacting with Shoppy right away.

""")

st.info("""
### Get Started

****Select a Guest Profile****: Choose from one of the two available guest profiles below.

****Login and Explore****: Once logged in, feel free to ask about products, check order details, and navigate through various e-commerce support options.

****Enjoy Full Support****: Shoppy will guide you through any action, whether it's placing a new order, viewing existing orders, or canceling one—all through simple, conversational chat.
""")

# Display circular images using Streamlit's `st.image`
st.markdown(
    """
    <style>
    .container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .image-container-1 {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .circular-image-container {
        width: 2px; /* Adjust width as needed */
        height: 2px;
        overflow: hidden;
        border-radius: 1%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .circular-image {
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display:flex;
        object-fit: cover;
    }
    .stButton>button {
        background-color: violet !important;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        margin-top: 0px;
        cursor: pointer;
        text-align: center;
        
    }
    .stButton>button:hover {
        background-color: violet!important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
# Display images in two columns
col1, col2 = st.columns([1,1],gap="large")

# Left profile image
with col1:
    st.markdown('<div class="image-container-1">', unsafe_allow_html=True)
    st.markdown('<div class="circular-image-container">', unsafe_allow_html=True)
    st.image(img1, use_column_width=False, output_format="JPEG", caption="User: Tanya")  # Display the image
    st.markdown('</div>', unsafe_allow_html=True) 
    if st.button("Login as Tanya"):
        with st.spinner("Logging in as Tanya.."):
            time.sleep(3)
        st.success("Welcome! 🎉 You're now logged in as Tanya — start exploring Shoppy by asking questions or managing your orders! 😊")
        st.session_state.user_credentials = ["Tanya",1003]
        if len(st.session_state.messages)>2:
            st.session_state.messages=st.session_state.messages[:1]
    st.markdown('</div>', unsafe_allow_html=True)

# Right profile image
with col2:
    st.markdown('<div class="image-container-2">', unsafe_allow_html=True)
    st.markdown('<div class="circular-image-container">', unsafe_allow_html=True)
    st.image(img2, use_column_width=False, output_format="JPEG", caption="User: Arjun")  # Display the image
    st.markdown('</div>', unsafe_allow_html=True) 
    if st.button("Login as Arjun"):
        with st.spinner("Logging in as Arjun.."):
            time.sleep(3)
        st.success("Welcome! 🎉 You're now logged in as Arjun — start exploring Shoppy by asking questions or managing your orders! 😊!")
        st.session_state.user_credentials = ["Arjun",1009]
        if len(st.session_state.messages)>2:
            st.session_state.messages=st.session_state.messages[:1]
    st.markdown('</div>', unsafe_allow_html=True)
