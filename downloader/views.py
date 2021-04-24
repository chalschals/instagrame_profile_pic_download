from django.shortcuts import render
from django.views.generic import TemplateView
from downloader.forms import InstaForm
import instaloader 
from django.conf import settings
import os
import shutil
from pathlib import Path
from django.http import HttpResponse, Http404
# Create your views here.


def InstaFormView(request):
    formObj = InstaForm()
    error = 0
    error_msg = ""
    image_url = None
    if request.method == 'POST':
        data = request.POST
        formObj = InstaForm(data)
        if formObj.is_valid():
            formObj.save()
            PROFILE_NAME = data.get('profile_name')
            OUT_PATH = os.path.join(settings.MEDIA_DIR,PROFILE_NAME)#FULL PATH
            if Path(OUT_PATH).exists() and Path(OUT_PATH).is_dir():
                shutil.rmtree(OUT_PATH)
            ig = instaloader.Instaloader(dirname_pattern=str(OUT_PATH),filename_pattern='')
            try:
                ig.download_profile(PROFILE_NAME,profile_pic_only=True)
                for filename in os.listdir(OUT_PATH):
                    CURRENTFILE = os.path.join(OUT_PATH,filename)
                    if filename.endswith('.jpg'):
                        image_url = os.path.join(settings.MEDIA_URL,PROFILE_NAME,filename)
                    else:
                        os.remove(CURRENTFILE)
            except:
                error = 1
                error_msg = "Invalid Instagram Profile ID"
                image_url = None
        else:
            error = 1
            error_msg = "Please Fill All The Fields"
            image_url = None
    return render(request,'index.html',context={'form':formObj,"error":error,"error_msg":error_msg,"image_url":image_url})