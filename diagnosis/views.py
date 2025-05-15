from django.shortcuts import render, redirect
from .forms import UserRequestForm
from .models import UserRequest
from django.views.decorators.csrf import csrf_exempt
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def submit_request(request):
    if request.method == 'POST':
        form = UserRequestForm(request.POST, request.FILES)
        if form.is_valid():
            user_request = form.save()

            try:
                user_file = user_request.file.read().decode("utf-8")
            except:
                user_file = ''

            prompt = f"{user_request.question}\n\n{user_file}"

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000
                )
                ai_answer = response['choices'][0]['message']['content']
            except:
                ai_answer = "Произошла ошибка при обработке запроса."

            user_request.ai_response = ai_answer
            user_request.save()

            request.session['user_request_id'] = user_request.id

            return render(request, 'result.html', {'response': ai_answer})
    else:
        form = UserRequestForm()

    return render(request, 'submit.html', {'form': form})


def result(request):
    return render(request, 'result.html')


def premium_result(request):
    user_request_id = request.session.get('user_request_id')
    if not user_request_id:
        return redirect('submit_request')

    try:
        user_request = UserRequest.objects.get(id=user_request_id)
    except UserRequest.DoesNotExist:
        return redirect('submit_request')

    return render(request, 'premium_result.html', {
        'response': user_request.ai_response,
        'full_name': user_request.full_name,
        'email': user_request.email
    })
