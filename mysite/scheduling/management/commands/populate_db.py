from django.core.management.base import BaseCommand
from scheduling.models import *

class Command(BaseCommand):

    def _populate(self):
        #Student Types
        student_type = StudentType(name="N/A")
        student_type2.save()

        #Preference Options
        option1 = PreferenceOption(name="First Choice", color_coding="green")
        option1.save()
        option2 = PreferenceOption(name="Second Choice", color_coding="DarkGoldenRod")
        option2.save()
        option3 = PreferenceOption(name="Available", color_coding="black")
        option3.save()
        option4 = PreferenceOption(name="Not Available", color_coding="gray")
        option4.save()

    def handle(self, *args, **options):
        self._populate()