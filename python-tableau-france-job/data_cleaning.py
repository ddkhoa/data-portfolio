import duckdb

source_file_path = "./data/valeurs_trimestrielles.csv"

connection = duckdb.connect()
connection.execute(
    f"CREATE TABLE job_data AS SELECT * FROM read_csv_auto('{source_file_path}')",
)


# Observations:
# Column Libellé contains multiple info: the series's name, the industry, the location and the type of series (Série arrêtée)
# We need to split the info in different columns
# We need to unpivot the table to have 1 value by row
# Target format
# Industry (string)
# Region (string)
# Quarter (string)
# Value (int)
# Last_Update (date)

connection.execute("ALTER TABLE job_data DROP COLUMN idBank")
connection.execute("ALTER TABLE job_data DROP COLUMN Période")
connection.execute("ALTER TABLE job_data RENAME COLUMN Libellé TO label")
connection.execute(
    "ALTER TABLE job_data RENAME COLUMN 'Dernière mise à jour' TO last_updated_at"
)

connection.execute("ALTER TABLE job_data RENAME COLUMN '2001-T4' TO '2001-10-01'")
dates = ["2001-10-01"]
for year in range(2002, 2024):
    for quarter in range(1, 5):
        date = f"{year}-{str.rjust(str(quarter*3-2), 2, '0')}-01"
        connection.execute(
            f"ALTER TABLE job_data RENAME COLUMN '{year}-T{quarter}' TO '{date}'"
        )
        dates.append(date)
connection.execute("ALTER TABLE job_data RENAME COLUMN '2024-T1' TO '2024-01-01'")
connection.execute("ALTER TABLE job_data RENAME COLUMN '2024-T2' TO '2024-04-01'")
dates.extend(["2024-01-01", "2024-04-01"])

# we need to wrap the string by "" to handle columns with - character
dates_value_str = ",".join(f'"{item}"' for item in dates)
dates_column_str = ",".join(f"'{item}'" for item in dates)

label_split_character = "' - '"
connection.execute(
    "CREATE TABLE job_data_unpivot AS"
    f" (SELECT split_part(label, {label_split_character}, 2) AS industry, split_part(label, {label_split_character}, 3) AS region, last_updated_at,"
    f" unnest(array[{dates_column_str}]) AS 'date', unnest(array[{dates_value_str}]) AS 'value'"
    f" FROM job_data WHERE label != 'Codes')"
)
connection.execute("ALTER TABLE job_data_unpivot ALTER COLUMN value TYPE INTEGER")

regions = [
    "Auvergne-Rhône-Alpes",
    "Bourgogne-Franche-Comté",
    "Bretagne",
    "Centre-Val de Loire",
    "Corse",
    "Grand Est",
    "Hauts-de-France",
    "Île-de-France",
    "Normandie",
    "Nouvelle-Aquitaine",
    "Occitanie",
    "Pays de la Loire",
    "Provence-Alpes-Côte d''Azur",
]
regions_str = ",".join(f"'{item}'" for item in regions)

industries = [
    "Agriculture (A5-AZ)",
    "Industries manufacturières, industries extractives et autres (A5-BE)",
    "Construction (A5-FZ)",
    "Tertiaire marchand (A5-GU)",
    "Tertiaire non marchand (A5-OQ)",
    # "Agriculture, sylviculture et pêche (A17-AZ)",
    # "Fabrication de denrées alimentaires, de boissons et de produits à base de tabac (A17-C1)",
    # "Industries extractives, énergie, eau, gestion des déchets et dépollution ; Cokéfaction et raffinage (A17-C2DE)",
    # "Fabrication d''équipements électriques, électroniques, informatiques ; fabrication de machines (A17-C3)",
    # "Fabrication de matériels de transport (A17-C4)",
    # "Fabrication d''autres produits industriels (A17-C5)",
    # "Construction (A17-FZ)",
    # "Commerce ; réparation d''automobiles et de motocycles (A17-GZ)",
    # "Transports et entreposage (A17-HZ)",
    # "Hébergement et restauration (A17-IZ)",
    # "Information et communication (A17-JZ)",
    # "Activités financières et d''assurance (A17-KZ)",
    # "Activités immobilières (A17-LZ)",
    # "Activités scientifiques et techniques ; services administratifs et de soutien (A17-MN)",
    # "Activités scientifiques et techniques ; services administratifs et de soutien ; hors intérim (A17-MNO)",
    # "Administration publique, enseignement, santé humaine et action sociale (A17-OQ)",
    # "Autres activités de services (A17-RU)",
]
industries_str = ",".join(f"'{item}'" for item in industries)

df = connection.execute(
    f"SELECT *, value - (LAG(value, 1) OVER (PARTITION BY industry, region ORDER BY date)) delta, SUM(value) OVER (PARTITION BY region, date) all_industries_value"
    " FROM job_data_unpivot"
    f" WHERE region IN ({regions_str})"
    f" AND industry IN ({industries_str})"
    " AND date >= '2011-01-01' ORDER BY industry, date"
).fetch_df()


df.to_csv("./data/clean.csv", index=False)
