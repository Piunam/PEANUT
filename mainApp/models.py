from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Room(models.Model):
    name = models.CharField(max_length=50)
    is_occupied = models.BooleanField(default=False)
    max_capacity = models.IntegerField(default=2)
    current_players = models.IntegerField(default=0)
    # is_over = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def can_add_player(self, player_rank):
        # Check if the room is not fully occupied
        if self.current_players < self.max_capacity:
            # Fetch all players in this room
            players_in_room = Player.objects.filter(room=self)
            # Allow if room is empty or ranks match within allowed range
            for player in players_in_room:
                if not self.is_rank_compatible(player.rank, player_rank):
                    return False
            return True
        return False

    @staticmethod
    def is_rank_compatible(room_rank, player_rank):
        rank_order = ['Bronze - 1', 'Bronze - 2', 'Bronze - 3', 'Bronze - 4',
                      'Silver - 1', 'Silver - 2', 'Silver - 3', 'Silver - 4',
                      'Gold - 1', 'Gold - 2', 'Gold - 3', 'Gold - 4']

        room_rank_index = rank_order.index(room_rank)
        player_rank_index = rank_order.index(player_rank)

        # Allow if both ranks are within the same rank group (Bronze, Silver, etc.)
        return abs(room_rank_index - player_rank_index) <= 3


class FreelanceProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Change to ForeignKey
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    application_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def increment_application_count(self):
        self.application_count += 1
        self.save()


class Application(models.Model):
    project = models.ForeignKey(FreelanceProject, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    custom_timer = models.IntegerField(default=20*60)  # Default to 20 minutes

    def __str__(self):
        return self.user.username


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.CharField(max_length=50, default='Bronze - 1')
    is_online = models.BooleanField(default=False)
    is_in_queue = models.BooleanField(default=False)
    matches_won = models.IntegerField(default=0)
    matches_lost = models.IntegerField(default=0)
    match_start_time = models.DateTimeField(null=True, blank=True)
    username = models.CharField(max_length=50)
    question = models.TextField(null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    USER_TYPE_CHOICES = (
        ('hiree', 'Hiree'),
        ('hirer', 'Hirer'),
    )
    user_type = models.CharField(max_length=5, choices=USER_TYPE_CHOICES)


#community shiy

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.title

class Achievement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.title

class Question(models.Model):
    title = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    content = models.TextField()
    expected_output = models.TextField()

    def __str__(self):
        return self.title


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FeedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content[:50]}'

class Violation(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    violation_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.player.user.username} - {self.violation_type}"


# PROJECT
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    project = models.ForeignKey(Project, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  
    # cover_letter = models.TextField()
    price_offer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ubmitted_at = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(default="No cover letter provided")


    # Recommendations


class Field(models.Model):
    name = models.CharField(max_length=255)
    roadmap = models.TextField()
    books = models.TextField()
    youtube_videos = models.TextField()
    courses = models.TextField()

    def __str__(self):
        return self.name


# PRACTICE
class DSATopic(models.Model):
    name = models.CharField(max_length=100)

class DSAQuestion(models.Model):
    topic = models.ForeignKey(DSATopic, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')])
    question = models.TextField()
    answer = models.TextField()
