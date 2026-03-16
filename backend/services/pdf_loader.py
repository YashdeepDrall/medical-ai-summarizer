import os
import pandas as pd
from pypdf import PdfReader

DATA_FOLDER = "data"


# --------------------------------
# Load PDF files
# --------------------------------
def load_pdfs():

    documents = []

    for file in os.listdir(DATA_FOLDER):

        if file.endswith(".pdf"):

            path = os.path.join(DATA_FOLDER, file)

            reader = PdfReader(path)

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

            if text.strip():
                documents.append(text)

    return documents


# --------------------------------
# Load CSV files
# --------------------------------
def load_csvs():

    documents = []

    for file in os.listdir(DATA_FOLDER):

        if file.endswith(".csv"):

            path = os.path.join(DATA_FOLDER, file)

            df = pd.read_csv(path)

            # convert rows to text
            text = df.to_string()

            documents.append(text)

    return documents


# --------------------------------
# Split text into chunks
# --------------------------------
def split_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunks.append(text[i:i + chunk_size])

    return chunks


# --------------------------------
# Load all knowledge data
# --------------------------------
def load_and_chunk_data():

    pdf_docs = load_pdfs()
    csv_docs = load_csvs()

    docs = pdf_docs + csv_docs

    all_chunks = []

    for doc in docs:

        chunks = split_text(doc)

        all_chunks.extend(chunks)

    print("Total knowledge chunks:", len(all_chunks))

    return all_chunks