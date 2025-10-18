"""
Tests for Claude Code skill creation and management
"""

import pytest
from pathlib import Path
import tempfile
import shutil

from specmap.skills import SkillManager, SkillTemplate


class TestSkillTemplate:
    """Test SkillTemplate class"""

    def test_templates_exist(self):
        """Test that predefined templates are available"""
        assert len(SkillTemplate.TEMPLATES) > 0

    def test_template_structure(self):
        """Test that templates have required fields"""
        for name, template in SkillTemplate.TEMPLATES.items():
            assert 'name' in template
            assert 'description' in template
            assert 'content' in template
            assert len(template['description']) > 0
            assert len(template['content']) > 0


class TestSkillManager:
    """Test SkillManager class"""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    def test_create_skills_directory(self, temp_project):
        """Test creating .claude/skills directory"""
        manager = SkillManager(temp_project)
        skills_dir = manager.create_skills_directory()

        assert skills_dir.exists()
        assert skills_dir.is_dir()
        assert (skills_dir / "README.md").exists()

    def test_create_custom_skill(self, temp_project):
        """Test creating a custom skill"""
        manager = SkillManager(temp_project)
        result = manager.create_skill(
            name="test-skill",
            description="A test skill",
            content="# Test Content\n\nThis is a test."
        )

        assert result['created'] is True
        assert result['skill_name'] == "test-skill"
        assert Path(result['skill_file']).exists()

        # Verify content
        skill_file = Path(result['skill_file'])
        content = skill_file.read_text(encoding='utf-8')
        assert "name: test-skill" in content
        assert "description: A test skill" in content
        assert "# Test Content" in content

    def test_create_skill_from_template(self, temp_project):
        """Test creating skill from template"""
        manager = SkillManager(temp_project)

        # Get first template
        template_name = list(SkillTemplate.TEMPLATES.keys())[0]
        result = manager.create_skill_from_template(template_name)

        assert result['created'] is True
        assert Path(result['skill_file']).exists()

    def test_invalid_template_name(self, temp_project):
        """Test creating skill with invalid template name"""
        manager = SkillManager(temp_project)

        with pytest.raises(ValueError):
            manager.create_skill_from_template("non-existent-template")

    def test_install_all_templates(self, temp_project):
        """Test installing all templates"""
        manager = SkillManager(temp_project)
        result = manager.install_all_templates()

        assert result['installed_count'] == len(SkillTemplate.TEMPLATES)
        assert len(result['installed_skills']) == len(SkillTemplate.TEMPLATES)
        assert len(result['errors']) == 0

    def test_list_skills(self, temp_project):
        """Test listing installed skills"""
        manager = SkillManager(temp_project)

        # Install some skills
        manager.install_all_templates()

        # List skills
        skills = manager.list_skills()

        assert len(skills) == len(SkillTemplate.TEMPLATES)
        for skill in skills:
            assert 'name' in skill
            assert 'description' in skill
            assert 'file' in skill

    def test_get_available_templates(self, temp_project):
        """Test getting available templates"""
        manager = SkillManager(temp_project)
        templates = manager.get_available_templates()

        assert len(templates) == len(SkillTemplate.TEMPLATES)
        for template in templates:
            assert 'name' in template
            assert 'description' in template

    def test_delete_skill(self, temp_project):
        """Test deleting a skill"""
        manager = SkillManager(temp_project)

        # Create a skill
        result = manager.create_skill(
            name="delete-me",
            description="Skill to be deleted",
            content="Test content"
        )

        # Verify it exists
        assert Path(result['skill_file']).exists()

        # Delete it
        delete_result = manager.delete_skill("delete-me")
        assert delete_result['success'] is True

        # Verify it's gone
        assert not Path(result['skill_file']).exists()

    def test_delete_nonexistent_skill(self, temp_project):
        """Test deleting a skill that doesn't exist"""
        manager = SkillManager(temp_project)
        result = manager.delete_skill("nonexistent")

        assert result['success'] is False
        assert 'error' in result

    def test_skill_name_sanitization(self, temp_project):
        """Test that skill names are sanitized"""
        manager = SkillManager(temp_project)
        result = manager.create_skill(
            name="Test Skill With Spaces!",
            description="Test",
            content="Content"
        )

        # Name should be sanitized for filename
        skill_file = Path(result['skill_file'])
        assert "test-skill-with-spaces" in skill_file.name.lower()

    def test_skill_with_metadata(self, temp_project):
        """Test creating skill with custom metadata"""
        manager = SkillManager(temp_project)
        result = manager.create_skill(
            name="meta-skill",
            description="Skill with metadata",
            content="Content",
            metadata={'author': 'Test Author', 'version': '1.0'}
        )

        skill_file = Path(result['skill_file'])
        content = skill_file.read_text(encoding='utf-8')

        assert "author: Test Author" in content
        assert "version: 1.0" in content
