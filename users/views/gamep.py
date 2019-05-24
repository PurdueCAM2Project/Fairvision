from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from users.models import CustomUser, ImageModel, Attribute, RoundsNum, PhaseBreak, Phase01_instruction, Phase02_instruction, Phase03_instruction, Question, Answer

from django.contrib.auth.admin import UserAdmin

from django.http import HttpResponse

from django.shortcuts import render

import boto3
import csv, os
import botocore
from botocore.client import Config
import random
import json
from .roundsgenerator import rphase02


# We should set up in backend manually
KEY = settings.KEY
NUMROUNDS = settings.NUMROUNDS


old_csvPath = os.path.join(settings.BASE_DIR, 'Q & A - Haobo.csv')
new_csvPath = os.path.join(settings.BASE_DIR, 'test_att.csv')


from client import send__receive_data
#@login_required
def phase01a(request):
    rounds, _ = RoundsNum.objects.get_or_create(phase='phase01a', defaults={'num': 1})
    roundsnum = rounds.num

    if roundsnum > NUMROUNDS:
        # push all to waiting page
        return render(request, 'over.html', {'phase': 'PHASE 01a'})

    ''' Test case 
    old_Q = list(Question.objects.filter(isFinal=True).values_list('text', 'id'))
    new_Q = list(Question.objects.filter(isFinal=False).values_list('text', 'id'))

    result_array, id_merge = send__receive_data([new_Q, old_Q])
    # print("I got result array: ", result_array)
    print("I got the merge id: ", id_merge)

    if id_merge:
            for entry in id_merge:
                Question.objects.filter(id=id_merge[entry]).update(isFinal=False)
                Question.objects.filter(id=entry).update(isFinal=True)

    '''

    # Need to check 
    if request.method == 'POST':

        # Get the Q and Ans for the current question, they should be at least one Q&A for all of the set
        questions = request.POST.getlist('questionArray')
        answers = request.POST.getlist('answerArray')

        # retrieve the json data for updating skip count for the previous questions
        dictionary = json.loads(request.POST['data[dict]'])
        '''
        for d in dictionary:
            # print("key: ", d, " value: ", dictionary[d])
            old_Q = Question.objects.get(word=d)
            old_Q.skipCount += dictionary[d]
            old_Q.save()

        # Query list for the old data in the table
        old_Q_list = list(Question.objects.values_list('text', 'id'))

        answers = Answer.objects.bulk_create([Answer(text=ans) for ans in new_answers])
        # print("Well bulk answer objects", answers)

        new_Qs = []
        for que in new_questions:
            new_Q = Question.objects.create(text=que, isFinal=False)
            for ans in answers:
                new_Q.answer_set.add(ans)
            new_Qs.append((new_Q.text, new_Q.id))


        # Call the NLP function and get back with results, it should be something like wether it gets merged or kept 
        # backend call NLP and get back the results, it should be a boolean and a string telling whether the new entry will be created or not
        # exist_q should be telling which new question got merged into
        result_array, id_merge = send__receive_data([new_Q, old_Q])
         # print("I got result array: ", result_array)
        print("I got the merge id: ", id_merge)

        if id_merge:
            for entry in id_merge:
                Question.objects.filter(id=id_merge[entry]).update(isFinal=False)
                Question.objects.filter(id=entry).update(isFinal=True)
                for ans in answers:
                    Question.answer_set.add(ans) 


        # Update the rounds number for phase 01a
        roundsnum = RoundsNum.objects.filter(phase='phase01a').first().num + 1
        RoundsNum.objects.filter(phase='phase01a').update(num=roundsnum)
    '''
    # Single image that will be sent to front-end, will expire in 300 seconds (temporary)
    serving_img_url = default_storage.url(KEY.format(roundsnum)) or "https://media.giphy.com/media/noPodzKTnZvfW/giphy.gif"
    print("I got: ", serving_img_url)
    # Previous all question pairs that will be sent to front-end 
    if roundsnum >= 1 and roundsnum <= NUMROUNDS:
        # Get the previous question 
        previous_questions = Question.objects.all()
        if not previous_questions:
            raise Exception("The previous images does not have any question which is wired")
    return render(request, 'phase01a.html', {'url' : serving_img_url, 'questions': previous_questions })
'''
View for phase 01 b
Output to front-end: list of all questions and 4 images without overlapping (similar to what we did before)
POST = me
'''
#@login_required
def phase01b(request):

    # Only show people all the question and the answer. Keep in mind that people have the chance to click skip for different questions
    # There should be an array of question that got skipped. Each entry should the final question value
    rounds, _ = RoundsNum.objects.get_or_create(phase='phase01b', defaults={'num': 1})
    roundsnum = rounds.num

    data = []
    for i in range(0, 4):
        data.append(default_storage.url(KEY.format(4 * (roundsnum - 1) + i)))

    if roundsnum > NUMROUNDS:
        return render(request, 'over.html', {'phase' : 'PHASE 01b'})

    if request.method == 'POST':
        # Get the answer array for different 
        # Update the rounds number for phase 01b
        roundsnum = RoundsNum.objects.filter(phase='phase01b').first().num + 1
        RoundsNum.objects.filter(phase='phase01b ').update(num=roundsnum)
        # get the dictionary from the front-end back
        dictionary = json.loads(request.POST['data[dict'])
        for d in dictionary:
            if not dictionary[a]:
                skipc = Question.objects.get(text=d).skipCount
                Question.objects.filter(text=d).update(skipCount=skipc)
            else:
                new_Ans = Answer.objects.create(text=dictionary[d])
                new_Ans.question = Question.objects.get(text=d)

    questions = Question.objects.all()
    return render(request, 'over.html', {'phase': 'PHASE 01b', 'image_url' : data, 'quetion_list' : questions})
    # The NLP server will be updated later?

# Remove what we have for phase02
#@login_required
def phase02(request):

    return render(request, 'over.html', {'phase' : 'PHASE 02'})


# View for phase3
#@login_required
def phase03(request):
    attr = Attribute.objects.all()
    attributes = list()

    if attr.exists():
        attributes = attr
    else:
        # just send only none
        attributes = ['none']
    
    inst = Phase03_instruction.get_queryset(Phase03_instruction)
    instructions = list()
    if inst.exists():
        instructions = inst
    else: 
        instructions = ['none']
    
    # Update count
    if request.method == 'POST':
        dictionary = json.loads(request.POST['data[dict]'])
        for d in dictionary:
            # print("key: ", d, " value: ", dictionary[d])
            at = Attribute.objects.get(word=d)
            at.count += dictionary[d]
            at.save()
            
        return HttpResponse(None)
    else:
        return render(request, 'phase03.html', {'attributes': attributes, 'instructions': instructions})


