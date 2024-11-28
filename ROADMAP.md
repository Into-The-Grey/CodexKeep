# CodexKeep Project Roadmap

This roadmap outlines the planned features, improvements, and milestones for the CodexKeep project.

---

## **Current State**

- **Core Functionalities:**
  - Fetching manifest data from the Bungie API.
  - Processing and structuring data for PostgreSQL insertion.
  - Comprehensive error handling and logging.
  - Validation of database records.

- **Supported Tables:**
  - Items
  - Activities
  - Locations
  - Vendors
  - Quests
  - Currencies

---

## **Short-Term Goals (Next 1-3 Months)**

1. **Database Schema Enhancements**
   - Introduce foreign key relationships between tables (e.g., items ↔ activities).
   - Optimize schema for query performance.

2. **Improved Validation**
   - Add stricter validation rules for critical fields (e.g., null checks, type validations).
   - Enhance validation logging with suggestions for fixes.

3. **Testing Framework**
   - Implement unit and integration tests for:
     - API data fetching.
     - Batch processing logic.
     - Database integrity validation.

4. **Configuration Enhancements**
   - Allow dynamic batch sizes via `.env` or CLI arguments.
   - Support for multi-language manifests from the Bungie API.

---

## **Medium-Term Goals (Next 3-6 Months)**

1. **Extended Data Processing**
   - Add support for more data definitions (e.g., DestinyTalentGridDefinition, DestinyProgressionDefinition).

2. **Improved Error Recovery**
   - Retry mechanism for failed API calls or database transactions.
   - Graceful handling of partial batch failures.

3. **Dashboard and Reporting**
   - Develop a web-based dashboard to visualize and manage database records.
   - Provide insights into errors, invalid records, and processing metrics.

4. **Scalability**
   - Parallelize batch processing for faster execution.
   - Add support for other database systems (e.g., MySQL, SQLite).

---

## **Long-Term Goals (Next 6-12 Months)**

1. **Automation**
   - Automate the data fetching and processing pipeline using CRON jobs or a task scheduler.
   - Add notifications for errors and status updates (e.g., email or Slack).

2. **Enhanced Data Insights**
   - Generate analytical reports on game data (e.g., rarest items, top quest rewards).
   - Provide tools to query the database for specific insights.

3. **Integration with Third-Party Tools**
   - Integrate with analytics platforms (e.g., Tableau, Power BI).
   - Add API endpoints for external applications to query CodexKeep's data.

4. **Community Features**
   - Allow users to contribute their own data processing modules.
   - Create a plugin system for extending CodexKeep’s functionality.

---

## **Completed Milestones**

- Initial script for fetching and processing Bungie API data.
- Batch insertion of data into PostgreSQL.
- Logging system for errors and validation issues.

---

## **Feedback and Suggestions**

If you have ideas or suggestions for the roadmap, feel free to reach out or submit an issue in the repository.

---

## **Timeline**

| Milestone                 | Target Date   | Status        |
| ------------------------- | ------------- | ------------- |
| Initial release           | November 2024 | ✅ Completed   |
| Database schema review    | January 2025  | ⏳ In Progress |
| Validation enhancements   | February 2025 | 🔜 Planned     |
| Dashboard development     | April 2025    | 🔜 Planned     |
| Automation implementation | June 2025     | 🔜 Planned     |
