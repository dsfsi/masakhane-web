from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM
from optimum.pipelines import pipeline
from pathlib import Path


class OptimizedM100Model:
    def __init__(self, model_path, src_lang, tgt_lang):
        self._tokenizer = AutoTokenizer.from_pretrained(model_path)
        self._model = ORTModelForSeq2SeqLM.from_pretrained(model_path)
        self.pipeline = pipeline(f"translation_{src_lang}_to_{tgt_lang}", model=self._model, tokenizer=self._tokenizer)

    def predict(self, X):
        output = self.pipeline(X)
        return output
    
    def health_status(self):
        text_to_translate = "Hello, my name is Espoir Murhabazi,  I am a Software Engineer from Congo DRC but living in UK"
        translation = self.predict(text_to_translate)
        assert len(translation) == 1, "health check returning bad translation"
        assert translation[0].get("translation_text") is not None, "health check returning bad translation"
        return translation[0].get("translation_text")
