# PDF Word Frequency Analyzer

**A Python command-line tool for extracting, normalizing, filtering, and visualizing English vocabulary from text-based PDF documents.**

The tool is useful for language study and document exploration. It extracts PDF text, applies part-of-speech-aware lemmatization, separates user-known words from unknown vocabulary, and produces CSV reports and word-cloud images.

## Engineering highlights

- Page-by-page text extraction with `pdfplumber`
- NLTK token filtering, POS tagging, WordNet lemmatization, and morphology fallback
- User-supplied known-word lists
- Filtering for stopwords, short tokens, digits, and Roman numerals
- Frequency reports for all, known, and unknown words
- Word-cloud generation
- Progress reporting for page extraction and lemmatization
- Configurable top-N size and output directory
- Input validation and clear exit behavior

## Technology

`Python` · `pdfplumber` · `NLTK` · `WordNet` · `WordCloud` · `tqdm` · `CSV`

## Processing pipeline

```text
Text-based PDF
      │
      ▼
Page text extraction
      │
      ▼
Token cleanup and filtering
      │
      ▼
POS tagging and lemmatization
      │
      ├── known-word matches
      └── unknown vocabulary
      │
      ▼
CSV frequency reports and word clouds
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Analyze a PDF:

```bash
python main.py path/to/document.pdf
```

Analyze the top 500 words while excluding a personal vocabulary list:

```bash
python main.py path/to/document.pdf \
  --num_top_words 500 \
  --known_words_file data/known_words.txt
```

Use a custom output directory:

```bash
python main.py path/to/document.pdf \
  --output_dir outputs/document-analysis
```

## CLI reference

```text
python main.py PDF_PATH [options]
```

| Option | Description | Default |
| --- | --- | --- |
| `PDF_PATH` | Path to a text-based PDF | required |
| `-n`, `--num_top_words` | Number of high-frequency words used in top-N reports and images | `100` |
| `-k`, `--known_words_file` | Text file containing one known word per line | empty set |
| `-o`, `--output_dir` | Output directory | `results/<pdf-name>/` |

## Known-word file

Create a UTF-8 text file with one word per line:

```text
analysis
architecture
configuration
reliable
```

Words are normalized before comparison, so common inflected forms may map to the same lemma.

## Outputs

```text
results/<pdf-name>/
├── top<N>_unknown_words.csv
├── wordcloud_top<N>_unknown_words.png
├── excluded_known_words.csv
├── all_words.csv
└── wordcloud_top<N>_all_words.png
```

### Report meaning

- `top<N>_unknown_words.csv`: most frequent vocabulary not found in the known-word list
- `excluded_known_words.csv`: known words that appeared in the document
- `all_words.csv`: complete normalized frequency table
- word-cloud images: visual summaries of the most frequent terms

## NLTK resources

The script checks for required NLTK resources and downloads missing packages at runtime. Environments without internet access should install these resources in advance:

```python
import nltk

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")
```

## Limitations

- The input must contain extractable text; scanned PDFs require OCR first.
- The language pipeline is currently configured for English.
- Complex layouts, tables, formulas, headers, and repeated footers can affect frequency counts.
- Word clouds are exploratory visualizations, not statistical evaluation.
- Automatic resource downloads may be unsuitable for locked-down production environments.

## Privacy notes

PDF text is processed locally, but generated CSV files and images can reveal document contents. Store or share output artifacts according to the sensitivity of the source document.

## Project status

This repository is a focused NLP utility demonstrating PDF extraction, linguistic normalization, command-line design, structured reporting, validation, and visual output generation.