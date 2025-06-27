from datasets import load_dataset

for i in range(10):
    print(load_dataset('arbml/Lebanon_Uprising_Arabic_Tweets', split='train')[i])