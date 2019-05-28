import pandas as pd

df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
                     'B': ['B0', 'B1', 'B2', 'B3'],
                     'C': ['C0', 'C1', 'C2', 'C3'],
                     'D': ['D0', 'D1', 'D2', 'first']},
                    index=[0, 1, 2, 3])


df2 = pd.DataFrame({'A': ['A3', 'A5', 'A6', 'A7'],
                     'B': ['B4', 'B5', 'B6', 'B7'],
                     'C': ['C4', 'C5', 'C6', 'C7'],
                     'D': ['second', 'D5', 'D6', 'D7']},
                    index=[1,2,3,4])

df3 = pd.concat([df1,df2])

print('-----------------------------------------')
print('Here is the joined dataframes (with duplicates) :')
print(df3)
print('-----------------------------------------')
print('\n')

print('-----------------------------------------')
print('Here is the joined dataframes (without duplicates, keeping first instance) :')
df3.drop_duplicates(subset=['A'], inplace=True, keep='first')
print(df3)
print('-----------------------------------------')

print('-----------------------------------------')
print('Here is the joined dataframes (with reset index) :')
df3.reset_index(inplace=True,drop=True)
print(df3)
print('-----------------------------------------')