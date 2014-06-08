from django import forms
from .models import UserProfile
from .models import Link
from .models import Vote
from .models import idea

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ("submitter", "rank_score")

class HackForm(forms.ModelForm):
    class Meta:
        model = idea
        

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
