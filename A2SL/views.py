from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from django.views.decorators.csrf import csrf_exempt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import os
import json

# Add custom NLTK data path (if needed)
nltk.data.path.append(os.path.join(os.getcwd(), "nltk_data"))

# Safe-download punkt
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir=os.path.join(os.getcwd(), "nltk_data"))

from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required

def home_view(request):
	return render(request,'home.html')


def about_view(request):
	return render(request,'about.html')


def contact_view(request):
	return render(request,'contact.html')

@csrf_exempt
def animation_view(request):
	if request.method == 'POST':
		text = request.POST.get('sen')
		#tokenizing the sentence
		text.lower()
	
		#tokenizing the sentence
		words = word_tokenize(text)

		tagged = nltk.pos_tag(words)
		tense = {}
		tense["future"] = len([word for word in tagged if word[1] == "MD"])
		tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
		tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
		tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



		#stopwords that will be removed
		stop_words = set(["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've",'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])



		#removing stopwords and applying lemmatizing nlp process to words
		lr = WordNetLemmatizer()
		filtered_text = []
		for w,p in zip(words,tagged):
			if w not in stop_words:
				if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
					filtered_text.append(lr.lemmatize(w,pos='v'))
				elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
					filtered_text.append(lr.lemmatize(w,pos='a'))

				else:
					filtered_text.append(lr.lemmatize(w))


		#adding the specific word to specify tense
		words = filtered_text
		temp=[]
		for w in words:
			if w=='I':
				temp.append('Me')
			else:
				temp.append(w)
		words = temp
		probable_tense = max(tense,key=tense.get)

		if probable_tense == "past" and tense["past"]>=1:
			temp = ["Before"]
			temp = temp + words
			words = temp
		elif probable_tense == "future" and tense["future"]>=1:
			if "Will" not in words:
					temp = ["Will"]
					temp = temp + words
					words = temp
			else:
				pass
		elif probable_tense == "present":
			if tense["present_continuous"]>=1:
				temp = ["Now"]
				temp = temp + words
				words = temp


		filtered_text = []
		for w in words:
			path = w + ".mp4"
			f = finders.find(path)
			#splitting the word if its animation is not present in database
			if not f:
				for c in w:
					filtered_text.append(c)
			#otherwise animation of word
			else:
				filtered_text.append(w)
		words = filtered_text;


		return render(request,'animation.html',{'words':words,'text':text})
	else:
		return render(request,'animation.html')




def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request,user)
			# log the user in
			return redirect('animation')
	else:
		form = UserCreationForm()
	return render(request,'signup.html',{'form':form})



def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			#log in user
			user = form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('animation')
	else:
		form = AuthenticationForm()
	return render(request,'login.html',{'form':form})


def logout_view(request):
	logout(request)
	return redirect("home")

# API endpoint for Next.js frontend (no login required)
@csrf_exempt
def api_animation_view(request):
	if request.method != 'POST':
		return JsonResponse({'error': 'Method not allowed'}, status=405)

	try:
		text = request.POST.get('sen', '').strip()
		if not text:
			return JsonResponse({'error': 'No text provided'}, status=400)

		# Build available asset set (title-case keys) for O(1) lookup
		available = {}
		for name in os.listdir(os.path.join(os.getcwd(), 'assets')):
			if name.endswith('.mp4'):
				available[name[:-4].lower()] = name[:-4]  # lowercase -> title-case key

		# Synonym map → maps common words to available asset names
		SYNONYMS = {
			'glad': 'Happy', 'joyful': 'Happy', 'joyous': 'Happy',
			'hi': 'Hello', 'hey': 'Hello', 'greetings': 'Hello',
			'thanks': 'Thank You', 'thank you': 'Thank You',
			'bye bye': 'Bye', 'goodbye': 'Bye', 'farewell': 'Bye',
			'cannot': 'Cannot', "can't": 'Cannot',
			'will not': 'Do Not', "won't": 'Do Not',
			'does not': 'Does Not', "doesn't": 'Does Not',
			'do not': 'Do Not', "don't": 'Do Not',
			'me': 'ME', 'myself': 'ME',
		}

		# Multi-word phrases to detect before tokenizing (longest first)
		PHRASES = ['thank you', 'do not', 'does not', 'will not', 'bye bye', 'can not']

		# Preserve original case for asset lookup but process lowercased
		text_lower = text.lower()

		# Detect multi-word phrases and replace with placeholder tokens
		phrase_map = {}
		processed = text_lower
		for phrase in sorted(PHRASES, key=len, reverse=True):
			if phrase in processed:
				token = '__phrase_' + phrase.replace(' ', '_') + '__'
				phrase_map[token] = SYNONYMS.get(phrase, phrase.title())
				processed = processed.replace(phrase, token)

		# Tokenize
		raw_words = word_tokenize(processed)

		# Restore phrase tokens
		expanded = []
		for w in raw_words:
			if w in phrase_map:
				expanded.append(phrase_map[w])
			else:
				expanded.append(w)
		raw_words = expanded

		# POS tag on original-case tokens for tense detection
		tagged = nltk.pos_tag(raw_words)
		tense = {
			'future': len([w for w in tagged if w[1] == 'MD']),
			'present': len([w for w in tagged if w[1] in ['VBP', 'VBZ', 'VBG']]),
			'past': len([w for w in tagged if w[1] in ['VBD', 'VBN']]),
			'present_continuous': len([w for w in tagged if w[1] == 'VBG']),
		}

		# Stopwords — keep negation words (not, no, never, cannot)
		stop_words = set([
			're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn',
			"you've", 'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't",
			'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'weren',
			's', "you'd", 'doesn', "hadn't", 'is', 'was', "that'll",
			"should've", 'a', 'then', 'the', 'mustn', 'nor', 'as', "it's",
			"needn't", 'd', 'am', 'have', 'hasn', 'o', "aren't", "you'll",
			"couldn't", "you're", "mustn't", 'didn', 'll', 'an', 'hadn',
			'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't",
			'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being',
			'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't",
			"won't", 'do', 'i',
		])

		lr = WordNetLemmatizer()
		filtered_text = []
		for w, p in zip(raw_words, tagged):
			if w.lower() in stop_words:
				continue
			# Apply synonym map first
			synonym = SYNONYMS.get(w.lower())
			if synonym:
				filtered_text.append(synonym)
				continue
			# Lemmatize based on POS
			if p[1] in ('VBG', 'VBD', 'VBZ', 'VBN', 'NN'):
				filtered_text.append(lr.lemmatize(w, pos='v').title())
			elif p[1] in ('JJ', 'JJR', 'JJS', 'RBR', 'RBS'):
				filtered_text.append(lr.lemmatize(w, pos='a').title())
			else:
				filtered_text.append(lr.lemmatize(w).title())

		words = filtered_text

		# ISL word order: move subject (Me/You) to front, verb to end (basic SOV)
		subjects = [w for w in words if w in ('Me', 'You', 'We', 'They', 'He', 'She')]
		non_subjects = [w for w in words if w not in ('Me', 'You', 'We', 'They', 'He', 'She')]
		words = subjects + non_subjects

		# Tense markers
		probable_tense = max(tense, key=tense.get)
		if probable_tense == 'past' and tense['past'] >= 1:
			words = ['Before'] + words
		elif probable_tense == 'future' and tense['future'] >= 1:
			if 'Will' not in words:
				words = ['Will'] + words
		elif probable_tense == 'present' and tense['present_continuous'] >= 1:
			words = ['Now'] + words

		# Asset resolution: title-case lookup, fallback to fingerspelling
		final = []
		for w in words:
			if w.lower() in available:
				final.append(available[w.lower()])  # use exact asset filename casing
			else:
				for c in w.upper():
					if c.isalpha() or c.isdigit():
						final.append(c)

		return JsonResponse({'words': final, 'text': text})

	except Exception as e:
		return JsonResponse({'error': str(e)}, status=500)
