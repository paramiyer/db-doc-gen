
# 🧾 Automated Database Documentation Generator

This tool automates the process of documenting relational databases by extracting schema metadata, generating column descriptions using GPT, and exporting a complete DBML file for publishing via [dbdocs.io](https://dbdocs.io).

---

## 🚀 Features

- Extracts full schema metadata using Python (tables, columns, keys, indexes)
- Generates intelligent column descriptions using GPT
- Outputs DBML file ready to publish on `dbdocs.io`
- Publishes DBML file once the dbdocs session is active
- Tested with PostgreSQL + Chinook sample DB
- Works with most relational databases (PostgreSQL, MySQL, SQLite, etc.)

---

## 📦 Setup Instructions

### 1. Install Required Tools

#### 📌 Install Node.js and NPM
You need `npm` to install `dbdocs` CLI.

```bash
brew install node    # for macOS
# or visit https://nodejs.org to install manually
```

#### 📌 Install dbdocs CLI
```bash
npm install -g dbdocs
```

Confirm installation:
```bash
dbdocs --version
```

---

### 2. Clone This Repository

```bash
git clone https://github.com/your-username/db-doc-automation.git
cd db-doc-automation
```

---

### 3. Install Python Dependencies

Use a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## 🧪 Test with Chinook Sample Database

### Step 1: Download the Chinook DB

- Download the PostgreSQL `.sql` file from:  
  https://github.com/lerocha/chinook-database

### Step 2: Set Up Chinook in PostgreSQL

```bash
# Launch Postgres
psql -U your_user

# Create DB
CREATE DATABASE chinook;

# Load schema + data
\c chinook
\i /path/to/chinook_postgres.sql
```

Make sure the DB is running and accessible at `localhost:5432`.

---

## ⚙️ Configuration

Edit the `user_config.py` file with your connection details:

```python
db_uri: "postgresql://parameshwaraniyer@localhost:5432/chinook"
schema: "public"

user_prompt:  |
  You are a data documentation assistant.

  The database is designed for a {industry} and supports {domain}.
  Its purpose is to manage digital track sales, track customer purchases, oversee employee sales teams, and store metadata about artists, albums, and genres.

  In this database, for the table {table}, generate a short documentation string for the column {col}.

  Guidelines:
  - If the column name ends in "Id" or "ID" use "ID for <entity name derived from column name, in lowercase>"
  - For other columns, write short, noun-style labels like "Track name", "Creation date", "Total amount"
  - Avoid full sentences — do not start with "The column..." or "This field..."
  - Do not use special characters: apostrophes ('), commas (,), colons (:), semicolons (;)
  - Return only the documentation string (no quotes or formatting)

output_filename: "chinhook.dbml"
dotenv_path: ".env"
industry: 'digital media store'
domain: 'customer relationship management, sales tracking, and catalog navigation'
openai_model: "gpt-3.5-turbo"
```

Also ensure your OpenAI API key is set in the environment:

```bash
export OPENAI_API_KEY="your-api-key"
```

---

## ▶️ Run the Notebook

Launch the Jupyter notebook and execute:

```bash
jupyter notebook
```

Open `generate_db_docs.ipynb` and run all cells.

- This will:
  - Connect to your DB
  - Extract schema
  - Generate column descriptions via GPT
  - Export a `.dbml` file

---

## 🌐 Publish to dbdocs.io

1. Login using your email:
   ```bash
   dbdocs login
   ```

2. Publish your DBML file:
   ```bash
   dbdocs publish my_schema.dbml
   ```

Your docs will be available at:
```
https://dbdocs.io/your_username/my_project_name
```

---

## 🛠️ Coming Soon

- Support for MySQL and MSSQL
- Plugin-style model for business metadata enrichment
- Integration with dbt model documentation
