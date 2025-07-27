
# PDF Word Frequency Analyzer

A Python command-line tool to extract, clean, and analyze word frequencies from PDF files.  
It lemmatizes words, excludes stopwords and known/common words, and outputs CSV reports and word cloud images to help you identify unknown or important vocabulary in your PDFs.

---

## Features

- Extracts text from PDF files using `pdfplumber`.
- Cleans and lemmatizes text with `NLTK`.
- Filters out stopwords and user-provided known words.
- Generates frequency CSVs for:
  - All words
  - Known (excluded) words
  - Unknown words (not in known words)
- Creates word cloud images from the most frequent words.
- Command-line interface with flexible flags and options.


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/M2002HR/pdf-word-frequency-analyzer.git
   cd pdf-word-frequency-analyzer
    ```

2. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Download necessary NLTK data (if not already available):

   ```python
   import nltk
   nltk.download('stopwords')
   nltk.download('wordnet')
   ```

---

## Usage

Run the script from the command line with:

```bash
python word_frequency_finder.py path/to/your/file.pdf [--top_n 100] [--known_words_file known_words.txt] [--output_dir path/to/output]
```

### Arguments

* Path to the PDF file to analyze **(required)** 
* `--top_n` **(optional)**: Number of top frequent words for reports and word clouds (default: 100).
* `--known_words_file` **(optional)**: Path to a text file containing known/common words to exclude from unknown words.
* `--output_dir` **(optional)**: Directory to save the results. Defaults to `results/<pdf_filename>/` inside the project directory.

### Example

```bash
python main.py data/sample.pdf --num_top_words 500 --known_words_file data/known_words.txt
```

---

## Output

The tool will create a results directory with the following files:

* `top<N>_unknown_words.csv` — Top N unknown words and their frequencies.
* `wordcloud_top<N>_unknown_words.png` — Word cloud image of unknown words.
* `excluded_known_words.csv` — All known/excluded words found in the document.
* `all_words.csv` — Frequency of all words found.
* `wordcloud_top<N>_all_words.png` — Word cloud image for all words.

---

## Acknowledgments

* [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF text extraction
* [NLTK](https://www.nltk.org/) for natural language processing tools
* [WordCloud](https://github.com/amueller/word_cloud) for word cloud generation

