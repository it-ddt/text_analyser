import re  # разбирем строку на отдельные слова
from docx import Document  # pip install python-docx
from bs4 import BeautifulSoup  # прасинг xml
import pymorphy2  # нормализация частей речи
from collections import Counter  # считаем самые частые слова
from wordcloud import WordCloud  # pip install wordcloud
from charset_normalizer import from_path  # нормализуем кодировку


class Analyser:
    # Все аргументы в конструктор класса!
    def __init__(
            self,
            source_file_path="",
            parts_of_speech=None,
            words_num=None,
            dest_file_path="",
            wordcloud_width="1920",
            wordcloud_height="1080",
            wordcloud_background_color="black"
    ):
        if not words_num:
            raise ValueError("Не выбрано количество слов в картинке облака")
        if not parts_of_speech:
            raise ValueError("Части речи не выбраны, анализ текста невозможен")
        self.source_file_path = source_file_path
        self.dest_file_path = dest_file_path
        self.wordcloud_width = wordcloud_width
        self.wordcloud_height = wordcloud_height
        self.wordcloud_background_color = wordcloud_background_color
        self.make_text_from_file()
        self.make_words_from_text()
        self.make_normalized_words(parts_of_speech)
        self.make_most_frequent_words(words_num)
        self.make_wordcloud()
        self.save_wordcloud_to_file()


    def make_text_from_file(self):  # неточное название
        """
        определяет расширение текстового файла,
        вызывает соответствуйющий метод для типов TXT, DOCX, FB2
        """
        if self.source_file_path.endswith(".txt"):
            self.make_text_from_txt()
        elif self.source_file_path.endswith(".docx"):
            self.make_text_from_docx()
        elif self.source_file_path.endswith(".fb2"):
            self.make_text_from_fb2()
        else:
            # прервать выполнение при пустой строке
            print("Тип файла не определен. Завершение работы.")  # exception

    def make_text_from_txt(self):
        """
        Делает строку из TXT
        """
        self.content = str(from_path(self.source_file_path).best())

    def make_text_from_docx(self):
        """
        Делает строку из DOCX
        """
        file = Document(self.source_file_path)
        self.content = " ".join([p.text for p in file.paragraphs])

    def make_text_from_fb2(self):
        """
        Делает строку из FB2
        """
        with open(self.source_file_path, 'rb') as f:
            data = f.read()
        bs_data = BeautifulSoup(data, "xml")
        sections = bs_data.find_all('section')
        self.content = " ".join([s.text for s in sections])

    def make_words_from_text(self):
        """
        Создает список русских слов со строчной буквы без знаков препинания
        """
        self.words = re.findall("[а-яё]+", self.content.lower())

    def make_normalized_words(self, parts_of_speech):
        """
        Создает список нормальных форм слов
        для определенных в part_of_speech частей речи.
        https://pymorphy2.readthedocs.io/en/stable/user/grammemes.html#grammeme-docs
        """
        morph = pymorphy2.MorphAnalyzer()
        self.normalized_words = []
        for word in self.words:
            parse = morph.parse(word)[0]
            for part in parts_of_speech:
                if part in parse.tag:
                    self.normalized_words.append(parse.normal_form)


    def make_most_frequent_words(self, num):
        """
        Создает словарь длинной num из самых частых слов по убыванию частоты
        слово: частота
        """
        self.most_frequent_words = dict(Counter(
            self.normalized_words).most_common(num))
        
    def make_wordcloud(self):
        """
        Создает объект Wordcloud из словаря self.most_frequent_words
        """
        self.wordcloud = WordCloud(
            width=self.wordcloud_width,
            height=self.wordcloud_height,
            background_color=self.wordcloud_background_color
        )
        self.wordcloud = self.wordcloud.generate_from_frequencies(
            self.most_frequent_words
        )

    def save_wordcloud_to_file(self):
        """
        сохраняет Wordcloud в файл filename
        """
        self.wordcloud.to_file(self.dest_file_path)
        print("Done!")


if __name__ == "__main__":
    analyser = Analyser(
        source_file_path="C:/Users/DDT/Desktop/text_short.txt",
        dest_file_path="C:/Users/DDT/Desktop/wordcloud.png",
        parts_of_speech=["NOUN"],
        wordcloud_width=800,
        wordcloud_height=600,
        wordcloud_background_color="#0000ff"
    )
