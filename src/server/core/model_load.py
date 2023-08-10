import os, yaml, logging, re, ipdb
# external imports
import torch
from joeynmt.helpers import load_config
from subword_nmt import apply_bpe
from subword_nmt import apply_bpe
from sacremoses import MosesTokenizer, MosesDetokenizer
from joeynmt.helpers import load_config, get_latest_checkpoint, \
    load_checkpoint
from joeynmt.vocabulary import build_vocab
from joeynmt.model import build_model
from joeynmt.prediction import validate_on_data
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

# internal imports
from core.utils import load_line_as_data

class MasakhaneModelLoader():
    """User Defined Class to manage the download of machine trasnlation models"""
    def __init__(self, available_models_file):
        # model directory to store the modeks
        self._model_dir_prefix = os.environ.get('MODEL',
                                                "./models/joeynmt/")
        self._src_language = ''
        #load availiable models into memory
        self.models = self.load_available_models(available_models_file)

    def load_available_models(self, available_models_file):
        """Load a dictonary with available models to download"""
        models = {}
        with open(available_models_file, 'r') as ofile:
            # iterate over file entries
            for i, line in enumerate(ofile):
                entries = line.strip().split("\t")
                # extract headers
                if i == 0:
                    header_keys = [h.__str__() for h in entries]
                    continue
                
                # build available model dictionary from the headers & entries:
                # https://www.geeksforgeeks.org/python-dictionary-comprehension/
                model = {key:value for key,value in zip(header_keys, entries)}
                # don't add incomplete models
                if model['complete'] != 'yes':
                    continue
    
                models[f"{model['src_language']}-{model['tgt_language']}-{model['domain']}"] = model

        print('Found {} Masakhane models.'.format(len(models)))

        return models

    def download_model(self, src_language, tgt_language, domain):
        """ Download model for given trg language. """
        model_dir = f"{self._model_dir_prefix}{src_language}-{tgt_language}-{domain}"

        print("Inside download")
        if not os.path.exists(model_dir):
            print(f"{model_dir} doesn't exist")
            os.system(f'mkdir -p {model_dir}')
        print(f"{model_dir} exist")
        
        model_files = self.models[f"{src_language}-{tgt_language}-{domain}"]

        # Check if files exist
        ckpt_path = os.path.join(model_dir, 'model.ckpt')
        src_vocab_path = os.path.join(model_dir, 'src_vocab.txt')
        trg_vocab_path = os.path.join(model_dir, 'trg_vocab.txt')
        config_path = os.path.join(model_dir, 'config_orig.yaml')
        # config_path = os.path.join(model_dir, 'config.yaml')
        src_bpe_path = os.path.join(model_dir, 'src.bpe.model')
        trg_bpe_path = os.path.join(model_dir, 'trg.bpe.model')

        if not os.path.exists in [ckpt_path, src_vocab_path, trg_vocab_path, config_path, src_bpe_path, trg_bpe_path]:
            URL = "https://zenodo.org/record/7636723/files/" + \
                src_language + "-" + tgt_language
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
        
        print('Downloaded model for {}-{}.'.format(src_language, tgt_language))

    def load_model(self, src_language, tgt_language, domain, bpe_src_code=None, tokenize=None):
        """ Load model for given trg language. """
        model_dir = f"{self._model_dir_prefix}{src_language}-{tgt_language}-{domain}"

        ckpt_path = os.path.join(model_dir, 'model.ckpt')
        src_vocab_path = os.path.join(model_dir, 'src_vocab.txt')
        trg_vocab_path = os.path.join(model_dir, 'trg_vocab.txt')
        config_path = os.path.join(model_dir, 'config_orig.yaml')
        # config_path = os.path.join(model_dir, 'config.yaml')
        # Adjust config.
        config = load_config(config_path)
        new_config_file = os.path.join(model_dir, 'config.yaml')
        config = self._update_config(config, src_vocab_path, trg_vocab_path,
                                     model_dir, ckpt_path)
        with open(new_config_file, 'w') as cfile:
            yaml.dump(config, cfile)

        print('Loaded model for {}-{}.'.format(src_language, tgt_language))

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
        if conf["use_cuda"]:
            model.cuda()
        conf["model"] = model
        print("Joey NMT model loaded successfully.")
        
        return conf

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

    def _is_lowercase(self, src_vocab_path):
        # Infer whether the model is built on lowercased data.
        lowercase = True
        with open(src_vocab_path, 'r') as ofile:
            for line in ofile:
                if line != line.lower():
                    lowercase = False
                    break
        return lowercase

# Doesn't look like these functions are ever called... 

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

