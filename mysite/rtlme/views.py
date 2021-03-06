from django.shortcuts import render, redirect
from rtlparse import CSSRtlParser
from models import Result, Feedback


def index(request):
    return render(request, "rtlme/index.html")


def rtl(request):
    try:
        input_text = request.POST['input_text']
        try:
            output_text = CSSRtlParser(input_text).parse()
            result = Result.create(input_text, output_text, True)
            result.save()
            return redirect('/rtlme/%s/' % result.pk)
        # TODO arikg: handle smaller exception
        except Exception:
            result = Result.create(input_text, Exception.message, False)
            result.save()
            return redirect('/rtlme/%s/' % result.pk)
    except KeyError:
        return render(request, 'rtlme/index.html', {
            'error_message': "Please fill in the text to rtl",
        })


def feedback(request, result_id):
    try:
        rate_text = request.POST['rate-text']
        rate_score = request.POST['score']
        result = Result.objects.get(pk=result_id)
        feedback = Feedback(rating=rate_score, text=rate_text, result=result)
        feedback.save()
    # TODO arikg: handle smaller exception
    except Exception:
        return redirect('/rtlme/%s/' % result_id, {
            'error_message': "Please fill in the rating and text",
        })
    return redirect('/rtlme/thanks')


def thanks(request):
    return render(request, "rtlme/thanks.html")