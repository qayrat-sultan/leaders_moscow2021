from django.shortcuts import render
from django.views.generic import CreateView
from demo.demo import bluring_the_text, abs_path
from .forms import FileForm
# Create your views here.
from os import listdir
from os.path import isfile, join
from .models import FileModel
from django.core.files.base import File
from django.views.generic.base import TemplateView


class MyFilesView(TemplateView):

    template_name = "files.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # List of files in your MEDIA_ROOT
        media_path = abs_path + "/bluring_zip_files"

        myfiles = [f for f in listdir(media_path) if isfile(join(media_path, f))]
        context['myfiles'] = myfiles
        return context


class FileView(CreateView):
    # model = File
    form_class = FileForm
    success_url = "/"
    template_name = "file.html"


    def form_valid(self, form):
        form.save()
        dir_return_file = bluring_the_text(form.instance.file.file.name)
        # file = FileModel.objects.get(file=form.instance.file)
        #
        # file.returned_file = File(open(dir_return_file, "wb"))
        # file.save()
        return super().form_valid(form)