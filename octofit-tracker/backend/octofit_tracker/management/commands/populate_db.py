from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections
from pymongo import ASCENDING

from django.contrib.auth import get_user_model
from django.apps import apps

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating octofit_db with test data...'))
        # Get the MongoDB client from the Djongo connection
        mongo_client = connections['default'].connection.client
        db = mongo_client[settings.DATABASES['default']['NAME']]

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([('email', ASCENDING)], unique=True)

        # Teams
        teams = [
            {'name': 'Team Marvel'},
            {'name': 'Team DC'}
        ]
        team_ids = db.teams.insert_many(teams).inserted_ids

        # Users
        users = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': team_ids[0]},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': team_ids[0]},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': team_ids[1]},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': team_ids[1]},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Activities
        activities = [
            {'user': user_ids[0], 'type': 'run', 'distance': 5, 'duration': 30},
            {'user': user_ids[1], 'type': 'cycle', 'distance': 20, 'duration': 60},
            {'user': user_ids[2], 'type': 'swim', 'distance': 1, 'duration': 40},
            {'user': user_ids[3], 'type': 'walk', 'distance': 3, 'duration': 50},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'user': user_ids[0], 'points': 100},
            {'user': user_ids[1], 'points': 90},
            {'user': user_ids[2], 'points': 110},
            {'user': user_ids[3], 'points': 95},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'user': user_ids[0], 'workout': 'Pushups', 'reps': 50},
            {'user': user_ids[1], 'workout': 'Situps', 'reps': 40},
            {'user': user_ids[2], 'workout': 'Squats', 'reps': 60},
            {'user': user_ids[3], 'workout': 'Lunges', 'reps': 30},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated successfully.'))
