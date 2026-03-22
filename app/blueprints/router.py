# -------------------------------------------------
# UI Blueprint – the three‑step ETL wizard
# -------------------------------------------------
from __future__ import annotations

import os
import uuid
from typing import List, Dict, Any
from ..core.handler import apply_transformations
import pandas as pd
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
)
from werkzeug.utils import secure_filename

client_bp = Blueprint("client", __name__)
# -----------------------------------------------------------------
# 1️⃣ Folder for temporary CSV uploads
# -----------------------------------------------------------------
# Project root is one level above the `client` package.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------------------------------------------
# 3️⃣ Home route – redirects to the first wizard step
# -----------------------------------------------------------------
@client_bp.route("/", methods=["GET"])
def home() -> Any:
    """Landing page – simply forwards to step 1."""
    return redirect(url_for("client.upload"))

# -----------------------------------------------------------------
# 4️⃣ Step 1 – CSV upload
# -----------------------------------------------------------------
@client_bp.route("/upload", methods=["GET", "POST"])
def upload() -> Any:
    """Render upload form (GET) or process the CSV upload (POST)."""
    if request.method == "POST":
        file = request.files.get("csv_file")
        if not file:
            return render_template("upload.html", error="No file selected")

        # Sanitize the original name and prepend a UUID to avoid collisions
        filename = secure_filename(file.filename) or "uploaded.csv" # type: ignore
        temp_name = f"{uuid.uuid4().hex}_{filename}"
        save_path = os.path.join(UPLOAD_DIR, temp_name)
        file.save(save_path)

        # Remember the temporary filename for later steps
        session["uploaded_file"] = temp_name
        session.modified = True

        return redirect(url_for("client.transform"))

    return render_template("upload.html")

# -----------------------------------------------------------------
# 5️⃣ Step 2 – choose transformations (GET shows form, POST stores)
# -----------------------------------------------------------------
@client_bp.route("/transform_pre", methods=["GET", "POST"])
def transform() -> Any:
    """Show the transformation checklist (GET) or store the selection (POST)."""
    if "uploaded_file" not in session:
        # User tried to skip step 1
        return redirect(url_for("client.upload"))

    if request.method == "POST":
        selected: List[str] = request.form.getlist("transformations")
        session["transformations"] = selected

        # Capture rename details if that option was chosen
        if "rename_column" in selected:
            session["rename"] = {
                "old_name": request.form.get("old_name", "").strip(),
                "new_name": request.form.get("new_name", "").strip(),
            }
        else:
            session.pop("rename", None)

        session.modified = True
        return redirect(url_for("client.transform"))

    return render_template("transform.html")


# -----------------------------------------------------------------
# 7️⃣ API endpoint used by the “Preview” button on Step 2
# -----------------------------------------------------------------
@client_bp.route("/preview-transform", methods=["POST"])
def preview_transform() -> Any:
    """
    Expected JSON payload:
    {
        "transformations": ["drop_duplicate_rows", "fill_nulls_zero", …],
        "rename": {"old_name": "...", "new_name": "..."}   # optional
    }

    Returns the first 5 rows after applying the requested transformations.
    """
    payload = request.get_json(silent=True) or {}
    transforms: List[str] = payload.get("transformations", [])
    rename_info: Dict[str, str] = payload.get("rename", {})

    temp_file = session.get("uploaded_file")
    if not temp_file:
        return jsonify({"error": "No uploaded file in session"}), 400

    csv_path = os.path.join(UPLOAD_DIR, temp_file)
    if not os.path.exists(csv_path):
        return jsonify({"error": "Uploaded file not found"}), 404

    try:
        # Load a modest chunk (first 100 rows) for speed
        df = pd.read_csv(csv_path, nrows=100)
        df = apply_transformations(df, transforms, rename_info)
        preview_str = df.head().to_string(index=False)
        return jsonify({"preview": preview_str})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# -----------------------------------------------------------------
# 9️⃣ Download endpoint – applies transformations to entire file
# -----------------------------------------------------------------
@client_bp.route("/download-csv", methods=["GET"])
def download_csv() -> Any:
    """Download the transformed CSV file (full data, not just preview)."""
    temp_file = session.get("uploaded_file")
    transforms = session.get("transformations", [])
    rename_info = session.get("rename", {})

    if not temp_file:
        return jsonify({"error": "No uploaded file in session"}), 400

    csv_path = os.path.join(UPLOAD_DIR, temp_file)
    if not os.path.exists(csv_path):
        return jsonify({"error": "Uploaded file not found"}), 404

    try:
        # Load entire CSV and apply transformations
        df = pd.read_csv(csv_path)
        df = apply_transformations(df, transforms, rename_info)
        
        # Convert to CSV bytes and return as attachment
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        return (
            csv_bytes,
            200,
            {
                "Content-Disposition": "attachment; filename=transformed_data.csv",
                "Content-Type": "text/csv",
            },
        )
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500