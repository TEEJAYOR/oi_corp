import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

st.set_page_config(page_title="AI CORP Web", layout="wide")
st.title("🚀 AI Group Corp v1.0")

with st.sidebar:
    st.header("Settings")
    openai_key = st.text_input("OpenAI API Key", type="password")
    serper_key = st.text_input("Serper API Key", type="password")

topic = st.text_input("Project Objective", placeholder="Describe what to build...")

if st.button("ENGAGE AI GROUP"):
    if not openai_key or not serper_key:
        st.error("Please provide both API keys in the sidebar.")
    else:
        os.environ["OPENAI_API_KEY"] = openai_key
        os.environ["SERPER_API_KEY"] = serper_key
        
        with st.status("AI Agents are working...", expanded=True) as status:
            # Defined the internal logic for the web version
            researcher = Agent(role='Researcher', goal=f'Analyze {topic}', backstory='Expert analyst.', tools=[SerperDevTool()])
            engineer = Agent(role='Engineer', goal=f'Build {topic}', backstory='Senior developer.')
            
            t1 = Task(description=f"Research {topic}", agent=researcher, expected_output="Research data.")
            t2 = Task(description=f"Code {topic}", agent=engineer, expected_output="Python script.")

            crew = Crew(agents=[researcher, engineer], tasks=[t1, t2], process=Process.sequential)
            
            result = crew.kickoff()
            st.success("Task Complete!")
        
        st.subheader("Final Generated Code")
        st.code(result) # Display as code block