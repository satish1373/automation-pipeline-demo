from crewai import Agent, Task, Crew
import json
from datetime import datetime

# Load application context
def load_application_context():
    try:
        with open("application_context.json", "r") as f:
            return json.load(f)
    except:
        return {"error": "Context not found"}

# Define Agents with application context awareness
requirements_agent = Agent(
    role="Requirements Analyst with Context Awareness",
    goal="Analyze requirements using deep knowledge of the existing React application",
    backstory="""You are an expert requirements analyst who has complete knowledge of 
    the current React application structure. You know it uses React Hooks for state 
    management, has a DarkModeToggle component, and follows TypeScript patterns. 
    You always consider existing components for reuse and architectural consistency.""",
    verbose=True,
    allow_delegation=False
)

code_review_agent = Agent(
    role="Senior Code Reviewer with Application Knowledge", 
    goal="Review code changes considering the existing application architecture",
    backstory="""You are a senior code reviewer with intimate knowledge of this 
    React TypeScript application. You understand the current component structure, 
    the dark mode implementation, and the hook-based state management patterns. 
    You ensure all changes maintain consistency with existing code quality.""",
    verbose=True,
    allow_delegation=False
)

# Demo Functions
def demo_requirement_analysis():
    """Demo: Analyze a new requirement with application context"""
    print("=" * 60)
    print("DEMO: AI-Powered Requirement Analysis")
    print("=" * 60)
    
    # Load current application context
    context = load_application_context()
    
    requirement = "Add a search functionality to filter the application features list"
    
    task = Task(
        description=f"""
        Analyze this requirement: "{requirement}"
        
        Current Application Context:
        - Framework: {context.get('framework', 'Unknown')}
        - Components: {list(context.get('components', {}).keys())}
        - State Management: {context.get('state_management', [])}
        - Dependencies: {len(context.get('dependencies', {}))} packages
        
        Provide:
        1. Implementation approach using existing patterns
        2. Component reuse opportunities  
        3. New components needed
        4. Integration with current architecture
        5. Estimated complexity and effort
        """,
        agent=requirements_agent,
        expected_output="Detailed implementation plan with architectural considerations"
    )
    
    crew = Crew(
        agents=[requirements_agent],
        tasks=[task],
        verbose=2
    )
    
    result = crew.kickoff()
    return result

def demo_code_review():
    """Demo: AI-powered code review with context"""
    print("=" * 60)
    print("DEMO: AI-Powered Code Review")  
    print("=" * 60)
    
    context = load_application_context()
    
    # Simulate code changes
    changed_files = ["src/components/SearchFilter.tsx", "src/App.tsx"]
    
    task = Task(
        description=f"""
        Review these changed files: {changed_files}
        
        Application Context:
        - Existing components: {list(context.get('components', {}).keys())}
        - Current hooks used: React Hooks (useState, useEffect)
        - Architecture: React TypeScript with component-based structure
        
        Analyze:
        1. Code quality and consistency with existing patterns
        2. Proper integration with DarkModeToggle and App components
        3. TypeScript usage and type safety
        4. Hook usage following existing patterns
        5. Potential impact on existing functionality
        
        Provide approval recommendation.
        """,
        agent=code_review_agent,
        expected_output="Code review analysis with approval recommendation"
    )
    
    crew = Crew(
        agents=[code_review_agent],
        tasks=[task],
        verbose=2
    )
    
    result = crew.kickoff()
    return result

def demo_impact_analysis():
    """Demo: Analyze impact of changes on existing application"""
    print("=" * 60)
    print("DEMO: Change Impact Analysis")
    print("=" * 60)
    
    context = load_application_context()
    
    proposed_changes = {
        "new_component": "SearchFilter",
        "modified_files": ["App.tsx"],
        "new_dependencies": ["fuse.js for fuzzy search"]
    }
    
    task = Task(
        description=f"""
        Analyze the impact of these proposed changes: {proposed_changes}
        
        Current Application State:
        - Total components: {len(context.get('components', {}))}
        - Current dependencies: {len(context.get('dependencies', {}))}
        - State management: {context.get('state_management', [])}
        
        Assess:
        1. Impact on existing DarkModeToggle and App components
        2. Bundle size implications of new dependencies
        3. Compatibility with current React Hooks patterns
        4. Risk of breaking existing functionality
        5. Testing strategy recommendations
        
        Provide risk assessment and mitigation strategies.
        """,
        agent=code_review_agent,
        expected_output="Impact analysis with risk assessment and recommendations"
    )
    
    crew = Crew(
        agents=[code_review_agent],
        tasks=[task],
        verbose=2
    )
    
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    print("CrewAI Automation Pipeline Demo")
    print("Context-Aware AI Agents for React Application")
    print()
    
    # Load and display application context
    context = load_application_context()
    print(f"Application: {context.get('project_name', 'automation-pipeline-demo')}")
    print(f"Framework: {context.get('framework', 'Unknown')}")
    print(f"Components: {len(context.get('components', {}))}")
    print(f"Dependencies: {len(context.get('dependencies', {}))}")
    print(f"State Management: {context.get('state_management', [])}")
    print()
    
    print("Available Demos:")
    print("1. Requirement Analysis")
    print("2. Code Review")
    print("3. Impact Analysis")
    print("4. Run All Demos")
    
    choice = input("\nEnter demo number (1-4): ").strip()
    
    try:
        if choice == "1":
            result = demo_requirement_analysis()
        elif choice == "2":
            result = demo_code_review()
        elif choice == "3":
            result = demo_impact_analysis()
        elif choice == "4":
            print("\nRunning all demos...\n")
            demo_requirement_analysis()
            print("\n" + "="*60 + "\n")
            demo_code_review()
            print("\n" + "="*60 + "\n") 
            demo_impact_analysis()
        else:
            print("Invalid choice. Running requirement analysis demo...")
            result = demo_requirement_analysis()
            
        print("\nDemo completed successfully!")
        
    except Exception as e:
        print(f"Error running demo: {e}")
        print("Make sure CrewAI is properly installed and configured.")
