# Bank Holiday Updater

## In England And Wales, Scotland And Northern Ireland

The Bank Holiday Updater is a Python class designed to fetch bank holiday data from a specified free API endpoint, cache it in a SQLite database, and periodically update the database with the latest bank holiday information.

## Endpoint that can be used with this example

[The Bank Holidays API](https://www.api.gov.uk/gds/bank-holidays/#bank-holidays)

## Installation

You can install the Bank Holiday Updater using pip:

```
python3 -m venv env
. ./env/bin/activate or source ./env/bin/activate
pip install -r requirements.txt
```

## Usage

```
python ./bank_holiday_updater.py
```

# Create an instance of BankHolidayUpdater

updater = BankHolidayUpdater()

# Start the updater

updater.main()

## Configuration

An **.env** file needs to be created. This can be done by copy the **.env.example** to **.env** and swap the default url to another. For example: [The Bank Holidays API](https://www.api.gov.uk/gds/bank-holidays/#bank-holidays).
You can configure the Bank Holiday Updater by providing the following parameters:

- `time_loop`: Time interval (in seconds) for periodic updates (default is 60 seconds).
- `database_name`: Name of the SQLite database file (default is "bank_holidays.db").
- `api_url`: URL of the API endpoint to fetch bank holiday data (default is "https://example.com/endpoint").

You can pass these parameters when creating an instance of `BankHolidayUpdater`:

python

Copy code

`updater = BankHolidayUpdater(time_loop=300, database_name="custom_database.db", api_url="https://example.com/endpoint")`

## Testing

To run the unit tests, please clone the repository and run the following command:

Copy code

`pytest or pytest ./test_bank_holiday_updater.py`

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

The data of [The Bank Holidays API](https://www.api.gov.uk/gds/bank-holidays/#bank-holidays) is [© Crown copyright](http://www.nationalarchives.gov.uk/information-management/re-using-public-sector-information/copyright-and-re-use/crown-copyright/) and available under the terms of the [Open Government 3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) licence.
