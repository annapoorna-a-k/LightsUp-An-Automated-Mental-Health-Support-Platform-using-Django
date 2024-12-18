from django.db import models
from django.contrib.auth.models import User

# User Profile
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     username = models.CharField(max_length=100)
#     email = models.EmailField()

#     def __str__(self):
#         return f"{self.username}'s Profile"


# Goal Model
class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    custom_goal = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} Goal"


# Mood Model
class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emotion = models.CharField(max_length=50)  # Happy, Sad, etc.
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.emotion} - {self.created_at}"


# Affirmation Model
class Affirmation(models.Model):
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)  # Mood is related to this table using foreign key
    text = models.TextField()

    def __str__(self):
        return f"Affirmation for {self.mood.emotion}"


# Journaling Prompt Model
class JournalingPrompt(models.Model):
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)  # Related to Mood model
    text = models.TextField()

    def __str__(self):
        return f"Prompt for {self.mood.emotion}"


class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.ForeignKey(JournalingPrompt, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Journal Entry by {self.user.username} for prompt: {self.prompt.text}"


# Recommendation Model
class Recommendation(models.Model):
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)  # Related to Mood model
    text = models.TextField()

    def __str__(self):
        return f"Recommendation for {self.mood.emotion}"


# Daily Challenge Model
class DailyChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Challenge for {self.user.username}"
