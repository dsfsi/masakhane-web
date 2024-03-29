import json
import os
import sys
from pathlib import Path
import torch
import transformers
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoModelForQuestionAnswering,
    AutoModelForSequenceClassification,
    AutoModelForTokenClassification,
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    set_seed,
)

print("Transformers version", transformers.__version__)
set_seed(1)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def transformers_model_downloader(
    mode, pretrained_model_name, num_labels, do_lower_case, max_length, torchscript
):
    """This function, save the checkpoint, config file along with tokenizer config and vocab files
    of a transformer model of your choice.
    """
    print("Download model and tokenizer", pretrained_model_name)
    # loading pre-trained model and tokenizer
    if mode == "sequence_classification":
        config = AutoConfig.from_pretrained(
            pretrained_model_name, num_labels=num_labels, torchscript=torchscript
        )
        model = AutoModelForSequenceClassification.from_pretrained(
            pretrained_model_name, config=config
        )
        tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name, do_lower_case=do_lower_case
        )
    elif mode == "question_answering":
        config = AutoConfig.from_pretrained(
            pretrained_model_name, torchscript=torchscript
        )
        model = AutoModelForQuestionAnswering.from_pretrained(
            pretrained_model_name, config=config
        )
        tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name, do_lower_case=do_lower_case
        )
    elif mode == "token_classification":
        config = AutoConfig.from_pretrained(
            pretrained_model_name, num_labels=num_labels, torchscript=torchscript
        )
        model = AutoModelForTokenClassification.from_pretrained(
            pretrained_model_name, config=config
        )
        tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name, do_lower_case=do_lower_case
        )
    elif mode == "text_generation":
        config = AutoConfig.from_pretrained(
            pretrained_model_name, num_labels=num_labels, torchscript=torchscript
        )
        model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name, config=config
        )
        tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name, do_lower_case=do_lower_case
        )
    elif mode == "translation":
        # new mode create to handle the masakhane translation models
        tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(pretrained_model_name)

        # NOTE : for demonstration purposes, we do not go through the fine-tune processing here.
        # A Fine_tunining process based on your needs can be added.
        # An example of  Fine_tuned model has been provided in the README.

    NEW_DIR = Path(__file__).parent.joinpath("transformer_models", pretrained_model_name)
    NEW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Successfully created directory {NEW_DIR.__str__()} ")

    print(
        "Save model and tokenizer/ Torchscript model based on the setting from setup_config",
        pretrained_model_name,
        "in directory",
        NEW_DIR,
    )
    if save_mode == "pretrained":
        model.save_pretrained(NEW_DIR)
        tokenizer.save_pretrained(NEW_DIR)
    elif save_mode == "torchscript":
        dummy_input = "This is a dummy input for torch jit trace"
        inputs = tokenizer.encode_plus(
            dummy_input,
            max_length=int(max_length),
            pad_to_max_length=True,
            add_special_tokens=True,
            return_tensors="pt",
        )
        input_ids = inputs["input_ids"].to(device)
        attention_mask = inputs["attention_mask"].to(device)
        model.to(device).eval()
        traced_model = torch.jit.trace(model, (input_ids, attention_mask))
        torch.jit.save(traced_model, os.path.join(NEW_DIR, "traced_model.pt"))
    return


if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    if len(sys.argv) > 1:
        filename = os.path.join(dirname, sys.argv[1])
    else:
        filename = os.path.join(dirname, "setup_config.json")
    f = open(filename)
    settings = json.load(f)
    mode = settings["mode"]
    model_name = settings["model_name"]
    num_labels = int(settings["num_labels"])
    do_lower_case = settings["do_lower_case"]
    max_length = settings["max_length"]
    save_mode = settings["save_mode"]
    if save_mode == "torchscript":
        torchscript = True
    else:
        torchscript = False

    transformers_model_downloader(
        mode, model_name, num_labels, do_lower_case, max_length, torchscript
    )
