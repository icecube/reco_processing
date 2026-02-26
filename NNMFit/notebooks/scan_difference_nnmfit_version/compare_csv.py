import pandas as pd
import sys

df1 = pd.read_csv(sys.argv[1])
df2 = pd.read_csv(sys.argv[2])

if df1.equals(df2):
    print("DataFrames are identical")
else:
    print("DataFrames are NOT identical")

    diff = pd.concat([df1, df2]).drop_duplicates(keep=False)
    if not diff.empty:
        print("\nDifferences:")
        print(diff)