# MVP 1 – Core ETL Engine (Detailed Task Sheet)

This sheet breaks each MVP 1 task into a brief description and a checkbox you can mark when the work is complete.  
Use it as your personal “to‑do” list; the checkboxes are purely for tracking.

---

## Module 1️⃣: Data Ingestion

- [ ] **CSV upload endpoint**
  *FastAPI `POST /ingest/csv` that accepts multipart files, validates size/encoding, and stores the file temporarily for processing.*  

- [ ] **JSON upload endpoint**  
  *Similar to the CSV endpoint but expects `application/json`. Parses the payload into a Pandas `DataFrame`.*  

- [ ] **PostgreSQL source connector**  
  *Implement a configurable connector using SQLAlchemy/psycopg2 that reads a table or custom query into a DataFrame.*  

- [ ] **Google Sheets connector (stretch)**  
  *OAuth 2.0 flow to fetch a sheet range via the Google Sheets API and convert it to a DataFrame.*  

- [ ] **Schema inference**  
  *Automatically detect column names and data types from the uploaded file or source and store the schema as JSON for later steps.*  

- [ ] **Validation layer**  
  *Reject files > 50 MB, unsupported encodings, or malformed JSON/CSV; return clear error messages to the client.*  

- [ ] **Unit tests**  
  *Write pytest cases for each ingestion route, mocking file I/O and DB connections.*  

- [ ] **Documentation snippet**  
  *Add example `curl` commands and usage notes to the project README.*  

---

## Module 2️⃣: Transformation Engine

- [ ] **Base `Transformation` class**  
  *Encapsulates a Pandas `DataFrame` and a list of transformation callables; provides a `run()` method.*  

- [ ] **Filter operation**  
  *Method `filter_rows(condition: str)` that parses simple expressions (e.g., `col > 0`) and returns a filtered DataFrame.*  

- [ ] **Column rename / map**  
  *Method `rename_columns(mapping: dict)` to rename columns according to a user‑provided map.*  

- [ ] **Add calculated column**  
  *Method `add_column(name: str, formula: str)` using `DataFrame.eval` to compute new columns.*  

- [ ] **Drop duplicates**  
  *Method `drop_duplicates(subset: List[str])` that removes duplicate rows based on given columns.*  

- [ ] **Chaining API**  
  *Enable fluent calls like `t.filter(...).rename(...).add_column(...)` for a clean user experience.*  

- [ ] **Preview mode**  
  *Run the transformation chain on a sample (first 500 rows) and return both the original and transformed snapshots.*  

- [ ] **Error handling**  
  *Catch common errors (`KeyError`, `SyntaxError`, type mismatches) and surface user‑friendly messages.*  

---

## Module 3️⃣: Load / Destination Layer

- [ ] **Write to PostgreSQL**  
  *Bulk upsert transformed data using `psycopg2.extras.execute_batch` for efficiency.*  

- [ ] **Write to CSV**  
  *Export the final DataFrame to a user‑specified file path with optional compression.*  

- [ ] **Append vs. Overwrite option**  
  *Allow the user to choose whether new data should append to or replace existing destination data.*  

- [ ] **Transaction safety**  
  *Wrap DB writes in a transaction; roll back on any failure to keep data consistent.*  

- [ ] **Logging of load stats**  
  *Record rows written, duration, and any rejected rows; expose via an endpoint or log file.*  

- [ ] **Unit tests**  
  *Mock DB connections and file writes; assert that row counts match expectations.*  

- [ ] **Config file schema**  
  *Define a YAML/JSON template for destination settings (host, port, credentials, table name, etc.).*  

- [ ] **Documentation**  
  *Provide sample config files and usage examples in the repository docs.*  

- [ ] **Error reporting**  
  *Standardized error objects for load failures, with actionable suggestions.*  

---

## Module 4️⃣: Scheduler & Orchestration

- [ ] **Cron‑style UI**  
  *Simple front‑end form that lets users enter a cron expression (e.g., `0 2 * * *`).*  

- [ ] **Background worker**  
  *Integrate `APScheduler` (or similar) to schedule pipeline runs based on the stored cron expressions.*  

- [ ] **One‑off run endpoint**  
  *FastAPI `POST /pipeline/run` that triggers an immediate execution of a selected pipeline.*  

- [ ] **Run history table**  
  *Persist pipeline ID, start/end timestamps, status, and row counts in a PostgreSQL table for auditability.*  

- [ ] **Retry logic**  
  *Automatic retry up to 3 times for transient errors (network, temporary DB outage). Log each attempt.*  

- [ ] **Alert webhook**  
  *Optional user‑provided URL that receives a POST payload on success or failure of a run.*  

- [ ] **Unit & integration tests**  
  *Simulate scheduled runs using mocked data sources and verify proper state transitions.*  

- [ ] **Documentation**  
  *Explain how to configure schedules, view history, and set up alerts.*  

- [ ] **Monitoring hooks**  
  *Expose Prometheus metrics for scheduled job counts, failures, and execution duration.*  

---

## Module 5️⃣: Minimal UI (Web Front‑End)

- [ ] **Pipeline builder page**  
  *React (or similar) page with dropdowns for source selection, transformation steps, and destination.*  

- [ ] **Live preview pane**  
  *Show “before” and “after” tables after the user clicks **Preview**; use the preview API from the backend.*  

- [ ] **Run button**  
  *Triggers the pipeline via the `/pipeline/run` endpoint; disables UI while the job is in progress.*  

- [ ] **Status indicator**  
  *Poll `/pipeline/status/{id}` and display a progress bar or spinner with success/failure messages.*  

- [ ] **Error display modal**  
  *Render any transformation or load errors in a user‑friendly modal dialog.*  

- [ ] **Responsive design**  
  *Ensure the UI works on desktop and tablet screen sizes (CSS flex/grid).*  

- [ ] **Unit tests with React Testing Library**  
  *Test component rendering, API call handling, and checkbox interactions.*  

- [ ] **Style guide**  
  *Define a simple color palette, typography, and button styles for consistency.*  

- [ ] **Accessibility check**  
  *Add ARIA labels and keyboard navigation support.*  

---

## Module 6️⃣: Testing & CI/CD

- [ ] **Pytest suite**  
  *Cover all backend modules; aim for ≥ 80 % line coverage.*  

- [ ] **GitHub Actions workflow**  
  *Run lint (`ruff`), type checks (`mypy`), security scan (`bandit`), and Docker build on each push.*  

- [ ] **Static type checking**  
  *Configure `mypy` to enforce type safety across the `app/` package.*  

- [ ] **Security scan**  
  *Run `bandit` (or `safety`) to detect common Python security issues.*  

- [ ] **Docker healthcheck**  
  *Add a health‑check endpoint (`/health`) and ensure the container reports healthy status.*  

- [ ] **Version bump script**  
  *Automate `__version__` increment on new Git tags (e.g., using `bump2version`).*  

- [ ] **Release notes generator**  
  *Extract PR titles and labels to auto‑populate a changelog file for each release.*  

- [ ] **Rollback plan**  
  *Document steps to revert a failed deployment (docker image tag rollback, DB migration revert, etc.).*  

---

### How to use this sheet
1. Paste the above content into `mvp1.md` (or replace the existing file).  
2. Click **Apply** on this code block (or enable *Agent Mode* to have the file written automatically).  
3. As you complete each task, tick the corresponding checkbox (`- [x]`) in the markdown file.  

Feel free to ask for any further elaboration on a particular task, or for a similar detailed sheet for the other MVPs!