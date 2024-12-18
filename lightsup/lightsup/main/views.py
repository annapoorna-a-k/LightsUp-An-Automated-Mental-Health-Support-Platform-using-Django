import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import (
     Goal, Mood, Affirmation, JournalingPrompt, Recommendation, DailyChallenge, JournalEntry  
)
from django.contrib import messages
from django.contrib.auth import authenticate, login
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
import matplotlib.dates as mdates

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password == confirm_password:
            if User.objects.filter(email=email).exists(): #same email address checking
                messages.info(request, 'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists(): #same username exists
                messages.info(request, 'Username already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save() #saves this to the database

                user_login = authenticate(username=username, password=password)
                login(request, user_login)
                
                return redirect('goals')
        else:
            messages.info(request, 'Password doesnt match')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print("username", username, "password", password)
        
        user = authenticate(request, username=username, password=password)
        #print(user)
        if user is not None:
            login(request, user) #django creates/update the session for this user
            return redirect('/moodlogin')
        else:
            messages.info(request, 'Invalid Credentials')
    return render(request, 'login.html')



@login_required
def goals(request):
    if request.method == 'POST':
        predefined_goals = request.POST.getlist('goals')

        if not predefined_goals:
            messages.error(request, 'Please select at least one goal.')
            return render(request, 'goals.html', {'predefined_goals': predefined_goals})

        for goal in predefined_goals:
            Goal.objects.create(user=request.user, name=goal)
        
        return redirect('moodlogin')

    predefined_goals = [
        "Mindfulness", "Emotional Balance", "Better Sleep",
        "Reduce Stress", "Personal Growth", "Build Positive Habits"
    ]
    return render(request, 'goals.html', {'predefined_goals': predefined_goals})


@login_required
def add_goal(request):
    if request.method == 'POST':
        goal_name = request.POST.get('custom-goal')
        if goal_name:
            Goal.objects.create(user=request.user, name=goal_name)  
            #messages.success(request, 'Goal added successfully!')
        else:
            print(Goal)
            #messages.error(request, 'Please enter a goal name.')
    return redirect('dashboard')  

@login_required
def remove_goals(request):
    if request.method == 'POST':
        selected_goals = request.POST.getlist('selected_goals') 
        if selected_goals:
            Goal.objects.filter(id__in=selected_goals, user=request.user).delete()
            #messages.success(request, 'Selected goals removed successfully!')
        else:
            print(Goal)
            #messages.error(request, 'No goals were selected for removal.')
    return redirect('dashboard')



@login_required
def moodlogin(request):
    if request.method == 'POST':
        mood = request.POST.get('emotion')  
        reason = request.POST.get('emotionReason')
        notes = request.POST.get('notes')

        Mood.objects.create(user=request.user, emotion=mood, reason=reason, notes=notes)
        return redirect('dashboard')
    return render(request, 'moodlogin.html')


@login_required
def dashboard(request):
    user = request.user
    latest_mood = Mood.objects.filter(user=user).order_by('-created_at').first()
    print(f"Latest Mood: {latest_mood}")  
    
    if latest_mood:
        affirmations = Affirmation.objects.filter(mood__emotion=latest_mood.emotion).order_by('?')
        print(f"Affirmation Count for mood '{latest_mood.emotion}': {affirmations.count()}")  

        random_affirmation = None

        if affirmations.exists():
            random_affirmation = affirmations.order_by('?').first().text
            print(f"Random Affirmation: {random_affirmation}") 
        else:
            print(f"No affirmations found for mood '{latest_mood.emotion}'.")
    else:
        print("No mood logged for the user.")
        random_affirmation = None


    prompts = JournalingPrompt.objects.filter(mood__emotion=latest_mood.emotion).order_by('?')[:2]
    recommendations = Recommendation.objects.filter(mood__emotion=latest_mood.emotion).order_by('?')[:3]
    challenges = DailyChallenge.objects.filter(user=user, completed=False)
    goals = Goal.objects.filter(user=user)

    context = { # all the data that will be passed to the template
        'latest_mood': latest_mood,
        'affirmations': random_affirmation,  
        'prompts': prompts,
        'recommendations': recommendations,
        'challenges': challenges,
        'goals': goals,
    }
    
    return render(request, 'dashboard.html', context)




def add_challenge(request):
    if request.method == 'POST':
        task = request.POST.get('custom-challenge')
        if task:
            DailyChallenge.objects.create(user=request.user, task=task)
            #messages.success(request, 'Challenge added successfully!')
        else:
            messages.error(request, 'Please enter a challenge task.')
    return redirect('dashboard')



@login_required
def journaling(request):    
    if request.method == 'POST':
        for prompt in JournalingPrompt.objects.all():
            journal_text = request.POST.get(f'journal_{prompt.id}')
            if journal_text:
                JournalEntry.objects.create(
                    user=request.user,
                    prompt=prompt,
                    text=journal_text
                )
        return redirect('dashboard')
    return render(request, 'dashboard.html')



def logout_view(request):
    logout(request)
    return redirect('home')



@login_required
def mood_graph(request):
    moods = Mood.objects.filter(user=request.user).order_by('created_at') #fetches all moods of that user

    if not moods.exists():
        plt.figure(figsize=(10, 5))
        plt.text(0.5, 0.5, "No mood data available", fontsize=14, ha='center', va='center')
        plt.axis('off')
    else:
        mood_mapping = {
            'sad': 0,
            'anxious': 1,
            'angry': 2,
            'neutral': 3,
            'happy': 4,
            'excited': 5
        }

        dates = [mood.created_at for mood in moods] #creates a list of dates
        mood_values = [mood_mapping.get(mood.emotion.lower(), 0) for mood in moods] #list of numbers corresponding to each moode 
        #print("mood",mood_values)
        emotions = [mood.emotion.capitalize() for mood in moods]  #for annotating the graph

        plt.figure(figsize=(12, 5))

        # x-axis: date    ,   y-axis:mood_values
        plt.plot(dates, mood_values, marker='o', linestyle='-', color='#ffa500', linewidth=2)

        #area under the line
        plt.fill_between(dates, mood_values, min(mood_values), color='#ffefd5', alpha=0.5) #alpha: semi-transparent fill

        for i, (date, value) in enumerate(zip(dates, mood_values)):
            #print(i,date,value)
            plt.annotate(
                emotions[i],  
                xy=(date, value),
                xytext=(0, 8), #offset the text by 8pts above the round
                textcoords='offset points', #where to place the annotation
                fontsize=10,
                color='#d2691e',
                ha='center',
                bbox=dict(boxstyle="round,pad=0.3", edgecolor='#ffa07a', facecolor='#ffefd5', alpha=0.7)
            )

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d')) #abbreviated month name, date
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))  #used to define the spacing: every day will have a tick
        plt.gcf().autofmt_xdate() #when dates overlap -> rotate and make it readable

        plt.title('Mood Progression Over Time', fontsize=16, color='#ff8c00')
        plt.xlabel('Date', fontsize=12, color='#d2691e')
        plt.ylabel('Mood Scale', fontsize=12, color='#d2691e')
        plt.grid(True, linestyle='--', alpha=0.5)  
        plt.tight_layout() #fit evrything inside the figure

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight') #save it to the buffer instead
    buffer.seek(0)
    plt.close()

    return HttpResponse(buffer, content_type='image/png')
