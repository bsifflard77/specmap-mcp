"""
Agent management for SpecMap
Handles RULEMAP specialized agents and their orchestration
"""

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class AgentManager:
    """Manages RULEMAP specialized agents"""

    AGENT_TYPES = {
        'prd-generator': {
            'name': 'PRD Generator Agent',
            'role': 'Requirements Analysis & Documentation',
            'persona': 'Brilliant recent graduate with advanced training in product management',
            'output_location': '01-specifications/',
            'session_tracking': '04-agents/session-summaries/'
        },
        'task-planner': {
            'name': 'Task Planning Agent',
            'role': 'Implementation Planning & Breakdown',
            'persona': 'Brilliant recent graduate with advanced training in software architecture',
            'output_location': '02-planning/',
            'session_tracking': '04-agents/session-summaries/'
        },
        'dev-guide': {
            'name': 'Development Guide Agent',
            'role': 'Implementation Guidance & Support',
            'persona': 'Brilliant recent graduate with advanced training in software engineering',
            'output_location': '03-implementation/',
            'session_tracking': '04-agents/session-summaries/'
        },
        'qa-monitor': {
            'name': 'Quality Assurance Agent',
            'role': 'Quality Control & RULEMAP Scoring',
            'persona': 'Brilliant recent graduate with advanced training in quality assurance',
            'output_location': '05-quality-assurance/',
            'session_tracking': '04-agents/session-summaries/'
        }
    }

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.assignments_file = project_path / "04-agents" / "agent-assignments.md"

    def activate_agent(self, agent_type: str) -> Dict[str, Any]:
        """Activate a specialized agent"""

        if agent_type not in self.AGENT_TYPES:
            raise ValueError(f"Unknown agent type: {agent_type}")

        agent_info = self.AGENT_TYPES[agent_type]

        # Create session directory if it doesn't exist
        session_dir = self.project_path / agent_info['session_tracking']
        session_dir.mkdir(parents=True, exist_ok=True)

        # Create agent configuration if it doesn't exist
        config_dir = self.project_path / "04-agents" / "agent-configurations" / "rulemap"
        config_dir.mkdir(parents=True, exist_ok=True)

        config_file = config_dir / f"{agent_type}.yaml"
        if not config_file.exists():
            self._create_agent_config(agent_type, config_file)

        # Update workflow state
        from .config import WorkflowState
        workflow = WorkflowState(self.project_path)
        workflow.load()
        workflow.activate_agent(agent_type)

        return {
            'agent_type': agent_type,
            'name': agent_info['name'],
            'status': 'activated',
            'timestamp': datetime.now().isoformat()
        }

    def get_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all agents"""

        from .config import WorkflowState
        workflow = WorkflowState(self.project_path)
        workflow.load()

        status = {}
        for agent_type, agent_info in self.AGENT_TYPES.items():
            is_active = workflow.state.get('active_agent') == agent_type
            status[agent_type] = {
                'name': agent_info['name'],
                'role': agent_info['role'],
                'status': 'active' if is_active else 'standby',
                'focus': workflow.state.get('current_phase', 'N/A') if is_active else 'N/A'
            }

        return status

    def _create_agent_config(self, agent_type: str, config_file: Path):
        """Create agent configuration file"""

        agent_info = self.AGENT_TYPES[agent_type]

        content = f"""# {agent_info['name']} Configuration

agent_id: "{agent_type}-v1"
specialization: "{agent_info['role']}"
persona: "{agent_info['persona']}"

## Core Strengths
- Deep understanding of {agent_info['role'].lower()}
- Superior analytical skills
- Comprehensive knowledge of best practices

## Experience Gaps
- Limited real-world experience
- Needs guidance on business context
- Must learn organizational constraints

## Collaboration Style
- Always explain reasoning in detail
- Break down complex concepts
- Seek validation frequently
- Treat user as experienced mentor

## Output Configuration
output_location: "{agent_info['output_location']}"
session_tracking: "{agent_info['session_tracking']}"

## Behavioral Requirements
- Explain all reasoning
- Ask clarifying questions
- Document decisions
- Maintain RULEMAP score >= 8.0
"""

        config_file.write_text(content, encoding='utf-8')