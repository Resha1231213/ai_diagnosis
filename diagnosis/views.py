from django.shortcuts import render, redirect
from .forms import UserRequestForm
from .models import UserRequest
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def submit_request(request):
    if request.method == 'POST':
        form = UserRequestForm(request.POST, request.FILES)
        if form.is_valid():
            user_request = form.save(commit=False)
            user_question = form.cleaned_data['question']

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Ты медицинский ассистент. Отвечай чётко, безопасно, полезно."},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.4,
                max_tokens=1000
            )

            user_request.ai_response = response['choices'][0]['message']['content']
            user_request.save()

            return render(request, 'result.html', {
                'response': user_request.ai_response,
                'request_id': user_request.id
            })

    else:
        form = UserRequestForm()

    return render(request, 'submit.html', {'form': form})


def premium_result(request, request_id):
    try:
        user_request = UserRequest.objects.get(id=request_id)
        return render(request, 'premium_result.html', {
            'response': user_request.ai_response
        })
    except UserRequest.DoesNotExist:
        return redirect('/')
