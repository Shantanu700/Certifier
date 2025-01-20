from django.http import JsonResponse, HttpResponse, FileResponse
from django.core.files.storage import default_storage
from django.core.files import File
from hurry.filesize import size as zipsize, alternative
import json
import re
from django.contrib.auth import authenticate, login, logout
import os
from certifier_app.models import *
from PIL import Image, ImageDraw, ImageFont
from django.db.models import F, Count, When, Case
from datetime import date, datetime, timedelta
import csv
import magic
from django.conf import settings
import shutil
import openpyxl
import random
import string





def get_path(folder_id: int, path: list):
    folder = Folders.objects.get(id=folder_id)
    if folder.parent is None:
        return path
    else:
        path.append({'id':folder.parent_id, 'name':folder.parent.folder_name})
        return get_path(folder.parent_id, path)

def get_valid_filename(filename: str, user_id: int, rand_str=''):
    if not os.path.exists(f'user_files/user_{user_id}/{filename}'):
        return filename, rand_str
    else:
        length = 8
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        ext = filename.split('.')[-1]
        return get_valid_filename(random_string+filename, user_id, random_string)

def resize_image(box: tuple, img: Image):
    img_height = img.height
    img_width = img.width
    box_height = box[3] - box[1]
    box_width = box[2] - box[0]
    if img_height/box_height > img_width/box_width:
        new_image_height = box_height
        new_image_width = int(img_width / (img_height/box_height))
        new_image = img.resize((new_image_width, new_image_height))
        plotting_point = (box_width-new_image_width)//2+box[0],box[1]
        return new_image, plotting_point
    elif img_height/box_height < img_width/box_width:
        new_image_width = box_width
        new_image_height = int(img_height / (img_width/box_width))
        new_image = img.resize((new_image_width, new_image_height))
        plotting_point = box[0],(box_height-new_image_height)//2+box[1]
        return new_image, (box[0], box[1])
    else:
        new_image_width = box_width
        new_image_height = box_height
        new_image = img.resize((new_image_width, new_image_height))
        return new_image, (box[0], box[1])

def get_fitting_font(text: str, myfont: ImageFont, boxlen: float):    
    text_box = myfont.getbbox(text)
    text_len = text_box[2] - text_box[0]
    if boxlen > text_len or myfont.size < 0:
        return myfont
    else:
        new_font = ImageFont.truetype(myfont.path, myfont.size-1)
        return get_fitting_font(text, new_font, boxlen)

def generate_plotting_data(data: str, boxes: list, used_font: ImageFont):
    plotting_data = list()
    total_box_length = 0
    for box in boxes:
        total_box_length += box[2] - box[0]
    total_data_length = used_font.getbbox(data)[2] - used_font.getbbox(data)[0]
    if total_box_length - total_data_length > 0:
        def insert_plotting_data(partial_data, box):
            inserted_data = partial_data
            remaining_data = ''
            space_counter = 1
            box_len = box[2] - box[0]
            while True:
                inserted_data_len = used_font.getbbox(inserted_data)[2] - used_font.getbbox(inserted_data)[0]
                if inserted_data_len < box_len:
                    return (inserted_data, box), remaining_data
                else:
                    remaining_data = ' '.join(partial_data.split()[-1*space_counter:])
                    inserted_data = ' '.join(partial_data.split()[:-1*space_counter])
                    space_counter += 1
#         # while True:
        data_tobe_inserted = data
        for box in boxes:
            node, data_left = insert_plotting_data(data_tobe_inserted, box)
            plotting_data.append(node)
            if data_left:
                data_tobe_inserted = data_left
            else:
                break
        if data_left:
            new_font = ImageFont.truetype(used_font.path, used_font.size-1)
            return generate_plotting_data(data, boxes, new_font)
        else:
            return plotting_data, used_font
    else:
        new_font = get_fitting_font(data, used_font, total_box_length)
        return generate_plotting_data(data, boxes, new_font)

def get_plotting_coordinates(box: tuple, alignment: str):
    if alignment == 'center':
        points = (box[0] + box[2])//2, box[3]
        anchor = 'ms'
    elif alignment == 'right':
        points =  box[2] ,box[3]
        anchor = 'rs'
    else:
        points = box[0], box[3]
        anchor = 'ls'
    return points, anchor

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
    if request.method == 'GET':
        data = Fonts.objects.filter(is_deleted=0).values(key=F('id'), font=F('font_name'))
        return JsonResponse({'fonts':list(data)})
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

            if not os.path.exists(f'user_files/tmp_{request.user.id}'):
                os.mkdir(f'user_files/tmp_{request.user.id}')
            if csv_file:
                with default_storage.open(f'tmp_{request.user.id}/'+csv_file.name, 'wb') as destination:
                    for index,chunk in enumerate(csv_file.chunks()):
                        destination.write(chunk)
            csvfile = open(f'user_files/tmp_{request.user.id}/'+csv_file.name, 'r')
            print(format)
            csv_dict_reader = csv.DictReader(csvfile)
            first_row = csv_dict_reader.fieldnames
            keys = [data.get('key') for data in format if data.get('type')=='text']
            print(keys)
            if None in keys or not set(keys).issubset(set(first_row)):
                return JsonResponse({'status':'Invalid keys'}, status=400)
            for index_csv,row in enumerate(csv_dict_reader):
                img = Image.open(image)
                img = img.convert("RGBA")
                image.name = image.name.split(".")[0]+'.png'
                for key in format:
                    if key.get('type') == 'text':                        
                        key_data = row.get(key.get('key'))
                        boxes = key.get('boxes')
                        box_coordinates = [(box['x1'],box['y1'],box['x2'],box['y2']) for box in boxes]
                        default_box_font = ImageFont.truetype(Fonts.objects.get(id=boxes[0].get('font')).font_file, boxes[0].get('y2') - boxes[0].get('y1'))
                        plotting_box_data, actual_font = generate_plotting_data(key_data, box_coordinates, default_box_font)
                        for index,plotting_box in enumerate(plotting_box_data):
                            color = boxes[index].get('color')
                            plot_coordinates, anchor = get_plotting_coordinates(plotting_box[1], boxes[index].get('align'))
                            I1 = ImageDraw.Draw(img)
                            I1.text(plot_coordinates, plotting_box[0], font=actual_font, anchor=anchor,  fill =color)
                    elif key.get('type') == 'image':
                        key_data = key.get('key')
                        boxes = key.get('boxes')
                        box_coordinates = [(box['x1'],box['y1'],box['x2'],box['y2']) for box in boxes]
                        if len(box_coordinates) != 1:
                            return JsonResponse({'status':f'invalid boxes for {key_data}'}, status=400)
                        key_image = request.FILES.get(key_data)
                        if not key_image:
                            return JsonResponse({'status':f'{key_data} image not found'}, status=404)
                        pil_key_img = Image.open(key_image)
                        pil_key_img = pil_key_img.convert("RGBA")
                        resized_image, point = resize_image(box_coordinates[0], pil_key_img)
                        img.paste(resized_image, point, resized_image)
                    img.save(f'user_files/tmp_{request.user.id}/'+str(index_csv)+'_'+image.name, format='png')
            csvfile.close()
            os.remove(f'user_files/tmp_{request.user.id}/'+csv_file.name)
            valid_filename, rand_string = get_valid_filename(image.name.split('.')[0]+'.zip', request.user.id)
            img.save(f'user_files/user_{request.user.id}/'+rand_string+str(index_csv)+image.name)
            shutil.make_archive(f'user_files/user_{request.user.id}/'+rand_string+image.name.split('.')[0], 'zip', os.path.join(default_storage.base_location, f'tmp_{request.user.id}/'))
            user_zip_file = Files()
            user_zip_file.file.name = f'user_{request.user.id}/'+rand_string+image.name.split('.')[0]+'.zip'
            user_zip_file.thumbnail.name = f'user_{request.user.id}/'+rand_string+str(index_csv)+image.name
            user_zip_file.filename = image.name.split('.')[0]+'.zip'
            user_zip_file.file_size = zipsize(user_zip_file.file.size, system=alternative)
            user_zip_file.file_user = request.user
            user_zip_file.save()
            shutil.rmtree(os.path.join(default_storage.base_location,f'tmp_{request.user.id}'))
            return JsonResponse({'status':'Zip file created successfully', 'route':'download-zip/', 'file_id':user_zip_file.id, 'preview':'media/'+user_zip_file.thumbnail.name})
        return JsonResponse({"status":"Unautherized"},status=401)
    return JsonResponse({"status":"Invalid request method"},status=405)

def manage_file_folders(request, task=None, object_type=None):
    if request.method == 'GET':
        if request.user.is_authenticated:
            folder_id = request.GET.get('folder_id')
            if not folder_id:
                if task == 'star':
                    folders = Folders.objects.filter(is_deleted=0, folder_user=request.user, is_starred=True).annotate(items=Count('child_folder')).values('folder_name', 'created_datetime__date', 'id', 'items', 'is_starred')
                    files = Files.objects.filter(is_deleted=0, file_user=request.user, is_starred=True).values('filename', 'created_datetime__date', 'id', 'file_size', 'is_starred', 'thumbnail')
                    return JsonResponse({'parent_folder':None, 'folders': list(folders), 'files': list(files), 'path':'starred'})
                elif task == 'quick-access':
                    folders = Folders.objects.filter(is_deleted=0, folder_user=request.user, quickly_accessible=True).annotate(items=Count('child_folder')).values('folder_name', 'created_datetime__date', 'id', 'items', 'is_starred')
                    files = Files.objects.filter(is_deleted=0, file_user=request.user, quickly_accessible=True).values('filename', 'created_datetime__date', 'id', 'file_size', 'is_starred', 'thumbnail')
                    return JsonResponse({'parent_folder':None, 'folders': list(folders), 'files': list(files), 'path':'starred'})
                elif task == 'trash':
                    folders = Folders.objects.filter(is_deleted=1, folder_user=request.user, is_permanently_deleted=False).annotate(items=Count('child_folder')).values('folder_name', 'created_datetime__date', 'id', 'items', 'is_starred')
                    files = Files.objects.filter(is_deleted=1, file_user=request.user, is_permanently_deleted=False).values('filename', 'created_datetime__date', 'id', 'file_size', 'is_starred', 'thumbnail')
                    return JsonResponse({'parent_folder':None, 'folders': list(folders), 'files': list(files), 'path':'starred'})
                elif task == 'recents':
                    lookup_date = datetime.today() - timedelta(days=2)
                    folders = Folders.objects.filter(is_deleted=0, folder_user=request.user, created_datetime__date__gt=lookup_date).annotate(items=Count('child_folder')).values('folder_name', 'created_datetime__date', 'id', 'items', 'is_starred')
                    files = Files.objects.filter(is_deleted=0, file_user=request.user, created_datetime__date__gt=lookup_date).values('filename', 'created_datetime__date', 'id', 'file_size', 'is_starred', 'thumbnail')
                    return JsonResponse({'parent_folder':None, 'folders': list(folders), 'files': list(files), 'path':'starred'})
                    
                folders = Folders.objects.filter(is_deleted=0, folder_user=request.user, parent__isnull=True).annotate(items=Count('child_folder')).values('folder_name', 'created_datetime__date', 'id', 'items', 'is_starred')
                files = Files.objects.filter(is_deleted=0, file_user=request.user, parent_folder__isnull=True).values('filename', 'created_datetime__date', 'id', 'file_size', 'is_starred', 'thumbnail')
                return JsonResponse({'parent_folder':None, 'folders': list(folders), 'files': list(files), 'path':'home/'})
            else:                    
                if not folder_id.isnumeric():
                    return JsonResponse({'status':'Invalid folder ID'}, status=400)
                if eval(folder_id) not in list(Folders.objects.filter(folder_user=request.user, is_deleted=0).values_list('id', flat=True)):
                    return JsonResponse({'status':'Folder Not found'}, status=404)
                current_folder = Folders.objects.get(id=folder_id)
                folders = Folders.objects.filter(is_deleted=0, folder_user=request.user, parent_id=folder_id).annotate(items=Count('child_folder')).values('folder_name', 'created_datetime__date', 'id', 'items','is_starred')
                files = Files.objects.filter(is_deleted=0, file_user=request.user, parent_folder_id=folder_id).values('filename', 'created_datetime__date', 'id', 'file_size','is_starred', 'thumbnail')
                return JsonResponse({'parent_folder':current_folder.parent_id, 'folders': list(folders), 'files': list(files), 'path': list(reversed(get_path(eval(folder_id), [{'id':eval(folder_id), 'name':current_folder.folder_name}]))), 'quick_access':current_folder.quickly_accessible})
        return JsonResponse({"status":"Unautherized"},status=401)
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            folder_name = data.get('folder_name')
            if not folder_name:
                return JsonResponse({'status':'Invalid folder name'}, status=400)
            parent_folder = data.get('parent_id')
            if Folders.objects.filter(folder_user=request.user, folder_name=folder_name, is_deleted=0).exists():
                return JsonResponse({'status':'Already exists'}, status=400)
            if parent_folder:
                if parent_folder not in Folders.objects.filter(folder_user=request.user).values_list('id', flat=True):
                    return JsonResponse({'status':'Access Denied'}, status = 403)
                folder = Folders(folder_name=folder_name, folder_user=request.user, parent_id=parent_folder)
                folder.save()
            else:
                folder = Folders(folder_name=folder_name, folder_user=request.user, parent_id=None)
                folder.save()
            return JsonResponse({'status':'Folder created successfully'})
        return JsonResponse({"status":"Unautherized"},status=401)
    if request.method == 'PATCH':
        if request.user.is_authenticated:
            folder_id = request.GET.get('folder_id')
            if not folder_id:
                return JsonResponse({'status':'Folder ID is required'}, status=400)
            if task == 'quick-access':
                if object_type == 'file':
                    updated = Files.objects.filter(file_user=request.user, id=folder_id, is_deleted=False).update(quickly_accessible=~F('quickly_accessible'))
                    if updated:
                        if Files.objects.get(file_user=request.user, id=folder_id).quickly_accessible:
                            return JsonResponse({'status':'File added to quick access'})
                        else:
                            return JsonResponse({'status':'File removed from quick access'})
                    return JsonResponse({'status':'File not found'}, status=404)
                elif object_type == 'folder':
                    updated = Folders.objects.filter(folder_user=request.user, id=folder_id, is_deleted=False).update(quickly_accessible =~F('quickly_accessible'))
                    if updated:
                        if Folders.objects.get(folder_user=request.user, id=folder_id).quickly_accessible:
                            return JsonResponse({'status':'Folder added to quick access'})
                        else:
                            return JsonResponse({'status':'Folder removed from quick access'})
                    return JsonResponse({'status':'Folder not found'}, status=404)
                else:
                    return JsonResponse({'status':'Invalid type'},status=400)
            elif task == 'restore':
                if object_type == 'file':
                    updated = Files.objects.filter(file_user=request.user, id=folder_id, is_deleted=True).update(is_deleted=0)
                    if updated:
                        return JsonResponse({'status':'File restored successfully'})
                    return JsonResponse({'status':'File not found'}, status=404)
                elif object_type == 'folder':
                    updated = Folders.objects.filter(folder_user=request.user, id=folder_id, is_deleted=True).update(is_deleted=0)
                    if updated:
                        return JsonResponse({'status':'Folder restored successfully'})
                    return JsonResponse({'status':'Folder not found'}, status=404)
                else:
                    return JsonResponse({'status':'Invalid type'},status=400)
            elif task == 'star':
                if object_type == 'file':
                    updated = Files.objects.filter(file_user=request.user, id=folder_id, is_deleted=False).update(is_starred=~F('is_starred'))
                    if updated:
                        if Files.objects.get(file_user=request.user, id=folder_id).is_starred:
                            return JsonResponse({'status':'File added to starred'})
                        else:
                            return JsonResponse({'status':'File removed from starred'})
                    return JsonResponse({'status':'File not found'}, status=404)
                elif object_type == 'folder':
                    updated = Folders.objects.filter(folder_user=request.user, id=folder_id, is_deleted=False).update(is_starred =~F('is_starred'))
                    if updated:
                        if Folders.objects.get(folder_user=request.user, id=folder_id).is_starred:
                            return JsonResponse({'status':'Folder added to starred'})
                        else:
                            return JsonResponse({'status':'Folder removed from starred'})
                    return JsonResponse({'status':'Folder not found'}, status=404)
                else:
                    return JsonResponse({'status':'Invalid type'},status=400)
            elif task == 'delete':
                if object_type == 'file':
                    updated = Files.objects.filter(file_user=request.user, id=folder_id, is_permanently_deleted=0).update(is_permanently_deleted=Case(When(is_deleted=True, then=True),When(is_deleted=False, then=False)),is_deleted=1)
                    if updated:
                        return JsonResponse({'status':'File deleted successfully'})
                    return JsonResponse({'status':'File not found'}, status=404)
                elif object_type == 'folder':
                    updated = Folders.objects.filter(folder_user=request.user, id=folder_id, is_permanently_deleted=0).update(is_permanently_deleted=Case(When(is_deleted=True, then=True),When(is_deleted=False, then=False)),is_deleted=1)
                    if updated:
                        return JsonResponse({'status':'Folder deleted successfully'})
                    return JsonResponse({'status':'Folder not found'}, status=404)
                else:
                    return JsonResponse({'status':'Invalid type'},status=400)
            elif task == 'rename':
                new_name = request.GET.get('new_name')
                if not new_name:
                    return JsonResponse({'status':'New Name not found'},status=404)
                if object_type == 'file':
                    if Files.objects.filter(file_user=request.user, filename=new_name+'.zip', is_deleted=False).exists():
                        return JsonResponse({'status':'Already exists'}, status=400)
                    updated = Files.objects.filter(file_user=request.user, id=folder_id, is_deleted=False).update(filename=new_name+'.zip')
                    if updated:
                        return JsonResponse({'status':'File renamed successfully'})
                    return JsonResponse({'status':'File not found'}, status=404)
                elif object_type == 'folder':
                    if Folders.objects.filter(folder_user=request.user, folder_name=new_name, is_deleted=False).exists():
                        return JsonResponse({'status':'Already exists'}, status=400)
                    updated = Folders.objects.filter(folder_user=request.user, id=folder_id, is_deleted=False).update(folder_name=new_name)
                    if updated:
                        return JsonResponse({'status':'Folder renamed successfully'})
                    return JsonResponse({'status':'Folder not found'}, status=404)
                else:
                    return JsonResponse({'status':'Invalid type'},status=400)                            
            # elif task == 'quick':

            else:
                return JsonResponse({'status':'Invalid task'}, status=400)    
        return JsonResponse({"status":"Unautherized"},status=401)
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            files_updated = Files.objects.filter(file_user=request.user, is_permanently_deleted=0, is_deleted=1).update(is_permanently_deleted=1)
            folders_updated = Folders.objects.filter(folder_user=request.user, is_permanently_deleted=0, is_deleted=1).update(is_permanently_deleted=1)
            if files_updated or folders_updated:
                return JsonResponse({'status':'Emptied trash'})
            return JsonResponse({'status':'No files or folders found in trash'}, status=404)
        return JsonResponse({"status":"Unautherized"},status=401)
    if request.method == 'PUT':
        if request.user.is_authenticated:
            folder_id = request.GET.get('folder_id')
            if not folder_id:
                return JsonResponse({'status':'Folder ID is required'}, status=400)
            data = json.loads(request.body)
            final_folder_id = data.get('final_folder_id')
            if final_folder_id is not None:
                if not Folders.objects.filter(folder_user=request.user, id=final_folder_id, is_deleted=False).exists():
                    return JsonResponse({'status':'Destination folder not found'}, status=404)
                if int(folder_id) == final_folder_id:
                    return JsonResponse({'status':"You can't move a folder into itself"}, status=400)
            if task == 'move':
                if object_type == 'file':
                    updated = Files.objects.filter(file_user=request.user, id=folder_id, is_deleted=False).update(parent_folder_id=final_folder_id)
                    if updated:
                        return JsonResponse({'status':'File moved successfully'})
                    return JsonResponse({'status':'File not found'}, status=404)
                elif object_type == 'folder':
                    updated = Folders.objects.filter(folder_user=request.user, id=folder_id, is_deleted=False).update(parent =final_folder_id)
                    if updated:
                        return JsonResponse({'status':'Folder moved successfully'})
                    return JsonResponse({'status':'Folder not found'}, status=404)
                else:
                    return JsonResponse({'status':'Invalid type'},status=400)
            return JsonResponse({'status':'Invalid operation'}, status=400)
        return JsonResponse({"status":"Unautherized"},status=401)
    return JsonResponse({"status":"Invalid request method"},status=405)

def test(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            file_id = request.GET.get('file_id')
            id = request.user.id
            zipfile = Files.objects.get(id=file_id)
            if zipfile.file_user != request.user:
                return JsonResponse({'status':'Access Denied'},status=403)
            file_name = zipfile.file.name
            complete_file_path = os.path.join(default_storage.base_location,file_name)
            if os.path.exists(complete_file_path):
                response = HttpResponse(open(complete_file_path, 'rb'), content_type='application/force-download')
                response['Content-Disposition'] = 'attachment; filename="%s"' % zipfile.filename
                return response
            return JsonResponse({'status':'file not found'}, status=404)
        return JsonResponse({"status":"Unautherized"},status=401)
    return JsonResponse({"status":"Invalid request method"},status=405)
def test2(request):
    if request.method == 'POST':
        xl_file = request.FILES.get('xl_file')
        print(xl_file.content_type)
        print(magic.from_buffer(xl_file.read(1024), mime=True))

        if not xl_file:
            return JsonResponse({'status':'xl file not found'}, status=404)
        with default_storage.open(xl_file.name, 'wb') as destination:
            for index,chunk in enumerate(xl_file.chunks()):
                destination.write(chunk)

        return JsonResponse({'status':'test'})
    return JsonResponse({"status":"Invalid request method"},status=405)
    