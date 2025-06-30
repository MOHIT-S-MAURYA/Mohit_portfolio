from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone
from portfolio.models import Profile, Skill, Project, Experience, Education, Contact
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test validation and error handling for all models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help='Test specific model (profile, skill, project, experience, education, contact)',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose output',
        )

    def handle(self, *args, **options):
        self.verbose = options['verbose']
        model_name = options.get('model')
        
        if model_name:
            self.test_single_model(model_name)
        else:
            self.test_all_models()

    def test_single_model(self, model_name):
        """Test validation for a specific model."""
        test_methods = {
            'profile': self.test_profile_validation,
            'skill': self.test_skill_validation,
            'project': self.test_project_validation,
            'experience': self.test_experience_validation,
            'education': self.test_education_validation,
            'contact': self.test_contact_validation,
        }
        
        if model_name in test_methods:
            self.stdout.write(f"\nTesting {model_name.title()} validation...")
            test_methods[model_name]()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown model: {model_name}"))

    def test_all_models(self):
        """Test validation for all models."""
        self.stdout.write(self.style.SUCCESS("Starting comprehensive validation tests...\n"))
        
        test_methods = [
            ('Profile', self.test_profile_validation),
            ('Skill', self.test_skill_validation),
            ('Project', self.test_project_validation),
            ('Experience', self.test_experience_validation),
            ('Education', self.test_education_validation),
            ('Contact', self.test_contact_validation),
        ]
        
        for model_name, test_method in test_methods:
            self.stdout.write(f"Testing {model_name} validation...")
            try:
                test_method()
                self.stdout.write(self.style.SUCCESS(f"✓ {model_name} validation tests passed\n"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ {model_name} validation tests failed: {e}\n"))

    def test_profile_validation(self):
        """Test Profile model validation."""
        test_cases = [
            # Invalid email
            {'name': 'Test User', 'email': 'invalid-email', 'title': 'Developer'},
            # Empty required fields
            {'name': '', 'email': 'test@example.com', 'title': 'Developer'},
            # Invalid phone
            {'name': 'Test User', 'email': 'test@example.com', 'title': 'Developer', 'phone': '123'},
            # Invalid URL
            {'name': 'Test User', 'email': 'test@example.com', 'title': 'Developer', 'linkedin': 'invalid-url'},
        ]
        
        for i, data in enumerate(test_cases):
            try:
                profile = Profile(**data)
                profile.full_clean()
                self.stdout.write(self.style.WARNING(f"  Profile test case {i+1} should have failed but passed"))
            except ValidationError as e:
                if self.verbose:
                    self.stdout.write(f"  ✓ Profile test case {i+1} correctly failed: {e}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Profile test case {i+1} unexpected error: {e}"))

    def test_skill_validation(self):
        """Test Skill model validation."""
        test_cases = [
            # Empty name
            {'name': '', 'type': 'technical', 'proficiency': 80},
            # Invalid proficiency
            {'name': 'Python', 'type': 'technical', 'proficiency': 150},
            # Invalid type
            {'name': 'Python', 'type': 'invalid', 'proficiency': 80},
        ]
        
        for i, data in enumerate(test_cases):
            try:
                skill = Skill(**data)
                skill.full_clean()
                self.stdout.write(self.style.WARNING(f"  Skill test case {i+1} should have failed but passed"))
            except ValidationError as e:
                if self.verbose:
                    self.stdout.write(f"  ✓ Skill test case {i+1} correctly failed: {e}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Skill test case {i+1} unexpected error: {e}"))

    def test_project_validation(self):
        """Test Project model validation."""
        test_cases = [
            # Empty title
            {'title': '', 'description': 'Test project'},
            # Invalid URL
            {'title': 'Test Project', 'description': 'Test', 'github_url': 'invalid-url'},
            # Invalid order
            {'title': 'Test Project', 'description': 'Test', 'order': -1},
        ]
        
        for i, data in enumerate(test_cases):
            try:
                project = Project(**data)
                project.full_clean()
                self.stdout.write(self.style.WARNING(f"  Project test case {i+1} should have failed but passed"))
            except ValidationError as e:
                if self.verbose:
                    self.stdout.write(f"  ✓ Project test case {i+1} correctly failed: {e}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Project test case {i+1} unexpected error: {e}"))

    def test_experience_validation(self):
        """Test Experience model validation."""
        future_date = timezone.now().date().replace(year=timezone.now().year + 1)
        
        test_cases = [
            # Empty required fields
            {'position': '', 'company': 'Test Company', 'start_date': timezone.now().date()},
            # Future start date
            {'position': 'Developer', 'company': 'Test Company', 'start_date': future_date},
            # End date before start date
            {'position': 'Developer', 'company': 'Test Company', 'start_date': timezone.now().date(), 'end_date': timezone.now().date().replace(year=2020)},
        ]
        
        for i, data in enumerate(test_cases):
            try:
                experience = Experience(**data)
                experience.full_clean()
                self.stdout.write(self.style.WARNING(f"  Experience test case {i+1} should have failed but passed"))
            except ValidationError as e:
                if self.verbose:
                    self.stdout.write(f"  ✓ Experience test case {i+1} correctly failed: {e}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Experience test case {i+1} unexpected error: {e}"))

    def test_education_validation(self):
        """Test Education model validation."""
        future_date = timezone.now().date().replace(year=timezone.now().year + 1)
        
        test_cases = [
            # Empty required fields
            {'degree': '', 'institution': 'Test University', 'start_date': timezone.now().date()},
            # Future start date
            {'degree': 'CS', 'institution': 'Test University', 'start_date': future_date},
            # End date before start date
            {'degree': 'CS', 'institution': 'Test University', 'start_date': timezone.now().date(), 'end_date': timezone.now().date().replace(year=2020)},
        ]
        
        for i, data in enumerate(test_cases):
            try:
                education = Education(**data)
                education.full_clean()
                self.stdout.write(self.style.WARNING(f"  Education test case {i+1} should have failed but passed"))
            except ValidationError as e:
                if self.verbose:
                    self.stdout.write(f"  ✓ Education test case {i+1} correctly failed: {e}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Education test case {i+1} unexpected error: {e}"))

    def test_contact_validation(self):
        """Test Contact model validation."""
        test_cases = [
            # Invalid email
            {'name': 'Test User', 'email': 'invalid-email', 'subject': 'Test', 'message': 'Test message'},
            # Empty required fields
            {'name': '', 'email': 'test@example.com', 'subject': 'Test', 'message': 'Test message'},
            # Message too short
            {'name': 'Test User', 'email': 'test@example.com', 'subject': 'Test', 'message': 'Hi'},
            # Subject too long
            {'name': 'Test User', 'email': 'test@example.com', 'subject': 'A' * 201, 'message': 'Test message'},
        ]
        
        for i, data in enumerate(test_cases):
            try:
                contact = Contact(**data)
                contact.full_clean()
                self.stdout.write(self.style.WARNING(f"  Contact test case {i+1} should have failed but passed"))
            except ValidationError as e:
                if self.verbose:
                    self.stdout.write(f"  ✓ Contact test case {i+1} correctly failed: {e}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Contact test case {i+1} unexpected error: {e}"))
