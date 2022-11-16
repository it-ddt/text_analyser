from django.shortcuts import render
from . import analyser
from . import forms


def index(request):
    """
    FIXME: поля source_file_path, dest_file_path, не проходят валидацию
    FIXME: поле wordcloud_background_color не джанговое, не проходит валидацию тоже
    """
    if request.method == "POST":
        form = forms.AnalyserForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["source_file_content"])
            wordcloud_background_color = request.POST["wordcloud_background_color"]
            analyser.Analyser(
                source_file_path=r"text_analyser\static\text_analyser\source_text.txt",
                dest_file_path=r"text_analyser\static\text_analyser\wordcloud.jpg",
                parts_of_speech=form.cleaned_data["part_of_speech"],
                words_num=form.cleaned_data["words_num"],
                wordcloud_width=form.cleaned_data["wordcloud_width"],
                wordcloud_height=form.cleaned_data["wordcloud_height"],
                wordcloud_background_color=wordcloud_background_color
            )
            return render(request, "text_analyser/result.html", {"wordcloud_background_color": wordcloud_background_color})
        else:
            print("форма невалидна")
            return render(request, "text_analyser/index.html", {"form": form})
    else:
        form = forms.AnalyserForm()
        return render(request, "text_analyser/index.html", {"form": form})


def handle_uploaded_file(f):
    with open(r"text_analyser\static\text_analyser\source_text.txt", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)