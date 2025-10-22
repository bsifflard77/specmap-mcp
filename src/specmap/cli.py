"""
SpecMap CLI - Main Command Line Interface
Unified Spec-Kit + RULEMAP-PRD system
"""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from pathlib import Path
from datetime import datetime
import sys
import os

from .config import SpecMapConfig, WorkflowState
from .structure import ProjectStructure, sanitize_name
from .init import ProjectInitializer
from .agents import AgentManager
from .skills import SkillManager
from .folders import FolderManager, format_size, get_folder_guide

console = Console()

# Supported AI agents
SUPPORTED_AGENTS = [
    'claude', 'gemini', 'copilot', 'cursor', 'qwen',
    'opencode', 'windsurf', 'codex', 'kilocode', 'auggie', 'roo'
]

# Project types
PROJECT_TYPES = [
    'web-app', 'mobile-app', 'api-service', 'desktop-app',
    'data-pipeline', 'ml-model', 'library'
]


@click.group()
@click.version_option(version="1.0.0", prog_name="specmap")
def main():
    """
    SpecMap CLI - Unified Spec-Kit + RULEMAP-PRD System

    Combines spec-driven development with comprehensive project management.
    """
    pass


@main.command()
@click.argument('project_name', required=False)
@click.option('--type', 'project_type', type=click.Choice(PROJECT_TYPES),
              default='web-app', help='Type of project')
@click.option('--agent', type=click.Choice(SUPPORTED_AGENTS),
              default='claude', help='AI agent to use')
@click.option('--path', default='.', help='Base path for project creation')
@click.option('--here', is_flag=True, help='Initialize in current directory')
@click.option('--force', is_flag=True, help='Force initialization (overwrite existing)')
def init(project_name, project_type, agent, path, here, force):
    """Initialize a new SpecMap project with unified structure."""

    console.print(Panel.fit(
        "[bold cyan]SpecMap Initialization[/bold cyan]\n"
        "Creating unified Spec-Kit + RULEMAP-PRD project",
        border_style="cyan"
    ))

    # Determine project path
    if here or project_name == '.':
        project_path = Path.cwd()
        if not project_name or project_name == '.':
            project_name = project_path.name
    else:
        if not project_name:
            console.print("[red]Error:[/red] Project name required", style="bold")
            sys.exit(1)
        safe_name = sanitize_name(project_name)
        timestamp = datetime.now().strftime("%Y-%m-%d")
        project_path = Path(path) / f"{safe_name}-{timestamp}"

    # Check if directory exists
    if project_path.exists() and not force and not here:
        console.print(f"[yellow]Warning:[/yellow] Directory {project_path} already exists")
        if not click.confirm("Continue and merge?"):
            sys.exit(0)

    try:
        # Initialize project
        initializer = ProjectInitializer(project_path, project_name, project_type, agent)
        result = initializer.initialize()

        # Display results
        console.print("\n[green]OK[/green] Project initialized successfully!", style="bold")
        console.print(f"\n[cyan]Project Location:[/cyan] {result['path']}")
        console.print(f"[cyan]Project Type:[/cyan] {project_type}")
        console.print(f"[cyan]Base Agent:[/cyan] {agent}")

        # Display next steps
        console.print("\n[bold yellow]Next Steps:[/bold yellow]")
        console.print("1. cd " + str(project_path))
        console.print("2. Review and complete 00-governance/project-charter.md")
        console.print("3. Update 00-governance/constitution.md with project principles")
        console.print("4. Run: [cyan]specmap specify[/cyan] to create your first feature spec")

        console.print(f"\n[dim]For detailed guidance, see: README.md[/dim]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        sys.exit(1)


@main.command()
@click.argument('content', required=False)
@click.option('--edit', is_flag=True, help='Open constitution in editor')
def constitution(content, edit):
    """Create or update project constitution (Spec-Kit governance)."""

    project_path = Path.cwd()
    constitution_file = project_path / "00-governance" / "constitution.md"

    if not constitution_file.parent.exists():
        console.print("[red]Error:[/red] Not in a SpecMap project directory")
        console.print("[dim]Run 'specmap init' first[/dim]")
        sys.exit(1)

    if edit:
        import subprocess
        editor = os.environ.get('EDITOR', 'nano')
        subprocess.call([editor, str(constitution_file)])
    elif content:
        # Append to constitution
        with open(constitution_file, 'a') as f:
            f.write(f"\n\n{content}\n")
        console.print("[green]OK[/green] Constitution updated")
    else:
        # Display current constitution
        if constitution_file.exists():
            console.print(constitution_file.read_text())
        else:
            console.print("[yellow]Constitution not yet created[/yellow]")


@main.command()
@click.option('--complete', is_flag=True, help='Interactive charter completion')
def charter(complete):
    """Manage project charter (RULEMAP governance)."""

    project_path = Path.cwd()
    charter_file = project_path / "00-governance" / "project-charter.md"

    if not charter_file.exists():
        console.print("[red]Error:[/red] Project charter not found")
        sys.exit(1)

    if complete:
        console.print("[cyan]Interactive charter completion coming soon...[/cyan]")
        console.print(f"[dim]For now, edit: {charter_file}[/dim]")
    else:
        console.print(charter_file.read_text())


@main.command()
@click.argument('description')
@click.option('--feature-id', help='Specific feature ID (default: auto-generate)')
def specify(description, feature_id):
    """Create RULEMAP-enhanced specification."""

    from .specify import SpecificationCreator

    console.print(Panel.fit(
        "[bold cyan]Creating Feature Specification[/bold cyan]\n"
        "RULEMAP-enhanced specification with tracking IDs",
        border_style="cyan"
    ))

    console.print(f"[yellow]Description:[/yellow] {description}\n")

    try:
        # Create the specification
        creator = SpecificationCreator(Path.cwd())
        result = creator.create_specification(description, feature_id)

        # Display success information
        console.print("[green]OK[/green] Feature specification created successfully!\n")

        # Display created files
        console.print("[bold]Created Files:[/bold]")
        console.print(f"* [cyan]Specification:[/cyan] {result['spec_file']}")
        console.print(f"? [cyan]Clarifications:[/cyan] {result['clarifications_file']}")
        console.print(f"> [cyan]Research:[/cyan] {result['research_file']}")

        # Display feature information
        console.print(f"\n[bold]Feature Details:[/bold]")
        console.print(f"#  [cyan]Feature ID:[/cyan] {result['feature_id']}")
        console.print(f"@ [cyan]Feature Path:[/cyan] {result['feature_path']}")

        # Display tracking IDs
        console.print(f"\n[bold]Initial Tracking IDs:[/bold]")
        for category, ids in result['tracking_ids'].items():
            console.print(f"* [cyan]{category.title()}:[/cyan] {', '.join(ids)}")

        # Display next steps
        console.print("\n[bold yellow]Next Steps:[/bold yellow]")
        console.print("1. Review and complete the specification in spec.md")
        console.print("2. Run: [cyan]specmap clarify[/cyan] to resolve open questions")
        console.print("3. Complete all RULEMAP sections for proper scoring")
        console.print("4. Aim for RULEMAP score >= 8.0 before proceeding")

        console.print(f"\n[dim]TIP: Tip: Use your AI agent to help complete the specification[/dim]")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {str(e)}", style="bold")
        console.print("[dim]Please check your project structure and try again[/dim]")
        sys.exit(1)


@main.command()
@click.argument('feature_id', required=False)
@click.option('--interactive', '-i', is_flag=True, default=True, help='Run interactive clarification session')
@click.option('--auto', is_flag=True, help='Auto-resolve simple clarifications')
def clarify(feature_id, interactive, auto):
    """Run systematic clarification process (Spec-Kit methodology)."""

    # Auto flag overrides interactive
    if auto:
        interactive = False

    from .clarify import ClarificationProcessor

    console.print(Panel.fit(
        "[bold cyan]Feature Clarification Process[/bold cyan]\n"
        "Interactive Q&A to resolve open questions",
        border_style="cyan"
    ))

    try:
        # Initialize clarification processor
        processor = ClarificationProcessor(Path.cwd())
        result = processor.run_clarification_process(feature_id, interactive)

        # Handle different result types
        if result.get('action_required') == 'feature_selection':
            console.print("[yellow]Multiple features available. Please specify which to clarify:[/yellow]\n")
            for i, feature in enumerate(result['available_features'], 1):
                console.print(f"{i}. [cyan]{feature}[/cyan]")
            console.print(f"\n[dim]Usage: specmap clarify [feature_id][/dim]")
            return

        if result.get('error'):
            console.print(f"[red]Error:[/red] {result['error']}")
            if result.get('available_features'):
                console.print("\n[yellow]Available features:[/yellow]")
                for feature in result['available_features']:
                    console.print(f"  • [cyan]{feature}[/cyan]")
            return

        feature_id = result['feature_id']

        if result.get('status') == 'no_questions_found':
            console.print(f"[green]OK[/green] No open questions found for [cyan]{feature_id}[/cyan]!")

            # Display RULEMAP score
            score_data = result.get('rulemap_score', {})
            score = score_data.get('score', 0.0)
            meets_threshold = score_data.get('meets_threshold', False)

            score_color = "green" if meets_threshold else "yellow"
            console.print(f"\n[bold]RULEMAP Score:[/bold] [{score_color}]{score}/10.0[/{score_color}]")

            if meets_threshold:
                console.print("[green]OK[/green] Specification meets quality threshold (≥8.0)")
                console.print(f"\n[bold yellow]Next Step:[/bold yellow] Run [cyan]specmap plan[/cyan] to generate implementation plan")
            else:
                console.print("[yellow]WARN[/yellow] Specification needs improvement to meet quality threshold")
                console.print("[dim]Complete more RULEMAP sections or add missing details[/dim]")

            # Show section completion
            if score_data.get('section_scores'):
                console.print(f"\n[bold]Section Completion:[/bold]")
                for section, scores in score_data['section_scores'].items():
                    completion = scores['completion']
                    color = "green" if completion >= 0.8 else "yellow" if completion >= 0.5 else "red"
                    console.print(f"  [{color}]{section}[/{color}]: {completion:.0%}")

            return

        if result.get('status') == 'questions_found':
            questions = result['questions']
            console.print(f"[yellow]Found {len(questions)} open questions for [cyan]{feature_id}[/cyan][/yellow]\n")

            if not interactive:
                # Just display the questions
                console.print("[bold]Open Questions:[/bold]")
                for i, q in enumerate(questions, 1):
                    console.print(f"{i}. [yellow]{q['question']}[/yellow]")
                    console.print(f"   [dim]Source: {q['source']} (line {q['line']})[/dim]")
                    console.print()

                console.print("[dim]TIP: Tip: Run with -i flag for interactive clarification session[/dim]")
                console.print("[dim]Usage: specmap clarify {} -i[/dim]".format(feature_id))
                return

            # Interactive clarification session
            console.print("[bold]Starting interactive clarification session...[/bold]\n")

            questions_and_answers = []
            for i, question in enumerate(questions, 1):
                console.print(f"[bold cyan]Question {i}/{len(questions)}:[/bold cyan]")
                console.print(f"[yellow]{question['question']}[/yellow]")
                console.print(f"[dim]Source: {question['source']} (line {question['line']})[/dim]")

                # Get answer from user
                try:
                    answer = click.prompt("\n[bold]Answer", type=str, default="", show_default=False)
                except click.Abort:
                    console.print("[yellow]SKIP[/yellow] User cancelled\n")
                    answer = ""

                if answer.strip():
                    questions_and_answers.append({
                        'id': question['id'],
                        'question': question['question'],
                        'answer': answer.strip(),
                        'context': question['context']
                    })
                    console.print("[green]OK[/green] Answer recorded\n")
                else:
                    console.print("[yellow]SKIP[/yellow] Skipped\n")

            if questions_and_answers:
                # Create clarification session
                session_result = processor.create_clarification_session(feature_id, questions_and_answers)

                # Update specification with clarifications
                update_result = processor.update_specification_with_clarifications(feature_id, questions_and_answers)

                console.print(f"[green]OK[/green] Clarification session completed!")
                console.print(f"[cyan]Resolved:[/cyan] {session_result['questions_resolved']} questions")
                console.print(f"[cyan]Updated:[/cyan] {update_result['clarifications_processed']} specification sections")

                # Calculate new RULEMAP score
                score_result = processor.calculate_rulemap_score(feature_id)
                score = score_result.get('score', 0.0)
                meets_threshold = score_result.get('meets_threshold', False)

                score_color = "green" if meets_threshold else "yellow"
                console.print(f"\n[bold]Updated RULEMAP Score:[/bold] [{score_color}]{score}/10.0[/{score_color}]")

                if meets_threshold:
                    console.print("[green]OK[/green] Specification now meets quality threshold!")
                    console.print(f"\n[bold yellow]Next Step:[/bold yellow] Run [cyan]specmap plan[/cyan] to generate implementation plan")
                else:
                    console.print("[yellow]WARN[/yellow] Consider running clarify again or adding more detail")

                console.print(f"\n[dim]* Updated files:[/dim]")
                console.print(f"[dim]  • {session_result['clarifications_file']}[/dim]")
                console.print(f"[dim]  • {update_result['spec_file']}[/dim]")

            else:
                console.print("[yellow]No questions were answered. Clarification session cancelled.[/yellow]")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        sys.exit(1)
    except Exception as e:
        import traceback
        console.print(f"[red]Unexpected error:[/red] {str(e)}", style="bold")
        console.print(f"[red]Exception type:[/red] {type(e).__name__}")
        console.print("[red]Full traceback:[/red]")
        traceback.print_exc()
        console.print("[dim]Please check your project structure and try again[/dim]")
        sys.exit(1)


@main.command()
@click.argument('feature_id', required=False)
@click.option('--force', is_flag=True, help='Force plan generation even if already exists')
def plan(feature_id, force):
    """Generate agent-driven implementation plan."""

    from .plan import PlanGenerator

    console.print(Panel.fit(
        "[bold cyan]Implementation Plan Generation[/bold cyan]\n"
        "Create comprehensive implementation plan from approved specification",
        border_style="cyan"
    ))

    try:
        # Initialize plan generator
        generator = PlanGenerator(Path.cwd())

        # Get available features if none specified
        if not feature_id:
            available_features = generator.get_available_features()
            if not available_features:
                console.print("[red]Error:[/red] No approved features found.")
                console.print("[dim]Features must have RULEMAP score ≥8.0 to generate plans[/dim]")
                console.print("[dim]Run 'specmap clarify' to improve specification quality[/dim]")
                return

            if len(available_features) == 1:
                feature_id = available_features[0]
                console.print(f"[cyan]Auto-selected feature:[/cyan] {feature_id}")
            else:
                console.print("[yellow]Multiple approved features available:[/yellow]\n")
                for i, feature in enumerate(available_features, 1):
                    console.print(f"{i}. [cyan]{feature}[/cyan]")
                console.print(f"\n[dim]Usage: specmap plan [feature_id][/dim]")
                return

        # Check if plan already exists
        feature_paths = generator.structure.get_feature_path(feature_id)
        plan_file = feature_paths['plan'] / "plan.md"

        if plan_file.exists() and not force:
            console.print(f"[yellow]Plan already exists for [cyan]{feature_id}[/cyan][/yellow]")
            console.print(f"[dim]Use --force flag to regenerate[/dim]")
            console.print(f"[dim]Current plan: {plan_file}[/dim]")
            return

        # Generate implementation plan
        console.print(f"[cyan]Generating implementation plan for [bold]{feature_id}[/bold]...[/cyan]\n")

        result = generator.generate_implementation_plan(feature_id)

        # Display success information
        console.print("[green]OK[/green] Implementation plan generated successfully!\n")

        # Display plan overview
        console.print("[bold]Plan Overview:[/bold]")
        console.print(f"* [cyan]Feature ID:[/cyan] {result['feature_id']}")
        console.print(f"@ [cyan]Estimated Duration:[/cyan] {result['estimated_duration']} days")
        console.print(f"# [cyan]Technical Decisions:[/cyan] {len(result['technical_decisions'])}")
        console.print(f"% [cyan]Milestones:[/cyan] {len(result['milestones'])}")

        # Display created files
        console.print(f"\n[bold]Generated Files:[/bold]")
        console.print(f"* [cyan]Implementation Plan:[/cyan] {result['plan_file']}")
        console.print(f"* [cyan]API Contracts:[/cyan] {result['contracts_file']}")
        console.print(f"* [cyan]Data Models:[/cyan] {result['data_models_file']}")

        # Display key technical decisions
        if result['technical_decisions']:
            console.print(f"\n[bold]Key Technical Decisions:[/bold]")
            for decision in result['technical_decisions'][:3]:  # Show first 3
                console.print(f"- [yellow]{decision['title']}:[/yellow] {decision['decision']}")

        # Display milestones
        if result['milestones']:
            console.print(f"\n[bold]Project Milestones:[/bold]")
            for milestone in result['milestones']:
                console.print(f"# [cyan]{milestone['title']}:[/cyan] {milestone['date']}")

        # Display analysis insights
        analysis = result['analysis']
        rulemap_score = analysis['rulemap_score']['score']
        complexity = analysis['complexity_indicators']['complexity_score']

        console.print(f"\n[bold]Analysis Summary:[/bold]")
        console.print(f"= [cyan]RULEMAP Score:[/cyan] {rulemap_score}/10.0")
        console.print(f"+ [cyan]Complexity Score:[/cyan] {complexity}")
        console.print(f"# [cyan]Requirements:[/cyan] {len(analysis['functional_requirements'])}")
        console.print(f"+ [cyan]Acceptance Criteria:[/cyan] {len(analysis['acceptance_criteria'])}")

        # Display next steps
        console.print("\n[bold yellow]Next Steps:[/bold yellow]")
        console.print("1. Review and approve the implementation plan")
        console.print("2. Validate technical decisions with stakeholders")
        console.print("3. Run: [cyan]specmap tasks[/cyan] to generate detailed task breakdown")
        console.print("4. Set up development environment and begin implementation")

        console.print(f"\n[dim]TIP: Tip: Review the plan files before proceeding to task generation[/dim]")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        console.print("\n[dim]Available commands:[/dim]")
        console.print("[dim]  • specmap specify - Create feature specification[/dim]")
        console.print("[dim]  • specmap clarify - Improve specification quality[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {str(e)}", style="bold")
        console.print("[dim]Please check your project structure and try again[/dim]")
        sys.exit(1)


@main.command()
@click.argument('feature_id', required=False)
@click.option('--force', is_flag=True, help='Force task generation even if already exists')
@click.option('--detailed', is_flag=True, help='Show detailed task breakdown')
def tasks(feature_id, force, detailed):
    """Generate RULEMAP agent task breakdown."""

    from .tasks import TaskGenerator

    console.print(Panel.fit(
        "[bold cyan]Task Generation[/bold cyan]\n"
        "Generate detailed task breakdown with TDD workflow",
        border_style="cyan"
    ))

    try:
        # Initialize task generator
        generator = TaskGenerator(Path.cwd())

        # Get features with plans if none specified
        if not feature_id:
            features_with_plans = generator.get_features_with_plans()
            if not features_with_plans:
                console.print("[red]Error:[/red] No implementation plans found.")
                console.print("[dim]Implementation plans are required to generate tasks[/dim]")
                console.print("[dim]Run 'specmap plan' to create implementation plans[/dim]")
                return

            if len(features_with_plans) == 1:
                feature_id = features_with_plans[0]
                console.print(f"[cyan]Auto-selected feature:[/cyan] {feature_id}")
            else:
                console.print("[yellow]Multiple features with plans available:[/yellow]\n")
                for i, feature in enumerate(features_with_plans, 1):
                    console.print(f"{i}. [cyan]{feature}[/cyan]")
                console.print(f"\n[dim]Usage: specmap tasks [feature_id][/dim]")
                return

        # Check if tasks already exist
        feature_path = generator.structure.get_feature_path(feature_id)['plan']
        tasks_file = feature_path / "tasks.md"

        if tasks_file.exists() and not force:
            console.print(f"[yellow]Tasks already exist for [cyan]{feature_id}[/cyan][/yellow]")
            console.print(f"[dim]Use --force flag to regenerate[/dim]")
            console.print(f"[dim]Current tasks: {tasks_file}[/dim]")
            return

        # Generate tasks
        console.print(f"[cyan]Generating task breakdown for [bold]{feature_id}[/bold]...[/cyan]\n")

        result = generator.generate_tasks_for_feature(feature_id)

        # Display success information
        console.print("[green]OK[/green] Task breakdown generated successfully!\n")

        # Display task overview
        console.print("[bold]Task Overview:[/bold]")
        console.print(f"* [cyan]Feature ID:[/cyan] {result['feature_id']}")
        console.print(f"# [cyan]Total Tasks:[/cyan] {result['total_tasks']}")
        console.print(f"@ [cyan]Estimated Duration:[/cyan] {result['estimated_duration']} days")
        console.print(f"* [cyan]Tasks File:[/cyan] {result['tasks_file']}")

        # Display tasks by phase
        console.print(f"\n[bold]Tasks by Phase:[/bold]")
        phase_names = {
            'setup': 'Setup & Prerequisites',
            'tdd_red': 'TDD Red Phase (Tests)',
            'tdd_green': 'TDD Green Phase (Implementation)',
            'integration': 'Integration & Enhancement',
            'qa': 'QA & Testing',
            'docs_deploy': 'Documentation & Deployment'
        }

        for phase, count in result['tasks_by_phase'].items():
            if count > 0:
                phase_display = phase_names.get(phase, phase.replace('_', ' ').title())
                console.print(f"  - [cyan]{phase_display}:[/cyan] {count} tasks")

        # Display parallel execution info
        console.print(f"\n[bold]Execution Info:[/bold]")
        console.print(f"|| [cyan]Parallel Groups:[/cyan] {result['parallel_groups']}")
        console.print(f">> [cyan]Max Parallelism:[/cyan] Up to {min(result['parallel_groups'], 4)} tasks simultaneously")

        # Display detailed breakdown if requested
        if detailed:
            analysis = result['analysis']
            complexity = analysis.get('complexity_indicators', {})

            console.print(f"\n[bold]Technical Analysis:[/bold]")
            console.print(f"+ [cyan]Complexity Score:[/cyan] {complexity.get('complexity_score', 0)}")
            console.print(f"^ [cyan]Architecture:[/cyan] {'Database' if complexity.get('has_database') else 'Simple'}")
            console.print(f"* [cyan]API Layer:[/cyan] {'Yes' if complexity.get('has_api') else 'No'}")
            console.print(f"@ [cyan]Authentication:[/cyan] {'Yes' if complexity.get('has_auth') else 'No'}")
            console.print(f"& [cyan]Integrations:[/cyan] {'Yes' if complexity.get('has_external_integrations') else 'No'}")

            # Show technology stack
            tech_stack = analysis.get('technology_stack', {})
            if any(tech_stack.values()):
                console.print(f"\n[bold]Technology Stack:[/bold]")
                for tech_type, tech_value in tech_stack.items():
                    if tech_value:
                        console.print(f"  • [cyan]{tech_type.title()}:[/cyan] {tech_value}")

        # Display next steps
        console.print("\n[bold yellow]Next Steps:[/bold yellow]")
        console.print("1. Review the generated task breakdown")
        console.print("2. Set up development environment (Phase 0)")
        console.print("3. Begin TDD Red Phase - write failing tests first")
        console.print("4. Run: [cyan]specmap track[/cyan] to start progress tracking")
        console.print("5. Follow TDD workflow: Red -> Green -> Refactor")

        console.print(f"\n[dim]TIP: Tip: Tasks follow strict TDD workflow - tests must be written before implementation[/dim]")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}", style="bold")
        console.print("\n[dim]Available commands:[/dim]")
        console.print("[dim]  • specmap specify - Create feature specification[/dim]")
        console.print("[dim]  • specmap clarify - Improve specification quality[/dim]")
        console.print("[dim]  • specmap plan - Generate implementation plan[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {str(e)}", style="bold")
        console.print("[dim]Please check your project structure and try again[/dim]")
        sys.exit(1)


@main.command()
def implement():
    """Begin agent-guided implementation."""

    console.print("[cyan]Starting guided implementation...[/cyan]")
    console.print("[yellow]Note:[/yellow] This command should be run with your AI agent")
    console.print("[dim]Implementation coming in next phase...[/dim]")


@main.group()
def agent():
    """Manage RULEMAP agents."""
    pass


@agent.command('activate')
@click.argument('agent_type', type=click.Choice([
    'prd-generator', 'task-planner', 'dev-guide', 'qa-monitor'
]))
def agent_activate(agent_type):
    """Activate a RULEMAP specialized agent."""

    project_path = Path.cwd()
    manager = AgentManager(project_path)

    try:
        manager.activate_agent(agent_type)
        console.print(f"[green]OK[/green] Activated {agent_type} agent")
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@agent.command('status')
def agent_status():
    """View all agent assignments and status."""

    project_path = Path.cwd()
    manager = AgentManager(project_path)

    try:
        status = manager.get_status()

        table = Table(title="Agent Status")
        table.add_column("Agent", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Current Focus", style="yellow")

        for agent_name, agent_data in status.items():
            table.add_row(
                agent_name,
                agent_data.get('status', 'Unknown'),
                agent_data.get('focus', 'N/A')
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@agent.command('handoff')
@click.argument('from_agent')
@click.argument('to_agent')
def agent_handoff(from_agent, to_agent):
    """Transfer work between agents."""

    console.print(f"[cyan]Handing off from {from_agent} to {to_agent}...[/cyan]")
    console.print("[dim]Implementation coming in next phase...[/dim]")


@main.command()
@click.option('--type', 'score_type', type=click.Choice(['rulemap', 'constitution', 'both']),
              default='both', help='Type of scoring to perform')
def score(score_type):
    """Perform quality assessment (RULEMAP scoring or constitution validation)."""

    console.print(f"[cyan]Running {score_type} quality assessment...[/cyan]")
    console.print("[dim]Implementation coming in next phase...[/dim]")


@main.command()
@click.option('--detailed', is_flag=True, help='Show detailed status')
def status(detailed):
    """Show project progress overview."""

    project_path = Path.cwd()

    try:
        config = SpecMapConfig(project_path)
        config.load()

        workflow = WorkflowState(project_path)
        workflow.load()

        # Display project info
        console.print(Panel.fit(
            f"[bold cyan]{config.get('project.name', 'Unknown Project')}[/bold cyan]\n"
            f"Type: {config.get('project.type', 'Unknown')}\n"
            f"Version: {config.get('project.version', '1.0.0')}",
            title="Project Status",
            border_style="cyan"
        ))

        # Display workflow state
        console.print(f"\n[yellow]Current Phase:[/yellow] {workflow.state.get('current_phase', 'Unknown')}")
        console.print(f"[yellow]Active Agent:[/yellow] {workflow.state.get('active_agent', 'None')}")

        if detailed and workflow.state.get('features'):
            console.print("\n[bold]Features:[/bold]")
            for feature_id, feature_data in workflow.state['features'].items():
                console.print(f"  • {feature_id}: {feature_data.get('status', 'Unknown')}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")


@main.command()
def sync():
    """Update all agent contexts and configurations."""

    console.print("[cyan]Syncing agent contexts...[/cyan]")
    console.print("[dim]Implementation coming in next phase...[/dim]")


@main.command()
def check():
    """Check system prerequisites and agent availability."""

    console.print("[bold cyan]SpecMap System Check[/bold cyan]\n")

    # Check Python version
    import sys
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    console.print(f"[green]OK[/green] Python {python_version}")

    # Check for git
    import subprocess
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            console.print(f"[green]OK[/green] {result.stdout.strip()}")
        else:
            console.print("[red]FAIL[/red] Git not found")
    except FileNotFoundError:
        console.print("[red]FAIL[/red] Git not installed")

    # Check for AI agents
    console.print("\n[bold]AI Agent Availability:[/bold]")
    agents_to_check = {
        'claude': 'Claude Code CLI',
        'gemini': 'Gemini CLI',
        'cursor': 'Cursor CLI'
    }

    for cmd, name in agents_to_check.items():
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                console.print(f"[green]OK[/green] {name}")
            else:
                console.print(f"[dim]--[/dim] {name} (not found)")
        except FileNotFoundError:
            console.print(f"[dim]--[/dim] {name} (not found)")

    console.print("\n[dim]Note: AI agents are optional - you can use IDE-based agents like Copilot or Windsurf[/dim]")


@main.group()
def skill():
    """Manage Claude Code skills for SpecMap."""
    pass


@skill.command('list')
def skill_list():
    """List all installed Claude Code skills."""
    project_path = Path.cwd()
    manager = SkillManager(project_path)

    try:
        skills = manager.list_skills()

        if not skills:
            console.print("[yellow]No skills installed yet[/yellow]")
            console.print("[dim]Run 'specmap skill install-all' to install SpecMap skill templates[/dim]")
            return

        console.print(Panel.fit(
            "[bold cyan]Installed Claude Code Skills[/bold cyan]",
            border_style="cyan"
        ))

        for skill in skills:
            console.print(f"\n[cyan]{skill['name']}[/cyan]")
            console.print(f"  {skill['description']}")
            console.print(f"  [dim]{skill['file']}[/dim]")

        console.print(f"\n[green]Total:[/green] {len(skills)} skills")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@skill.command('templates')
def skill_templates():
    """Show available skill templates."""
    manager = SkillManager()

    try:
        templates = manager.get_available_templates()

        console.print(Panel.fit(
            "[bold cyan]Available SpecMap Skill Templates[/bold cyan]",
            border_style="cyan"
        ))

        for template in templates:
            console.print(f"\n[cyan]{template['name']}[/cyan]")
            console.print(f"  {template['description']}")

        console.print(f"\n[green]Total:[/green] {len(templates)} templates available")
        console.print("\n[dim]Install with: specmap skill install <template-name>[/dim]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@skill.command('install')
@click.argument('template_name')
def skill_install(template_name):
    """Install a specific skill template."""
    project_path = Path.cwd()
    manager = SkillManager(project_path)

    try:
        result = manager.create_skill_from_template(template_name)

        console.print(f"[green]OK[/green] Skill installed successfully!")
        console.print(f"[cyan]Name:[/cyan] {result['skill_name']}")
        console.print(f"[cyan]File:[/cyan] {result['skill_file']}")
        console.print(f"\n[dim]Use in Claude Code: /skill {result['skill_name']}[/dim]")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        console.print("\n[dim]View available templates: specmap skill templates[/dim]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@skill.command('install-all')
def skill_install_all():
    """Install all SpecMap skill templates."""
    project_path = Path.cwd()
    manager = SkillManager(project_path)

    try:
        console.print("[cyan]Installing all SpecMap skill templates...[/cyan]\n")
        result = manager.install_all_templates()

        if result['errors']:
            console.print("[yellow]Warnings:[/yellow]")
            for error in result['errors']:
                console.print(f"  [yellow]•[/yellow] {error}")
            console.print()

        console.print(f"[green]OK[/green] Installed {result['installed_count']} skills")
        console.print(f"[cyan]Location:[/cyan] {result['skills_dir']}")

        console.print("\n[bold]Installed Skills:[/bold]")
        for skill_name in result['installed_skills']:
            console.print(f"  [green]✓[/green] {skill_name}")

        console.print(f"\n[dim]View all skills: specmap skill list[/dim]")
        console.print(f"[dim]Use in Claude Code: /skill <name>[/dim]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@skill.command('create')
@click.argument('name')
@click.argument('description')
@click.option('--content', '-c', help='Skill content (or use stdin)')
def skill_create(name, description, content):
    """Create a custom Claude Code skill."""
    project_path = Path.cwd()
    manager = SkillManager(project_path)

    try:
        # If no content provided, prompt for it or read from stdin
        if not content:
            console.print("[yellow]Enter skill content (press Ctrl+D when done):[/yellow]")
            content_lines = []
            try:
                while True:
                    line = input()
                    content_lines.append(line)
            except EOFError:
                content = '\n'.join(content_lines)

        if not content.strip():
            console.print("[red]Error:[/red] Skill content cannot be empty")
            sys.exit(1)

        result = manager.create_skill(name, description, content)

        console.print(f"[green]OK[/green] Custom skill created!")
        console.print(f"[cyan]Name:[/cyan] {result['skill_name']}")
        console.print(f"[cyan]File:[/cyan] {result['skill_file']}")
        console.print(f"\n[dim]Use in Claude Code: /skill {result['skill_name']}[/dim]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@skill.command('delete')
@click.argument('skill_name')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
def skill_delete(skill_name, force):
    """Delete a Claude Code skill."""
    project_path = Path.cwd()
    manager = SkillManager(project_path)

    try:
        if not force:
            if not click.confirm(f"Delete skill '{skill_name}'?"):
                console.print("[yellow]Cancelled[/yellow]")
                return

        result = manager.delete_skill(skill_name)

        if result['success']:
            console.print(f"[green]OK[/green] {result['message']}")
        else:
            console.print(f"[red]Error:[/red] {result['error']}")
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


# ============================================================================
# Folder Management Commands
# ============================================================================

@main.group()
def folder():
    """Manage project folders and session organization."""
    pass


@folder.group()
def session():
    """Session summary folder management."""
    pass


@session.command('create')
@click.option('--date', help='Date for session (YYYY-MM-DD, default: today)')
@click.option('--open', '-o', 'open_editor', is_flag=True, help='Open in editor after creation')
def session_create(date, open_editor):
    """Create a new session summary file."""
    project_path = Path.cwd()
    manager = FolderManager(project_path)

    try:
        # Parse date if provided
        session_date = None
        if date:
            try:
                session_date = datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                console.print(f"[red]Error:[/red] Invalid date format. Use YYYY-MM-DD")
                sys.exit(1)

        # Create session file
        session_file = manager.create_session_file(session_date)

        console.print(f"[green]OK[/green] Session file created!")
        console.print(f"[cyan]Location:[/cyan] {session_file.relative_to(project_path)}")
        console.print(f"[cyan]Full path:[/cyan] {session_file}")

        # Open in editor if requested
        if open_editor:
            editor = os.environ.get('EDITOR', 'nano')
            os.system(f'{editor} "{session_file}"')

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@session.command('list')
@click.option('--year', type=int, help='Filter by year')
@click.option('--month', type=int, help='Filter by month (1-12)')
@click.option('--limit', type=int, default=20, help='Max sessions to display')
def session_list(year, month, limit):
    """List all session summaries."""
    project_path = Path.cwd()
    manager = FolderManager(project_path)

    try:
        sessions = manager.list_sessions(year, month)

        if not sessions:
            console.print("[yellow]No sessions found[/yellow]")
            return

        # Create table
        table = Table(title=f"Session Summaries ({len(sessions)} total)")
        table.add_column("Date", style="cyan")
        table.add_column("Path", style="white")
        table.add_column("Size", justify="right", style="green")
        table.add_column("Modified", style="dim")

        for session in sessions[:limit]:
            table.add_row(
                session['date'].strftime("%Y-%m-%d"),
                str(session['relative_path']),
                format_size(session['size']),
                session['modified'].strftime("%Y-%m-%d %H:%M")
            )

        console.print(table)

        if len(sessions) > limit:
            console.print(f"\n[dim]Showing {limit} of {len(sessions)} sessions[/dim]")
            console.print(f"[dim]Use --limit to show more[/dim]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@session.command('migrate')
@click.option('--dry-run', is_flag=True, help='Show what would be migrated without doing it')
def session_migrate(dry_run):
    """Migrate legacy flat session files to hierarchical structure."""
    project_path = Path.cwd()
    manager = FolderManager(project_path)

    try:
        if dry_run:
            console.print("[yellow]DRY RUN MODE[/yellow] - No files will be moved\n")

        console.print("Migrating legacy session files...")

        if not dry_run:
            stats = manager.migrate_legacy_sessions()
        else:
            # Just count what would be migrated
            legacy_files = list(manager.session_summaries_root.glob("*.md"))
            legacy_files = [f for f in legacy_files if f.name not in ['README.md', 'TEMPLATE.md']]
            stats = {'migrated': 0, 'skipped': len(legacy_files), 'errors': 0}

        console.print(f"\n[green]Migration complete![/green]")
        console.print(f"  Migrated: {stats['migrated']}")
        console.print(f"  Skipped:  {stats['skipped']}")
        console.print(f"  Errors:   {stats['errors']}")

        if dry_run and stats['skipped'] > 0:
            console.print(f"\n[dim]Run without --dry-run to perform migration[/dim]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@folder.command('categories')
def folder_categories():
    """List all document categories and their purposes."""
    project_path = Path.cwd()
    manager = FolderManager(project_path)

    console.print(Panel.fit(
        "[bold cyan]SpecMap Document Categories[/bold cyan]",
        border_style="cyan"
    ))

    categories = manager.list_document_categories()

    for category, info in categories.items():
        console.print(f"\n[bold cyan]{category.upper()}[/bold cyan]")
        console.print(f"  Path: [white]{info['path']}[/white]")
        console.print(f"  Purpose: [dim]{info['description']}[/dim]")
        console.print(f"  Subdirectories:")
        for subdir in info['subdirs']:
            console.print(f"    • {subdir}")


@folder.command('validate')
def folder_validate():
    """Validate project folder structure."""
    project_path = Path.cwd()
    manager = FolderManager(project_path)

    console.print("Validating folder structure...\n")

    validation = manager.validate_folder_structure()

    # Count status
    exists = sum(1 for v in validation.values() if v)
    missing = len(validation) - exists

    # Display results
    table = Table(title="Folder Structure Validation")
    table.add_column("Folder", style="white")
    table.add_column("Status", justify="center")

    for folder, exists_flag in sorted(validation.items()):
        status = "[green]✓[/green]" if exists_flag else "[red]✗[/red]"
        table.add_row(folder, status)

    console.print(table)

    # Summary
    if missing == 0:
        console.print(f"\n[green]OK[/green] All folders exist ({exists}/{len(validation)})")
    else:
        console.print(f"\n[yellow]Warning:[/yellow] {missing} folders missing")
        console.print(f"[dim]Run 'specmap folder create-all' to create missing folders[/dim]")


@folder.command('create-all')
def folder_create_all():
    """Create all standard folders if they don't exist."""
    project_path = Path.cwd()
    manager = FolderManager(project_path)

    try:
        console.print("Creating folder structure...")
        created = manager.create_all_folders()

        console.print(f"\n[green]OK[/green] Folder structure created!")
        console.print(f"Total folders: {len(created)}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@folder.command('stats')
def folder_stats():
    """Show folder usage statistics."""
    project_path = Path.cwd()
    manager = FolderManager(project_path)

    try:
        console.print("Calculating folder statistics...\n")
        stats = manager.get_folder_stats()

        # Overall stats
        console.print(Panel.fit(
            f"[bold]Total Files:[/bold] {stats['total_files']}\n"
            f"[bold]Total Folders:[/bold] {stats['total_folders']}\n"
            f"[bold]Total Size:[/bold] {format_size(stats['total_size_bytes'])}\n"
            f"[bold]Session Summaries:[/bold] {stats['sessions_count']}",
            title="[cyan]Overall Statistics[/cyan]",
            border_style="cyan"
        ))

        # Category breakdown
        if stats['categories']:
            console.print("\n[bold cyan]Category Breakdown:[/bold cyan]\n")

            table = Table()
            table.add_column("Category", style="cyan")
            table.add_column("Files", justify="right", style="white")
            table.add_column("Folders", justify="right", style="white")
            table.add_column("Size", justify="right", style="green")

            for category, cat_stats in stats['categories'].items():
                table.add_row(
                    category,
                    str(cat_stats['files']),
                    str(cat_stats['folders']),
                    format_size(cat_stats['size_bytes'])
                )

            console.print(table)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        sys.exit(1)


@folder.command('guide')
@click.option('--save', is_flag=True, help='Save guide to FOLDER-GUIDE.md')
def folder_guide(save):
    """Display folder organization guide."""
    guide_text = get_folder_guide()

    if save:
        guide_file = Path.cwd() / "FOLDER-GUIDE.md"
        guide_file.write_text(guide_text, encoding='utf-8')
        console.print(f"[green]OK[/green] Guide saved to {guide_file}")
    else:
        console.print(guide_text)


if __name__ == '__main__':
    main()