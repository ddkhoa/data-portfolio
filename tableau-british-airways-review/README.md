# Data Visualization: British Airways Service Review

**Source:** [YouTube Video](https://www.youtube.com/watch?v=KlAKAarfLRQ&t=276s)

In this project, I followed a YouTube tutorial to set up a Tableau dashboard for British Airways executives. The dashboard visualizes service **performance reviews**. While I applied the tutorial’s Tableau manipulations, I modified several visual elements based on the principles from the book [*Communicating with Data*](https://www.oreilly.com/library/view/communicating-with-data/9781098101848/).

## Visual Design & Customization
- **Summary Metric**: Used [British Airways' brand color (#0035AD)](https://www.brandcolorcode.com/british-airways) as the background to establish a cohesive theme aligned with the company’s identity.
  
- **Average Custom Metric by Month**: Maintained consistent blue hues across monthly charts for a visually unified look.

- **Average Custom Metric by Country**: Removed coastline details from the map to avoid unnecessary complexity. Applied the company’s blue color scheme instead of green to enhance brand coherence.

- **Average Custom Metric by Aircraft**: Chose a single shade of blue instead of gradient coloring, which would introduce double encoding with bar length and increase cognitive load. Used red for the number of reviews chart, aligning with the company’s branding. Added the number of reviews in the tooltips of the custom metric charts but chose not to display the custom metric in the review count chart to avoid redundant information.

## Result
The completed dashboard can be viewed on Tableau Public: [British Airways Review Dashboard](https://public.tableau.com/app/profile/khoa8102/viz/BritishAirwaysReviewDashboard_17297625359330/Dashboard1). Below is a screenshot:

![British airways review dashboard](./british-airways-review-dashboard.png)

## Key Learnings
This project helped solidify my understanding of basic Tableau concepts:
- **Data Sources**
- **Dimensions**
  - Grouping elements, converting strings to graphical roles, and configuring date field behavior.
  - Using categories as filters.
- **Measures**
- **Parameters**
- **Calculated Fields**

Additionally, I applied several visualization principles from *Communicating with Data* to improve the clarity and effectiveness of the dashboard.
