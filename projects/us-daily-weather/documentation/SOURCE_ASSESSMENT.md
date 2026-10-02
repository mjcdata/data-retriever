# U.S. Daily Weather — Source Assessment

## Assessment date
2026-10-02

## Project need
Identify an authoritative, nationwide U.S. source of daily historical weather observations that can support an approximately ten-year training window, repeatable updates, and future forecasting work involving temperature, precipitation, snowfall, and related daily measures.

## Sources assessed

### 1. NOAA NCEI Global Historical Climatology Network Daily (GHCNd)

**Publisher:** NOAA National Centers for Environmental Information (NCEI)

**Coverage:** Global station-based daily climate summaries, including extensive U.S. coverage. NOAA describes GHCNd as containing more than 100,000 stations across 180 countries and territories and as its most complete collection of U.S. daily climate summaries.

**Relevant variables:** Daily maximum temperature, minimum temperature, precipitation, snowfall, snow depth, and additional station variables when reported.

**Update behavior:** Updated daily. NOAA also reconstructs the dataset each weekend from its constituent sources. Recent U.S. observations can arrive through real-time feeds and later be replaced by archive-quality observations, commonly 45–60 days after the end of a month.

**Quality/provenance:** Integrated from numerous source datasets and subjected to NOAA quality-assurance checks. Values include flags that preserve quality, measurement, and source information.

**Access:** HTTPS bulk files, including per-station files, annual compressed CSV files, and a complete compressed archive; also accessible through NOAA Climate Data Online.

**Practical retrieval:** Bulk annual files are preferable to the CDO API for the initial nationwide historical load. The CDO API requires a token, is limited to 5 requests per second and 10,000 requests per day, limits individual result pages to 1,000 records, and limits daily-data requests to one year.

**Size consideration:** The complete global GHCNd compressed archive is roughly 3.7 GB as observed during source assessment. Recent annual global compressed CSV files are roughly 160–175 MB for complete years. The U.S.-only ten-year subset will be smaller than the global files but is still large enough that raw data should not automatically be committed to GitHub.

**Limitations:** Coverage and variables vary by station. Many stations report precipitation without a complete set of temperature or snow variables. Near-real-time values can later change as archive-quality observations replace preliminary feeds.

### 2. NOAA NCEI nClimGrid-Daily

**Publisher:** NOAA NCEI

**Coverage:** Gridded daily fields for the contiguous United States (CONUS), 1951–present.

**Relevant variables:** Daily maximum, minimum, and average temperature plus precipitation.

**Access:** Monthly NetCDF bulk files and THREDDS access for filtered retrieval.

**Strengths:** Spatially regular grid, designed for climate monitoring, and useful where consistent geographic coverage is more important than station-level observations.

**Limitations for this project:** It covers CONUS rather than the entire United States and does not provide the snowfall and snow-depth variables required by the approved project scope. It is therefore not the primary source for this project.

### 3. NOAA NCEI United States Historical Climatology Network (USHCN)

**Publisher:** NOAA NCEI

**Coverage/use:** Long-term U.S. climate station series with adjustments intended to improve climate-record homogeneity.

**Update behavior:** Weekly.

**Strengths:** Useful for long-term climate analysis.

**Limitations for this project:** It is a specialized climate network rather than the broadest source of current nationwide daily station observations. GHCNd provides broader operational coverage and more directly matches the project's updateable daily-data objective.

### 4. NOAA NCEI Global Historical Climatology Network Hourly (GHCNh)

**Publisher:** NOAA NCEI

**Coverage/use:** Hourly station observations with variables such as temperature, precipitation, humidity, pressure, wind, visibility, and present weather.

**Strengths:** Richer meteorological feature set that could later improve a forecasting model.

**Limitations for this project:** Hourly granularity substantially increases volume and complexity, while the approved first project calls for daily weather data. Treat GHCNh as a possible future enrichment source rather than the initial dataset.

## Recommendation

Use **NOAA NCEI GHCNd as the primary source**.

It most closely matches the approved requirements: authoritative U.S. daily observations, long historical coverage, daily updates, temperature and precipitation, U.S. snowfall and snow-depth observations where available, quality/source flags, and bulk retrieval options suitable for building a reproducible pipeline.

For the initial historical load, prefer NOAA's bulk distribution over the CDO API. Design the pipeline to filter to U.S. stations and the approved approximately ten-year period while retaining station metadata and NOAA quality/source flags. Use the latest bulk data for incremental refreshes or a targeted retrieval mechanism after profiling the source structure.

## Important modeling implication

GHCNd is station-based observational data, not a ready-made nationwide forecast table. Coverage and variable completeness differ by station. Before modeling, the project must define how stations are selected and how geographic prediction targets will be represented. That decision belongs to later profiling/model-design work and should not be silently resolved during retrieval.

## Phase 1 decision

**Recommended source:** NOAA NCEI Global Historical Climatology Network Daily (GHCNd)

**Status:** Source discovery complete; proceed to Phase 2 storage decision and retrieval architecture.
