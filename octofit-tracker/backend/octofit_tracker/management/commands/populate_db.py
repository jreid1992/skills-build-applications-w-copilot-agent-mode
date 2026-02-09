from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models

# Define minimal models for direct DB access (not migrations)
from django.contrib.auth import get_user_model
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating octofit_db with test data...'))
        db = connection.cursor().db_conn.client[settings.DATABASES['default']['NAME']]

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Users
        users = [
            {"name": "Tony Stark", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Steve Rogers", "email": "cap@marvel.com", "team": "Marvel"},
            {"name": "Bruce Wayne", "email": "batman@dc.com", "team": "DC"},
            {"name": "Clark Kent", "email": "superman@dc.com", "team": "DC"},
        ]
        db.users.insert_many(users)
        db.users.create_index("email", unique=True)

        # Teams
        teams = [
            {"name": "Marvel", "members": [u["email"] for u in users if u["team"] == "Marvel"]},
            {"name": "DC", "members": [u["email"] for u in users if u["team"] == "DC"]},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {"user": "ironman@marvel.com", "activity": "Running", "duration": 30},
            {"user": "cap@marvel.com", "activity": "Cycling", "duration": 45},
            {"user": "batman@dc.com", "activity": "Swimming", "duration": 25},
            {"user": "superman@dc.com", "activity": "Flying", "duration": 60},
        ]
        db.activities.insert_many(activities)

        # Workouts
        workouts = [
            {"user": "ironman@marvel.com", "workout": "Chest Day", "reps": 100},
            {"user": "cap@marvel.com", "workout": "Leg Day", "reps": 120},
            {"user": "batman@dc.com", "workout": "Core", "reps": 80},
            {"user": "superman@dc.com", "workout": "Full Body", "reps": 150},
        ]
        db.workouts.insert_many(workouts)

        # Leaderboard
        leaderboard = [
            {"user": "superman@dc.com", "points": 1000},
            {"user": "ironman@marvel.com", "points": 900},
            {"user": "cap@marvel.com", "points": 850},
            {"user": "batman@dc.com", "points": 800},
        ]
        db.leaderboard.insert_many(leaderboard)

        self.stdout.write(self.style.SUCCESS('octofit_db test data created!'))
