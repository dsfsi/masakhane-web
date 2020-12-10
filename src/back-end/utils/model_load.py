#@title Imports

import os
import re
import yaml
import sacrebleu
import numpy as np
import pandas as pd
import functools
import pyter

import ipdb
# import ipywidgets as widgets
# from IPython.display import display
# from polyglot.text import Text
# from subword_nmt import apply_bpe
# #@title Target language selection

from joeynmt.helpers import load_config

class MasakhaneModelLoader():

  def __init__(self, available_models_file):
    self._model_dir_prefix = 'joeynmt/models/'
    self._src_language = ''
    self.models = self.load_available_models(available_models_file)
  
  def load_available_models(self, available_models_file, 
                            src_language='en', domain='JW300'):
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
        if model['src_language'] != src_language or model['complete'] != 'yes':
          continue
        if model['trg_language'] in models.keys() and model['domain'] != domain:
          continue
        models[model['trg_language']] = model
    print('Found {} Masakhane models.'.format(len(models)))
    self._model_dir_prefix += src_language
    self._src_language = src_language
    return models
  
  def download_model(self, trg_language):
    """ Download model for given trg language. """
    model_dir = "{}-{}".format(self._model_dir_prefix, trg_language)

    if not os.path.exists(model_dir):
        os.system(f'mkdir -p {model_dir}')

    model_files = self.models[trg_language]

    # Download the checkpoint.
    ckpt_path = os.path.join(model_dir, 'model.ckpt')
    if not os.path.exists(ckpt_path):
        self._download(model_files['ckpt'], ckpt_path)
        
    # Download the vocabularies.
    src_vocab_file = model_files['src_vocab']
    trg_vocab_file = model_files['trg_vocab']
    src_vocab_path = os.path.join(model_dir, 'src_vocab.txt')

    if not os.path.exists(src_vocab_path):
        self._download(src_vocab_file, src_vocab_path)

    trg_vocab_path = os.path.join(model_dir, 'trg_vocab.txt')
    if not os.path.exists(src_vocab_path):
        self._download(trg_vocab_file, trg_vocab_path)
    
    # Download the config.
    config_file = model_files['config.yaml']
    config_path = os.path.join(model_dir, 'config_orig.yaml')
    if not os.path.exists(config_path):
        self._download(config_file, config_path)

    # Adjust config.
    config = load_config(config_path)
    new_config_file = os.path.join(model_dir, 'config.yaml')
    config = self._update_config(config, src_vocab_path, trg_vocab_path,
                                 model_dir, ckpt_path)
    with open(new_config_file, 'w') as cfile:
      yaml.dump(config, cfile)

    # Download BPE codes.
    src_bpe_path = os.path.join(model_dir, 'src.bpe.model')
    trg_bpe_path = os.path.join(model_dir, 'trg.bpe.model')

    if not os.path.exists(src_bpe_path) or not os.path.exists(trg_bpe_path):
        self._download(model_files['src_bpe'], src_bpe_path)
        self._download(model_files['trg_bpe'], trg_bpe_path)

    print('Downloaded model for {}-{}.'.format(self._src_language, trg_language))
    return model_dir, config, self._is_lc(src_vocab_path)

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

# import ipywidgets as widgets
# print('Please select a target language.')
# lang_picker = widgets.Dropdown(options=model_loader.models.keys(), value='yo')
# lang_picker

# if __name__=='__main__':
#     available_models_file = '../data/available_models.tsv'
#     model_loader = MasakhaneModelLoader(available_models_file=available_models_file)
