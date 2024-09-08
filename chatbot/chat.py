import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('data/intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE, map_location=device)
print(data)

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

# Expanded dictionary of bad words
bad_words = {
    'funck': 'severe', 'shit': 'severe', 'fuck': 'severe', 'bitch': 'severe',
    'asshole': 'severe', 'bastard': 'severe', 'cunt': 'severe', 'nigger': 'severe',
    'whore': 'severe', 'slut': 'severe', 'piss': 'severe', 'dick': 'severe',
    'prick': 'severe', 'cock': 'severe', 'fag': 'severe', 'motherfucker': 'severe',
    'damn': 'moderate', 'crap': 'moderate', 'hell': 'moderate', 'bullshit': 'moderate',
    'pussy': 'severe', 'twat': 'severe', 'wanker': 'severe', 'arsehole': 'severe',
    'jerk': 'moderate', 'freak': 'mild', 'darn': 'mild', 'suck': 'moderate',
    'bugger': 'moderate', 'bloody': 'moderate', 'bollocks': 'moderate', 'arse': 'moderate',
    'shithead': 'severe', 'douche': 'severe', 'numbnuts': 'moderate', 'knob': 'moderate',
    'tosser': 'moderate', 'wank': 'severe', 'shitfaced': 'severe', 'pisshead': 'severe',
    'skank': 'severe', 'dumbass': 'severe', 'butthead': 'mild', 'butt': 'mild',
    'bollocking': 'moderate', 'pissant': 'moderate', 'arsewipe': 'severe',
    'shitbag': 'severe', 'shitstain': 'severe'
}

print("Let's chat! (type 'quit' to exit)")
while True:
    sentence = input("You: ") 
    if sentence == "quit":
        break

    # Convert the input to lowercase to handle case sensitivity
    sentence_lower = sentence.lower()

    # Bad word filtration step
    if any(bad_word in sentence_lower for bad_word in bad_words):
        print(f"{bot_name}: Please refrain from using inappropriate language.")
        continue

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
    else:
        print(f"{bot_name}: I do not understand...")