import random
import string
from django.shortcuts import render
from django.http import HttpResponse
from django.middleware.csrf import get_token

def generate_password(request):
    if request.method == 'POST':
        min_length = request.POST.get('min_length')
        has_number = request.POST.get('has_number') == 'on'
        has_special = request.POST.get('has_special') == 'on'

        try:
            min_length = int(min_length)
            if min_length <= 0:
                raise ValueError("Minimum length should be a positive integer.")
        except ValueError:
            return HttpResponse("Invalid input for minimum length.")

        letters = string.ascii_letters
        digits = string.digits
        special = string.punctuation

        characters = letters
        if has_number:
            characters += digits

        if has_special:
            characters += special

        pwd = generate_random_password(characters, min_length)

        return render(request, 'pwd_gen_app/generate_password.html', {'password': pwd})

    csrf_token = get_token(request)
    return render(request, 'pwd_gen_app/generate_password.html', {'csrf_token': csrf_token})

def generate_random_password(characters, min_length):
    pwd = ""
    meets_criteria = False
    has_number = False
    has_special = False

    while not meets_criteria or len(pwd) < min_length:
        new_char = random.choice(characters)
        pwd += new_char

        if new_char in string.digits:
            has_number = True
        elif new_char in string.punctuation:
            has_special = True

        meets_criteria = True
        if has_number and has_special:
            meets_criteria = True

    return pwd
