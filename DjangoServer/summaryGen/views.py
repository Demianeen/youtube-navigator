import re
from django.shortcuts import render
from summaryGen.forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import datetime
import logging
import environ
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

env = environ.Env()

# Create your views here.
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user  = authenticate(email=email, password=password)

        if user:
            if user.is_active:
                login(request,user)
                response_dict = {'email':user.email}
                return JsonResponse(response_dict)
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print('SOMEONE tried to login and failed')
            print('email: {}'.format(email))
            return HttpResponse('invalid login details supplied')
    else:
        return HttpResponse('no post request')
    
def user_logout(request):
    return HttpResponse('Logged Out')

@csrf_exempt
def registerHtml(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            print('valid user')
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            response_dict = {'email':user.email}
            return JsonResponse(response_dict)
        else:
            #Django delivers errors in a dict, the dict is turned into a string and sent as a response
            error_json = user_form.errors.get_json_data(escape_html=False)
            print(error_json)
            error_response = ""
            for fieldName in error_json.keys():
                error_response += fieldName + ": " +error_json[fieldName][0]['message'] + "\n"
            print(error_response)
            return HttpResponse(error_response)
    else:
        print('no post request')
        return HttpResponse('no post request')

# def clean_text(text):
#     # removes stop words like "a", "an", "the", "of", "in"
#     stop_words = set(stopwords.words('english'))
#     words = text.split()
#     words = [w for w in words if not w in stop_words]
#     text = ' '.join(words)
    
#     # Remove text within square brackets like [Music]
#     text = re.sub(r'\[.*?\]', '', text)
    
#     # transform text into lowercase
#     text = text.lower()
#     return text

def retrieveSummary(videoID,user_prompt):
    try:
        # Retrieve the transcript for the specified video ID
        transcript_list = YouTubeTranscriptApi.list_transcripts(videoID)
        transcript = transcript_list.find_transcript(['en'])
        transcript_fetched = transcript.fetch()

        # Set OpenAI API key
        openai.api_key = env("OPENAI_API_KEY")

        # Initialize result and user prompt variables
        result = ''

        # Define function to split transcript into chunks by time interval
        def split_transcript_by_seconds(transcript_fetched, seconds):
            chunks = []
            current_chunk = []
            current_time = None

            for i, line_data in enumerate(transcript_fetched):
                line_time = datetime.timedelta(seconds=line_data['start'])

                # If current time interval is greater than specified interval, start new chunk
                if current_time is None:
                    current_time = line_time
                if (line_time - current_time).total_seconds() > seconds:
                    chunks.append(current_chunk)
                    current_chunk = []
                    current_time = line_time
                else:
                    # If last line, add to current chunk and append to list
                    if i == len(transcript_fetched) - 1:
                        chunks.append(current_chunk)

                current_chunk.append(line_data['text'])

            return chunks

        # Split transcript into chunks by specified time interval (300 seconds = 5 minutes)
        chunks = split_transcript_by_seconds(transcript_fetched, 450)

        # Iterate through each chunk and summarize using OpenAI API
        for chunk in range(len(chunks)):
            transcript_texted = ' '.join(chunks[chunk])
            prompt = f"\n\n{transcript_texted}\n Summarize the previous text\n"
            try:
                # Use OpenAI's text-curie-001 model to summarize chunk of transcript
                response = openai.Completion.create(
                    model="text-curie-001",
                    temperature=0.1,
                    prompt=prompt,
                    max_tokens=300
                )

                # Retrieve summary and append to result string
                summary = response.choices[0].text
                result += summary
            
            except openai.error.OpenAIError as error:
                # If there is an error with the OpenAI API, print the error message
                print(f"OpenAI API Error: {error}")

        # Generate prompt for final summarization using OpenAI's text-davinci-003 model
        if user_prompt == '':
            prompt = f'\n{result} \nTL;DR\n'
        else:
            prompt = f'{result}\n\nTL;DR. And {user_prompt}\n'
        response = openai.Completion.create(
            model="text-davinci-003",
            temperature=0.1,
            prompt=prompt,
            max_tokens=800
        )
        # Retrieve final summary
        summary = response.choices[0].text
        return summary
    except Exception as e:
        logging.error('Error at %s', 'division', exc_info=e)

@csrf_exempt
def summary(request):
    if request.method == 'POST':
        try:
            print(request.POST)
            #expected: {'videoID':'theVideoId'}
            videoID = request.POST.get('videoID')
            
            try:
                user_prompt = request.POST.get('user_prompt')
            except:
                user_prompt = ''
                
            if user_prompt == None:
                user_prompt = ''
                
            summaryStr = retrieveSummary(videoID,user_prompt)
            return JsonResponse({ 'summary': summaryStr })
        
        except Exception as e:
            logging.error('Error at %s', 'division', exc_info=e)
    else:
        print('no post request')
        return HttpResponse('no post request')


    