# Retail Customer Experience Analytics

An end-to-end customer-insights project built in R. The analysis compares satisfaction across four retail brand aliases, investigates operational experience measures, evaluates customer segments, and translates the findings into a measurable 90-day pilot.

## The decision

A VP of Customer Experience can fund one 90-day intervention. Acting as the independent analyst, I framed the business question, defined the research design, tested whether the brand differences were meaningful, modeled experience drivers, evaluated possible customer segments, and converted the result into a pilot plan.

**Recommendation:** prioritize Urban Basket's availability gap rather than apply one program across all brands. Test real-time stock alerts and price-protected substitutions with digital customers who recently experienced an unavailable item. The proposed design uses a randomized holdout, a 0.20-point satisfaction threshold defined before launch, and repeat visits as a business guardrail.

> Independent case study using generated data modeled on common retail survey patterns. No confidential or real customer records are used.

## Project highlights

- Analyzed 2,189 quality-approved survey responses across four brands and three purchasing channels.
- Identified a 0.83-point weighted satisfaction gap between the highest- and lowest-performing brands.
- Connected Urban Basket's weaker availability scores and 34% reported stockout incidence to a focused intervention opportunity.
- Designed a customer-level randomized pilot with power analysis, attrition planning, success criteria, and operational guardrails.

## Skills demonstrated

- Data generation, quality assurance, and survey weighting
- Customer-experience and NPS-style summaries
- Brand and channel comparisons
- Weighted multivariable regression and holdout validation
- Confidence intervals and standardized effect estimates
- Principal component analysis
- K-means clustering with silhouette-based model selection
- Experiment design, power analysis, and decision storytelling

## View the report

Open [`index.html`](index.html), or publish this repository with GitHub Pages using the repository root as the deployment source.

## Reproduce locally

Requires R 4.2+ plus `rmarkdown` and `knitr`.

```r
source("scripts/generate_data.R")
rmarkdown::render("report.Rmd")
file.copy("report.html", "index.html", overwrite = TRUE)
```

## Project structure

```text
data/retail_experience_survey.csv     Analysis dataset
scripts/generate_data.R               Reproducible data generator
report.Rmd                            Source analysis and narrative
styles.css                            Report presentation layer
index.html                            Pre-rendered GitHub Pages report
```

## Data provenance

This is a simulated portfolio case study; no real customers or companies are represented. The source generator is included so every observation and fieldwork artifact can be reproduced and audited.

