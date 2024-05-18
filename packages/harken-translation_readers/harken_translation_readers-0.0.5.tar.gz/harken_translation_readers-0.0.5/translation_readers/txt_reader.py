import structlog

logger = structlog.getLogger(__name__)

from translation_readers.reader import Reader
from languages.languages import detect_language_code, ISO_639_2


class TextReader(Reader):

    def __init__(self, input_path, src_lang, tgt_lang, **kwargs):
        super().__init__(input_path, src_lang, tgt_lang, **kwargs)
        self.separator = kwargs.get('separator', "|||")
        self.is_binary = False
        self.patience = kwargs.get('patience', 100)
        self.idx_tgt = -1
        self.idx_src = -1

    def parse_data(self):
        try:
            with open(self.input_path, 'r') as reader:
                reader.readline()
        except:
            self.is_binary = True

        with open(self.input_path, 'rb') if self.is_binary else open(self.input_path, 'r') as reader:
            for idx, line in enumerate(reader):
                line = line.decode().strip() if self.is_binary else line.strip()
                if idx == 0:
                    cols = len(line.split(self.separator))
                    self.idx_tgt = cols - 1
                    self.idx_src = cols - 2
                parts = line.split(self.separator)
                lang_1 = detect_language_code(parts[self.idx_src], iso=ISO_639_2)
                lang_2 = detect_language_code(parts[self.idx_tgt], iso=ISO_639_2)
                if (lang_1 == self.src_lang and lang_2 == self.tgt_lang) or (
                        lang_1 == self.tgt_lang and lang_2 == self.src_lang):
                    break
                self.patience -= 1
                if self.patience <= 0:
                    raise Exception("Please review the pair of languages")

    def get_data(self):
        with open(self.input_path, 'rb') if self.is_binary else open(self.input_path, 'r') as reader:
            for line in reader:
                parts = line.decode().strip().split(self.separator) \
                    if self.is_binary else line.strip().split(self.separator)
                yield parts[self.idx_src], parts[self.idx_tgt]


__all__ = ["TextReader"]
