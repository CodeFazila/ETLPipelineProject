# ETL Client for Solar and Wind Data
## Overview

This ETL (Extract, Transform, Load) client is designed to efficiently process and manage data from Solar and Wind energy sources. Utilizing Clean Architecture principles and asynchronous programming, the client focuses on handling data from the latest week, transforming timestamps into a consistent format, and ensuring data integrity and proper naming conventions before loading it into a structured output directory.

## Features

- **Data Extraction**: Fetches the latest week's data from both Solar and Wind endpoints using asynchronous requests to enhance performance.
- **Concurrent Data Handling**: Implements asynchronous programming to run data extraction for Solar and Wind concurrently, significantly reducing the overall processing time and increasing throughput.
- **Data Transformation**: Converts naive timestamps into UTC time zone aware timestamps and standardizes column names and types using the pandas library for robust data manipulation.
- **Data Loading**: Saves the transformed data into an `/output` directory using a structured file format, adhering to predefined naming conventions and data structures.

## Architecture and Design Overview

The ETL (Extract, Transform, Load) client for Solar and Wind data is architecturally designed to maximize flexibility, maintainability, and testability by adhering to the principles of Clean Architecture. This design ensures that the system's business logic is decoupled from external interfaces and frameworks, which promotes easier testing and adaptation to changes over time.

### 1. Domain Layer

This layer encapsulates the core business logic of the application:

#### Use Cases
- **Purpose**: Use cases like `RenewablesETLUseCase` orchestrate the ETL process, detailing how data is fetched, processed, and stored.

#### Repositories
- **Purpose**: Repositories serve as contracts for data access within the domain layer, abstracting the specifics of data fetching and persistence.

### 2. Data Layer

Located under `/source/data`, this layer implements the interfaces specified by the domain to manage data interactions:

This structured approach not only facilitates easier testing and maintenance but also allows the system to adapt more smoothly to changes in data sources or business rules without extensive modifications. By keeping business logic separate from data access and external interactions, the ETL client remains flexible and robust against various challenges that might arise during its operation.

## File Structure

The project is organized into several directories and key files for efficient navigation and understanding:

## Root Files
- `/.env`: Configuration file for environment variables and API keys.
- `/main.py`: The main executable script for running the ETL process.
- `/requirements.txt`: Lists all dependencies, installable via `pip install -r requirements.txt`.

## Directories
- **/source**: Houses all the core application code.
  - **/source/domain**: Contains business logic and use case implementations.
    - **/source/domain/usecase**: Modules for specific ETL use cases.
  - **/source/data**: Manages data handling functionalities.
    - **/source/data/repository**: Abstractions for data access.
      - **/source/data/repository/renewable_repository**: Specialized repositories for renewable energy data.

- **/resources**: Provides utilities and external resource management.
  - **/resources/api_client**: API client module for fetching data from external sources.

- **/output**: Destination directory for storing processed data files in a structured format.


## Running the ETL Process

- Run the API data source: `python -m uvicorn api_data_source.main:app –reload`.
- Execute the main script: `python main.py`.

## Testing

Comprehensive unit tests are included to ensure the functionality and reliability of the ETL process:

- Run tests using: `pytest`.
- Tests cover each component of the ETL process, including data extraction, transformation, and loading.

## Dependencies

List of main libraries and tools used:

- `pandas`: For data manipulation and transformation.
- `pytest`: For running unit tests.
- `python-dotenv`: For managing environment variables.
- `asyncio`: For running asynchronous tasks concurrently, improving performance.

## Future Enhancements

The current ETL client architecture is robust and flexible, but there are several enhancements that can be made to accommodate growth, increase resilience, and improve efficiency. Here are the planned future enhancements:

### Enhanced Retry Logic for API Client
- **Proposed Enhancement**: Implement Retry Logic with Exponential Backoff.

### Automated Scheduling
- **Implement a Scheduler**: Integrate a scheduling mechanism for automated weekly runs to ensure that data is consistently processed without manual intervention. Tools like Apache Airflow or cron jobs could be utilized for this purpose.

### Data Source Integration
- **Extend Data Sources**: Expand the ETL process to incorporate additional data sources, enhancing the diversity and volume of data handled by the system. This will involve adapting existing data models and potentially introducing new use cases and repositories.

### Scalability and Performance
- **Optimize for Scalability**: Refactor the architecture to handle increased loads as data volume grows. 

### Big Data Handling
- **Big Data Technologies**: If the data becomes substantial, consider integrating Big Data technologies such as Apache Hadoop or Apache Spark to efficiently process large datasets.

### Robust Testing
- **Integration Testing**: Develop comprehensive integration tests to ensure that all components of the system work together seamlessly.
- **Performance Testing**: Regularly conduct performance testing to evaluate the system’s efficiency and responsiveness. 
- **Scalability Testing**: Test the system’s ability to scale up with increased loads, ensuring that it can handle large volumes of data without performance degradation.

### Cloud Integration
- **Cloud-Ready**: Prepare the architecture for possible migration to cloud platforms like AWS, Azure, or Google Cloud, to leverage their scalable infrastructure and big data processing services.

These enhancements will ensure that the ETL client not only meets current needs but is also poised to handle future challenges and opportunities effectively, maintaining high performance, reliability, and scalability.

