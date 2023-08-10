import os
import ipdb
import logging
import re

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




def load_model(model_dir, bpe_src_code=None, tokenize=None):
    """
    Start the bot. This means loading the model according to the config file.

    :param model_dir: Model directory of trained Joey NMT model.
    :param bpe_src_code: BPE codes for source side processing (optional).
    :param tokenize: If True, tokenize inputs with Moses tokenizer.
    :return:
    """
    conf = {}
    cfg_file = model_dir+"/config.yaml"

    logger = logging.getLogger(__name__)
    conf["logger"] = logger
    # load the Joey configuration
    cfg = load_config(cfg_file)

    # load the checkpoint
    if "load_model" in cfg['training'].keys():
        ckpt = cfg['training']["load_model"]
    else:
        ckpt = get_latest_checkpoint(model_dir)
        if ckpt is None:
            raise FileNotFoundError("No checkpoint found in directory {}."
                                    .format(model_dir))

    # prediction parameters from config
    conf["use_cuda"] = cfg["training"].get("use_cuda", False)
    conf["level"] = cfg["data"]["level"]
    conf["max_output_length"] = cfg["training"].get("max_output_length", None)
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
        tokenizer = lambda x: src_tokenizer.tokenize(x, return_str=True)
        detokenizer = lambda x: trg_tokenizer.detokenize(
            x.split(), return_str=True)
    else:
        tokenizer = lambda x: x
        detokenizer = lambda x: x

    if bpe_src_code is not None and level == "bpe":
        # load bpe merge file
        merge_file = open(bpe_src_code, "r")
        bpe = apply_bpe.BPE(codes=merge_file)
        segmenter = lambda x: bpe.process_line(x.strip())
    elif conf["level"] == "char":
        # split to chars
        segmenter = lambda x: list(x.strip())
    else:
        segmenter = lambda x: x.strip()

    conf["preprocess"] = [tokenizer, segmenter]
    conf["postprocess"] = [detokenizer]
    # build model and load parameters into it
    model_checkpoint = load_checkpoint(ckpt, conf["use_cuda"])
    model = build_model(cfg["model"], src_vocab=conf["src_vocab"], trg_vocab=conf["trg_vocab"])
    model.load_state_dict(model_checkpoint["model_state"])

    if conf["use_cuda"]:
        model.cuda()
    conf["model"] = model
    print("Joey NMT model loaded successfully.")
    return conf


class Predicter():
    # def __init__(self):
    #     pass

    def translate(self, message_text, model, src_vocab, trg_vocab, preprocess, postprocess,
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
          use_cuda=use_cuda, beam_size=beam_size,
          beam_alpha=beam_alpha, n_gpu=0)

      #  validate_on_data(model: Model, data: Dataset,
      #                batch_size: int,
      #                use_cuda: bool, max_output_length: int,
      #                level: str, eval_metric: Optional[str],
      #                n_gpu: int,
      #                batch_class: Batch = Batch,
      #                compute_loss: bool = False,
      #                beam_size: int = 1, beam_alpha: int = -1,
      #                batch_type: str = "sentence",
      #                postprocess: bool = True,
      #                bpe_type: str = "subword-nmt",
      #                sacrebleu: dict = None) \

      # post-process
      if level == "char":
          response = "".join(hypotheses)
      else:
          response = " ".join(hypotheses)

      for p in postprocess:
          response = p(response)

      return response

        
    def predict_translation(self, source, model_dir, lc):
        new_config_path = os.path.join(model_dir, 'config.yaml')

        # joenmt takes as input a file, so for the moment 
        # I made the code to write the input into a file, ...
        
        if not os.path.exists(current_app.config['TEMP']):
          os.mkdir(current_app.config['TEMP'])

        path_to_temp = current_app.config['TEMP']

        # if not os.path.exists("../../data/temps/"):
        #       os.mkdir("../../data/temps/")
        # path_to_temp = "../../data/temps/"

        if not os.path.exists(path_to_temp):
              os.mkdir(path_to_temp)
              

        src_input_file = 'src_input.bpe.txt'
        # src_bpe_path = os.path.join(model_dir, 'src.bpe.model')
        
        # ted_link = 'https://raw.githubusercontent.com/juliakreutzer/masakhane-eval/master/data/multitarget-ted-filt.en.tsv'
        os.system(f'echo {source} > {path_to_temp}input.tsv')
        # src_data = SourceData(path_to_temp+'input.tsv', lc, \
        #                             bpe_path=src_bpe_path, out_file=path_to_temp+src_input_file)
        # sources = src_data.get_sources()
        # ted_df = src_data.get_df()
        
        os.system(f"sed 's/@@ //g' {path_to_temp}{src_input_file} > {path_to_temp}src_input.txt")

        # os.system(f'echo {source} > input.txt')        
        os.system(f'python -m joeynmt translate {new_config_path} < {path_to_temp}src_input.txt > {path_to_temp}trg_output_file')

        targets = post_process(path_to_temp+'trg_output_file', lc)
# 
        # with open('output.txt', 'r') as file:
        #     output = file.read().replace('\n', '')

        # with open('trg_output_file', 'r') as file:
        #     output = file.read().replace('\n', '')

        # return output

        return targets[0] if len(targets)>0 else ""


class SourceData():
  def __init__(self, data_link, lc, bpe_path, out_file):
    self._src_df = pd.read_csv(data_link, sep='\t', header=None,
                               names=['source'])
    print("Loaded {} lines.".format(len(self._src_df)))
    self._bpe_model = self.load_bpe(bpe_path)
    self._src_df, self._sources = self.preprocess(out_file, lc)
    self.lc = lc
  
  def get_df(self):
    return self._src_df
  
  def get_sources(self):
    return self._sources

  def preprocess(self, out_file, lc):
    """Tokenize, (lowercase,) sub-word split.
    
    Using Polyglot since it was used for JW300.
    Preprocess the source column of a dataframe object and write to file.
  
    Pipeline:
    - tokenize
    - split into sub-words

    Append pre-processed sources to dataframe."""
    tokenized_sentences = []
    bped_sentences = []
    sources = []
    with open(out_file, 'w') as ofile:
      for i, row in self._src_df.iterrows():
        sentence_i = Text(row[0]).sentences[0]
        tokenized_sentence = ""
        bped_sentence = ""
        tokenized = " ".join(sentence_i.words)
        sources.append(str(sentence_i))
        if lc:
          tokenized = tokenized.lower()
        tokenized_sentence = tokenized
        bped = self._bpe_model.process_line(tokenized)
        bped_sentence = bped
        ofile.write("{}\n".format(bped))
        tokenized_sentences.append(tokenized_sentence)
        bped_sentences.append(bped_sentence)
    data = self._src_df.assign(
        tokenized_sentences=tokenized_sentences)
    data = data.assign(
        bped_sentences=bped_sentences)
    return data, sources

  def load_bpe(self, bpe_path):
    with open(bpe_path, 'r') as ofile:
      bpe_model = apply_bpe.BPE(codes=ofile)
    return bpe_model
  
# Post-processing
def post_process(output_file, lc):
  """Load and detokenize translations.
  
  There is no given Polyglot detokenizer, so we do it by heuristics.
  """
  targets = []
  with open(output_file, 'r') as ofile:
    for line in ofile:
      sent = line.strip()
      sent = sent.replace('<pad>', '')
      sent = re.sub(r'\s+([?.!"-,:’])', r'\1', sent)
      sent = sent.replace('( ', '(').replace(' - ', '-').replace(' / ', '/').replace(' /', '/')
      if lc:
        # Cheap casing restoration... only first character but better than nothing.
        sent = sent[0].upper() + sent[1:]
      targets.append(sent)
  return targets