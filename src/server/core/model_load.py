# @title Imports
import os
import yaml
import logging
import torch
import ipdb

# from flask import current_app
from joeynmt.helpers import load_config
# from utils.upload_download import
import pandas as pd
from subword_nmt import apply_bpe
from polyglot.text import Text
from flask import current_app
from subword_nmt import apply_bpe
from sacremoses import MosesTokenizer, MosesDetokenizer
from core.utils import load_line_as_data
from joeynmt.helpers import load_config, get_latest_checkpoint, \
    load_checkpoint
from joeynmt.vocabulary import build_vocab
from joeynmt.model import build_model
from joeynmt.prediction import validate_on_data
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile


class MasakhaneModelLoader():

    def __init__(self, available_models_file):
        # self._model_dir_prefix = current_app.config['MODEL']
        self._model_dir_prefix = os.environ.get('MODEL',
                                                "./models/joeynmt/")
        self._src_language = ''
        self.models = self.load_available_models(available_models_file)

    def load_available_models(self, available_models_file):
        # Get list of available models.
        # If multiple models: select domain.
        # Only select relevant models with correct src language.
        models = {}
        with open(available_models_file, 'r') as ofile:
            for i, line in enumerate(ofile):
                entries = line.strip().split("\t")

                if i == 0:
                    headers = entries
                    header_keys = [h.__str__() for h in headers]
                    continue

                model = {h: v for h, v in zip(header_keys, entries)}

                if model['complete'] != 'yes':
                    continue

                # if model['trg_language'] in models.keys() and model['domain'] != domain:
                #   continue

                models[f"{model['src_language']}-{model['trg_language']}-{model['domain']}"] = model

        print('Found {} Masakhane models.'.format(len(models)))

        # self._model_dir_prefix += src_language
        # self._src_language = src_language

        # ipdb.set_trace()
        return models

    def download_model(self, src_language, trg_language, domain):
        """ Download model for given trg language. """
        # ipdb.set_trace()
        model_dir = f"{self._model_dir_prefix}{src_language}-{trg_language}-{domain}"

        if not os.path.exists(model_dir):
            os.system(f'mkdir -p {model_dir}')

        # print(self.models)
        # ipdb.set_trace()
        model_files = self.models[f"{src_language}-{trg_language}-{domain}"]

        # Check if files exist
        ckpt_path = os.path.join(model_dir, 'model.ckpt')
        src_vocab_path = os.path.join(model_dir, 'src_vocab.txt')
        trg_vocab_path = os.path.join(model_dir, 'trg_vocab.txt')
        config_path = os.path.join(model_dir, 'config_orig.yaml')
        src_bpe_path = os.path.join(model_dir, 'src.bpe.model')
        trg_bpe_path = os.path.join(model_dir, 'trg.bpe.model')

        if not os.path.exists(ckpt_path) or not os.path.exists(src_vocab_path) or not os.path.exists(trg_vocab_path) or not os.path.exists(config_path) or not os.path.exists(src_bpe_path) or not os.path.exists(trg_bpe_path):
            URL = "https://zenodo.org/record/7417644/files/" + \
                src_language + "-" + trg_language
            if domain == "":
                URL += "-baseline.zip?download=1"
            else:
                URL += "-" + domain + "-baseline.zip?download=1"

            http_response = urlopen(URL)
            zipfile = ZipFile(BytesIO(http_response.read()))
            zipfile.extractall(path=model_dir)        

        # Rename config file to config_orig.yaml.
        os.rename(os.path.join(model_dir, 'config.yaml'), config_path)

        # Adjust config.
        config = load_config(config_path)
        new_config_file = os.path.join(model_dir, 'config.yaml')
        config = self._update_config(config, src_vocab_path, trg_vocab_path,
                                     model_dir, ckpt_path)
        with open(new_config_file, 'w') as cfile:
            yaml.dump(config, cfile)

        # # Download the checkpoint.
        # ckpt_path = os.path.join(model_dir, 'model.ckpt')
        # if not os.path.exists(ckpt_path):
        #     self._download(model_files['ckpt'], ckpt_path)

        # # Download the vocabularies.
        # src_vocab_file = model_files['src_vocab']
        # trg_vocab_file = model_files['trg_vocab']
        # src_vocab_path = os.path.join(model_dir, 'src_vocab.txt')

        # if not os.path.exists(src_vocab_path):
        #     self._download(src_vocab_file, src_vocab_path)

        # trg_vocab_path = os.path.join(model_dir, 'trg_vocab.txt')
        # if not os.path.exists(trg_vocab_path):
        #     self._download(trg_vocab_file, trg_vocab_path)

        # # Download the config.
        # config_file = model_files['config.yaml']
        # config_path = os.path.join(model_dir, 'config_orig.yaml')
        # if not os.path.exists(config_path):
        #     self._download(config_file, config_path)

        # # Adjust config.
        # config = load_config(config_path)
        # new_config_file = os.path.join(model_dir, 'config.yaml')
        # config = self._update_config(config, src_vocab_path, trg_vocab_path,
        #                              model_dir, ckpt_path)
        # with open(new_config_file, 'w') as cfile:
        #     yaml.dump(config, cfile)

        # # Download BPE codes.
        # src_bpe_path = os.path.join(model_dir, 'src.bpe.model')
        # trg_bpe_path = os.path.join(model_dir, 'trg.bpe.model')

        # if not os.path.exists(src_bpe_path) or not os.path.exists(trg_bpe_path):
        #     self._download(model_files['src_bpe'], src_bpe_path)
        #     self._download(model_files['trg_bpe'], trg_bpe_path)

        # print('Downloaded model for {}-{}.'.format(self._src_language, trg_language))
        print('Downloaded model for {}-{}.'.format(src_language, trg_language))
        # return model_dir, config, self._is_lc(src_vocab_path)
        # return

    def load_model(self, src_language, trg_language, domain, bpe_src_code=None, tokenize=None):
        """ Load model for given trg language. """
        # model_dir = "{}-{}".format(self._model_dir_prefix, trg_language)
        model_dir = f"{self._model_dir_prefix}{src_language}-{trg_language}-{domain}"

        # Load the checkpoint.
        ckpt_path = os.path.join(model_dir, 'model.ckpt')

        # Load the vocabularies.
        src_vocab_path = os.path.join(model_dir, 'src_vocab.txt')

        trg_vocab_path = os.path.join(model_dir, 'trg_vocab.txt')

        # Load the config.
        config_path = os.path.join(model_dir, 'config_orig.yaml')

        # Adjust config.
        config = load_config(config_path)
        new_config_file = os.path.join(model_dir, 'config.yaml')
        config = self._update_config(config, src_vocab_path, trg_vocab_path,
                                     model_dir, ckpt_path)
        with open(new_config_file, 'w') as cfile:
            yaml.dump(config, cfile)

        # print('Loaded model for {}-{}.'.format(self._src_language, trg_language))
        print('Loaded model for {}-{}.'.format(src_language, trg_language))

        conf = {}

        logger = logging.getLogger(__name__)
        conf["logger"] = logger

        # load the Joey configuration
        cfg = load_config(new_config_file)

        # load the checkpoint
        if "load_model" in cfg['training'].keys():
            ckpt = cfg['training']["load_model"]
        else:
            ckpt = get_latest_checkpoint(model_dir)
            if ckpt is None:
                raise FileNotFoundError("No checkpoint found in directory {}."
                                        .format(model_dir))

        # prediction parameters from config
        conf["use_cuda"] = cfg["training"].get(
            "use_cuda", False) if torch.cuda.is_available() else False

        conf["level"] = cfg["data"]["level"]
        conf["max_output_length"] = cfg["training"].get(
            "max_output_length", None)
        conf["lowercase"] = cfg["data"].get("lowercase", False)

        # load the vocabularies
        src_vocab_file = cfg["training"]["model_dir"] + "/src_vocab.txt"
        trg_vocab_file = cfg["training"]["model_dir"] + "/trg_vocab.txt"

        conf["src_vocab"] = build_vocab(field="src", vocab_file=src_vocab_file,
                                        dataset=None, max_size=-1, min_freq=0)
        conf["trg_vocab"] = build_vocab(field="trg", vocab_file=trg_vocab_file,
                                        dataset=None, max_size=-1, min_freq=0)

        # whether to use beam search for decoding, 0: greedy decoding
        if "testing" in cfg.keys():
            conf["beam_size"] = cfg["testing"].get("beam_size", 0)
            conf["beam_alpha"] = cfg["testing"].get("alpha", -1)
        else:
            conf["beam_size"] = 1
            conf["beam_alpha"] = -1

        # pre-processing
        if tokenize is not None:
            src_tokenizer = MosesTokenizer(lang=cfg["data"]["src"])
            trg_tokenizer = MosesDetokenizer(lang=cfg["data"]["trg"])
            # tokenize input
            def tokenizer(x): return src_tokenizer.tokenize(x, return_str=True)
            def detokenizer(x): return trg_tokenizer.detokenize(
                x.split(), return_str=True)
        else:
            def tokenizer(x): return x
            def detokenizer(x): return x

        if bpe_src_code is not None and level == "bpe":
            # load bpe merge file
            merge_file = open(bpe_src_code, "r")
            bpe = apply_bpe.BPE(codes=merge_file)
            def segmenter(x): return bpe.process_line(x.strip())
        elif conf["level"] == "char":
            # split to chars
            def segmenter(x): return list(x.strip())
        else:
            def segmenter(x): return x.strip()

        conf["preprocess"] = [tokenizer, segmenter]
        conf["postprocess"] = [detokenizer]
        # build model and load parameters into it
        model_checkpoint = load_checkpoint(ckpt, conf["use_cuda"])
        model = build_model(
            cfg["model"], src_vocab=conf["src_vocab"], trg_vocab=conf["trg_vocab"])
        model.load_state_dict(model_checkpoint["model_state"])
        # ipdb.set_trace()
        if conf["use_cuda"]:
            model.cuda()
        conf["model"] = model
        print("Joey NMT model loaded successfully.")
        return conf

        # return model_dir, config, self._is_lc(src_vocab_path)

    def translate(message_text, model, src_vocab, trg_vocab, preprocess, postprocess,
                  logger, beam_size, beam_alpha, level, lowercase,
                  max_output_length, use_cuda):
        """
        Describes how to translate a text message.

        :param message_text: Slack command, could be text.
        :param model: The Joey NMT model.
        :param src_vocab: Source vocabulary.
        :param trg_vocab: Target vocabulary.
        :param preprocess: Preprocessing pipeline (a list).
        :param postprocess: Postprocessing pipeline (a list).
        :param beam_size: Beam size for decoding.
        :param beam_alpha: Beam alpha for decoding.
        :param level: Segmentation level.
        :param lowercase: Lowercasing.
        :param max_output_length: Maximum output length.
        :param use_cuda: Using CUDA or not.
        :return:
        """
        sentence = message_text.strip()
        # remove emojis
        emoji_pattern = re.compile("\:[a-zA-Z]+\:")
        sentence = re.sub(emoji_pattern, "", sentence)
        sentence = sentence.strip()
        if lowercase:
            sentence = sentence.lower()
        for p in preprocess:
            sentence = p(sentence)

        # load the data which consists only of this sentence
        test_data, src_vocab, trg_vocab = load_line_as_data(lowercase=lowercase,
                                                            line=sentence, src_vocab=src_vocab, trg_vocab=trg_vocab, level=level)

        # generate outputs
        score, loss, ppl, sources, sources_raw, references, hypotheses, \
            hypotheses_raw, attention_scores = validate_on_data(
                model, data=test_data, batch_size=1, level=level,
                max_output_length=max_output_length, eval_metric=None,
                use_cuda=use_cuda, loss_function=None, beam_size=beam_size,
                beam_alpha=beam_alpha, logger=logger)

        # post-process
        if level == "char":
            response = "".join(hypotheses)
        else:
            response = " ".join(hypotheses)

        for p in postprocess:
            response = p(response)

        return response

    def _update_config(self, config, new_src_vocab_path, new_trg_vocab_path,
                       new_model_dir, new_ckpt_path):
        """Overwrite the settings in the given config."""
        config['data']['src_vocab'] = new_src_vocab_path
        if config['model'].get('tied_embeddings', False):
            config['data']['trg_vocab'] = new_src_vocab_path
        else:
            config['data']['trg_vocab'] = new_trg_vocab_path
        config['training']['model_dir'] = new_model_dir
        config['training']['load_model'] = new_ckpt_path
        return config

    def _is_lc(self, src_vocab_path):
        # Infer whether the model is built on lowercased data.
        lc = True
        with open(src_vocab_path, 'r') as ofile:
            for line in ofile:
                if line != line.lower():
                    lc = False
                    break
        return lc

    def _download_gdrive_file(self, file_id, destination):
        """Download a file from Google Drive and store in local file."""
        download_link = 'https://drive.google.com/uc?id={}'.format(file_id)
        os.system(f'gdown -q -O {destination} {download_link}')

    def _download_github_file(self, github_raw_path, destination):
        """Download a file from GitHub."""
        os.system(f'wget -q -O {destination} {github_raw_path}')

    def _download(self, url, destination):
        """Download file from Github or Googledrive."""
        try:
            if 'drive.google.com' in url:
                if url.startswith('https://drive.google.com/file'):
                    file_id = url.split("/")[-1]
                elif url.startswith('https://drive.google.com/open?'):
                    file_id = url.split('id=')[-1]
                self._download_gdrive_file(file_id, destination)
            else:
                self._download_github_file(url, destination)
        except:
            print("Download failed, didn't recognize url {}.".format(url))

# if __name__=='__main__':
#     available_models_file = '../data/available_models.tsv'
#     model_loader = MasakhaneModelLoader(available_models_file=available_models_file)
