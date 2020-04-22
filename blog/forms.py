from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment, ReplyComment, Profile
from django.core.exceptions import ValidationError


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!"
        })
    )
    class Meta:
        model = Comment
        fields = ['body']


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=60,
        widget = forms.TextInput(attrs={
            "class" : "form-control",
            "placeholder" : "User Name"
        })
    )
    password = forms.CharField(
        max_length=60,
        widget = forms.PasswordInput(attrs={
            "class" : "form-control",
            "placeholder" : "Password"
        })
    )


class ProfileForm(forms.ModelForm):
    pro_pic = forms.ImageField()
        


    about = forms.CharField(
        widget = forms.Textarea(attrs={
            "class" : "form-control",
            "placeholder" : "About Yourself"
        })
    )
    skills = forms.CharField(max_length=60,
    widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Skills'
        }
    ))
    linkdin = forms.CharField(max_length=60,
    widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'LinkedIn Profile'
        }
    ))
    github = forms.CharField(max_length=60,
    widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Github Profile'
        }
    ))
    class Meta:
        model = Profile
        fields = ['pro_pic', 'about', 'skills', 'linkdin', 'github']




class ReplyForm(forms.ModelForm):
    reply_body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Reply here!"
        })
    )
    class Meta:
        model = ReplyComment
        fields = ['reply_body']
        

class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=60,
        widget = forms.TextInput(attrs={
            "class" : "form-control",
            "placeholder" : "Title"
        })
    )

    cat = forms.CharField(
        max_length=60,
        widget = forms.TextInput(attrs={
            "class" : "form-control",
            "placeholder" : "Category"
        })
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            'class':'form-control',
            'placeholder':'Write your post here'
        }
    ))
    class Meta:
        model = Post
        fields = ['title', 'body', 'cat']


class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=60,
        widget = forms.TextInput(attrs={
            "class" : "form-control",
            "placeholder" : "First Name"
        })
    )

    last_name = forms.CharField(
        max_length=60,
        widget = forms.TextInput(attrs={
            "class" : "form-control",
            "placeholder" : "Last Name"
        })
    )

    email = forms.EmailField(
        max_length=60,
        widget = forms.TextInput(attrs={
            "class" : "form-control",
            "placeholder" : "Email"
        })
    )

    username = forms.CharField(
        max_length=60,
        widget = forms.TextInput(attrs={
            "class" : "form-control",
            "placeholder" : "User Name (Letters, digits and @/./+/-/_ only without space!)"
        })
    )

    password = forms.CharField(
        max_length=60,
        widget = forms.PasswordInput(attrs={
            "class" : "form-control",
            "placeholder" : "Password"
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username' , 'password']

        label = {
            'password': 'Password'
        }

    def save(self):
        password = self.cleaned_data.pop('password')
        u = super().save()
        u.set_password(password)
        u.save()
        return u



class OTPForm(forms.Form):
    body = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter OTP"
        })
    )