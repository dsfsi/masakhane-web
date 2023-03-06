from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM
from optimum.pipelines import pipeline
from pathlib import Path


class OptimizedM100Model:
    def __init__(self, model_path, src_lang, tgt_lang):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self._model = ORTModelForSeq2SeqLM.from_pretrained(model_path)
        self.pipeline = pipeline(f"translation_{src_lang}_to_{tgt_lang}", model=self.model, tokenizer=self.tokenizer)

    def predict(self, X):
        output = self.pipeline(X)
        return output
