from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def scan_pen_sevice(request):
    msg = "welcome to visit Dr.Cao's blog,2020!"

    fileStream = request.FILES.get("file")

    print('1', fileStream)

    file_buffer = fileStream.file.read()
    #
    print(len(file_buffer))

    file_name = request.FILES.get("file").name
    print('2', file_name)

    return HttpResponse(msg)
