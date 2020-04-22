from YakeSummarization import YakeSummarization

ob = YakeSummarization()

with open('test1.txt', 'r') as f:
    text = f.read()

keywords = ob.generate_tags(text)
print(keywords)
