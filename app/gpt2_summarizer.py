from optparse import OptionParser
from summarizer import TransformerSummarizer
import os
import sys

DEFAULT_MIN_LENGTH = 100
DEFAULT_MAX_LENGTH = 3000

def load_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file-path", dest="file_path")
    parser.add_option("--min", "--min-length", dest="min_length")
    parser.add_option("--max", "--max-length", dest="max_length")

    (options, args) = parser.parse_args()

    min_length = int(options.min_length) if options.min_length is not None else DEFAULT_MIN_LENGTH
    max_length = int(options.max_length) if options.max_length is not None else DEFAULT_MAX_LENGTH

    if options.file_path is None or not os.path.isfile(options.file_path):
        sys.stderr.write("Invalid Input\n")
        exit(0x1)

    try:
        if min_length < 0:
            raise ValueError
    except ValueError:
        sys.stderr.write("Invalid Min Length\n")
        exit(0x2)

    try:
        if max_length < 0:
            raise ValueError
    except ValueError:
        sys.stderr.write("Invalid Max Length\n")
        exit(0x3)

    text = load_file_content(options.file_path)

    gpt2_summarizer = TransformerSummarizer(transformer_type="GPT2",
                                            transformer_model_key="gpt2-large"
                                            )

    gpt2_summary = "".join(gpt2_summarizer(text,
                                           min_length=min_length,
                                           max_length=max_length))

    print(gpt2_summary)