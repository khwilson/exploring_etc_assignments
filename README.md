# Brief exploration of dialysis facilities

In this repo we briefly examine [Medicare's End-Stage Renal Disease Treatment Choices (ETC)](https://innovation.cms.gov/innovation-models/esrd-treatment-choices-model). In particular, we look at the distribution of assignment to treatment following up on [this paper](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2794962) in JAMA Network Open from Wilk, et al.

That paper didn't publicly provide data or code that I could find, so I attempted to, as best as possible, recreate one of their analyses. In particular, I was curious how "strange" it was that the second largest provider of dialysis "ETC-assigned facilities were 14% (5.1 [95% CI, 0.9-9.4] percentage points) more likely than control facilities to be owned by the second largest dialysis organization." The paper calculates this outcome based on a categorical χ² test with a Bonferroni correction for 27 comparisons. This is appropriate if you want to measure deviation from a "balanced experiment." But given that there were only 306 units of randomization (healthcare referral regions), I was curious as to how unexpected this was for a simple randomized experiment.

## Requirements and Running Code

This repository uses Python 3.8+ and its dependencies are managed by [poetry](https://python-poetry.org/). Once you have poetry installed, you should be able to run the following commands to run the analysis:

```bash
cd data
mkdir dialysis_current_facilities
cp dialysis_facilities_current_data.zip
cd dialysis_current_facilities
unzip dialysis_facilities_current_data.zip
cd ..; cd..
poetry install
poetry run jupyter notebook
```

Then in a browser you can `Restart and Run All` the notebooks in `src/notebooks` in the order they appear.

## Data

The data come from three sources as described below

### Dialysis Facilities Data

Provided directly from [CMS](https://data.cms.gov/provider-data/topics/dialysis-facilities). A copy is included with this repo for convenience.

### Hospital Referral Region Shapefiles

Provided by [Cartography Vectors](https://cartographyvectors.com/map/1580-us-hospital-referral-regions-hrr). A copy is included with this repo for convenience.

### Geocodings

The [Census Geocoder](https://geocoding.geo.census.gov/geocoder/) was used to geocode all the addresses in the Dialysis Facilities data. This was done with the [censusgeocode](https://pypi.org/project/censusgeocode/) package in Python.

Note that (as can bee seen in notebook 100), the Census geocoder misses on about 20% of the addresses. Typing a few of these into Google Maps indicates that (a) they are geocodable and (b) they are in fact the dialysis facilities indicated in the CMS data. This is a very big limitation of this quick exploration, but it's quick, so that's how it goes. :-)

## Exploration

We look at *all* dialysis facilities, not the filtered list that Wilk et al look at, as doing so requires requesting restricted data. Moreover, I could not find the filtered list available on the internet.

### Notebook 100

This notebook is just a geocoder. This takes about 30min to run. The output has been provided at `data/dialysis_facilities_geocoded.parquet`. This is all that is used in Notebook 200.

### Notebook 200

This notebook actually does the aforementioned exploration. We randomly select 30% of the 306 HRRs for inclusion into the "study" and we ask what percentage of the facilities in the treatment HRRs and control HRRs are owned by the second-largest dialysis treatment company (Fresnius). We compare this to the numbers described in Table 2 of the paper in the final cell of the notebook, which shows a 5.2% difference in the chosen sample, which the authors find significant even with a Bonferroni correction for 27 comparisons.

But as seen in the final cell of the notebook, you would expect a deviation of this size in about 6% of all random draws. So not crazy at all when looking at 27 comparisons.

Before the final cell of the notebook, we look at some limitations of this very quick analysis. E.g., our HRR shapefile clearly misplaced Alaska and Hawaii and didn't include Puerto Rico. And as mentioned above, about 20% of the facility addresses could not be found by the Census geocoder. But about 20% of our top dialysis providers couldn't be found, so for this quick look, we're not super fussed. A serious analysis would need to correct this.

## Takeaways and Follow Ups

It's very, very, very hard to balance 27 covariates when you only have 306 clusters, and so you expect a few imbalanced covariates. Indeed, we looked at what would happen if you just had a fully randomized design not attempting to balance anything, and found that the percentage of Fresnius treatment and control facilities in the actual experiment are very within the realm of possibility.

Thus, I'd be curious to know what would happen if Wilk et al compared the ETC assignments _not_ in an abstract balance test, but against and optimal design, e.g., with the `designmatch` package. Which is to say, how close *can* you get to optimal? And if you were to use a balanced design, how *deterministic* would the design be, which in turn spoils the notion of an RCT in the first place.
