# geonames-cities-processor
 GeoNames Cities Processor


## Project Overview

A Python script to process GeoNames raw data into a clean, filtered CSV file
suitable for dating services, local discovery apps, or any database requiring
global city information with coordinates and timezones.


## Features

- Filters only populated places (PPL, PPLA, PPLA2, PPLC).
- Maps numeric region and district codes to their ASCII names.
- Fixes common issues like Namibia (NA) ISO code loss.
- Optimized for large files using Pandas.


## CSV Schema

The output is saved as `output/world_cities.csv` and contains the following columns:

- `name`: Local city name.
- `ascii_name`: Name in ASCII characters.
- `alternate_names`: Comma-separated list of names in different languages (up to 10k chars).
- `latitude` / `longitude`: WGS84 coordinates (Decimal).
- `time_zone`: IANA timezone ID (e.g., `Europe/Minsk`).
- `country_name`: Full country name.
- `country_code_iso2`: 2-letter ISO code.
- `country_code_iso3`: 3-letter ISO code.
- `region_name`: State, Province, or Oblast (Administrative Division 1).
- `district_name`: County or District (Administrative Division 2).
- `population`: Number of inhabitants.


## Installation

The project is launched using a Python virtual environment.

### Requirements

- Python 3.8+
- Pandas library: `pip install pandas`

### Setup Instructions

##### 1. Clone the repository

    git clone https://github.com/andreibaliyevich/geonames-cities-processor.git

##### 2. Navigate to the project directory

    cd geonames-cities-processor

##### 3. Create a data directory in the project root

    mkdir data

##### 4. Download the following files from [GeoNames Export](https://download.geonames.org/export/dump/) and place them into the `data/` folder

- `allCountries.zip` (unzip to `allCountries.txt`)
- `countryInfo.txt`
- `admin1CodesASCII.txt`
- `admin2Codes.txt`

##### 5. Create a virtual environment

    python -m venv venv

##### 6. Activate the virtual environment

    source venv/bin/activate

##### 7. Install dependencies

    pip install -r requirements.txt

##### 8. Run the script

    python main.py


## License

This project is licensed under the
[The MIT License](https://opensource.org/license/mit).

Data provided by GeoNames under CC BY 4.0.
