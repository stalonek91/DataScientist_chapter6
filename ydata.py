from ydata_profiling import ProfileReport
import pandas as pd

csv_path = '35__welcome_survey_cleaned.csv'

df = pd.read_csv(csv_path, sep=';')

report = ProfileReport(df, title="Data report ankieta", explorative=True)
report.to_file('report.html')


statistics = report.get_description()

print(statistics)