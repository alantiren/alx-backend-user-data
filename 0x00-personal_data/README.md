# Personal Data Logger

This project provides functionalities for logging and filtering personal data in a secure manner. It includes modules for encrypting passwords, redacting sensitive information in log messages, connecting to a secure database, and more.

## Table of Contents
- [Requirements](#requirements)
- [Usage](#usage)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Requirements
- Python 3.7
- Pycodestyle 2.5
- MySQL Connector Python (Install with `pip3 install mysql-connector-python`)
- Bcrypt (Install with `pip3 install bcrypt`)

## Usage

### Setting Up the Database
```bash
# Run the SQL script to set up the MySQL server and create a users table
cat main.sql | mysql -uroot -p
```

### Running the Application
```bash
# Run the main application
PERSONAL_DATA_DB_USERNAME=root PERSONAL_DATA_DB_PASSWORD=root PERSONAL_DATA_DB_HOST=localhost PERSONAL_DATA_DB_NAME=my_db ./filtered_logger.py
```

### Example Output
```text
[HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: name=***; email=***; phone=***; ssn=***; password=***; ip=60ed:c396:2ff:244:bbd0:9208:26f2:93ea; last_login=2019-11-14 06:14:24; user_agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36;
[HOLBERTON] user_data INFO 2019-11-19 18:37:59,621: name=***; email=***; phone=***; ssn=***; password=***; ip=f724:c5d1:a14d:c4c5:bae2:9457:3769:1969; last_login=2019-11-14 06:16:19; user_agent=Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-I9100 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30;
```

## Files
- [filtered_logger.py](filtered_logger.py): Module for logging and filtering personal data.
- [encrypt_password.py](encrypt_password.py): Module for encrypting passwords using bcrypt.

## Contributing
Contributions are welcome! If you find any issues or have improvements to suggest, please create an issue or submit a pull request.
