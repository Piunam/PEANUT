from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from mainApp.models import *
from mainApp.forms import*
from django.contrib import messages
from django.http import JsonResponse
from .models import Player

# Create your views here.

# def login(request):
#     return render(request, 'login.html')

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


@login_required

def profile(request:HttpRequest):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'edit_profile.html', {'form': form})


#registration......................

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user_type = request.POST['user_type']
        

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            print("HI")
            print(user_type)
            new_user = User(username=username, password=password, email=email, user_type=user_type)
            new_user.save()
            return redirect('thank_you')

    return render(request, 'register.html')

#community.........................................................


@login_required
def community_page(request):
    # Fetch all jobs and achievements to display
    jobs = Job.objects.all()
    achievements = Achievement.objects.all()

    context = {
        'jobs': jobs,
        'achievements': achievements,
    }

    return render(request, 'community_page.html', context)

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('community_page')
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})

@login_required
def post_achievement(request):
    if request.method == 'POST':
        form = AchievementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('community_page')
    else:
        form = AchievementForm()
    return render(request, 'post_achievement.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.get(username=username, password=password)

        if user:
            if user.user_type == 'hiree':
                # return redirect('hiree_home')
                return redirect('home')
            elif user.user_type == 'hirer':
                return redirect('community_page')
            
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'user_login.html')

def thank_you(request):
    return render(request, 'thank_you.html')




@login_required
def store(request):
    return render(request, 'store.html')

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
            room.save()
        
        room.current_players += 1
        player.room = room
        player.is_in_queue = True
        player.save()
        room.save()
        print(f"Player {player.username} joined room {room.id}")
        print(room.name, room.current_players, room.max_capacity)

        
        # Mark room as occupied if it's full
        if room.current_players >= room.max_capacity:
            room.is_occupied = True
            room.save()
        print(room.name, room.is_occupied)

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


@login_required
def question_page(request):
    room_id = request.GET.get('room_id')
    
    # Ensure that room_id is provided
    if not room_id:
        return redirect('home')  # Redirect to home or an error page if no room_id is provided
    
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Room not found'}, status=404)
    
    player, created = Player.objects.get_or_create(user=request.user)
    
    context = {
        'room_id': room.id,
        'player': player
    }
    return render(request, 'game/question_page.html', context)

@csrf_exempt
def submit_answer(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)
        
        user = request.user
        try:
            player = Player.objects.get(user=user)
        except Player.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Player does not exist'}, status=404)
        
        # Assume the answer was correct (this needs actual answer validation)
        answer_correct = True  # Replace with actual validation

        if answer_correct:

            # Promotion logic
            current_rank = player.rank
            if current_rank != 'Bronze - 4':  # Example highest rank
                next_rank = get_next_rank(current_rank)
                player.rank = next_rank
                player.save()

                # Find the opponent player
                opponent = Player.objects.filter(room=player.room).exclude(user=user).first()
                if opponent:
                    # Demotion logic
                    opponent_rank = opponent.rank
                    if opponent_rank != 'Bronze - 1':  # Example base rank
                        new_rank = get_previous_rank(opponent_rank)
                        opponent.rank = new_rank
                        opponent.save()
                        print(player,new_rank)
        
            return JsonResponse({'status': 'success', 'message': 'Submitted successfully. Rank updated.'})
           
        else:
            return JsonResponse({'status': 'error', 'message': 'Incorrect answer.'})
        


def get_next_rank(current_rank):
    # Define rank progression
    ranks = ['Bronze - 1', 'Bronze - 2', 'Bronze - 3', 'Bronze - 4', 'Silver - 1']
    try:
        current_index = ranks.index(current_rank)
        return ranks[current_index + 1] if current_index + 1 < len(ranks) else current_rank
    except ValueError:
        return current_rank

def get_previous_rank(current_rank):
    # Define rank demotion
    ranks = ['Bronze - 1', 'Bronze - 2', 'Bronze - 3', 'Bronze - 4', 'Silver - 1']
    try:
        current_index = ranks.index(current_rank)
        return ranks[current_index - 1] if current_index - 1 >= 0 else current_rank
    except ValueError:
        return current_rank
    

def get_next_rank(current_rank):
    # Rank progression logic
    ranks = ['Bronze - 1', 'Bronze - 2', 'Bronze - 3', 'Bronze - 4', 
             'Silver - 1', 'Silver - 2', 'Silver - 3', 'Silver - 4', 
             'Gold - 1', 'Gold - 2', 'Gold - 3', 'Gold - 4', 
             'Platinum - 1', 'Platinum - 2', 'Platinum - 3', 'Platinum - 4', 
             'Diamond - 1', 'Diamond - 2', 'Diamond - 3', 'Diamond - 4', 
             'Master - 1', 'Master - 2', 'Master - 3', 'Master - 4', 
             'Grandmaster - 1', 'Grandmaster - 2', 'Grandmaster - 3', 'Grandmaster - 4', 
             'Champion']
    
    if current_rank in ranks:
        idx = ranks.index(current_rank)
        if idx < len(ranks) - 1:
            return ranks[idx + 1]
    return current_rank

def get_previous_rank(current_rank):
    # Rank progression logic
    ranks = ['Bronze - 1', 'Bronze - 2', 'Bronze - 3', 'Bronze - 4', 
             'Silver - 1', 'Silver - 2', 'Silver - 3', 'Silver - 4', 
             'Gold - 1', 'Gold - 2', 'Gold - 3', 'Gold - 4', 
             'Platinum - 1', 'Platinum - 2', 'Platinum - 3', 'Platinum - 4', 
             'Diamond - 1', 'Diamond - 2', 'Diamond - 3', 'Diamond - 4', 
             'Master - 1', 'Master - 2', 'Master - 3', 'Master - 4', 
             'Grandmaster - 1', 'Grandmaster - 2', 'Grandmaster - 3', 'Grandmaster - 4', 
             'Champion']
    
    if current_rank in ranks:
        idx = ranks.index(current_rank)
        if idx > 0:
            return ranks[idx - 1]
    return current_rank


# New attribute bnanaya hai is over jo match start hone pe false 
# jabhi koi banda submit karega, fir code check karega ki match over hain ya nhi. 
# If true hain, apne aap hargaya and kuch return kardega. 
# If is_over (of that room) false hain, and sahi answer hain bande ka, do the promotion and demotion 
# logic and is_over ko true set kardo
# also u will get the room by checking the room_id attribute of the player