from CommonMethods import *

from collections import Counter


class Keywords(CommonMethods):
    def keywords_generate_essay(self):
        for filename in self.filenames:
            data_str = ''
            self.cu.execute("""SELECT sentence FROM processed_file_content WHERE name = ?""", (filename,))
            data = self.cu.fetchall()
            for sentence in data:
                data_str += ' '.join(sentence)
            data_list = data_str.split()
            counted_data = Counter(data_list)
            most_freq = []
            for key in counted_data:
                most_freq.append(key)

    def get_words(self):
        lower_threshold = 3
        for filename in self.filenames:
            words_list = []
            final_words_list = []
            self.cu.execute("""SELECT sentence FROM processed_file_content WHERE name = ? AND weight > ?""",
                            (filename, lower_threshold))
            data = self.cu.fetchall()
            for tup in data:
                for word in tup[0].split():
                    if len(word) > 3 and word not in self.russian_stopwords:
                        words_list.append(word)
            counted_words_dict = Counter(words_list)
            for key in counted_words_dict:
                if counted_words_dict[key] > 1:
                    final_words_list.append(key)
            result_words_str = '\n'.join(final_words_list)
            self.write_keyword_essays(filename, result_words_str)

    def write_keyword_essays(self, filename, content):
        with open(f'./Keywords_essays/{filename}', 'w', encoding='utf-8') as file:
            file.write(content)
