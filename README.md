# Taiwan Air Quality Index Data 2016~2024

This is a practice for Statistics and ML skills.

Data from:
`https://www.kaggle.com/datasets/taweilo/taiwan-air-quality-data-20162024`

Steps:
1. Run to install needed dependencies
```
pip install -r requirements.txt
```
2. Run, keep in hand your kaggle token to login
```
python utils/download_dataset.py taweilo/taiwan-air-quality-data-20162024
```
<!-- 3. Run the full EDA.ipynb notebook to get air_quality.pkl
```
jupyter nbconvert --execute utils/EDA.ipynb
```
4. Run dashboard
```
streamlit run utils/st_dashboard.py
``` -->

## Streamlit Dashboard
<img src="/data/images/taiwan_aqi_st_dashboard.png">


> _"Practice isn't the thing you do once you're good/ It's the thing you do that makes you good."_ - Malcom Gladwell
