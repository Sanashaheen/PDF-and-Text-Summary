from flask import Flask , render_template, request
from text_summary import read_text_from_file, summary_text

app=Flask(__name__)

@app.route('/')

def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    if 'rawtext' in request.form:
        rawtext = request.form['rawtext']
        if rawtext.strip():  # Check if the text is not empty
            summary, original_text, len_of_text, len_of_summary = summary_text(rawtext)
            return render_template('summary.html', summary=summary, original_text=original_text, len_of_text=len_of_text, len_of_summary=len_of_summary)
    
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '' and file.filename.lower().endswith(('.pdf')):  # Check if a file is uploaded and it's a PDF file
            text = read_text_from_file(file)
            if text.strip():  # Check if text is extracted from the file
                summary, _, len_of_text, len_of_summary = summary_text(text)
                return render_template('summary.html', summary=summary, original_text=text, len_of_text=len_of_text, len_of_summary=len_of_summary)

    # If neither text nor file is provided or if the file is not a PDF, render the index template with an error message
    return render_template('index.html', error='No valid input provided')

if __name__ == "__main__":
     app.run(debug=False , host='0.0.0.0')