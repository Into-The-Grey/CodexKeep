# CodexKeep `README.md`

## CodexKeep Initialization Script

**CodexKeep Initialization Script** is a Python-based tool designed to fetch, process, and store data from the Bungie API into a PostgreSQL database. It ensures reliable data management, error handling, and structured batch processing for large datasets.

---

## **Features**

- Fetches Destiny 2 manifest data via the Bungie API.
- Processes game data into structured formats for:
  - Items
  - Activities
  - Locations
  - Vendors
  - Quests
  - Currencies
- Handles batch processing with robust error logging.
- Integrates environment variables for secure API and database credentials.
- Validates database integrity post-insertion.
- Detailed logging for error diagnostics.

---

## **Requirements**

### **Dependencies**

- Python 3.8 or higher
- Required Python libraries:
  - `psycopg2`
  - `requests`
  - `python-dotenv`

Install dependencies using:

```bash
pip install -r requirements.txt
```

### **Environment Variables**

Create a `.env` file in the root directory with the following:

```plaintext
API_KEY=your_bungie_api_key
DB_NAME=your_database_name
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
```

---

## **Setup Instructions**

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/codexkeep.git
   cd codexkeep
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your `.env` file with the required credentials.

4. Run the script:

   ```bash
   python codexkeep_initialization.py
   ```

---

## **How It Works**

1. **Initialization Phase**
   - Validates environment variables.
   - Tests connections to both the Bungie API and PostgreSQL database.

2. **Error Handling and Logging**
   - Logs errors to `error_log.txt` and provides runtime diagnostics.

3. **Data Fetching**
   - Fetches the manifest and game data definitions from the Bungie API.

4. **Batch Processing**
   - Processes data into structured formats and inserts it into the PostgreSQL database in batches of 2500 records.

5. **Validation**
   - Ensures the integrity of database records and logs any validation errors to `validation_errors.txt`.

---

## **Directory Structure**

```plaintext
.
├── codexkeep_initialization.py  # Main script
├── .env                         # Environment variables (user-created)
├── requirements.txt             # Python dependencies
├── error_log.txt                # Logs runtime errors
├── validation_errors.txt        # Logs invalid database records
├── README.md                    # Project documentation
└── ROADMAP.md                   # Future plans and milestones
```

---

## **Logs and Validation**

- Errors are logged in `error_log.txt`.
- Database validation issues are logged in `validation_errors.txt`.
- Debugging tools allow for inspecting invalid rows.

---

## **Contributing**

We welcome contributions to enhance CodexKeep! To contribute:

1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed explanation.

---

## **License**

This project is licensed under the MIT License. See `LICENSE` for details.

---

## **Contact**

For any questions or suggestions, feel free to contact:

- **Name:** [Your Name]
- **Email:** [Your Email]
- **GitHub:** [Your GitHub Profile]

---
