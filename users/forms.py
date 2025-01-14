from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser, Products, Category
from django.contrib.auth.forms import AuthenticationForm
class CustomUserCreationForm(UserCreationForm):


    fullname = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
    email= forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password1= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
    password2= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    department = forms.Select(attrs={'class': 'form-control', 'placeholder': 'Department'}),
    picture = forms.ClearableFileInput(attrs={'required': False}),
    class Meta:
       
        model = CustomUser
        fields = ('fullname', 'email', 'password1', 'password2', 'department', 'picture')

        
    # Remove help texts, including for password fields
   
    


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))


    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if picture:
            # Example validation: Check file size (max 5MB)
            if picture.size > 5 * 1024 * 1024:
                raise forms.ValidationError("The file size is too large. Max size is 5MB.")
        return picture


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Old Password',
            'class': 'form-control',
            'data-toggle': 'password',
            'id': 'password'
        })
    )
    new_password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter New Password',
            'class': 'form-control',
            'data-toggle': 'password',
            'id': 'new_password'
        })
    )
    new_password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm New Password',
            'class': 'form-control',
            'data-toggle': 'password',
            'id': 'confirm_new_password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'product_description': forms.Textarea(attrs={'class': 'form-control'}),
            'product_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
        help_texts = {
            'product_name': 'Enter the name of the product.',
            'product_description': 'Provide a brief description of the product.',
            'product_quantity': 'Enter the available quantity of the product.',
        }

    def clean_product_quantity(self):
        quantity = self.cleaned_data.get('product_quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be a positive number.")
        return quantity
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['fullname', 'picture']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter category name"}),
        }


        