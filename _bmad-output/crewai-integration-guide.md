# CrewAI + BMAD Method Integration Guide

**Version**: 1.0.0  
**Last Updated**: 2026-09-03  
**Author**: Hsantos  
**Status**: Production Ready

---

## 1. Overview

This guide documents the integration of **CrewAI** with the **BMAD Method** framework, enabling multi-agent orchestration for automated development workflows.

### 1.1 What is CrewAI?

CrewAI is an open-source Python framework for orchestrating role-playing, autonomous AI agents. It provides:

- **Crews**: Teams of AI agents with roles, goals, tools, and tasks
- **Flows**: Event-driven workflows with state management
- **Production-ready patterns**: Human-in-the-loop, async execution, checkpointing

### 1.2 Why Integrate with BMAD?

| BMAD Strength | CrewAI Strength | Combined Benefit |
|---------------|-----------------|------------------|
| Development workflow expertise | Multi-agent orchestration | Automated development pipelines |
| 57 specialized skills | Role-based agent collaboration | Specialized agent teams |
| Technology-specific agents | Event-driven workflows | Complex automation flows |
| Code validation scripts | Tool integration | End-to-end quality assurance |

---

## 2. Compatibility Analysis

### 2.1 Technical Compatibility

| Component | BMAD | CrewAI | Compatible |
|-----------|------|--------|------------|
| Python | >= 3.10 | >= 3.10, < 3.14 | ✅ Yes |
| Package Manager | uv | uv | ✅ Yes |
| LLM Support | OpenCode, Claude | OpenAI, Ollama, etc. | ✅ Yes |
| Agent Framework | Skills-based | Role-based | ✅ Complementary |

### 2.2 Integration Points

```
┌─────────────────────────────────────────────────────────────┐
│                    BMAD Method                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Skills    │  │   Agents    │  │  Workflows  │         │
│  │  (57 total) │  │ (4 tech)    │  │  (5 phases) │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                  │
│         └────────────────┼────────────────┘                  │
│                          │                                   │
│                          ▼                                   │
│              ┌─────────────────────┐                         │
│              │   CrewAI Bridge     │                         │
│              │  (Python Layer)     │                         │
│              └──────────┬──────────┘                         │
│                         │                                    │
└─────────────────────────┼────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      CrewAI                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Crews     │  │   Flows     │  │   Tools     │         │
│  │ (Agents)    │  │ (Workflows) │  │ (Integrations│         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Installation

### 3.1 Prerequisites

Ensure you have:
- Python >= 3.10, < 3.14
- uv package manager
- BMAD Method installed

### 3.2 Install CrewAI

```bash
# Install CrewAI CLI globally
uv tool install crewai

# Verify installation
crewai --version
```

### 3.3 Environment Setup

```bash
# Create .env file for API keys
cat > .env << 'EOF'
# LLM Provider Keys
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here

# Optional: Serper for web search
SERPER_API_KEY=your-serper-key-here

# Optional: Disable telemetry
OTEL_SDK_DISABLED=true
EOF
```

---

## 4. Integration Architecture

### 4.1 BMAD-CrewAI Bridge

Create a Python module to bridge BMAD skills with CrewAI agents:

```python
# bmad_crewai_bridge.py
"""Bridge between BMAD Method and CrewAI framework."""

from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass

@dataclass
class BMADSkill:
    """Represents a BMAD skill for CrewAI integration."""
    name: str
    path: Path
    description: str
    category: str

class BMADBridge:
    """Bridge class for BMAD-CrewAI integration."""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.skills_dir = self.project_root / ".agents" / "skills"
        self.scripts_dir = self.project_root / "_bmad" / "scripts"
        
    def list_skills(self) -> list[BMADSkill]:
        """List all available BMAD skills."""
        skills = []
        for skill_dir in self.skills_dir.glob("bmad-*"):
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    skills.append(BMADSkill(
                        name=skill_dir.name,
                        path=skill_dir,
                        description=self._extract_description(skill_md),
                        category=self._categorize_skill(skill_dir.name)
                    ))
        return skills
    
    def render_skill(self, skill_name: str) -> str:
        """Render a BMAD skill using the render script."""
        render_script = self.scripts_dir / "render_skill.py"
        skill_path = f".agents/skills/{skill_name}"
        
        import subprocess
        result = subprocess.run(
            ["uv", "run", str(render_script), 
             "--project-root", str(self.project_root),
             "--skill", skill_path],
            capture_output=True,
            text=True
        )
        return result.stdout if result.returncode == 0 else result.stderr
    
    def validate_dockerfile(self, dockerfile_path: str) -> dict[str, Any]:
        """Validate a Dockerfile using BMAD validator."""
        validator = self.scripts_dir / "validate_dockerfile.py"
        
        import subprocess
        result = subprocess.run(
            ["uv", "run", str(validator), dockerfile_path],
            capture_output=True,
            text=True
        )
        
        return {
            "valid": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr
        }
    
    def _extract_description(self, skill_md: Path) -> str:
        """Extract description from SKILL.md."""
        content = skill_md.read_text()
        for line in content.split("\n"):
            if line.startswith("# "):
                return line[2:].strip()
        return "No description"
    
    def _categorize_skill(self, skill_name: str) -> str:
        """Categorize skill based on name."""
        if "docker" in skill_name:
            return "infrastructure"
        elif "python" in skill_name:
            return "language"
        elif "php" in skill_name:
            return "language"
        elif "postgres" in skill_name:
            return "database"
        else:
            return "workflow"
```

### 4.2 CrewAI Agents with BMAD Skills

```python
# crewai_bmad_agents.py
"""CrewAI agents enhanced with BMAD skills."""

from crewai import Agent, Task, Crew, Process
from bmad_crewai_bridge import BMADBridge

class BMADAgents:
    """Factory for creating CrewAI agents with BMAD capabilities."""
    
    def __init__(self, project_root: str):
        self.bridge = BMADBridge(project_root)
        
    def create_docker_architect(self) -> Agent:
        """Create a Docker Architect agent using BMAD Docker skill."""
        return Agent(
            role="Docker Architect",
            goal="Create optimized, secure Docker configurations",
            backstory="""You are an expert in containerization with deep knowledge
            of Docker best practices, multi-stage builds, security hardening,
            and BuildKit optimization.""",
            tools=[],  # Add Docker-specific tools here
            verbose=True,
            allow_delegation=False
        )
    
    def create_python_developer(self) -> Agent:
        """Create a Python Developer agent using BMAD Python 3.14 skill."""
        return Agent(
            role="Python 3.14 Developer",
            goal="Write modern Python 3.14 code with best practices",
            backstory="""You are a Python expert specializing in Python 3.14 features
            including free-threading, subinterpreters, t-strings, and
            performance optimization.""",
            tools=[],
            verbose=True,
            allow_delegation=False
        )
    
    def create_postgres_architect(self) -> Agent:
        """Create a PostgreSQL Architect agent using BMAD Postgres 18 skill."""
        return Agent(
            role="PostgreSQL 18 Architect",
            goal="Design optimal PostgreSQL 18 schemas and queries",
            backstory="""You are a PostgreSQL expert with deep knowledge of PG18
            features including AIO, Skip Scan, UUIDv7, pgvector,
            and advanced concurrency patterns.""",
            tools=[],
            verbose=True,
            allow_delegation=False
        )
    
    def create_code_reviewer(self) -> Agent:
        """Create a Code Reviewer agent using BMAD review skills."""
        return Agent(
            role="Code Reviewer",
            goal="Perform thorough code reviews with security focus",
            backstory="""You are a senior code reviewer who ensures code quality,
            security best practices, and adherence to standards.""",
            tools=[],
            verbose=True,
            allow_delegation=False
        )
```

### 4.3 CrewAI Flows for BMAD Workflows

```python
# crewai_bmad_flows.py
"""CrewAI flows for BMAD workflow automation."""

from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel
from crewai_bmad_agents import BMADAgents

class DevelopmentState(BaseModel):
    """State for development workflow."""
    project_name: str = ""
    requirements: str = ""
    architecture: str = ""
    code: str = ""
    tests: str = ""
    review_status: str = "pending"

class BMADDevelopmentFlow(Flow[DevelopmentState]):
    """Flow for automated BMAD development workflow."""
    
    def __init__(self, project_root: str):
        super().__init__()
        self.agents = BMADAgents(project_root)
    
    @start()
    def initialize_project(self):
        """Initialize project with BMAD configuration."""
        self.state.project_name = "New Project"
        return {"phase": "clarify"}
    
    @listen(initialize_project)
    def clarify_requirements(self, data):
        """Phase 1: Clarify requirements using BMAD brainstorming."""
        # Use BMAD brainstorming skill
        return {"phase": "plan"}
    
    @listen(clarify_requirements)
    def plan_architecture(self, data):
        """Phase 2: Plan architecture using BMAD architecture skill."""
        architect = self.agents.create_postgres_architect()
        
        planning_task = Task(
            description="Design database architecture for {project_name}",
            expected_output="Database schema with tables, indexes, and relationships",
            agent=architect
        )
        
        crew = Crew(
            agents=[architect],
            tasks=[planning_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff(inputs={"project_name": self.state.project_name})
        self.state.architecture = str(result)
        return {"phase": "build"}
    
    @listen(plan_architecture)
    def build_implementation(self, data):
        """Phase 3: Build implementation using BMAD build skill."""
        docker_agent = self.agents.create_docker_architect()
        python_agent = self.agents.create_python_developer()
        
        build_task = Task(
            description="Implement {project_name} with Docker and Python",
            expected_output="Working code with Docker configuration",
            agent=docker_agent
        )
        
        crew = Crew(
            agents=[docker_agent, python_agent],
            tasks=[build_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff(inputs={"project_name": self.state.project_name})
        self.state.code = str(result)
        return {"phase": "review"}
    
    @listen(build_implementation)
    def review_code(self, data):
        """Phase 4: Review code using BMAD code review skill."""
        reviewer = self.agents.create_code_reviewer()
        
        review_task = Task(
            description="Review code for {project_name}",
            expected_output="Code review with issues and recommendations",
            agent=reviewer
        )
        
        crew = Crew(
            agents=[reviewer],
            tasks=[review_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff(inputs={"project_name": self.state.project_name})
        self.state.review_status = str(result)
        return {"complete": True}
```

---

## 5. Usage Examples

### 5.1 Create a CrewAI Project

```bash
# Create a new CrewAI project
crewai create crew bmad-project

# Navigate to project
cd bmad-project

# Install dependencies
crewai install
```

### 5.2 Configure Agents with BMAD Skills

Edit `agents/researcher.jsonc`:

```json
{
  "role": "BMAD Research Specialist",
  "goal": "Research and analyze project requirements using BMAD methodology",
  "backstory": "You are an expert in BMAD Method who helps gather and structure project requirements.",
  "llm": "openai/gpt-4o",
  "tools": ["SerperDevTool"],
  "settings": {
    "verbose": true
  }
}
```

### 5.3 Run the Integration

```python
# main.py
from crewai_bmad_flows import BMADDevelopmentFlow

# Initialize flow
flow = BMADDevelopmentFlow(project_root="/path/to/project")

# Run the flow
result = flow.kickoff()
print(f"Development complete: {result}")
```

### 5.4 CLI Usage

```bash
# Run CrewAI crew
crewai run

# Or run specific flow
python main.py
```

---

## 6. Advanced Integration Patterns

### 6.1 BMAD Skill as CrewAI Tool

```python
# bmad_skill_tool.py
"""Wrap BMAD skill as CrewAI tool."""

from crewai.tools import BaseTool
from bmad_craftai_bridge import BMADBridge

class BMADSkillTool(BaseTool):
    """Tool for executing BMAD skills."""
    name: str = "bmad_skill_executor"
    description: str = "Execute a BMAD skill by name"
    
    def __init__(self, project_root: str):
        super().__init__()
        self.bridge = BMADBridge(project_root)
    
    def _run(self, skill_name: str) -> str:
        """Execute a BMAD skill."""
        return self.bridge.render_skill(skill_name)
```

### 6.2 Automated Testing with BMAD

```python
# automated_testing.py
"""Automated testing using BMAD and CrewAI."""

from crewai import Agent, Task, Crew, Process

def create_testing_crew():
    """Create a crew for automated testing."""
    
    tester = Agent(
        role="QA Engineer",
        goal="Write and execute comprehensive tests",
        backstory="You are an expert in test automation using pytest and BMAD patterns.",
        verbose=True
    )
    
    test_task = Task(
        description="Write unit tests for the application",
        expected_output="Complete test suite with pytest",
        agent=tester
    )
    
    return Crew(
        agents=[tester],
        tasks=[test_task],
        process=Process.sequential,
        verbose=True
    )
```

---

## 7. Configuration

### 7.1 Environment Variables

```bash
# .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
SERPER_API_KEY=...
OTEL_SDK_DISABLED=true
```

### 7.2 BMAD-CrewAI Configuration

```yaml
# bmad_crewai_config.yaml
integration:
  enabled: true
  project_root: "/home/hsantos/app"
  
agents:
  docker_architect:
    enabled: true
    skills: ["bmad-docker", "bmad-agent-docker"]
  python_developer:
    enabled: true
    skills: ["bmad-python314", "bmad-agent-python314"]
  php_developer:
    enabled: true
    skills: ["bmad-php84", "bmad-agent-php84"]
  postgres_architect:
    enabled: true
    skills: ["bmad-postgres18", "bmad-agent-postgres18"]

workflows:
  development:
    phases: ["clarify", "plan", "build", "review", "learn"]
    auto_advance: true
```

---

## 8. Best Practices

### 8.1 Agent Design

1. **Clear Roles**: Define specific roles for each agent
2. **Focused Goals**: Each agent should have a clear, measurable goal
3. **Rich Backstories**: Provide context for better decision-making
4. **Tool Selection**: Use appropriate tools for each task

### 8.2 Flow Design

1. **State Management**: Use Pydantic models for structured state
2. **Error Handling**: Implement proper error handling in flows
3. **Human-in-the-loop**: Add human review points for critical decisions
4. **Checkpointing**: Use checkpointing for long-running flows

### 8.3 Integration Tips

1. **Start Simple**: Begin with basic integration and expand
2. **Validate Outputs**: Always validate CrewAI outputs against BMAD standards
3. **Use BMAD Skills**: Leverage existing BMAD skills as CrewAI tools
4. **Monitor Performance**: Track agent performance and optimize

---

## 9. Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| CrewAI not found | Run `uv tool install crewai` |
| Python version error | Ensure Python >= 3.10, < 3.14 |
| API key errors | Check `.env` file configuration |
| Import errors | Run `crewai install` in project directory |
| BMAD skill not found | Verify skill exists in `.agents/skills/` |

### Debug Mode

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with verbose output
crew = Crew(agents=[...], tasks=[...], verbose=True)
result = crew.kickoff()
```

---

## 10. References

| Resource | URL |
|----------|-----|
| CrewAI Documentation | https://docs.crewai.com |
| CrewAI GitHub | https://github.com/crewAIInc/crewAI |
| BMAD Method | https://github.com/bmadmethod/bmad-method |
| CrewAI Examples | https://github.com/crewAIInc/crewAI-examples |

---

## 11. Next Steps

1. **Explore CrewAI Examples**: Check out the CrewAI examples repository
2. **Create Custom Tools**: Build tools specific to your development workflow
3. **Build Complex Flows**: Design multi-stage development pipelines
4. **Contribute**: Share your integration patterns with the community
