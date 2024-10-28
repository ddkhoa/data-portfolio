import duckdb

source_file_path = "./data/dvf.csv"

connection = duckdb.connect()
connection.execute(
    "CREATE TABLE house_sales_data AS SELECT * FROM read_csv_auto('./data/dvf.csv', sample_size=-1)",
)

# Observations:
# id_mutation is not unique: a mutation might concerns multiple parts
# there are some lines with 100% duplication -> need to deduplicate AND "bien multiple"
# bien multiples: share the same surface_terrain: https://explore.data.gouv.fr/fr/immobilier?onglet=carte&filtre=tous&lat=43.48678&lng=5.22371&zoom=18.54&code=13081000BN0198&level=parcelle
# our grain is not a sale but a property, what about the price ? calculate the prorate using surface_reelle_bati

# different type_local: appartement, maison, dependance, Local industriel. commercial ou assimilé. 
# we can filter out dependance rows (attached to the "main" property)
# in addition, we focus on appartement and maison rows

# we also filter on nature_mutation: Vente, Vente en l'état futur d'achèvement . We do not take Vente terrain a batir, Echange, Expropriation, Adjudication

# measures: number of rooms and surface
# surface_reelle_bati -> internal space, surface_terrain -> total space (including external space if exist)
# lot number, lot surface, number of lots are not important

selected_columns = [
    "id_mutation",
    "date_mutation",
    "nature_mutation",
    "valeur_fonciere",
    "adresse_numero",
    "adresse_suffixe",
    "adresse_nom_voie",
    "code_postal",
    "nom_commune",
    "id_parcelle",
    "type_local",
    "surface_reelle_bati",
    "nombre_pieces_principales",
    "surface_terrain",
    "longitude",
    "latitude"
]
selected_columns_str = ','.join(selected_columns)

connection.execute("CREATE TABLE house_sales_data_filtered AS"
                   f" SELECT {selected_columns_str} FROM house_sales_data" 
                   " WHERE (type_local = 'Appartement' OR type_local = 'Maison')" 
                   " AND (nature_mutation = 'Vente' OR nature_mutation = 'Vente en l''état futur d''achèvement')")
connection.execute("CREATE TABLE house_sales_data_unique AS (SELECT DISTINCT * FROM house_sales_data_filtered)")

connection.execute("ALTER TABLE house_sales_data_unique ALTER COLUMN valeur_fonciere SET DATA TYPE FLOAT")
connection.execute("ALTER TABLE house_sales_data_unique ALTER COLUMN surface_reelle_bati SET DATA TYPE FLOAT")
connection.execute("ALTER TABLE house_sales_data_unique ALTER COLUMN nombre_pieces_principales SET DATA TYPE INTEGER")
connection.execute("ALTER TABLE house_sales_data_unique ALTER COLUMN surface_terrain SET DATA TYPE FLOAT")

connection.execute("CREATE TABLE house_sales_price_per_m2 AS ("
                   " SELECT id_mutation id_mutation_2, MAX(valeur_fonciere) / SUM(surface_reelle_bati) price_per_m2"
                   " FROM house_sales_data_unique"
                   " GROUP BY id_mutation)")
final = connection.execute("SELECT l.*, ROUND(r.price_per_m2, 2) price_per_m2, ROUND((l.surface_reelle_bati * r.price_per_m2), 2) valeur_fonciere_part" 
                         " FROM house_sales_data_unique l"
                         " INNER JOIN house_sales_price_per_m2 r ON l.id_mutation = r.id_mutation_2"
                         " WHERE l.nombre_pieces_principales IS NOT NULL AND l.code_postal IS NOT NULL"
                         " ORDER BY l.id_mutation ASC" ).fetch_df()

final.to_csv("./data/clean.csv", index=False)
