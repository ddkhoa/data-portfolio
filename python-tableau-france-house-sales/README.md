# Data Visualization Project: House Prices in Bouches-du-Rhone, France

## Context - A Hands-On Approach to Data Visualization
In my journey to improve data visualization skills, I decided to turn theory into practice after reading chapters from *Communicating with Data*. Though insightful, I found the book a bit theoretical, so I supplemented it with Tableau tutorials ([this video](https://www.youtube.com/watch?v=KlAKAarfLRQ&t=276s) and [this video](https://www.youtube.com/watch?v=CmOAXW24y2Y)). Once I grasped the basics, I applied key concepts independently by building this dashboard, going beyond tutorial steps to troubleshoot and overcome unexpected challenges.

## Dataset
The dataset, ["Demandes de valeurs foncières géolocalisées"](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres-geolocalisees/#/information), is an open-source repository from the French government containing property sales data from 2019 to the present, updated biannually. This dataset provided a valuable opportunity to:

- Work with real-world data: cleaning, transforming, and analyzing a dataset.
- Apply the visualization principles learned to design a clear and impactful dashboard.

Key Data Considerations:
- **Deduplication**: Some rows had identical values, which I removed.
- **Transaction Details**: Each `id_mutation` could include multiple property parts with a shared price value. I adjusted these values to reflect property-specific prices by prorating them based on `surface_reelle_bati`.
- **Property & Transaction Types**: Limited the analysis to relevant property types (`Appartement` and `Maison`) and standard house sale transactions (`Vente`, `Vente en l'état futur d'achèvement`).
- **Measures**: For insights, I focused on `nombre_pieces_principales` (number of rooms) and `valeur_fonciere` (price).

## Data Cleaning & Transformation
This project presented a chance to explore **DuckDB** for data transformation instead of my usual tool, **Pandas**. DuckDB’s SQL capabilities allowed for efficient data manipulation using a familiar SQL syntax. Here’s a sample of the data cleaning workflow:

```python
import duckdb

connection = duckdb.connect()
# errors when the engine encounter an unexpected values after guessing type from the sample data
connection.execute("CREATE TABLE house_sales_data AS SELECT * FROM read_csv_auto('./data/dvf.csv', sample_size=-1)")

selected_columns = [ "id_mutation", "date_mutation", "nature_mutation", "valeur_fonciere", "adresse_numero",
    "adresse_suffixe", "adresse_nom_voie", "code_postal", "nom_commune", "id_parcelle", "type_local", 
    "surface_reelle_bati", "nombre_pieces_principales", "surface_terrain", "longitude", "latitude"]

connection.execute("CREATE TABLE house_sales_data_filtered AS"
                   f" SELECT {', '.join(selected_columns)} FROM house_sales_data"
                   " WHERE (type_local = 'Appartement' OR type_local = 'Maison')"
                   " AND (nature_mutation = 'Vente' OR nature_mutation = 'Vente en l''état futur d''achèvement')")

# Further deduplication, type conversion, and price calculation
# ...
```

## Dashboard Design
Building this dashboard enhanced my Tableau skills by requiring the implementation of each component from scratch. Key elements of the dashboard include:

### Median Price vs Transaction Volume Over Time
- **Purpose**: Analyze trends in property prices from 2019 to 2024 alongside transaction volumes.
- **Skill Gained**: Implemented dual-axis charts.

### Map Visualization by Town
- **Purpose**: Highlight geographic differences in property prices across towns and enabling users to filter specific towns.
I customized the tooltip to display clear information, including the town's name, median price, and median price per m².

### Distribution of House Prices
- **Purpose**: Simplify insights into the distribution of house prices.
- **Skill Gained**: Created Calculated Fields to transform continuous values into categorized price ranges, allowing for a more interpretable histogram that avoids data overload.

### Room Distribution
- **Purpose**: Visualize the distribution of properties by room count and enabling users to filter by the number of rooms.
- **Skill Gained**: Used Calculated Fields in Tableau to group room counts over six into a single category, which simplified the histogram by reducing the impact of outliers.

## Error encountered & Solutions

#### Manual axis tick
In some charts, I noticed that the gap between values was too small, so I applied a manual configuration. While this initially resolved the issue, the ticks shifted significantly when filters were applied. To ensure stability, I reverted to automatic mode, which maintained consistent tick gap even with filters.

#### Update the visualization when the dataset change
Initially, I didn’t include the `nom_commune` column in the visualization file. After adding it, all the charts broke, as if the data source hadn’t updated correctly. When I clicked the refresh button, I encountered an error: Unexpected Error [SQLSTATE:42601]. Adding the file to the workspace a second time resolved the issue, and I removed the duplicate table afterward. This behavior was unexpected.

## Results
The completed dashboard can be viewed on Tableau Public: [Bouches-du-Rhône, France House Sales Price Dashboard](https://public.tableau.com/app/profile/khoa8102/viz/bouches-du-rhone-house-sales/Dashboard). Below is a screenshot:

![Bouches-du-Rhône, France House Sales Price Dashboard](./bouches-du-rhone-house-sales-dashboard.png)

## Key Learnings & Skills Developed

This project strengthened my data proficiency by enabling me to move beyond tutorials and solve real-world data challenges. Key skills developed include:
- Explored DuckDB for data transformation and cleaning tasks..
- Enhanced Tableau skills with **dual-axis charts** and **custom calculated fields**, improved troubleshooting abilities.
- Applied visualization principles from *Communicating with Data*, which helped to refine clarity and improve the dashboard’s interpretability.

