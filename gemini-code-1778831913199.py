import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# --- UI CONFIGURATION ---
st.set_page_config(page_title="AI CORP Web", layout="wide", page_icon="🚀")
st.title("🚀 AI Group Corp v1.0")
st.markdown("---")

# --- SIDEBAR: API KEYS ---
with st.sidebar:
    st.header("🔑 Authentication")
    openai_key = st.text_input("OpenAI API Key", type="password", help="Needed for the AI brain")
    serper_key = st.text_input("Serper API Key", type="password", help="Needed for internet research")
    st.info("Your keys are used only for this session.")

# --- MAIN INTERFACE ---
topic = st.text_input("Project Objective", placeholder="Example: Create a Python script that tracks stock prices...")

if st.button("ENGAGE AI GROUP", use_container_width=True):
    if not openai_key or not serper_key:
        st.error("❌ Missing Keys: Please enter your OpenAI and Serper API keys in the sidebar.")
    elif not topic:
        st.warning("⚠️ Please describe what you want the AI Group to build.")
    else:
        # Set Environment Variables for the agents to use
        os.environ["OPENAI_API_KEY"] = openai_key
        os.environ["SERPER_API_KEY"] = serper_key
        
        try:
            with st.status("🛠️ AI Agents are collaborating...", expanded=True) as status:
                # 1. THE TOOLS
                search_tool = SerperDevTool()

                # 2. THE AGENTS (The Brains)
                researcher = Agent(
                    role='Senior Research Analyst',
                    goal=f'Research the best Python libraries and logic for: {topic}',
                    backstory='Specialized in technical documentation and finding efficient code solutions.',
                    tools=[search_tool],
                    verbose=True,
                    allow_delegation=False
                )

                engineer = Agent(
                    role='Software Engineer',
                    goal=f'Develop the complete, bug-free Python code for: {topic}',
                    backstory='Expert programmer known for writing clean, high-performance Python scripts.',
                    verbose=True,
                    allow_delegation=False
                )

                # 3. THE TASKS
                research_task = Task(
                    description=f"Identify the requirements and best approach for building: {topic}",
                    agent=researcher,
                    expected_output="A technical blueprint including required libraries."
                )

                coding_task = Task(
                    description=f"Write the final Python code based on the research provided.",
                    agent=engineer,
                    expected_output="The full source code as a single block."
                )

                # 4. THE CREW (The Execution)
                crew = Crew(
                    agents=[researcher, engineer],
                    tasks=[research_task, coding_task],
                    process=Process.sequential
                )
                
                st.write("🕵️ Researcher is investigating tech stacks...")
                result = crew.kickoff()
                status.update(label="✅ Project Complete!", state="complete", expanded=False)

            # --- DISPLAY RESULT ---
            st.markdown("### 🏁 Final Generated Project")
            st.markdown("Below is the output from your AI Engineering team:")
            st.code(result, language="python")
            
        except Exception as e:
            st.error(f"🚨 An unexpected error occurred: {str(e)}")