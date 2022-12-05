import sqlite3
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
import os


class CommonMethods:
    def __init__(self):
        self.db = sqlite3.connect('DataBase')
        self.cu = self.db.cursor()

        self.files_path = r'./FileBase'
        self.full_files_path = 'C:\\Users\\Archi\\PycharmProjects\\EYAZIIS-3\\FileBase\\'
        self.SentenceExtraction_path = r'./SentenceExtraction_essays'
        self.full_SentenceExtraction_path = 'C:\\Users\\Archi\\PycharmProjects\\EYAZIIS-3\\SentenceExtraction_essays\\'
        self.full_keywords_path = 'C:\\Users\\Archi\\PycharmProjects\\EYAZIIS-3\\Keywords_essays\\'
        # Create lemmatizer and stopwords list
        self.mystem = Mystem()
        self.russian_stopwords = stopwords.words("russian")
        self.filenames = []
        self.range = 2

    def create_dbs(self):
        self.cu.execute("""
        CREATE TABLE IF NOT EXISTS file_content(
            name TEXT,
            content TEXT
        )
        """)
        self.db.commit()

        self.cu.execute("""
                CREATE TABLE IF NOT EXISTS processed_file_content(
                    name TEXT,
                    sentence TEXT,
                    weight TEXT
                )
                """)
        self.db.commit()

    def add_to_db_file_content(self):
        # doesn't work if filename already exists in DataBase. First of all delete row with similar filename.
        files = os.listdir(f'{self.files_path}')
        for path in files:
            self.filenames = files
            self.cu.execute("""SELECT * FROM file_content WHERE name = ?""", (path,))
            db_content = self.cu.fetchall()
            if not db_content:
                with open(f'{self.files_path}/{path}', 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.cu.execute("""INSERT INTO file_content VALUES (?, ?)""", (path, content))
                    self.db.commit()

    def add_to_db_processed_file_content(self):
        data_dict = {}
        self.cu.execute("""SELECT * FROM file_content""")
        data = self.cu.fetchall()
        for row in data:
            data_dict[row[0]] = row[1].split('.')
        for key in data_dict:
            self.cu.execute("""Select * From processed_file_content WHERE name = ?""", (key,))
            res = self.cu.fetchall()
            if not res:
                for ex in data_dict[key]:
                    sentence = self.preprocess_text(ex)
                    self.cu.execute("""INSERT INTO processed_file_content VALUES (?,?,?)""", (key, sentence, 0))
                    self.db.commit()
            else:
                print(f'file "{key}" already exists in data base!')

    # Preprocess function
    def preprocess_text(self, text):
        tokens = self.mystem.lemmatize(text.lower())
        tokens = [token for token in tokens if token not in self.russian_stopwords \
                  and token != " " \
                  and token.strip() not in punctuation]
        text = " ".join(tokens)
        return text
