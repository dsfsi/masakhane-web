from torchtext import data
from torchtext.datasets import TranslationDataset


from joeynmt.constants import UNK_TOKEN, EOS_TOKEN, BOS_TOKEN, PAD_TOKEN


class MonoLineDataset(TranslationDataset):
    def __init__(self, line, field, **kwargs):
        examples = []
        line = line.strip()
        fields = [('src', field)]
        examples.append(data.Example.fromlist([line], fields))
        super(TranslationDataset, self).__init__(examples, fields, **kwargs)


def load_line_as_data(line, level, lowercase, src_vocab, trg_vocab):
    """
    Create a data set from one line.
    Workaround for the usual torchtext data handling.

    :param line: The input line to process.
    :param level: "char", "bpe" or "word". Determines segmentation of the input.
    :param lowercase: If True, lowercases inputs and outputs.
    :param src_vocab: Path to source vocabulary.
    :param trg_vocab: Path to target vocabulary.
    :return:
    """
    if level == "char":
        tok_fun = lambda s: list(s)
    else:  
        # bpe or word, pre-tokenized
        tok_fun = lambda s: s.split()

    src_field = data.Field(init_token=None, eos_token=EOS_TOKEN,  
                           pad_token=PAD_TOKEN, tokenize=tok_fun,
                           batch_first=True, lower=lowercase,
                           unk_token=UNK_TOKEN,
                           include_lengths=True)
    trg_field = data.Field(init_token=BOS_TOKEN, eos_token=EOS_TOKEN,
                           pad_token=PAD_TOKEN, tokenize=tok_fun,
                           unk_token=UNK_TOKEN,
                           batch_first=True, lower=lowercase,
                           include_lengths=True)
    test_data = MonoLineDataset(line=line, field=(src_field))
    src_field.vocab = src_vocab
    trg_field.vocab = trg_vocab
    return test_data, src_vocab, trg_vocab