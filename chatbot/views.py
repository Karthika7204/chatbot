import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import torch
from .nltk_utils import tokenize, bag_of_words
from .model import NeuralNet
from django.http import JsonResponse

# Define the path to the 'data.pth' file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, 'data.pth')

# Load the trained model data
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
data = torch.load(FILE)
print(f"Intents Data: {data.get('data/intents')}")

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

def process_message(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')  # Ensure this matches the input name in your HTML

        if user_message:
            # Tokenize and convert the message to a bag of words
            sentence = tokenize(user_message)
            X = bag_of_words(sentence, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)
            print(f"Tokenized Sentence: {sentence}")
            print(f"Bag of Words: {X}")

            # Predict the tag for the message
            output = model(X)
            _, predicted = torch.max(output, dim=1)
            tag = tags[predicted.item()]

            print(f"Data Content: {data}")
            print(f"Intents Data: {data.get('intents')}")

            # Get the appropriate response from the intents file
            response = "Sorry, I didn’t understand that."
            for intent in data.get('intents', []):
                if tag == intent.get("tag"):
                    response = random.choice(intent.get('responses', [response]))
            return JsonResponse({"response": f"{bot_name}: {response}"})

    return JsonResponse({"response": "No message received"})

# Create your views here.
def index(request):
    return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
import random
from django.core.mail import send_mail

# OTP storage (in-memory dictionary, for simplicity)
otp_storage = {}

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_email(email, otp):
    subject = 'Your OTP for Registration'
    message = f'Your OTP is {otp}. Please enter it to complete your registration.'
    send_mail(subject, message, 'noreply@example.com', [email])

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already registered')
                return redirect('blog:login')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already registered')
                return redirect('blog:login')
            else:
                # Store user details in session
                request.session['username'] = username
                request.session['email'] = email
                request.session['password'] = password

                # Send OTP
                otp = generate_otp()  # Assume you have a function to generate OTP
                request.session['otp'] = otp

                # Send OTP to user's email (you would implement this)
                send_otp_via_email(email, otp)  # Replace with your email sending logic

                return redirect('blog:otp_verify')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('blog:register')
    else:
        return render(request, 'register.html')

def otp_verify(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        stored_otp = request.session.get('otp')

        if entered_otp == stored_otp:
            # Retrieve user details from session
            username = request.session.get('username')
            email = request.session.get('email')
            password = request.session.get('password')

            # Check if the necessary details are present
            if username and email and password:
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Clear session data
                del request.session['otp']
                del request.session['username']
                del request.session['email']
                del request.session['password']

                return redirect('blog:login')
            else:
                messages.info(request, 'User details are missing')
                return redirect('blog:register')
        else:
            messages.info(request, 'Invalid OTP')
            return redirect('blog:otp_verify')
    else:
        return render(request, 'otp_verify.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('blog:login')
    else:
        return render(request, 'login.html')

def Logout(request):
    auth.logout(request)
    return redirect('/')
