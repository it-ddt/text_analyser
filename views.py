from django.shortcuts import render
from . import analyser
from . import forms


def index(request):
    """
    FIXME: поля source_file_path, dest_file_path, не проходят валидацию
    FIXME: поле wordcloud_background_color не джанговое, не проходит валидацию тоже
    """
    if request.method == "POST":
        form = forms.AnalyserForm(request.POST)
        print(form)
        if form.is_valid():
            analyser.Analyser(
                source_file_path=r"C:\Users\DDT\Desktop\texts\text_short.txt",
                dest_file_path=r"C:\Users\DDT\Desktop\django_test\my_project\text_analyser\static\text_analyser\wordcloud.jpg",
                parts_of_speech=form.cleaned_data["part_of_speech"],
                words_num=form.cleaned_data["words_num"],
                wordcloud_width=form.cleaned_data["wordcloud_width"],
                wordcloud_height=form.cleaned_data["wordcloud_height"]
            )
            return render(request, "text_analyser/result.html")
        else:
            return render(request, "text_analyser/index.html", {"form": form})
    else:
        form = forms.AnalyserForm()
        return render(request, "text_analyser/index.html", {"form": form})