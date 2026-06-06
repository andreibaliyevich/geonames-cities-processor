from pathlib import Path

import pandas as pd


def load_geonames_data():
    # Configuration
    MIN_POPULATION = 1
    ALLOWED_F_CODES = ["PPL", "PPLA", "PPLA2", "PPLC"]

    # Paths
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    OUTPUT_DIR = BASE_DIR / "output"
    COUNTRIES_FILE = DATA_DIR / "countryInfo.txt"
    ADMIN1_FILE = DATA_DIR / "admin1CodesASCII.txt"
    ADMIN2_FILE = DATA_DIR / "admin2Codes.txt"
    ALL_COUNTRIES_FILE = DATA_DIR / "allCountries.txt"
    OUTPUT_FILE = OUTPUT_DIR / "world_cities.csv"

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1: Loading reference dictionaries...")

    # Load Countries
    countries = pd.read_csv(
        COUNTRIES_FILE,
        sep="\t",
        skiprows=50,
        header=None,
        usecols=[0, 1, 4],
        keep_default_na=False,
    )
    countries.columns = ["iso2", "iso3", "country_name"]

    # Load Regions and Districts
    admin1 = pd.read_csv(
        ADMIN1_FILE,
        sep="\t",
        header=None,
        names=["full_code", "admin_name", "ascii_name", "id"],
    )
    admin2 = pd.read_csv(
        ADMIN2_FILE,
        sep="\t",
        header=None,
        names=["full_code", "admin_name2", "ascii_name", "id"],
    )

    print("Step 2: Processing allCountries.txt (Filtering populated places)...")

    cols = [
        "name",
        "asciiname",
        "alternatenames",
        "latitude",
        "longitude",
        "feature_class",
        "feature_code",
        "country_code",
        "admin1_code",
        "admin2_code",
        "population",
        "timezone",
    ]

    df = pd.read_csv(
        ALL_COUNTRIES_FILE,
        sep="\t",
        header=None,
        names=[
            "geonameid",
            "name",
            "asciiname",
            "alternatenames",
            "latitude",
            "longitude",
            "feature_class",
            "feature_code",
            "country_code",
            "cc2",
            "admin1_code",
            "admin2_code",
            "admin3_code",
            "admin4_code",
            "population",
            "elevation",
            "dem",
            "timezone",
            "modification_date",
        ],
        usecols=cols,
        dtype={"admin1_code": str, "admin2_code": str},
        keep_default_na=False,
        low_memory=False,
    )

    # Filtering logic
    mask = (
        (df["feature_class"] == "P")
        & (df["feature_code"].isin(ALLOWED_F_CODES))
        & (df["population"] >= MIN_POPULATION)
    )
    df = df[mask].copy()

    # Create join keys
    df["admin1_key"] = (
        df["country_code"].astype(str) + "." + df["admin1_code"].astype(str)
    )
    df["admin2_key"] = (
        df["admin1_key"].astype(str) + "." + df["admin2_code"].astype(str)
    )

    print("Step 3: Merging data...")

    df = df.merge(countries, left_on="country_code", right_on="iso2", how="left")
    df = df.merge(
        admin1[["full_code", "admin_name"]],
        left_on="admin1_key",
        right_on="full_code",
        how="left",
    )
    df = df.merge(
        admin2[["full_code", "admin_name2"]],
        left_on="admin2_key",
        right_on="full_code",
        how="left",
    )

    # Column selection and cleanup
    result = df[
        [
            "name",
            "asciiname",
            "alternatenames",
            "latitude",
            "longitude",
            "timezone",
            "country_name",
            "iso2",
            "iso3",
            "admin_name",
            "admin_name2",
            "population",
        ]
    ].copy()

    result.columns = [
        "name",
        "ascii_name",
        "alternate_names",
        "latitude",
        "longitude",
        "time_zone",
        "country_name",
        "country_code_iso2",
        "country_code_iso3",
        "region_name",
        "district_name",
        "population",
    ]

    # Final result save
    print(f"Step 4: Saving {len(result)} records to {OUTPUT_FILE}...")
    result.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print("Done! Processing complete.")


if __name__ == "__main__":
    load_geonames_data()
