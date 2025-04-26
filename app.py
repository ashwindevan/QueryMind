#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Querymind Web Application Module

This module implements a Streamlit-based web interface for the Querymind database
query assistant. It allows users to upload SQLite databases and interact with them
using natural language queries, which are then converted into SQL by the LLM agent.

Key features:
- Database file upload and management
- Interactive chat interface for natural language queries
- Sidebar with database schema information
- LLM-powered query translation and execution
"""

# Standard library imports
import os               # Operating system interfaces
import random           # Random number generation for loading messages
import shutil           # High-level file operations
from pathlib import Path  # Object-oriented filesystem paths

# Third-party imports
import streamlit as st  # Web application framework
from dotenv import load_dotenv  # Environment variable management
from langchain_core.language_models.chat_models import BaseChatModel  # LLM interfaces
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage  # Message types for chat history

# Local application imports
from Querymind.config import Config  # Application configuration
from Querymind.models import create_llm  # LLM initialization
from Querymind.tools import get_available_tools, with_sql_cursor  # Database interaction tools
from Querymind.agent import ask, create_history  # LLM agent functionality

# Load environment variables from .env file (API keys, etc.)
load_dotenv()

# Initialize database path to None (will be set when user uploads a database)
Config.Path.DATABASE_PATH = None

# Collection of thematic loading messages displayed during query processing
# These enhance the user experience with engaging feedback during wait times
LOADING_MESSAGES = [
    "Consulting the ancient tomes of SQL wisdom ... ",
    "Casting query spells on your database ... ",
    "Summoning data from the digital realms ... ",
    "Deciphering your request into database runes ... ",
    "Brewing a potion of perfect query syntax ... ",
    "Channeling the power of database magic ... ",
    "Translating your words into the language of tables ... ",
    "Waving my SQL wand to fetch your results ... ",
    "Performing database divination ... ",
    "Aligning the database stars for optimal results ... ",
    "Consulting with the database spirits ... ",
    "Transforming natural language into database incantations ... ",
    "Peering into the crystal ball of your database ... ",
    "Opening a portal to your data dimension ... ",
    "Enchanting your request with SQL magic ... ",
    "Invoking the ancient art of query optimization ... ",
    "Reading between the tables to find your answer ... ",
    "Conjuring insights from your database depths ... ",
    "Weaving a tapestry of joins and filters ... ",
    "Preparing a feast of data for your consideration ... ",
]


def reset_model_cache():
    """
    Reset the cached LLM model in session state.
    
    This function is called when a new database is uploaded to ensure the model
    is reinitialized with the correct context. This prevents the model from
    using outdated information about the database structure.
    """
    if 'model' in st.session_state:
        del st.session_state['model']


@st.cache_resource(show_spinner=False)
def get_model() -> BaseChatModel:
    """
    Create and cache an LLM instance with database tools bound.
    
    This function initializes the language model based on the configuration
    and attaches the database interaction tools to it. The @st.cache_resource
    decorator ensures the model is loaded only once and reused across queries,
    significantly improving response time.
    
    Returns:
        BaseChatModel: Configured language model with database tools attached
    """
    llm = create_llm(Config.MODEL)  # Initialize the LLM with configured model
    llm = llm.bind_tools(get_available_tools())  # Attach database tools to the LLM
    return llm


def load_css(css_file):
    """
    Load and apply CSS styling from an external file.
    
    Reads the content of a CSS file and injects it directly into the Streamlit
    application, allowing for custom styling beyond what Streamlit provides natively.
    
    Args:
        css_file (str): Path to the CSS file containing custom styles
    """
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def save_uploaded_file(uploaded_file):
    """
    Save an uploaded database file to the configured directory.
    
    This function:
    1. Determines the destination path based on configuration
    2. Writes the uploaded file to disk
    3. Updates the global database path configuration
    4. Resets the model cache to ensure it's aware of the new database
    
    Args:
        uploaded_file: Streamlit UploadedFile object containing the database
        
    Returns:
        Path: Path to the saved database file for reference
    """
    file_path = Config.Path.UPLOADED_DB_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # Write the file to disk
    Config.Path.DATABASE_PATH = file_path  # Update global database path
    reset_model_cache()  # Reset model to work with new database
    return file_path


def clear_chat():
    """
    Clear the chat history from session state.
    
    Removes all conversation messages from the session state,
    effectively resetting the conversation to its initial state.
    This allows users to start a fresh conversation without
    previous context influencing the responses.
    
    Returns:
        bool: True if successfully cleared
    """
    if "messages" in st.session_state:
        del st.session_state["messages"]
    return True


# ========================
# STREAMLIT UI SETUP
# ========================

# Initialize Streamlit page configuration with optimized settings
st.set_page_config(
    page_title="QueryMind",  # Browser tab title
    page_icon=".6",          # Favicon/icon
    layout="centered",       # Centered layout for better readability
    initial_sidebar_state="collapsed",  # Start with sidebar closed
)

# Load custom CSS styles for themed appearance
load_css("assets/style.css")

# Application Header with custom styling for visual appeal
st.markdown("""
<div style="text-align: center;">
    <h1 style="color: #39ffa2; text-shadow: 0 0 8px #39ffa2, 0 0 16px #39ffa2; font-size: 6rem; margin-bottom: 0.2rem;">
        QueryMind
    </h1>
    <p style="font-family: 'Orbitron', sans-serif; color: #ff69b4; font-size: 1.8rem; font-weight: 600; text-shadow: 0 0 6px #ff69b4, 0 0 12px #ffb6c1; margin: 0 0 0 -1.6rem;">
        Database Query Assistant
    </p>
    <p style="font-size: 1.1rem; color: #d2f5d0; max-width: 600px; margin: 0 auto 3rem auto; text-shadow: 0 0 6px #39ffa2; font-style: italic;">
        Intelligence that speaks your language to extract insights — Talk to your database using natural language.
    </p>
</div>
""", unsafe_allow_html=True)

# File Uploader component with padding for better visual spacing
st.markdown('<div style="padding: 1rem 0;">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["sqlite", "db", "sqlite3"], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# Custom font styling for alert messages
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap');
        div[data-testid="stAlert"] p {
            font-family: 'Orbitron', sans-serif !important;
            font-weight: 500;
            font-size: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ========================
# DATABASE UPLOAD HANDLING
# ========================

# Process uploaded database file and display feedback
if uploaded_file is not None:
    db_path = save_uploaded_file(uploaded_file)
    st.success("Database uploaded! 👏 Check the sidebar for table details 👈")
else:
    st.warning("Please upload a database file to proceed.", icon="⚠️")

# ========================
# SIDEBAR CONFIGURATION
# ========================

with st.sidebar:
    # Display database information if a database is loaded
    if Config.Path.DATABASE_PATH and Config.Path.DATABASE_PATH.exists():
        # Database info card showing file details
        st.markdown("""
            <div class="card db-info-card">
                <h3 class="glow-header db-details">📊  Database Details</h3>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <p class="db-info-text"><strong>File:</strong> {Config.Path.DATABASE_PATH.name}</p>
        """, unsafe_allow_html=True)

        # Calculate and display database file size
        db_size = Config.Path.DATABASE_PATH.stat().st_size / (1024 * 1024)
        st.markdown(f"""
            <p class="db-info-text"><strong>Size:</strong> {db_size:.2f} MB</p>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Display tables from the database with row counts
        try:
            with with_sql_cursor() as cursor:
                # Query to get all user tables (excluding SQLite system tables)
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                tables = [row[0] for row in cursor.fetchall()]
                
                if tables:
                    # Display table header
                    st.markdown("""
                        <div class="card tables-card">
                            <h3 class="glow-header db-details">📋 Available Tables</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Create expandable section with table list
                    with st.expander("View Tables", expanded=True):
                        for table in tables:
                            # Get row count for each table
                            cursor.execute(f"SELECT count(*) FROM {table};")
                            count = cursor.fetchone()[0]
                            
                            # Display table name and row count
                            st.markdown(f"""
                                <div class="table-item">
                                    <span>{table}</span>
                                    <span class="row-count">{count} rows</span>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("No tables found in the database.", icon="⚠️")
        except Exception as e:
            st.error(f"Error reading database: {str(e)}", icon="❌")
    else:
        # Pre-upload guidance message when no database is loaded
        st.markdown("""
            <div class="card sidebar-header">
                <h2 class="glow-header12 db-details">📃 Ready to Query?</h2>
                <p class="tagline">Upload an SQLite database to explore its tables and start querying!</p>
                <p class="hint" style="font-family: 'Audiowide', sans-serif; font-size: 0.9rem;">
                    Supported formats: .sqlite, .db, .sqlite3
                </p>
                    
            </div>
        """, unsafe_allow_html=True)

# ========================
# CHAT INTERFACE
# ========================

# Clear Chat button positioned on the right side of the interface
left_space = 2.3  # Increase to push button right
right_space = 3  # Increase to push button left
col1, col2 = st.columns([left_space, right_space])
with col2:
    if st.button("Clear Chat", type="secondary"):
        if clear_chat():
            st.success("Chat cleared successfully!")
            st.rerun()  # Refresh the page to show cleared chat

# Visual divider between controls and chat interface
st.markdown("<hr style='border: 1px solid rgba(57, 255, 162, 0.3); margin: 15px 0;'>", unsafe_allow_html=True)

# Initialize chat history if not present in session state
if "messages" not in st.session_state:
    st.session_state.messages = create_history()  # Create new history with system prompt

# Display conversation history from session state
for message in st.session_state.messages:
    # Skip system messages as they're not shown to the user
    if isinstance(message, SystemMessage):
        continue
        
    # Determine message type and avatar
    is_user = isinstance(message, HumanMessage)
    avatar = "🧐" if is_user else "🤖"
    
    # Display message with appropriate styling
    with st.chat_message("user" if is_user else "ai", avatar=avatar):
        st.markdown(message.content)


# Get user input from chat input field
if prompt := st.chat_input("Type your message ... "):
    # Display user message
    with st.chat_message("user", avatar="🧐"):
        st.session_state.messages.append(HumanMessage(content=prompt))
        st.markdown(prompt)

    # Process and display AI response
    with st.chat_message("ai", avatar="🤖"):
        # Create placeholder for loading state and final response
        message_placeholder = st.empty()
        
        # Show random loading message while processing
        message_placeholder.status(random.choice(LOADING_MESSAGES), state="running")

        # Check if database is available before processing
        if not Config.Path.DATABASE_PATH or not Config.Path.DATABASE_PATH.exists():
            message_placeholder.error("Please upload a valid SQLite database file first.")
        else:
            try:
                # Process the query through the LLM agent
                response = ask(prompt, st.session_state.messages, get_model())
                
                # Display the response and save to chat history
                message_placeholder.markdown(response)
                st.session_state.messages.append(AIMessage(content=response))
            except Exception as e:
                # Handle and display any errors that occur during processing
                message_placeholder.error(f"Error processing your request: {str(e)}")