from django.shortcuts import render
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

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Ты медицинский ассистент. Дай понятный, точный и безопасный медицинский анализ."},
                        {"role": "user", "content": user_question}
                    ],
                    temperature=0.4,
                    max_tokens=1000
                )
                ai_answer = response['choices'][0]['message']['content']
            except Exception as e:
                ai_answer = f"Ошибка при обработке запроса: {str(e)}"

            user_request.ai_response = ai_answer
            user_request.save()

            return render(request, 'result.html', {'response': ai_answer})
    else:
        form = UserRequestForm()

    return render(request, 'submit.html', {'form': form})