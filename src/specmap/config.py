"""
Configuration management for SpecMap
AI-powered specification-driven development system
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class SpecMapConfig:
    """Manages unified configuration for SpecMap projects"""

    DEFAULT_CONFIG = {
        'project': {
            'name': '',
            'type': 'web-app',
            'created': '',
            'version': '2.0.0'
        },
        'specmap': {
            'constitution_enabled': True,
            'clarification_required': True,
            'feature_branches': True,
            'scoring_threshold': 8.0,
            'quality_gates_enabled': True,
            'agent_orchestration': True
        },
        'agents': {
            'base_agent': 'claude',  # claude, gemini, copilot, cursor, etc.
            'prd_generator': {
                'enabled': True,
                'persona': 'brilliant-recent-graduate'
            },
            'task_planner': {
                'enabled': True,
                'persona': 'brilliant-recent-graduate'
            },
            'dev_guide': {
                'enabled': True,
                'persona': 'brilliant-recent-graduate'
            },
            'qa_monitor': {
                'enabled': True,
                'persona': 'brilliant-recent-graduate'
            }
        },
        'automation': {
            'session_logging': True,
            'progress_tracking': True,
            'metric_collection': True,
            'report_generation': 'weekly'
        },
        'validation': {
            'constitution_check': True,
            'rulemap_scoring': True,
            'dual_validation': True
        }
    }

    def __init__(self, project_path: Path):
        self.project_path = project_path
        # Support both new and legacy folder names for backward compatibility
        new_config_dir = project_path / ".specmap"
        legacy_config_dir = project_path / ".speckit-rulemap"

        if new_config_dir.exists():
            self.config_dir = new_config_dir
        elif legacy_config_dir.exists():
            self.config_dir = legacy_config_dir
        else:
            self.config_dir = new_config_dir  # Default to new for new projects

        self.config_file = self.config_dir / "config.yaml"
        self.config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()

    def load(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                loaded_config = yaml.safe_load(f)
                # Migrate old config format to new if needed
                loaded_config = self._migrate_config(loaded_config)
                self.config = self._merge_config(self.DEFAULT_CONFIG, loaded_config)
        return self.config

    def _migrate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate legacy config format to new unified format"""
        if 'speckit' in config or 'rulemap' in config:
            # Legacy format detected, merge into specmap section
            migrated = config.copy()
            specmap_config = {}

            if 'speckit' in config:
                specmap_config.update(config['speckit'])
                del migrated['speckit']

            if 'rulemap' in config:
                specmap_config.update(config['rulemap'])
                del migrated['rulemap']

            migrated['specmap'] = specmap_config
            return migrated

        return config

    def save(self):
        """Save configuration to file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, indent=2)

    def update(self, updates: Dict[str, Any]):
        """Update configuration with new values"""
        self.config = self._merge_config(self.config, updates)
        self.save()

    def _merge_config(self, base: Dict, updates: Dict) -> Dict:
        """Recursively merge configuration dictionaries"""
        result = base.copy()
        for key, value in updates.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'rulemap.scoring_threshold')"""
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, key_path: str, value: Any):
        """Set configuration value using dot notation"""
        keys = key_path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        self.save()


class WorkflowState:
    """Manages workflow state tracking"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        # Support both new and legacy folder names
        new_config_dir = project_path / ".specmap"
        legacy_config_dir = project_path / ".speckit-rulemap"

        if new_config_dir.exists():
            config_dir = new_config_dir
        elif legacy_config_dir.exists():
            config_dir = legacy_config_dir
        else:
            config_dir = new_config_dir  # Default to new

        self.state_file = config_dir / "workflow-state.json"
        self.state = {
            'current_phase': 'initialization',
            'active_agent': None,
            'last_updated': None,
            'features': {},
            'milestones': []
        }

    def load(self):
        """Load workflow state"""
        if self.state_file.exists():
            import json
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        return self.state

    def save(self):
        """Save workflow state"""
        import json
        self.state['last_updated'] = datetime.now().isoformat()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def update_phase(self, phase: str):
        """Update current workflow phase"""
        self.state['current_phase'] = phase
        self.save()

    def activate_agent(self, agent_type: str):
        """Activate an agent"""
        self.state['active_agent'] = agent_type
        self.save()

    def add_feature(self, feature_id: str, feature_data: Dict):
        """Add or update feature tracking"""
        self.state['features'][feature_id] = feature_data
        self.save()

    def get_feature(self, feature_id: str) -> Optional[Dict]:
        """Get feature tracking data"""
        return self.state['features'].get(feature_id)