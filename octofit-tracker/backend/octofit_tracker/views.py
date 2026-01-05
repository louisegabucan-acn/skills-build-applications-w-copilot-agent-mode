import os
from rest_framework import viewsets, routers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import UserSerializer, TeamSerializer, ActivitySerializer, LeaderboardSerializer, WorkoutSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

# Custom API root that returns the full API URL using $CODESPACE_NAME
def custom_api_root(request):
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        api_url = f"https://{codespace_name}-8000.app.github.dev/api/"
    else:
        api_url = request.build_absolute_uri('/api/')
    return api_url

@api_view(['GET'])
def api_root(request, format=None):
    base_url = custom_api_root(request)
    return Response({
        'users': f"{base_url}users/",
        'teams': f"{base_url}teams/",
        'activities': f"{base_url}activities/",
        'leaderboard': f"{base_url}leaderboard/",
        'workouts': f"{base_url}workouts/",
    })
