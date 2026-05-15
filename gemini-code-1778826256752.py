import customtkinter as ctk
import threading
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool # Tool for the Researcher to use

class AICorpApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Group Corp v1.0 - Windows Desktop")
        self.geometry("900x700")
        ctk.set_appearance_mode("dark")

        # --- UI LAYOUT ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="AI CORP", font=("Arial", 24, "bold"))
        self.logo.pack(pady=20)

        self.key_entry = ctk.CTkEntry(self.sidebar, placeholder_text="OpenAI API Key", show="*")
        self.key_entry.pack(pady=10, padx=20)
        
        self.serper_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Serper API Key", show="*")
        self.serper_entry.pack(pady=10, padx=20)

        # Main Panel
        self.main = ctk.CTkFrame(self, corner_radius=15)
        self.main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.label = ctk.CTkLabel(self.main, text="Project Objective", font=("Arial", 16))
        self.label.pack(pady=(20, 5))

        self.topic_input = ctk.CTkEntry(self.main, width=500, height=40, placeholder_text="Describe the software or video to build...")
        self.topic_input.pack(pady=10)

        self.btn = ctk.CTkButton(self.main, text="ENGAGE AI GROUP", font=("Arial", 14, "bold"), 
                                fg_color="#1f538d", hover_color="#14375e", command=self.launch)
        self.btn.pack(pady=20)

        self.console = ctk.CTkTextbox(self.main, width=600, height=350, font=("Consolas", 12))
        self.console.pack(pady=10, padx=20)

    def log(self, message):
        """Helper to update the console safely."""
        self.console.insert("end", f"{message}\n")
        self.console.see("end")

    def launch(self):
        topic = self.topic_input.get()
        if not topic: return
        self.console.delete("1.0", "end")
        self.log(f">>> INITIALIZING GROUP FOR: {topic}")
        # Run in thread so the UI doesn't freeze
        threading.Thread(target=self.run_logic, args=(topic,), daemon=True).start()

    def run_logic(self, topic):
        os.environ["OPENAI_API_KEY"] = self.key_entry.get()
        os.environ["SERPER_API_KEY"] = self.serper_entry.get()
        
        try:
            # 1. Setup Tools & Agents
            search_tool = SerperDevTool()

            researcher = Agent(
                role='Lead Researcher',
                goal=f'Find the best tech stack for {topic}',
                backstory='Expert in software architecture and technical research.',
                tools=[search_tool],
                verbose=True
            )

            engineer = Agent(
                role='Senior Engineer',
                goal=f'Write the full Python code for {topic}',
                backstory='Master of clean, functional Python implementation.',
                verbose=True
            )

            # 2. Define the Tasks
            research_task = Task(description=f"Research tool requirements for {topic}", agent=researcher, expected_output="A summary of libraries needed.")
            coding_task = Task(description=f"Write the final code for {topic}", agent=engineer, expected_output="The complete Python source code.")

            # 3. Form the Crew and Kickoff
            self.log("Manager: Organizing specialized agents...")
            crew = Crew(agents=[researcher, engineer], tasks=[research_task, coding_task], process=Process.sequential)
            
            self.log("Running AI Crew (this may take a minute)...")
            result = crew.kickoff()

            self.log("\n[SUCCESS] Final Logic Output:")
            self.log(result)
            
        except Exception as e:
            self.log(f"[ERROR] {str(e)}")

if __name__ == "__main__":
    app = AICorpApp()
    app.mainloop()