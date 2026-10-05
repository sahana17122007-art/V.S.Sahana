"""LegalEase - Flask application (main entry point)."""
import os
from flask import Flask, render_template, request, send_file
from clauses import generate_document
from pdf_utils import build_pdf
from validators import validate

app = Flask(__name__)

DOCUMENT_TYPES = {
    "rental": "Rental Agreement",
    "nda": "Non-Disclosure Agreement",
    "employment": "Employment Agreement",
    "leave": "Leave and License Agreement",
}


@app.route("/")
def index():
    return render_template("index.html", document_types=DOCUMENT_TYPES, errors=[], form={})


@app.route("/generate", methods=["POST"])
def generate():
    data, errors = validate(request.form)
    if errors:
        return render_template("index.html", document_types=DOCUMENT_TYPES,
                               errors=errors, form=request.form), 400
    title, clauses = generate_document(data["document_type"], data)
    return render_template("result.html", title=title, clauses=clauses, data=data)


@app.route("/download", methods=["POST"])
def download():
    data, errors = validate(request.form)
    if errors:
        return {"errors": errors}, 400
    title, clauses = generate_document(data["document_type"], data)
    pdf = build_pdf(title, clauses, data)
    return send_file(pdf, as_attachment=True, download_name="LegalEase_Document.pdf",
                     mimetype="application/pdf")


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
