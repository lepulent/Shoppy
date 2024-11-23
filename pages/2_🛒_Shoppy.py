from langchain_core.tools import tool
from typing import Optional, List, Annotated, TypedDict, Literal
from langgraph.graph import START, StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
import sqlite3
import os
from PIL import Image
import streamlit as st
from datetime import date, datetime, timedelta
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig, RunnableLambda
from langchain_core.messages import ToolMessage, HumanMessage
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
import shutil
import uuid




db="salesorders.db"
APP_TITLE="Shoppy"
APP_ICON="🛒"
img=Image.open(r"C:\Users\Varun Sai Kanuri\Downloads\men_5.jpg").resize((300,300), Image.ANTIALIAS)
img2=Image.open(r"C:\Users\Varun Sai Kanuri\Downloads\bot_3.jpg")
st.set_page_config(page_title=APP_TITLE,page_icon=APP_ICON)



    
with st.sidebar:
#     st.header(f"{APP_ICON} {APP_TITLE}")
#     "Assists users with product inquiries, order tracking, and support on e-commerce platforms. Built with Langgraph and Streamlit." 
    with st.popover(":material/settings: Settings", use_container_width=True):

            st.markdown("Settings")
            option = st.selectbox("Select Model",("Gemini-1.5-Falsh",),)
            temp = st.slider("Temparature", 0.0, 1.0,0.1)
            api_key=st.text_input("Your Google API Key",type="password")
            "Don't have an API key? No worries! Create one [here](https://makersuite.google.com/app/apikey)."
               
               
    if st.button("Clear Chat History"):
        st.session_state.messages.clear()
        
    st.caption("Made with :material/favorite: by [Varun](https://www.linkedin.com/in/varun-sai-kanuri-089b34226/)")
        


    
if "messages" not in st.session_state or st.session_state.messages==[]:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
try:
    user_data=st.session_state.user_credentials
    print(f"Length: {len(user_data)}")

    if user_data is not None:
        if user_data[0]=="Tanya":
            img=Image.open(r"C:\Users\Varun Sai Kanuri\Downloads\User_5.jpg")
            
except:
    st.info("Please log in as a guest to start chatting with Shoppy and explore all its features! 😊")
    st.stop()
for msg in st.session_state.messages:
    #st.chat_message(msg["role"]).write(msg["content"])
    if msg["role"]=="assistant":
        
        st.chat_message(msg["role"],avatar=img2).write(msg['content'])
                    
    else:
        
        st.chat_message(msg["role"],avatar=img).write(msg['content']) 



@tool
def search_products(
    categoryName: Optional[str]=None,
    productName: Optional[str]=None,
    min_price: Optional[int] = None,
    max_price: Optional[int]=None,
    limit: int=10 
) -> list[dict]:
    
    """ 
    Provides product descriptions and recommends products based on productName or Category Name or minimum price or maxmimum price.
    
    Returns:
        A list of dictionaries where each dictionary contains the Product details.
    
    """
    
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    query= """
    
        SELECT t1.ProductName, t1.ProductDescription, t1.RetailPrice, t1.QuantityOnHand, t2.CategoryName, t2.CategoryDescription 
        FROM products t1 
        JOIN categories t2 
        ON t1.CategoryID=t2.CategoryID
        WHERE 1=1
        
        """
    params=[]
    
    if categoryName:
        query+=" AND CategoryName = ?"
        params.append(categoryName)
    if productName:
        query+=" AND ProductName = ?"
        params.append(productName)
    if min_price:
        query+=" AND RetailPrice >= ?"
        params.append(min_price)
    if max_price:
        query+=" AND RetailPrice <= ?"
        params.append(max_price)
        
    query+=" LIMIT ?"
    params.append(limit)
    
    
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return results

@tool
def placeOrder(
    productName: str,
    quantity: Optional[int]=1,
    *,
    config: RunnableConfig
) -> str:
    """
    Places an order for a specified product and quantity.
    
    This tool processes an order request by verifying product availaility, calculating the total cost, and storing the order details in the system.
    
    If the required quantity is available, the function deducts the quantity from the products stock and returns the order confirmation with relevant details.
    
    Incase of insuffecient stock, an appropriate error message is returned
    
    """
    configuration = config.get("configurable", {})
    CustomerID = configuration.get("CustomerID", None)
    if not CustomerID:
        raise ValueError("No User ID Configured")
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    params1=[]
    t=date.today()
    order_date=t
    ship_date=t+timedelta(days=2)
    print(f"Order Date: {order_date}")
    print(f"Ship Date: {ship_date}")
    print("Above Order Number")
    cursor.execute("select OrderNumber from Orders Order by OrderNumber desc limit 1")
    order_num=cursor.fetchone()[0]+1
    print(f"Order ID: {order_num}")
    cursor.execute("select * from Order_Details")
    OD_sno=len(cursor.fetchall())+1
    cursor.execute("select * from Orders")
    O_sno=len(cursor.fetchall())+1
    cursor.execute("select ProductNumber, RetailPrice from Products WHERE ProductName = ? limit 1",(productName,))
    row=cursor.fetchone()
    print(f"ROw: {row}")
    if not row:
        
        cursor.close()
        conn.close()
        
        return "No such Product to Order. Check Out some other Products"    
    
    print("Out if loop")
    price=row[1]
    params1.extend([OD_sno,order_num,row[0],price ])
    print(params1)
    query1="INSERT INTO Order_Details VALUES(?, ?, ?, ? "
    query2="INSERT INTO Orders VALUES (?, ?, ?, ?, ?)"
    print(quantity)
    if quantity:
        print("In quantity condition")
        query1+=", ? "
        params1.append(int(quantity))

    query1+=")"
    print(f"Params1: {params1}")
    print(f"Query1: {query1}")
    print("Before query1")
    cursor.execute(query1,params1)

    print("After Query1")
    cursor.execute(query2,(O_sno,order_num, order_date,ship_date,CustomerID))
    print("After Query2")

    conn.commit()

    cursor.close()
    conn.close()

    return "Your Order Product is Placed Successfully. Order Successfully Placed and check your order history about your product"

    

@tool
def orderstatus(OrderNumber: int, *, config: RunnableConfig) -> list[dict]:
    
    """
    Fetching the Order status of the User based on Order ID
    Returns:
        A list of dictionaries where each dictionary contains the Ordert details,
        associated Order Shipping Dates, Price details and Days to deliver the order .
    
    """
    configuration = config.get("configurable", {})
    CustomerID = configuration.get("CustomerID", None)
    if not CustomerID:
        raise ValueError("No User ID Configured")
        
    if not OrderNumber:
        raise ValueError("Order ID is Not Informed.")

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    query="""
            SELECT od.OrderNumber, od.ProductNumber, p.ProductName, o.CustomerID, o.OrderDate, o.ShipDate, od.QuotedPrice, od.QuantityOrdered, pv.DaysToDeliver, v.VendorName, v.VendorCity, v.VendorState, V.VendorPhoneNumber 
            FROM Order_Details od 
            JOIN Products p ON p.ProductNumber=od.ProductNumber
            JOIN Orders o ON o.OrderNumber=od.OrderNumber
            JOIN Product_Vendors pv ON pv.ProductNumber=od.ProductNumber
            JOIN Vendors v ON pv.VendorID=v.VendorID
            WHERE od.OrderNumber = ? AND o.CustomerID = ?

          """
    
    cursor.execute(query, (OrderNumber,CustomerID))
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()
    
    return results

@tool
def cancelOrder(OrderNumber: int, *, config: RunnableConfig) -> str:
    """ To delete a specific order from the database based on the provided order ID. """
    configuration = config.get("configurable", {})
    CustomerID = configuration.get("CustomerID", None)
    if not CustomerID:
        raise ValueError("No User ID Configured")

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM Orders WHERE OrderNumber = ?", (OrderNumber,)
    )
    existing_order = cursor.fetchone()
    if not existing_order:
        cursor.close()
        conn.close()
        return "No existing Order found for the given Order number."
    cursor.execute(
        "SELECT * FROM Orders WHERE OrderNumber = ? AND CustomerID = ?",
        (OrderNumber, CustomerID),
    )
    current_order = cursor.fetchone()
    if not current_order:
        cursor.close()
        conn.close()
        return f"Current signed-in User with ID {CustomerID} couldn't have any Order with Order ID  {OrderNumber}"

    
    cursor.execute("DELETE FROM Orders WHERE orderNumber = ?", (OrderNumber,))
    cursor.execute("DELETE FROM Order_Details WHERE orderNumber = ?", (OrderNumber,))
    conn.commit()

    cursor.close()
    conn.close()
    return "Order successfully cancelled."


@tool
def showOrders(config: RunnableConfig) -> str:
    """ displays all orders """
    configuration = config.get("configurable", {})
    CustomerID = configuration.get("CustomerID", None)
    if not CustomerID:
        raise ValueError("No User ID Configured")

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    query="""
            SELECT od.OrderNumber, od.ProductNumber, p.ProductName, o.CustomerID, o.OrderDate, o.ShipDate, od.QuotedPrice, od.QuantityOrdered, pv.DaysToDeliver, v.VendorName, v.VendorCity, v.VendorState, V.VendorPhoneNumber 
            FROM Order_Details od 
            JOIN Products p ON p.ProductNumber=od.ProductNumber
            JOIN Orders o ON o.OrderNumber=od.OrderNumber
            JOIN Product_Vendors pv ON pv.ProductNumber=od.ProductNumber
            JOIN Vendors v ON pv.VendorID=v.VendorID
            WHERE o.CustomerID = ?

          """
    cursor.execute(query,(CustomerID,))
    rows = cursor.fetchall()
    
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()
    
    return results

def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def _print_event(event: dict, _printed: set, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)

            from typing import Annotated

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
        
class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            User_id = configuration.get("CustomerID", None)
            User_name=configuration.get("CustomerName", None)
            state = {**state, "CustomerID": User_id, "CustomerName":User_name}
            result = self.runnable.invoke(state)
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}
    
if not api_key:
    st.info("To start using Shoppy, please provide your Google API key in the Settings section. 😊")
    st.stop()
else:
    os.environ["GOOGLE_API_KEY"]=api_key

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=temp)

primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
                ("system", 
            """
                You are Shoppy, an AI assistant designed to support users on an e-commerce platform. Your primary role is to assist with product inquiries, order tracking, and general support using available tools and data. Follow these guidelines to provide helpful and efficient responses:

        User Assistance: Proactively help users with product searches, order tracking, and relevant support questions.
        Detailed Information Retrieval: For product searches or order tracking, be thorough. If your initial search does not yield satisfactory results, broaden the search query and try again to ensure accuracy.
        Personalized Interactions: Where possible, address users by name. You can find the user's name from the given information below.

        User Information:

            Current User Name: {CustomerName}
            User ID: {CustomerID}
            Current Time: {time}
        """),
                ("placeholder", "{messages}")
    ]
).partial(time=datetime.now())

tools = [search_products,placeOrder, orderstatus,cancelOrder, showOrders]

assistant_runnable = primary_assistant_prompt | llm.bind_tools(tools)

builder = StateGraph(State)


builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)


if prompt := st.chat_input():
    
    if user_data and api_key:
        thread_id = str(uuid.uuid4())
        username=user_data[0]
        userid=user_data[1]
        config = {
            "configurable": {
                "CustomerName":username,
                "CustomerID": userid,
                "thread_id": thread_id,
            }
        }   
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user",avatar=img).write(prompt)
        final_state = graph.invoke({"messages": [HumanMessage(content=prompt)]},config=config)
        print(final_state)
        msg=final_state["messages"][-1].content

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant",avatar=img2).write(msg)
    else:
        st.info("To start using Shoppy, please provide your Google API key in the Settings section. 😊")
        st.stop()
