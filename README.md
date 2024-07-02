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

- **Purpose**: This layer encapsulates the core business logic of the application. Use cases like `RenewablesETLUseCase` orchestrate the ETL process, detailing how data is fetched, processed(transformation) and stored.

### 2. Data Layer

#### Repositories

- **Purpose**: This layer manages data access and persistence. Repositories serve as contracts for data access, providing the domain layer with methods for fetching and persisting data.

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

- Run tests using: `python -m pytest -vv`.
- Tests cover each component of the ETL process, including data extraction, transformation, and loading.

## Dependencies

List of main libraries and tools used:

- `pandas`: For data manipulation and transformation.
- `pytest`: For running unit tests.
- `python-dotenv`: For managing environment variables.
- `asyncio`: For running asynchronous tasks concurrently, improving performance.

## Future Enhancements

The current ETL client architecture is robust and flexible, but there are several enhancements that can be made to accommodate growth, increase resilience, and improve efficiency. Here are the planned future enhancements:

### Specifying Return Types for Repository Functions
- To improve the clarity and predictability of the repository functions, I propose to explicitly specify return types using Python's type hints. This will not only aid in maintaining type safety but also enhance the readability and maintainability of our code.

### Implementing Interfaces for Repositories
- Usage of Python’s Abstract Base Classes (ABCs) to define interfaces for our repositories for further improvements. This approach will standardize our repository implementations, ensuring that all repositories adhere to a uniform structure and method signature. It will also facilitate the integration of new data sources as our application scales.

### Adding Instance Type Checks in Usecase Constructor
- To ensure that usecase interact with appropriate repository implementations, I suggest adding isinstance checks in the constructors of use cases. This will validate that the provided repository instances comply with the expected interfaces, thereby safeguarding against runtime errors and enhancing the robustness of our system.

### Adding More Unit Test Cases for Bug Free Program
- For further improvements, I propose adding more test cases to ensure that the program is bug-free and that all edge cases are thoroughly handled. 

### Automated Scheduling
- **Implement a Scheduler**: Integrate a scheduling mechanism for automated weekly runs to ensure that data is consistently processed without manual intervention. Tools like Apache Airflow or cron jobs could be utilized for this purpose.

### Data Source Integration
- **Extend Data Sources**: Expand the ETL process to incorporate additional data sources, enhancing the diversity and volume of data handled by the system. This will involve adapting existing data models and potentially introducing new use cases and repositories.

### Scalability and Performance
- **Optimize for Scalability**: Refactor the architecture to handle increased loads as data volume grows. 

### Big Data Handling
- **Big Data Technologies**: If the data becomes substantial, consider integrating Big Data technologies such as Apache Hadoop or Apache Spark to efficiently process large datasets.

### Cloud Integration
- **Cloud-Ready**: Prepare the architecture for possible migration to cloud platforms like AWS, Azure, or Google Cloud, to leverage their scalable infrastructure and big data processing services.

These enhancements will ensure that the ETL client not only meets current needs but is also poised to handle future challenges and opportunities effectively, maintaining high performance, reliability, and scalability.

