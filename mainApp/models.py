from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=50)
    is_occupied = models.BooleanField(default=False)
    max_capacity = models.IntegerField(default=2)
    current_players = models.IntegerField(default=0)

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
