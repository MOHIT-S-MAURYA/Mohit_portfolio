from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from portfolio.models import Profile, Skill, Project, Experience, Education

class Command(BaseCommand):
    help = 'Create sample data for the portfolio'

    def handle(self, *args, **options):
        # Create Profile
        profile, created = Profile.objects.get_or_create(
            defaults={
                'name': 'Mohit Maurya',
                'title': 'Full Stack Developer',
                'bio': 'Passionate full-stack developer with expertise in modern web technologies. I love creating beautiful, functional websites and applications that solve real-world problems.',
                'email': 'mohit@example.com',
                'phone': '+1 (555) 123-4567',
                'location': 'San Francisco, CA',
                'linkedin': 'https://linkedin.com/in/mohitmaurya',
                'github': 'https://github.com/mohitmaurya',
                'twitter': 'https://twitter.com/mohitmaurya',
                'website': 'https://mohitmaurya.dev',
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Profile created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Profile already exists'))

        # Create Skills
        skills_data = [
            {'name': 'Python', 'type': 'technical', 'proficiency': 95, 'icon': 'fab fa-python'},
            {'name': 'Django', 'type': 'technical', 'proficiency': 90, 'icon': 'fas fa-server'},
            {'name': 'JavaScript', 'type': 'technical', 'proficiency': 90, 'icon': 'fab fa-js'},
            {'name': 'React', 'type': 'technical', 'proficiency': 85, 'icon': 'fab fa-react'},
            {'name': 'HTML/CSS', 'type': 'technical', 'proficiency': 95, 'icon': 'fab fa-html5'},
            {'name': 'PostgreSQL', 'type': 'technical', 'proficiency': 80, 'icon': 'fas fa-database'},
            {'name': 'Git', 'type': 'tools', 'proficiency': 90, 'icon': 'fab fa-git-alt'},
            {'name': 'Docker', 'type': 'tools', 'proficiency': 75, 'icon': 'fab fa-docker'},
            {'name': 'AWS', 'type': 'tools', 'proficiency': 70, 'icon': 'fab fa-aws'},
            {'name': 'Problem Solving', 'type': 'soft', 'proficiency': 95, 'icon': 'fas fa-lightbulb'},
            {'name': 'Team Leadership', 'type': 'soft', 'proficiency': 85, 'icon': 'fas fa-users'},
            {'name': 'Communication', 'type': 'soft', 'proficiency': 90, 'icon': 'fas fa-comments'},
        ]

        for skill_data in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults=skill_data
            )
            if created:
                self.stdout.write(f'Created skill: {skill.name}')

        # Create Experience
        experiences_data = [
            {
                'company': 'Tech Innovations Inc.',
                'position': 'Senior Full Stack Developer',
                'description': 'Led development of multiple web applications using Django and React. Mentored junior developers and collaborated with cross-functional teams to deliver high-quality software solutions.',
                'start_date': date(2022, 1, 1),
                'end_date': None,
                'is_current': True,
                'location': 'San Francisco, CA',
                'company_url': 'https://techinnovations.com',
            },
            {
                'company': 'Digital Solutions LLC',
                'position': 'Full Stack Developer', 
                'description': 'Developed and maintained web applications using Python, Django, and modern frontend frameworks. Improved application performance by 40% through optimization techniques.',
                'start_date': date(2020, 6, 1),
                'end_date': date(2021, 12, 31),
                'is_current': False,
                'location': 'Remote',
                'company_url': 'https://digitalsolutions.com',
            },
            {
                'company': 'StartupXYZ',
                'position': 'Junior Developer',
                'description': 'Built responsive web applications and contributed to the development of the company\'s main product. Worked closely with designers to implement pixel-perfect UIs.',
                'start_date': date(2019, 1, 1),
                'end_date': date(2020, 5, 31),
                'is_current': False,
                'location': 'New York, NY',
                'company_url': '',
            },
        ]

        for exp_data in experiences_data:
            experience, created = Experience.objects.get_or_create(
                company=exp_data['company'],
                position=exp_data['position'],
                defaults=exp_data
            )
            if created:
                self.stdout.write(f'Created experience: {experience.position} at {experience.company}')

        # Create Education
        education_data = [
            {
                'institution': 'University of California, Berkeley',
                'degree': 'Bachelor of Science',
                'field_of_study': 'Computer Science',
                'start_date': date(2015, 9, 1),
                'end_date': date(2019, 5, 1),
                'is_current': False,
                'grade': '3.8 GPA',
                'description': 'Focused on software engineering, algorithms, and web development. Completed senior capstone project on machine learning applications.',
            },
        ]

        for edu_data in education_data:
            education, created = Education.objects.get_or_create(
                institution=edu_data['institution'],
                degree=edu_data['degree'],
                defaults=edu_data
            )
            if created:
                self.stdout.write(f'Created education: {education.degree} from {education.institution}')

        # Create Projects
        projects_data = [
            {
                'title': 'E-commerce Platform',
                'description': 'A full-featured e-commerce platform built with Django and React. Features include user authentication, product catalog, shopping cart, payment processing, and admin dashboard. Implemented responsive design and optimized for performance.',
                'short_description': 'Full-featured e-commerce platform with Django backend and React frontend',
                'technologies': 'Django, React, PostgreSQL, Stripe API, AWS S3, Redis',
                'github_url': 'https://github.com/mohitmaurya/ecommerce-platform',
                'live_url': 'https://ecommerce-demo.mohitmaurya.dev',
                'is_featured': True,
                'created_date': date(2023, 6, 1),
                'order': 1,
            },
            {
                'title': 'Task Management System',
                'description': 'A collaborative task management application with real-time updates. Built with Django Channels for WebSocket communication and React for the frontend. Features include project management, team collaboration, and progress tracking.',
                'short_description': 'Collaborative task management system with real-time updates',
                'technologies': 'Django, Django Channels, React, WebSocket, PostgreSQL',
                'github_url': 'https://github.com/mohitmaurya/task-manager',
                'live_url': 'https://tasks.mohitmaurya.dev',
                'is_featured': True,
                'created_date': date(2023, 3, 1),
                'order': 2,
            },
            {
                'title': 'Weather Dashboard',
                'description': 'A responsive weather dashboard that displays current weather conditions and forecasts for multiple cities. Built with vanilla JavaScript and integrated with OpenWeather API. Features clean UI design and location-based weather detection.',
                'short_description': 'Responsive weather dashboard with location-based detection',
                'technologies': 'HTML, CSS, JavaScript, OpenWeather API, Chart.js',
                'github_url': 'https://github.com/mohitmaurya/weather-dashboard',
                'live_url': 'https://weather.mohitmaurya.dev',
                'is_featured': True,
                'created_date': date(2023, 1, 1),
                'order': 3,
            },
            {
                'title': 'Blog Platform',
                'description': 'A modern blog platform with content management system. Features include rich text editing, category management, comment system, and SEO optimization. Built with Django and Bootstrap for responsive design.',
                'short_description': 'Modern blog platform with CMS and SEO optimization',
                'technologies': 'Django, Bootstrap, TinyMCE, PostgreSQL, Cloudinary',
                'github_url': 'https://github.com/mohitmaurya/blog-platform',
                'live_url': 'https://blog.mohitmaurya.dev',
                'is_featured': False,
                'created_date': date(2022, 11, 1),
                'order': 4,
            },
        ]

        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults=project_data
            )
            if created:
                self.stdout.write(f'Created project: {project.title}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('You can now visit the site and admin panel to see the content.'))
