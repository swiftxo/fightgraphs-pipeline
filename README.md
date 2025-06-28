# FightGraphs-Pipeline

## About The Project

This project is an ETL (Extract, Transform, Load) pipeline built to process and structure large datasets. Its primary function is to extract data from a NoSQL database (like MongoDB), transform it into a standardized relational format, and load it into a PostgreSQL database for easier querying and analysis.

## Current Status: Work in Progress

This project is currently under active development. The core extraction and loading functionalities are being built out, and the data models are being refined to handle various data sources.

- **Setup:** Detailed setup and installation instructions are not yet available but will be added once I am done with mapping out all the models.
- **Testing:** The tests currently in the `/tests` directory are rough scripts used for quick checks to see if the components are functioning correctly.

## Core Components

The pipeline is organized into a few key modules:

- **database:** Contains controller classes for managing connections and sessions with source databases (e.g., MongoDB) and target databases (e.g., PostgreSQL).
- **models:** Defines the data structures.
  - `mongodb_models.py`: Pydantic models that represent the schema of the data in the source collections.
  - `postgresql_models.py`: SQLAlchemy models that define the relational schema for the target database.
- **extract:** Includes functions responsible for pulling data from the various source collections.
- **transform:** (In-progress) This is where the logic for mapping the extracted source data to the target relational
