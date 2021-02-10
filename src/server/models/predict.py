import os
import ipdb

import pandas as pd
from subword_nmt import apply_bpe
from polyglot.text import Text
import re

class Predicter():
    def __init__(self):
        pass
        
    def predict_translation(self, source, model_dir, lc):
        new_config_path = os.path.join(model_dir, 'config.yaml')

        # joenmt takes as input a file, so for the moment 
        # I made the code to write the input into a file, ...
        
        path_to_temp = "../../data/temps/"

        src_input_file = 'src_input.bpe.txt'
        src_bpe_path = os.path.join(model_dir, 'src.bpe.model')
        
        # ted_link = 'https://raw.githubusercontent.com/juliakreutzer/masakhane-eval/master/data/multitarget-ted-filt.en.tsv'
        os.system(f'echo {source} > {path_to_temp}input.tsv')
        src_data = SourceData(path_to_temp+'input.tsv', lc, \
                                    bpe_path=src_bpe_path, out_file=path_to_temp+src_input_file)
        sources = src_data.get_sources()
        ted_df = src_data.get_df()
        
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

        return targets[0] if len(targets)>0 else "Nothing"


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