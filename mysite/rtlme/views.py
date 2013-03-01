from django.shortcuts import render, redirect, get_object_or_404
from models import Result
# from rtlparse.rtlparse import CSSRtlParser


def index(request):
    return render(request, "rtlme/index.html")


def rtl(request):
    try:
        input_text = request.POST['input_text']
    except (KeyError):
        return render(request, 'rtlme/index.html', {
            'error_message': "Please fill in the text to rtl",
            })
    # output_text = CSSRtlParser(input_text).parse()

    return redirect('/rtlme/%s/' % 1)


def result(request, result_id):
    current_result = get_object_or_404(Result, pk=result_id)
    context = {'result': current_result}
    return render(request, "rtlme/result.html", context)