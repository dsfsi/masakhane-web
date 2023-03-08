from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM
from optimum.pipelines import pipeline
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent.parent.joinpath("onnx", "m2m100_418M_en_swa_rel_news_quantized")


class OptimizedM100Model:
    def __init__(self, model_path=MODEL_PATH, src_lang="en", tgt_lang="sw"):
        print("start loading the model........")
        self._model = ORTModelForSeq2SeqLM.from_pretrained(model_path)
        print("Model loaded successfully!")
        self._tokenizer = AutoTokenizer.from_pretrained(model_path)
        print("Tokenizer loaded successfully")
        self.pipeline = pipeline(f"translation_{src_lang}_to_{tgt_lang}", model=self._model, tokenizer=self._tokenizer)
        print("Pipeline created successfully")
    
    def predict_raw(self, X):
        data_to_translate = X.get("data")
        output = self.pipeline(data_to_translate)
        return output
    
    def health_status(self):
        text_to_translate = {"data": "Hello, my name is Espoir Murhabazi,  I am a Software Engineer from Congo DRC but living in UK"}
        translation = self.predict_raw(text_to_translate)
        assert len(translation) == 1, "health check returning bad translation"
        assert translation[0].get("translation_text") is not None, "health check returning bad translation"
        return translation[0].get("translation_text")
