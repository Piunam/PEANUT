from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Room, Player 

# Create your views here.

def login(request):
    return render(request, 'login.html')

@login_required
def home(request):
    try:
        player = Player.objects.get(user=request.user)
    except Player.DoesNotExist:
        player = Player.objects.create(user=request.user, username=request.user.username)
    
    context = {
        'player': player
    }
    return render(request, 'home.html', context)

def profile(request:HttpRequest):
    return HttpResponse('Hello!')

def logout_view(request):
    logout(request)
    return redirect('home')

@csrf_exempt
@login_required
def start_match(request):
    if request.method == 'POST':
        user = request.user
        player, created = Player.objects.get_or_create(user=user)

        # Fetch the player's rank
        player_rank = player.rank

        # Find an available room that doesn't have the same rank player
        room = Room.objects.filter(
            is_occupied=False,
          
        ).first()

        print(room)

        if not room:
            
            # Create a new room if no available room is found
            room = Room.objects.create(name=f"Room-{Room.objects.count() + 1}")
            print("New Room created :)", room.id)
            

       

        # Assign player to room
        room.current_players += 1
        player.room = room
        player.is_in_queue = True
        player.save()
        room.save()
        print(f"Player {player.username} joined room {room.id}")
        # Mark room as occupied if it's full
        if room.current_players >= room.max_capacity:
            room.is_occupied = True
            room.save()

        return JsonResponse({
            'status': 'success',
            'room_id': room.id,
            'room_name': room.name
        })

@csrf_exempt
def check_room_status(request):
    if request.method == 'POST':
        user = request.user
        player = Player.objects.get(user=user)

        if player.room and player.room.current_players >= 2:
            return JsonResponse({
                'status': 'ready',
                'redirect_url': f'/question-page/?room_id={player.room.id}'
            })
        else:
            return JsonResponse({'status': 'waiting'})

def question_page(request):
    room_id = request.GET.get('room_id')
    room = get_object_or_404(Room, id=room_id)
    
    context = {
        'room_id': room_id,
        'room_name': room.name,
        # Add any other context variables you need
    }

    return render(request, 'game/question_page.html', context)
