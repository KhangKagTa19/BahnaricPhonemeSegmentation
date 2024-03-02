import pandas as pd
df = pd.read_parquet('KT_Bana_F1_part1_pham_2_pham.parquet', engine='pyarrow')
print(df)