class Translation:
    def __init__(self, source, target, input, output) -> None:
        super().__init__()
        self.source = source
        self.target = target
        self.input = input
        self.output = output
        self.review = None

    @property
    def data(self):
        return {
            'source': self.source,
            'target': self.target,
            'input': self.input,
            'output': self.output
        }