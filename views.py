from django.shortcuts import render
from . import analyser
from . import forms


def index(request):
    if request.method == "POST":
        form = forms.AnalyserForm(request.POST)
        if form.is_valid():
            my_analyser = analyser.Analyser(
                source_file_path=form.cleaned_data["source_file_path"],
                dest_file_path=form.cleaned_data["destination_file_path"],
                part_of_speech=form.cleaned_data["part_of_speech"],
                words_num=form.cleaned_data["words_num"],
                wordcloud_width=form.cleaned_data["wordcloud_width"],
                wordcloud_height=form.cleaned_data["wordcloud_height"],
            )
        return render(request, "text_analyser/result.html", {"wordcloud": my_analyser.wordcloud})
    else:
        form = forms.AnalyserForm()
        return render(request, "text_analyser/index.html", {"form": form})