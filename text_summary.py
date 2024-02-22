import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import PyPDF2
from heapq import nlargest

stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')

def read_text_from_file(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    print("Text extracted from PDF:", text)
    return text

def summary_text(text):
    doc = nlp(text)
    tokens = [token.text for token in doc]
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1
                
    if not word_freq:  # Check if word_freq is empty
        return "", doc, len(text.split(' ')), 0  # Return empty summary and summary length
    
    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq   # normalized frequency
        
    sent_token = [sent for sent in doc.sents]
    sent_score = {}
    for sent in sent_token:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word.text]
                else:
                    sent_score[sent] += word_freq[word.text]
    select_len = int(len(sent_token) * 0.3) 
    summary = nlargest(select_len, sent_score, key=sent_score.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    return summary, doc, len(text.split(' ')), len(summary.split(' '))

if __name__ == "__main__":
    # Test read_text_from_file function
    filename = "textfile.pdf"  # Replace "your_pdf_file.pdf" with the path to your PDF file
    text = read_text_from_file(filename)
    print("Text extracted from PDF:", text)

    # Test summary_text function
    summary, doc, len_of_text, len_of_summary = summary_text(text)
    print("Summary:", summary)
    print("Original Text:", doc)
    print("Length of Text:", len_of_text)
    print("Length of Summary:", len_of_summary)
