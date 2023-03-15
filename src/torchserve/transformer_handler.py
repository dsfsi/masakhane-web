import ast
import json
import logging
import os
from abc import ABC

import torch
import transformers
from captum.attr import LayerIntegratedGradients
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from ts.torch_handler.base_handler import BaseHandler

logger = logging.getLogger(__name__)
logger.info("Transformers version %s", transformers.__version__)


class M2MTranslatorHandler(BaseHandler, ABC):
    """
    Transformer handler for machine translation task using the m2m_100 model.
    """

    def __init__(self):
        super(M2MTranslatorHandler, self).__init__()
        self.initialized = False

    def initialize(self, ctx):
        """In this initialize function, the BERT model is loaded and
        the Layer Integrated Gradients Algorithm for Captum Explanations
        is initialized here.
        Args:
            ctx (context): It is a JSON Object containing information
            pertaining to the model artefacts parameters.
        """
        self.manifest = ctx.manifest
        properties = ctx.system_properties
        model_dir = properties.get("model_dir")
        serialized_file = self.manifest["model"]["serializedFile"]
        model_pt_path = os.path.join(model_dir, serialized_file)

        self.device = torch.device(
            "cuda:" + str(properties.get("gpu_id"))
            if torch.cuda.is_available() and properties.get("gpu_id") is not None
            else "cpu"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)

        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
        self.model.eval()

        logger.info("Transformer model from path %s loaded successfully", model_dir)
        
        self.initialized = True

    def preprocess(self, requests):
        """Basic text preprocessing, based on the user's choice of application mode.
        Args:
            requests (str): The Input data in the form of text is passed on to the preprocess
            function.
        Returns:
            list : The preprocess function returns a list of Tensor for the size of the word tokens.
        """
        input_ids_batch = None
        attention_mask_batch = None
        for idx, data in enumerate(requests):
            input_text = data.get("data")
            if input_text is None:
                input_text = data.get("body")
            if isinstance(input_text, (bytes, bytearray)):
                input_text = input_text.decode("utf-8")
            logger.info("Received text: '%s'", input_text)
        
            inputs = self.tokenizer.encode_plus(
                    input_text,
                    max_length=int(max_length),
                    pad_to_max_length=True,
                    add_special_tokens=True,
                    return_tensors="pt",
                )
            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs["attention_mask"].to(self.device)
            # making a batch out of the recieved requests
            # attention masks are passed for cases where input tokens are padded.
            if input_ids.shape is not None:
                if input_ids_batch is None:
                    input_ids_batch = input_ids
                    attention_mask_batch = attention_mask
                else:
                    input_ids_batch = torch.cat((input_ids_batch, input_ids), 0)
                    attention_mask_batch = torch.cat(
                        (attention_mask_batch, attention_mask), 0
                    )
        return (input_ids_batch, attention_mask_batch)

    def inference(self, input_batch):
        """Predict the class (or classes) of the received text using the
        serialized transformers checkpoint.
        Args:
            input_batch (list): List of Text Tensors from the pre-process function is passed here
        Returns:
            list : It returns a list of the predicted value for the input text
        """
        input_ids_batch, attention_mask_batch = input_batch
        inferences = []
        # todos need to change this to use the generation configuration
        outputs = self.model.generate(
                input_ids_batch, max_length=50, do_sample=True, top_p=0.95, top_k=60
            )
        for i, x in enumerate(outputs):
            inferences.append(self.tokenizer.decode(outputs[i], skip_special_tokens=True))
            logger.info("Generated text: '%s'", inferences)

        logger.info("Generated text", inferences)
        return inferences

    def postprocess(self, inference_output):
        """Post Process Function converts the predicted response into Torchserve readable format.
        Args:
            inference_output (list): It contains the predicted response of the input text.
        Returns:
            (list): Returns a list of the Predictions and Explanations.
        """
        return inference_output

    def get_insights(self, input_batch, text, target):
        """This function initialize and calls the layer integrated gradient to get word importance
        of the input text if captum explanation has been selected through setup_config
        Args:
            input_batch (int): Batches of tokens IDs of text
            text (str): The Text specified in the input request
            target (int): The Target can be set to any acceptable label under the user's discretion.
        Returns:
            (list): Returns a list of importances and words.
        """

        if self.setup_config["captum_explanation"]:
            embedding_layer = getattr(self.model, self.setup_config["embedding_name"])
            embeddings = embedding_layer.embeddings
            self.lig = LayerIntegratedGradients(captum_sequence_forward, embeddings)
        else:
            logger.warning("Captum Explanation is not chosen and will not be available")

        if isinstance(text, (bytes, bytearray)):
            text = text.decode("utf-8")
        text_target = ast.literal_eval(text)

        if not self.setup_config["mode"] == "question_answering":
            text = text_target["text"]
        self.target = text_target["target"]

        input_ids, ref_input_ids, attention_mask = construct_input_ref(
            text, self.tokenizer, self.device, self.setup_config["mode"]
        )
        all_tokens = get_word_token(input_ids, self.tokenizer)
        response = {}
        response["words"] = all_tokens
        return [response]


def construct_input_ref(text, tokenizer, device, mode):
    """For a given text, this function creates token id, reference id and
    attention mask based on encode which is faster for captum insights
    Args:
        text (str): The text specified in the input request
        tokenizer (AutoTokenizer Class Object): To word tokenize the input text
        device (cpu or gpu): Type of the Environment the server runs on.
    Returns:
        input_id(Tensor): It attributes to the tensor of the input tokenized words
        ref_input_ids(Tensor): Ref Input IDs are used as baseline for the attributions
        attention mask() :  The attention mask is a binary tensor indicating the position
         of the padded indices so that the model does not attend to them.
    """

    text_ids = tokenizer.encode(text, add_special_tokens=False)
    # construct input token ids
    logger.info("text_ids %s", text_ids)
    logger.info("[tokenizer.cls_token_id] %s", [tokenizer.cls_token_id])
    input_ids = [tokenizer.cls_token_id] + text_ids + [tokenizer.sep_token_id]
    logger.info("input_ids %s", input_ids)

    input_ids = torch.tensor([input_ids], device=device)
    # construct reference token ids
    ref_input_ids = (
        [tokenizer.cls_token_id]
        + [tokenizer.pad_token_id] * len(text_ids)
        + [tokenizer.sep_token_id]
    )
    ref_input_ids = torch.tensor([ref_input_ids], device=device)
    # construct attention mask
    attention_mask = torch.ones_like(input_ids)
    return input_ids, ref_input_ids, attention_mask


def captum_sequence_forward(inputs, attention_mask=None, position=0, model=None):
    """This function is used to get the predictions from the model and this function
    can be used independent of the type of the BERT Task.
    Args:
        inputs (list): Input for Predictions
        attention_mask (list, optional): The attention mask is a binary tensor indicating the position
         of the padded indices so that the model does not attend to them, it defaults to None.
        position (int, optional): Position depends on the BERT Task.
        model ([type], optional): Name of the model, it defaults to None.
    Returns:
        list: Prediction Outcome
    """
    model.eval()
    model.zero_grad()
    pred = model(inputs, attention_mask=attention_mask)
    pred = pred[position]
    return pred


def summarize_attributions(attributions):
    """Summarises the attribution across multiple runs
    Args:
        attributions ([list): attributions from the Layer Integrated Gradients
    Returns:
        list : Returns the attributions after normalizing them.
    """
    attributions = attributions.sum(dim=-1).squeeze(0)
    attributions = attributions / torch.norm(attributions)
    return attributions


def get_word_token(input_ids, tokenizer):
    """constructs word tokens from token id using the BERT's
    Auto Tokenizer
    Args:
        input_ids (list): Input IDs from construct_input_ref method
        tokenizer (class): The Auto Tokenizer Pre-Trained model object
    Returns:
        (list): Returns the word tokens
    """
    indices = input_ids[0].detach().tolist()
    tokens = tokenizer.convert_ids_to_tokens(indices)
    # Remove unicode space character from BPE Tokeniser
    tokens = [token.replace("Ġ", "") for token in tokens]
    return tokens
