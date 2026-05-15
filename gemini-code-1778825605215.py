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
        # Securely set keys
        os.environ["OPENAI_API_KEY"] = openai_key
        os.environ["SERPER_API_KEY"] = serper_key
        
        try:
            with st.status("AI Agents are working...", expanded=True) as status:
                st.write("Manager: Assigning Researcher...")
                
                search_tool = SerperDevTool()
                
                researcher = Agent(
                    role='Research Analyst',
                    goal=f'Conduct thorough research on {topic}',
                    backstory='Expert at analyzing and summarizing complex information.',
                    tools=[search_tool],
                    verbose=True
                )
                
                engineer = Agent(
                    role='Software Architect',
                    goal=f'Create a high-quality implementation of {topic}',
                    backstory='Experienced developer focused on scalable Python code.',
                    verbose=True
                )

                research_task = Task(description=f"Analyze {topic}", agent=researcher, expected_output="Tech stack report.")
                coding_task = Task(description=f"Build {topic}", agent=engineer, expected_output="Full Python script.")

                crew = Crew(agents=[researcher, engineer], tasks=[research_task, coding_task], process=Process.sequential)
                
                st.write("Agents are collaborating on your project...")
                result = crew.kickoff()
                st.success("Task Complete!")
            
            st.markdown("### 🏁 Final Result")
            st.code(result) # Displays code in a copyable box
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")