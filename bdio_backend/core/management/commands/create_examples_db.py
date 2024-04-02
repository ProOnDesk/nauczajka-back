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

class Command(BaseCommand):
    help = 'Creates a sample database with tutors, users, skills, etc.'

    def add_arguments(self, parser):
        parser.add_argument('number_of_users', nargs='?', type=int, default=10, help='Number of users to create')
        parser.add_argument('--no_schedule', action='store_true', help='Do not create tutor schedules')

    def handle(self, *args, **kwargs):
        try:
            number_of_users = kwargs['number_of_users']
            no_schedule = kwargs['no_schedule']
            
            # create admin user
            if not User.objects.filter(email="admin@admin.pl").exists():
                User.objects.create_superuser(email="admin@admin.pl", password="admin")
            
            fake = Faker('pl_PL')  
            
            settings.IS_CUSTOM_CONFIRM_EMAIL_REQUIRED = False
            
            # Tworzenie umiejętności
            skills_list = ['Angielski', 'Francuski', 'Matematyka', 'Informatyka', 'Fizyka', 'Chemia', 'Biologia', 'Polski', 'Hiszpański', 'Niemiecki', 'Włoski', 'Rosyjski', 'Historia', 'Geografia', 'Muzyka', 'Plastyka', 'WOS', 'WF', 'Technika', 'Inne']
            skills_objs = []
            for skill_name in skills_list:
                skill_obj, created = Skills.objects.get_or_create(skill=skill_name)
                skills_objs.append(skill_obj)

            # Pobranie aktualnego czasu
            date_now = now()
            second = date_now.second
            minute = date_now.minute
            hour = date_now.hour
            day = date_now.day
            month = date_now.month
            year = date_now.year
            to_email_str = f"{year}{month}{day}{hour}{minute}{second}"

            # Tworzenie użytkowników
            for i in range(number_of_users):
                first_name = fake.first_name()
                last_name = fake.last_name()
                password = 'haslo123'  #
                is_tutor = random.choice([True, False])

                if is_tutor:
                    email = f"{to_email_str}{i}@stud.prz.edu.pl"
                else:   
                    email = fake.email()
                    
                user_obj = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, is_confirmed=True, is_tutor=is_tutor)

                if user_obj.is_tutor:
                    user_obj.tutor.description = fake.text()

                    random_skills = random.sample(skills_objs, random.randint(1, 4))
                    user_obj.tutor.skills.set(random_skills)
                    tutor = Tutor.objects.get(user=user_obj)
                    tutor.description = fake.text()
                    tutor.save()
                user_obj.save()

            for user in User.objects.filter(is_tutor=False):
                for tutor in random.sample(list(User.objects.filter(is_tutor=True)), int(User.objects.filter(is_tutor=False).count() / 5)):
                    if not TutorRatings.objects.filter(tutor=tutor.tutor, student=user).exists():
                        tutor = TutorRatings.objects.create(tutor=tutor.tutor, student=user, rating=random.randint(3, 5), review=fake.text())
                        tutor.save()
                    
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
            self.stdout.write(self.style.SUCCESS('Pomyślnie utworzono przykładową bazę danych!'))
            
        except Exception as e:
            settings.IS_CUSTOM_CONFIRM_EMAIL_REQUIRED = True
            self.stdout.write(self.style.ERROR(f'Wystąpił błąd: {e}'))
            raise e
