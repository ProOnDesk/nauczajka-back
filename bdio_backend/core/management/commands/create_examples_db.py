from django.core.management.base import BaseCommand
from user.models import User
from tutor.models import Tutor, Skills, TutorRatings, TutorScheduleItems
from faker import Faker
import random
from django.test.utils import override_settings
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
import os
from dotenv import load_dotenv


class Command(BaseCommand):
    help = 'Creates a sample database with tutors, users, skills, etc.'

    def add_arguments(self, parser):
        parser.add_argument('number_of_users', nargs='?', type=int, default=10, help='Number of users to create')
        parser.add_argument('--no_schedule', action='store_true', help='Do not create tutor schedules')

    def handle(self, *args, **kwargs):
        try:
            number_of_users = kwargs['number_of_users']
            no_schedule = kwargs['no_schedule']

            # Create admin user
            if not User.objects.filter(email="admin@admin.pl").exists() and settings.DEBUG == True:
                User.objects.create_superuser(email="admin@admin.pl", password="admin")
            elif settings.DEBUG == False:
                load_dotenv()
                User.objects.create_superuser(email=os.environ.get('ADMIN_EMAIL'), password=os.environ.get('ADMIN_PASSWORD'))
            

            fake = Faker('pl_PL')

            settings.IS_CUSTOM_CONFIRM_EMAIL_REQUIRED = False

            # Creating skills
            skills_list = ['Angielski', 'Francuski', 'Matematyka', 'Informatyka', 'Fizyka', 'Chemia', 'Biologia', 'Polski', 'Hiszpański', 'Niemiecki', 'Włoski',
                           'Rosyjski', 'Historia', 'Geografia', 'Muzyka', 'Plastyka', 'WOS', 'Technika',]

            skills_objs = []
            for skill_name in skills_list:
                skill_obj, created = Skills.objects.get_or_create(skill=skill_name)
                skills_objs.append(skill_obj)

            # Getting current time
            date_now = now()
            second = date_now.second
            minute = date_now.minute
            hour = date_now.hour
            day = date_now.day
            month = date_now.month
            year = date_now.year
            to_email_str = f"{year}{month}{day}{hour}{minute}{second}"

            # Creating users
            for i in range(number_of_users):
                first_name = fake.first_name()
                last_name = fake.last_name()
                password = 'password123'  # For simplicity, use a constant password
                is_tutor = random.choice([True, False])
                price = random.randint(20, 200)
                online_sessions_available = random.choice([True, False])
                in_person_sessions_available = random.choice([True, False])
                tutoring_location = fake.city()
                individual_sessions_available = random.choice([True, False])
                group_sessions_available = random.choice([True, False])
                
                if is_tutor:
                    email = f"{to_email_str}{i}@stud.prz.edu.pl"
                else:
                    email = fake.email()

                user_obj = User.objects.create_user(email=email, password=password,
                                                    first_name=first_name,
                                                    last_name=last_name,
                                                    is_confirmed=True,
                                                    is_tutor=is_tutor, 
                                                    price=price,
                                                    online_sessions_available=online_sessions_available,
                                                    in_person_sessions_available=in_person_sessions_available,
                                                    tutoring_location=tutoring_location,
                                                    individual_sessions_available=individual_sessions_available,
                                                    group_sessions_available=group_sessions_available)

                if user_obj.is_tutor:
                    user_obj.tutor.description = fake.text()

                    random_skills = random.sample(skills_objs, random.randint(1, 4))
                    user_obj.tutor.skills.set(random_skills)
                    tutor = Tutor.objects.get(user=user_obj)
                    tutor.description = fake.text()
                    tutor.save()
                user_obj.save()

            # Assigning ratings to tutors
            for user in User.objects.filter(is_tutor=False):
                for tutor in random.sample(list(User.objects.filter(is_tutor=True)), int(User.objects.filter(is_tutor=False).count() / 5)):
                    if not TutorRatings.objects.filter(tutor=tutor.tutor, student=user).exists():
                        tutor = TutorRatings.objects.create(tutor=tutor.tutor, student=user, rating=random.randint(3, 5), review=fake.text())
                        tutor.save()

            # Creating tutor schedules
            if not no_schedule:
                current_time = now()
                for tutor in Tutor.objects.all():
                    for i in range(10):
                        for week in range(1, 4):
                            for day in range(1, 5):
                                current_time = current_time.replace(minute=0, second=0, hour=0)
                                start_time = current_time + timedelta(weeks=week, days=day, hours=random.randint(8, 18), minutes=0)
                                end_time = start_time + timedelta(hours=1)
                                try:
                                    schedule_item = TutorScheduleItems.objects.create(tutor=tutor, start_time=start_time, end_time=end_time)
                                    schedule_item.clean()
                                except ValidationError:
                                    pass

            settings.IS_CUSTOM_CONFIRM_EMAIL_REQUIRED = True
            self.stdout.write(self.style.SUCCESS('Successfully created sample database!'))

        except Exception as e:
            settings.IS_CUSTOM_CONFIRM_EMAIL_REQUIRED = True
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
            raise e
