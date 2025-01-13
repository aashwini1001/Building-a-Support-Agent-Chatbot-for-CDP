from flask import Flask, request, jsonify
from flask_cors import CORS
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser
import os

app = Flask(__name__)
CORS(app)

# Define schema for indexing
schema = Schema(cdp=TEXT(stored=True), content=TEXT(stored=True))

# Create index directory
if not os.path.exists("index"):
    os.mkdir("index")

# Create or open the Whoosh index
index_path = "index"
if not os.listdir(index_path):
    ix = create_in(index_path, schema)
    writer = ix.writer()
    # Add example data (can be extended with more detailed documentation snippets)
    writer.add_document(cdp="Segment", content="To set up a new source in Segment, go to the 'Sources' tab, click 'Add Source,' and follow the prompts.")
    writer.add_document(cdp="mParticle", content="To create a user profile in mParticle, navigate to 'Profiles,' select 'New Profile,' and configure the details.")
    writer.add_document(cdp="Lytics", content="To build an audience segment in Lytics, go to 'Audiences,' select 'Create Segment,' and define your audience.")
    writer.add_document(cdp="Zeotap", content="To integrate your data with Zeotap, access the 'Integration' tab and configure the integration settings.")
    writer.commit()

# Endpoint for chatbot
@app.route("/ask", methods=["POST"])
def ask_question():
    question = request.json.get("question", "").lower()
    ix = create_in(index_path, schema)

    with ix.searcher() as searcher:
        parser = QueryParser("content", ix.schema)
        query = parser.parse(question)
        results = searcher.search(query, limit=1)

        if results:
            return jsonify({"response": results[0]["content"]})
        else:
            return jsonify({"response": "I'm sorry, I couldn't find an answer to your question. Please check the documentation or refine your query."})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
