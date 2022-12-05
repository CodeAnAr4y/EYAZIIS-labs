from UI import *

if __name__ == '__main__':
    x = UI()
    x.create_dbs()
    x.add_to_db_file_content()
    x.add_to_db_processed_file_content()

    x.get_sentences()

    x.keywords_generate_essay()

    x.create_root()
    x.Labels()
    x.Buttons()

    x.run_ui()
