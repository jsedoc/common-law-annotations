1. Download AMT data excel files within folders named `group1/`, `group2/` etc.
2. Make sure all **Researcher** annotation data is available inside `data_scripts/annotations/`
3. Run `create_crowdsource_data.py` to parse AMT data and find common annotated prompts between *worker* and *researcher*
4. Run `crowdsource_calculate_cohen_kappa.py` to calculate cohen's kappa between