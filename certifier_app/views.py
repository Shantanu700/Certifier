from django.http import JsonResponse, HttpResponse, FileResponse
from django.core.files.storage import default_storage
import json
import re
from django.contrib.auth import authenticate, login, logout
import os
from certifier_app.models import *
from PIL import Image, ImageDraw, ImageFont
# from PIL import ImageDraw
# from PIL import ImageFont
from datetime import date, datetime
import csv
import magic
from django.conf import settings
from zipfile import ZipFile
import shutil
def create_zip(filepaths, user_id):
    with ZipFile(f"test{user_id}.zip", 'w') as zip:
        for file in filepaths:
            zip.write(file)
# def get_font_size(text: str, font: ImageFont, boxlen: float):    
    



def signin(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return JsonResponse({'user_data':{'name':request.user.first_name + ' '+ request.user.last_name, 'email':request.user.email}})
        return JsonResponse({})
    if request.method == 'POST':
        data = json.loads(request.body)
        e_mail = data.get('email')
        passwd = data.get('password')
        if e_mail and passwd:
            if CustomUser.objects.filter(email=e_mail).exists():
                User = authenticate(email=e_mail,password=passwd)
                if User is not None:
                    login(request,User)
                    return JsonResponse({"status":"Logged in Successfully", 'user_data':{'name':User.first_name + ' '+ User.last_name, 'email':User.email}},status=200 )
                return JsonResponse({"status":"Password entered is incorrect"},status=400)
            return JsonResponse({"status":"No user with these credentials"},status=400)
        return JsonResponse({'status':'Email and Password are required'},status=422)
    return JsonResponse({"status":"Invalid request method"},status=405)

def signout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({"status":"Logged out Successfully",'route':'/login',},status=200 )
        return JsonResponse({"status":"No any User was autherized"},status=400)
    return JsonResponse({"status":"Invalid request method"},status=405)

def generate_certificate(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            format = request.POST.get('format')
            print(type(format))
            if not request.POST.get('format'):
                return JsonResponse({'status':'Format not found'}, status=404)
            format = json.loads(format)
            if not isinstance(format, list):
                return JsonResponse({'status':'format is invalid'},status=400)
            image = request.FILES.get('image')
            if not request.FILES.get('image'):
                return JsonResponse({'status':'Certificate image not found'}, status=404)
            ext = image.name.split('.')[-1]
            content_type = image.content_type
            mime_type = magic.from_buffer(image.read(1024), mime=True)
            size = image.size
            if size > settings.MAX_FILE_SIZE:
                return JsonResponse({'status':f'size {size} larger than 1 MB'},status=400)
            if content_type not in settings.ALLOWED_IMG_TYPES.values():
                return JsonResponse({'status':'invalid image content-type'},status=400)
            if ext not in settings.ALLOWED_IMG_TYPES.keys():
                return JsonResponse({'status':'invalid image extension'},status=400)
            if mime_type not in settings.ALLOWED_IMG_TYPES.values() and mime_type != content_type:
                return JsonResponse({'status':'invalid image mime-type'},status=400)
            csv_file = request.FILES.get('data')
            csv_ext = csv_file.name.split('.')[-1]
            csv_content_type = csv_file.content_type
            csv_mime_type = magic.from_buffer(csv_file.read(1024), mime=True)
            csv_size = csv_file.size
            if csv_size > settings.MAX_FILE_SIZE:
                return JsonResponse({'status':f'size {csv_size} larger than 1 MB'},status=400)
            if csv_content_type not in settings.ALLOWED_CSV_TYPES.values():
                return JsonResponse({'status':'invalid csv file content-type'},status=400)
            if csv_ext not in settings.ALLOWED_CSV_TYPES.keys():
                return JsonResponse({'status':'invalid csv file extension'},status=400)
            if csv_mime_type not in settings.ALLOWED_CSV_TYPES.values() and csv_mime_type != csv_content_type:
                return JsonResponse({'status':'invalid csv file mime-type'},status=400)

            print(csv_file.content_type)
            print(magic.from_buffer(csv_file.read(1024), mime=True))
            if not os.path.exists('tmp'):
                os.mkdir('tmp')
            if csv_file:
                with default_storage.open('tmp/'+csv_file.name, 'wb') as destination:
                    for index,chunk in enumerate(csv_file.chunks()):
                        # print(index,chunk)
                        destination.write(chunk)
            csvfile = open('tmp/'+csv_file.name, 'r')
            csv_reader = csv.reader(csvfile)
            # csv_dict_reader = csv.DictReader(csvfile)
            first_row = next(csv_reader)
            csv_file.seek(0)
            keys = [data['key'] for data in format]
            plotting_data = [{'key':data['key'], 'mid_point' :((data['x1'] + data['x2'])/2,(data['y1'] + data['y2'])/2), 'font_size':abs(data['y2'] - data['y1']), 'box_length': abs(data['x2'] - data['x1'])} for data in format]
            if first_row!=keys:
                return JsonResponse({'status':'provided keys and csv file fields are different'},status=400)

            for index_csv, row in enumerate(csv_reader):
                img = Image.open(image)
                for index_field, field in enumerate(plotting_data):
                    I1 = ImageDraw.Draw(img)
                    myFont = ImageFont.truetype('GreatVibes-Regular.ttf', field['font_size'])
                    I1.text(field['mid_point'], row[index_field], font=myFont, anchor='mm',  fill =(1, 34, 92))
                img.save('tmp/'+str(index_csv)+image.name)
                filepaths = []
                for root, directories, files in os.walk('./tmp'):
                    for file in files:
                        filepath = os.path.join(root, file)
                        filepaths.append(filepath)
            print(filepaths)
            create_zip(filepaths=filepaths, user_id=request.user.id)
            # print(img.size)
            # print(image.name)
            # return FileResponse(open(image.name, 'rb'))
            # response = HttpResponse(open(image.name, 'rb'), content_type='application/force-download')
            # response['Content-Disposition'] = 'attachment; filename="%s"' % image.name
            return JsonResponse({'status':'Zip file created successfully', 'route':'download_zip/', 'user_id':request.user.id})
        return JsonResponse({"status":"No any User was autherized"},status=400)
    return JsonResponse({"status":"Invalid request method"},status=405)


def test(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            id = request.user.id
            id = 2
            print(id)
            file_name = f'test{id}.zip'
            print(file_name)
            if os.path.exists(file_name):
                response = HttpResponse(open(file_name, 'rb'), content_type='application/force-download')
                response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
                os.remove('test2.zip')
                shutil.rmtree('tmp')
                return response
            return JsonResponse({'status':'file not found'}, status=404)
        return JsonResponse({"status":"Unautherized"},status=401)
    return JsonResponse({"status":"Invalid request method"},status=405)
def test2(request):
    if request.method == 'GET':
        response = HttpResponse(open('pngfind.com-anime-guy-png-1692847 (1).png', 'rb'), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s"' % 'pngfind.com-anime-guy-png-1692847 (1).png'
        return response
    return JsonResponse({"status":"Invalid request method"},status=405)
    