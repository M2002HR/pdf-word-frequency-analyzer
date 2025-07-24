import os
import sys
import pdfplumber
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import csv
from wordcloud import WordCloud
from tqdm import tqdm
import argparse

# Ensure required NLTK resources are downloaded
for resource in ['stopwords', 'wordnet', 'averaged_perceptron_tagger']:
    try:
        nltk.data.find(f'corpora/{resource}')
    except LookupError:
        print(f"Downloading NLTK resource: {resource}...")
        nltk.download(resource)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(tag):
    """Map NLTK POS tags to WordNet POS tags."""
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN

def normalize_word(word, tag=None):
    """Lemmatize with POS, then apply morphy fallback."""
    lemma = lemmatizer.lemmatize(word, tag or wordnet.NOUN)
    morphed = wordnet.morphy(lemma)
    return morphed if morphed else lemma

def load_known_words(filepath=None):
    known_words = set()
    if filepath and os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                w = line.strip().lower()
                if w:
                    lw = normalize_word(w)
                    known_words.add(lw)
        print(f"Loaded and normalized {len(known_words)} known words from {filepath}")
    else:
        print("No known words file provided or file not found. Using empty known words list.")
    return known_words

def clean_and_lemmatize(text):
    text = text.replace('-\n', '').replace('\n', ' ')
    words = re.findall(r'\b\w+\b', text.lower())
    words = [w for w in words if w not in stop_words and not w.isdigit() and len(w) >= 3]

    print("Lemmatizing and normalizing words with POS tagging...")
    lemmatized_words = []
    tagged = pos_tag(words)
    for word, tag in tqdm(tagged, desc="Lemmatizing", unit="word", leave=False):
        wn_tag = get_wordnet_pos(tag)
        normalized = normalize_word(word, wn_tag)
        lemmatized_words.append(normalized)
    return lemmatized_words

def process_pdf(pdf_path):
    print(f"\n📄 Processing PDF: {pdf_path}")
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Reading {len(pdf.pages)} pages...")
            for page in tqdm(pdf.pages, desc="Extracting pages", unit="page"):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    except Exception as e:
        print(f"❌ Error reading {pdf_path}: {e}")
        return None

    if not text.strip():
        print("⚠️ No text extracted.")
        return None

    return clean_and_lemmatize(text)

def save_word_freq_csv(word_freq, output_path, top_n=None):
    if top_n is None:
        words_to_save = word_freq.items()
        print(f"💾 Saving all {len(word_freq)} words to CSV: {output_path}")
    else:
        words_to_save = word_freq.most_common(top_n)
        print(f"💾 Saving top {top_n} words to CSV: {output_path}")

    with open(output_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Word", "Frequency"])
        for word, freq in words_to_save:
            writer.writerow([word, freq])

def save_wordcloud(word_freq, output_path, top_n):
    print(f"🎨 Generating word cloud from top {top_n} words...")
    top_words = dict(word_freq.most_common(top_n))
    wordcloud = WordCloud(
        width=1600, height=800, background_color='white',
        colormap='viridis'
    ).generate_from_frequencies(top_words)

    wordcloud.to_file(output_path)
    print(f"✅ Word cloud image saved: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Extract words from a PDF, exclude known words, generate frequency CSVs and word clouds."
    )
    parser.add_argument("pdf_path", help="Path to the PDF file to process")
    parser.add_argument(
        "-n", "--num_top_words",
        type=int,
        default=100,
        help="Number of top words to save/display (default: 100)"
    )
    parser.add_argument(
        "-k", "--known_words_file",
        type=str,
        default=None,
        help="Path to a known words text file (one word per line) to exclude"
    )
    parser.add_argument(
        "-o", "--output_dir",
        type=str,
        default=None,
        help="Output directory to save results (default: './results/<pdf_filename_without_ext>')"
    )

    args = parser.parse_args()
    pdf_path = args.pdf_path
    top_n = args.num_top_words
    known_words_file = args.known_words_file
    output_dir = args.output_dir

    if not os.path.isfile(pdf_path) or not pdf_path.lower().endswith(".pdf"):
        print("❌ Provided path is not a valid PDF file.")
        sys.exit(1)

    if top_n <= 0:
        print("❌ NUM_TOP_WORDS must be a positive integer.")
        sys.exit(1)

    if output_dir:
        if not os.path.isdir(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                print(f"❌ Could not create output directory '{output_dir}': {e}")
                sys.exit(1)
    else:
        project_root = os.getcwd()
        pdf_basename = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = os.path.join(project_root, "results", pdf_basename)
        os.makedirs(output_dir, exist_ok=True)

    known_words = load_known_words(known_words_file)
    lemmatized_words = process_pdf(pdf_path)
    if lemmatized_words is None:
        sys.exit(1)

    excluded_words = [w for w in lemmatized_words if w in known_words]
    unknown_words = [w for w in lemmatized_words if w not in known_words]

    excluded_freq = Counter(excluded_words)
    unknown_freq = Counter(unknown_words)
    all_freq = Counter(lemmatized_words)

    # Save unknown words CSV and wordcloud
    unknown_csv = os.path.join(output_dir, f"top{top_n}_unknown_words.csv")
    unknown_img = os.path.join(output_dir, f"wordcloud_top{top_n}_unknown_words.png")
    save_word_freq_csv(unknown_freq, unknown_csv, top_n)
    save_wordcloud(unknown_freq, unknown_img, top_n)

    # Save excluded known words CSV (all)
    excluded_csv = os.path.join(output_dir, "excluded_known_words.csv")
    save_word_freq_csv(excluded_freq, excluded_csv)

    # Save all words CSV (all)
    all_words_csv = os.path.join(output_dir, "all_words.csv")
    save_word_freq_csv(all_freq, all_words_csv)

    # Save word cloud for all words
    all_words_img = os.path.join(output_dir, f"wordcloud_top{top_n}_all_words.png")
    save_wordcloud(all_freq, all_words_img, top_n)

    print("\n🎉 Done!")
    print(f"Results saved in directory: {output_dir}")

if __name__ == "__main__":
    main()
