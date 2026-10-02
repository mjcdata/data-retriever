# Data Retriever Glossary

This glossary is for terminology needed to understand the actual data, its source, its fields, and its measurements.

Each entry should spell out the acronym or abbreviation and explain in plain language what it is and how it relates to the data.

Do not add general project-management, workflow, programming, or file-format terminology unless it is necessary to interpret the dataset itself.

## Data Acronyms and Abbreviations

| Term | Full name | What it is / relationship to the data |
| --- | --- | --- |
| GHCNd | Global Historical Climatology Network Daily | The NOAA daily climate observation dataset used by the U.S. Daily Weather project. Also written as GHCN-Daily. |
| NCEI | National Centers for Environmental Information | The NOAA organization that maintains and provides access to historical environmental and climate data, including GHCN-Daily. |
| NOAA | National Oceanic and Atmospheric Administration | The U.S. federal agency that is the authoritative upstream source for the weather data used by the U.S. Daily Weather project. |
| PRCP | Precipitation | GHCN-Daily element code for daily precipitation. In the NOAA source used here, values are stored in tenths of millimeters. |
| SNOW | Snowfall | GHCN-Daily element code for daily snowfall, stored in millimeters. |
| SNWD | Snow depth | GHCN-Daily element code for snow depth, stored in millimeters. |
| TMAX | Maximum temperature | GHCN-Daily element code for daily maximum temperature, stored in tenths of degrees Celsius. |
| TMIN | Minimum temperature | GHCN-Daily element code for daily minimum temperature, stored in tenths of degrees Celsius. |
| MFLAG | Measurement flag | GHCN-Daily attribute that records special information about how an observation was measured or represented. |
| QFLAG | Quality flag | GHCN-Daily attribute that identifies an observation that failed a NOAA quality-assurance check; blank means it did not fail a listed check. |
| SFLAG | Source flag | GHCN-Daily attribute identifying the source selected for an observation. |

## Maintenance Rule

Add an entry when an acronym, abbreviation, field code, measurement code, source name, or domain-specific term is needed to understand a dataset.

For each abbreviation or acronym, include:
1. the abbreviation or acronym;
2. the full spelled-out name;
3. a plain-language explanation of what it is or how it relates to the data.

Do not add conversational or project-management shorthand such as POC, or general programming and storage terms such as DataFrame or Parquet, unless a term is itself required to interpret the dataset.
