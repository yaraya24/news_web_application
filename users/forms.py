from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    """Forms to create a user"""
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'username')

class CustomUserChangeForm(UserChangeForm):
    """Forms to Update a user"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'username')