import pyximport
pyximport.install()
from wrapper.Process import Process
from wrapper.core.File import File
from wrapper.core.Image import *
from wrapper.core.DocumentSearch import DocumentSearch
from wrapper.infra.DocLanguage import DocLanguage
from wrapper.core.SentenceTransformerVectorizer import SentenceTransformerVectorizer
import traceback
from LogTest import LogTest
import pytest
import os
import logging
logtest = LogTest('./tests/logs/docrx.log', __name__)
# logger = logtest.logger

class TestProcessPDFImage:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        logging.info('Setting up test')        
        self.base_path = "./tests/media"
        self.files = ['res/onus/pag1.pdf', 'res/onus/pag2.pdf', 'res/onus/pag3.pdf', 'res/docs_with_img/pdf_img.pdf']
        trained_data = self.base_path + '/trained_data'        
        Process.load(trained_data)

    def test_vectorizer(self):
        try:
            p = Process(self.base_path, True, DocLanguage.PORTUGUESE, None)
            file = p.compile_doc('res/onus/pag1.pdf', 'res/onus/pag1.pdf')
            assert file and file.text
            logging.info('Extracted text: ' + file.extracted_text)
            logging.info('File translated text: ' + file.text)
            logging.info('sentences from text:')
            for index, s in enumerate(file.sentences):
                logging.info(f'Sentence number {index}.Text: {s}')
                vectorizer = SentenceTransformerVectorizer.instance(self.base_path, DocLanguage.PORTUGUESE)
                vector = vectorizer.encode(s)
                if vector is not None:
                    assert True
                else:
                    assert False
                logging.info(f'vectorized sentence: {vector}')            
            
            logging.info(f'Language detected {file.detected_language} translate to {file.translate_to}')
        except:
            logging.error(traceback.format_exc())
            assert False

    # def test_search_on_file_by_sb(self):
    #     logging.info('test_search_on_file_by_sb')
    #     try:
    #         p = Process.create_online_pipeline_multilingual(self.base_path)
    #         file = p.compile_and_train('res/onus/pag1.pdf', 'res/onus/pag1.pdf')
    #         assert file and file.text
    #         logging.info('File text: ' + file.text)
    #         logging.info('searching for: "Tereza Almeida"')
    #         query, result = p.search("tereza almeida", page=1, results_per_page=10)
    #         assert query and result
    #         logging.info('Query: ' + query)
    #         logging.info('Result: ')
    #         logging.info(result)
    #         query = "206.424-ES"
    #         logging.info(f'searching for: {query}')
    #         query, result = p.search(query, DocLanguage.PORTUGUESE, page=1, results_per_page=10)
    #         assert query and result
    #         logging.info('Query: ' + query)
    #         logging.info('Result: ')
    #         logging.info(result)
    #     except:
    #         logging.error(traceback.format_exc())
    #         assert False