# CS2300-Database-Project

# Project Title: Language Learning and Translation Database

## Overview
This project is a comprehensive application designed to facilitate language learning and translation. It is built on a MySQL database and provides functionality for managing languages, words, translations, and user interactions through a command-line interface.

## Features
- **Language Management**: Add, edit, and delete languages in the database.
- **Word and Definition Handling**: Users can add, edit, and delete words and their definitions.
- **Translation Management**: Supports adding, editing, and removing translations for words across different languages.
- **User Hub**: Users can view their profile, edit settings, and manage the languages they are learning.
- **Learning Hub**: Facilitates the creation and management of word lists, reviewing learned words, practicing new vocabulary, and tracking learning progress.
- **Admin Panel**: Special administrative functions for managing users and viewing detailed user data.

## Setup and Installation

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What you need to install the software:

- Python 3.8+
- MySQL 8.0+
- mysql-connector-python

### Database Setup
1. Connect to your MySQL instance:
```bash
   mysql -u root -p
   ```

### Create a new database named test5 and use it:

```sql
CREATE DATABASE IF NOT EXISTS test5;
USE test5;
```
## Running the Application
1. Clone the repository or download the source code.
2. Navigate to the directory containing the code.
3. Run the Python script to start the application:
```bash
python main.py
```
## Usage
Upon launching the application, users are prompted to log in or sign up. Once authenticated, they can access various functionalities based on their user role (e.g., admin, standard user):

- Language Options: Access and manage language settings.
- Word & Definition Options: Manage words and their definitions in the database.
- Translation Options: Add or modify translations for better learning.
- User Hub: View and edit user profiles and settings.
- Learn Hub: Engage with learning modules and track progress.

## Contributing
Contributions to this project are welcome. You can enhance existing features or add new capabilities to enrich the user experience and functionality.

## License
We don't have one of those... but it would be cool!

## Authors
James Callender - Main Developer
Diego Acosta - Developer
Shem De Leon - Developer
Ryan Kluesner - Developer

Thanks to everyone who has contributed to this project with suggestions, code contributions, and bug reports.
