import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

from charts import page_2



pg = st.navigation([st.Page(page_2, title='Charts analysis'),
                    st.Page("basic_info.py", title='DF basic info')])
pg.run()








