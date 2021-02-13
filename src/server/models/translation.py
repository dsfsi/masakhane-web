class Translation:
    def __init__(self, src_lang, tgt_lang, input, output) -> None:
        super().__init__()
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.input = input
        self.output = output

    @property
    def data(self):
        return {
            'src_lang': self.src_lang,
            'tgt_lang': self.tgt_lang,
            'input': self.input,
            'output': self.output
        }