
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import EmailField
from user.validators import RegisteredEmailValidator

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'name')

class LoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

# field -> 유효성 검증과 위젯의 기능들을 호출
# widget -> 필드의 실제 렌더링

class VerificationEmailForm(forms.Form):
    email = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), validators=(EmailField.default_validators + [RegisteredEmailValidator()]))
