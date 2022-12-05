from CommonMethods import *

from collections import Counter
import math


class SentenceExtraction(CommonMethods):
    def get_sentences(self):
        self.cu.execute("""SELECT name FROM file_content""")
        res = self.cu.fetchall()
        for i in res:
            name = i[0]
            self.cu.execute("""Select sentence From processed_file_content Where name = ?""", (name,))
            sentences = self.cu.fetchall()
            for sentence in sentences:
                self.se_process(name, sentence[0])

    def se_process(self, name, sentence):
        words_list = sentence.split()
        sentence_score = 0
        for word in words_list:
            freq_in_doc = self.frequency_in_document(name, word)
            max_freq_word = self.max_frequency_in_document(name)
            num_of_docs = self.number_of_documents()
            num_of_docs_with_word = self.number_of_documents_with_word(word)

            word_weight = 0.5 * (1 + freq_in_doc / max_freq_word) * math.log(num_of_docs / num_of_docs_with_word)
            sentence_score += words_list.count(word) * word_weight

        self.cu.execute("""UPDATE processed_file_content SET weight = ? WHERE sentence = ?""",
                        (sentence_score, sentence))
        self.db.commit()
        self.sentence_extraction_generate_essay()

    def number_of_documents_with_word(self, word):
        res = 0
        for filename in self.filenames:
            content = ''
            self.cu.execute("""SELECT sentence FROM processed_file_content WHERE name = ?""", (filename,))
            request = self.cu.fetchall()
            for tup in request:
                temp = tup[0]
                content += ' ' + temp
            if word in content:
                res += 1
        return res

    def number_of_documents(self):
        return len(self.filenames)

    def frequency_in_document(self, name, word):
        self.cu.execute("""SELECT content FROM file_content WHERE name = ?""", (name,))
        content = self.cu.fetchone()[0]
        return content.count(word)

    def max_frequency_in_document(self, name):
        file_content_str = ''
        self.cu.execute("""SELECT sentence FROM processed_file_content WHERE name = ?""", (name,))
        file_content_raw = self.cu.fetchall()
        for single_tuple in file_content_raw:
            temp = single_tuple[0]
            file_content_str += ' ' + temp
        file_content_list = file_content_str.split()
        return max(Counter(file_content_list).values())

    def sentence_extraction_generate_essay(self):
        for filename in self.filenames:
            self.cu.execute("""SELECT content FROM file_content WHERE name = ?""", (filename,))
            data = self.cu.fetchall()
            self.cu.execute("""SELECT weight FROM processed_file_content WHERE name = ?""", (filename,))
            processed_data = self.cu.fetchall()
            lower_threshold = self.get_lower_threshold(processed_data)
            indexes = []
            for weight in processed_data:
                if float(weight[0]) >= lower_threshold:
                    indexes.append(processed_data.index(weight))
            data_list = data[0][0].split('.')
            essay = []
            for indx in indexes:
                essay.append(data_list[indx])
            essay_str = '. '.join(essay)
            with open(f"{self.SentenceExtraction_path}/{filename}", "w", encoding='utf-8') as f:
                f.write(essay_str)

    def get_lower_threshold(self, weights):
        sum_weights = 0
        for i in weights:
            num = float(i[0])
            sum_weights += num
        return sum_weights / len(weights)
