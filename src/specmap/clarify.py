"""
SpecMap Clarify Command Implementation
Interactive clarification process for resolving open questions
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from .config import WorkflowState


class ClarificationProcessor:
    """Handles interactive clarification of feature specifications"""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.workflow = WorkflowState(project_path)
        self.workflow.load()

    def get_available_features(self) -> List[str]:
        """Get list of available features for clarification"""
        features_dir = self.project_path / "01-specifications" / "features"
        if not features_dir.exists():
            return []

        features = []
        for item in features_dir.iterdir():
            if item.is_dir() and re.match(r'^\d{3}-', item.name):
                spec_file = item / "spec.md"
                if spec_file.exists():
                    features.append(item.name)

        return sorted(features)

    def find_open_questions(self, feature_id: str) -> List[Dict[str, str]]:
        """Extract open questions from specification and clarifications files"""

        feature_path = self.project_path / "01-specifications" / "features" / feature_id

        # Question patterns to search for
        question_patterns = [
            r'\[NEEDS CLARIFICATION:\s*([^\]]+)\]',  # [NEEDS CLARIFICATION: ...]
            r'-\s*\[\s*\]\s*\*\*(\d{3}-Q-\d{3})\*\*:\s*([^\n]+)',  # Checkbox questions
            r'-\s*(\d{3}-Q-\d{3}):\s*([^\n]+)',  # Simple question IDs
            r'\?\s*$',  # Lines ending with ?
        ]

        questions = []

        # Check specification file
        spec_file = feature_path / "spec.md"
        if spec_file.exists():
            content = spec_file.read_text()
            questions.extend(self._extract_questions_from_content(content, "spec.md", question_patterns))

        # Check clarifications file
        clarifications_file = feature_path / "clarifications.md"
        if clarifications_file.exists():
            content = clarifications_file.read_text()
            questions.extend(self._extract_questions_from_content(content, "clarifications.md", question_patterns))

        return questions

    def _extract_questions_from_content(self, content: str, source_file: str, patterns: List[str]) -> List[Dict[str, str]]:
        """Extract questions from content using various patterns"""
        questions = []
        lines = content.split('\n')

        for i, line in enumerate(lines):
            # Check for NEEDS CLARIFICATION markers
            if 'NEEDS CLARIFICATION' in line:
                match = re.search(r'\[NEEDS CLARIFICATION:\s*([^\]]+)\]', line)
                if match:
                    questions.append({
                        'id': f"auto-{len(questions)+1:03d}",
                        'question': match.group(1).strip(),
                        'source': source_file,
                        'line': i + 1,
                        'context': line.strip(),
                        'type': 'clarification_needed'
                    })

            # Check for checkbox questions (unchecked)
            if '- [ ]' in line and any(marker in line for marker in ['Q-', 'question', '?']):
                # Extract question ID and text
                question_match = re.search(r'\*\*(\d{3}-Q-\d{3})\*\*:\s*([^\n]+)', line)
                if question_match:
                    questions.append({
                        'id': question_match.group(1),
                        'question': question_match.group(2).strip(),
                        'source': source_file,
                        'line': i + 1,
                        'context': line.strip(),
                        'type': 'outstanding_question'
                    })
                else:
                    # Generic unchecked question
                    question_text = line.replace('- [ ]', '').strip()
                    if question_text:
                        questions.append({
                            'id': f"auto-{len(questions)+1:03d}",
                            'question': question_text,
                            'source': source_file,
                            'line': i + 1,
                            'context': line.strip(),
                            'type': 'unchecked_item'
                        })

            # Check for lines ending with question marks
            if line.strip().endswith('?') and len(line.strip()) > 5:
                questions.append({
                    'id': f"auto-{len(questions)+1:03d}",
                    'question': line.strip(),
                    'source': source_file,
                    'line': i + 1,
                    'context': line.strip(),
                    'type': 'question_line'
                })

        return questions

    def get_feature_status(self, feature_id: str) -> Dict:
        """Get current status of a feature"""

        feature_path = self.project_path / "01-specifications" / "features" / feature_id

        if not feature_path.exists():
            return {'exists': False}

        spec_file = feature_path / "spec.md"
        clarifications_file = feature_path / "clarifications.md"
        research_file = feature_path / "research.md"

        status = {
            'exists': True,
            'feature_id': feature_id,
            'path': str(feature_path),
            'files': {
                'spec': spec_file.exists(),
                'clarifications': clarifications_file.exists(),
                'research': research_file.exists()
            }
        }

        # Get workflow state
        feature_data = self.workflow.get_feature(feature_id)
        if feature_data:
            status['workflow_status'] = feature_data.get('status', 'unknown')
            status['created'] = feature_data.get('created')
            status['description'] = feature_data.get('description')

        return status

    def create_clarification_session(self, feature_id: str, questions_and_answers: List[Dict]) -> Dict:
        """Create a new clarification session with Q&A results"""

        feature_path = self.project_path / "01-specifications" / "features" / feature_id
        clarifications_file = feature_path / "clarifications.md"

        # Read existing clarifications
        if clarifications_file.exists():
            content = clarifications_file.read_text()
        else:
            content = f"""# Clarifications: {feature_id}

**Feature**: {feature_id}
**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Status**: Active

---

## Clarification Sessions

"""

        # Add new session
        session_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        session_content = f"""
### Session {session_date}
*Interactive clarification session*

#### Resolved Questions
"""

        for qa in questions_and_answers:
            question_id = qa.get('id', 'auto')
            question = qa.get('question', '')
            answer = qa.get('answer', '')

            session_content += f"""
- [x] **{question_id}**: {question}
  **Answer**: {answer}
"""

        # Insert session before outstanding questions section
        if "#### Outstanding Questions" in content:
            content = content.replace("#### Outstanding Questions", session_content + "\n#### Outstanding Questions")
        else:
            content += session_content

        # Write updated clarifications
        clarifications_file.write_text(content, encoding='utf-8')

        return {
            'session_date': session_date,
            'questions_resolved': len(questions_and_answers),
            'clarifications_file': str(clarifications_file)
        }

    def update_specification_with_clarifications(self, feature_id: str, clarifications: List[Dict]) -> Dict:
        """Update the specification file with resolved clarifications"""

        feature_path = self.project_path / "01-specifications" / "features" / feature_id
        spec_file = feature_path / "spec.md"

        if not spec_file.exists():
            raise ValueError(f"Specification file not found for feature {feature_id}")

        content = spec_file.read_text()
        updates_made = []

        for clarification in clarifications:
            question = clarification.get('question', '')
            answer = clarification.get('answer', '')
            context = clarification.get('context', '')

            # Find and replace NEEDS CLARIFICATION markers
            if 'NEEDS CLARIFICATION' in question:
                # Extract the clarification text
                clarification_text = question.replace('[NEEDS CLARIFICATION:', '').replace(']', '').strip()

                # Replace with the answer
                old_pattern = f"[NEEDS CLARIFICATION: {clarification_text}]"
                content = content.replace(old_pattern, answer)
                updates_made.append(f"Resolved clarification: {clarification_text}")

            # Update placeholder sections with specific information
            elif any(placeholder in question.lower() for placeholder in ['to be determined', 'to be clarified', 'tbd']):
                # Try to find and replace placeholder text
                for line in content.split('\n'):
                    if any(placeholder in line.lower() for placeholder in ['to be determined', 'to be clarified']):
                        old_line = line
                        # Replace the placeholder with the answer
                        new_line = re.sub(r'\[.*?(to be determined|to be clarified).*?\]', answer, line, flags=re.IGNORECASE)
                        if new_line != old_line:
                            content = content.replace(old_line, new_line)
                            updates_made.append(f"Updated: {old_line.strip()}")

        # Write updated specification
        spec_file.write_text(content, encoding='utf-8')

        # Update workflow status
        feature_data = self.workflow.get_feature(feature_id) or {}
        feature_data['last_clarification'] = datetime.now().isoformat()
        feature_data['clarifications_count'] = feature_data.get('clarifications_count', 0) + len(clarifications)
        self.workflow.add_feature(feature_id, feature_data)

        return {
            'updates_made': updates_made,
            'spec_file': str(spec_file),
            'clarifications_processed': len(clarifications)
        }

    def calculate_rulemap_score(self, feature_id: str) -> Dict:
        """Calculate basic RULEMAP score based on specification completeness"""

        feature_path = self.project_path / "01-specifications" / "features" / feature_id
        spec_file = feature_path / "spec.md"

        if not spec_file.exists():
            return {'score': 0.0, 'error': 'Specification file not found'}

        content = spec_file.read_text().lower()

        # Check for RULEMAP section completeness
        rulemap_sections = {
            'R - ROLE & AUTHORITY': ['specification owner', 'technical authority'],
            'U - UNDERSTANDING & OBJECTIVES': ['problem statement', 'user scenarios', 'acceptance scenarios'],
            'L - LOGIC & STRUCTURE': ['functional requirements', 'implementation sequence'],
            'E - ELEMENTS & SPECIFICATIONS': ['technical constraints', 'acceptance criteria'],
            'M - MOOD & EXPERIENCE': ['user experience goals', 'emotional journey'],
            'A - AUDIENCE & STAKEHOLDERS': ['primary users', 'stakeholder matrix'],
            'P - PERFORMANCE & METRICS': ['business kpis', 'technical performance']
        }

        total_sections = len(rulemap_sections)
        completed_sections = 0
        section_scores = {}

        for section, requirements in rulemap_sections.items():
            section_score = 0
            section_content = ""

            # Find section content
            section_start = content.find(section.lower())
            if section_start != -1:
                # Get content until next section or end
                next_section_start = content.find('\n## ', section_start + 1)
                if next_section_start != -1:
                    section_content = content[section_start:next_section_start]
                else:
                    section_content = content[section_start:]

            # Check if requirements are addressed
            for requirement in requirements:
                if requirement.lower() in section_content:
                    section_score += 1

            # Calculate section completion percentage
            if requirements:
                section_completion = section_score / len(requirements)
                if section_completion >= 0.8:  # 80% of requirements met
                    completed_sections += 1
                section_scores[section] = {
                    'completion': section_completion,
                    'score': section_score,
                    'total': len(requirements)
                }

        # Check for remaining clarification markers
        clarification_penalty = content.count('needs clarification') * 0.1

        # Calculate overall score
        base_score = (completed_sections / total_sections) * 10
        final_score = max(0.0, base_score - clarification_penalty)

        return {
            'score': round(final_score, 1),
            'completed_sections': completed_sections,
            'total_sections': total_sections,
            'section_scores': section_scores,
            'clarification_markers': content.count('needs clarification'),
            'meets_threshold': final_score >= 8.0
        }

    def run_clarification_process(self, feature_id: Optional[str] = None, interactive: bool = True) -> Dict:
        """Run the complete clarification process"""

        # Validate project structure
        if not (self.project_path / "01-specifications").exists():
            raise ValueError("Not in a SpecMap project directory. Run 'specmap init' first.")

        # Get available features
        available_features = self.get_available_features()
        if not available_features:
            raise ValueError("No features found. Run 'specmap specify' to create a feature first.")

        # Select feature if not specified
        if not feature_id:
            if len(available_features) == 1:
                feature_id = available_features[0]
            else:
                # Return available features for selection
                return {
                    'action_required': 'feature_selection',
                    'available_features': available_features,
                    'message': 'Multiple features available. Please specify which feature to clarify.'
                }

        # Validate feature exists
        if feature_id not in available_features:
            return {
                'error': f"Feature '{feature_id}' not found.",
                'available_features': available_features
            }

        # Get feature status
        status = self.get_feature_status(feature_id)

        # Find open questions
        questions = self.find_open_questions(feature_id)

        if not questions:
            # Calculate RULEMAP score
            score_result = self.calculate_rulemap_score(feature_id)

            return {
                'feature_id': feature_id,
                'status': 'no_questions_found',
                'message': 'No open questions found. Specification appears complete.',
                'rulemap_score': score_result,
                'next_phase': 'planning' if score_result.get('meets_threshold') else 'specification_improvement'
            }

        # Return questions for interactive session
        return {
            'feature_id': feature_id,
            'status': 'questions_found',
            'questions': questions,
            'questions_count': len(questions),
            'feature_status': status,
            'ready_for_interaction': True
        }