from YakeSummarization import YakeSummarization

ob = YakeSummarization()

with open('/Users/shashanks./college/semester-8/Software-Engineering/project/summarize/inp1.txt', 'r') as f:
    text = f.read()

keywords = ob.summarize(text)
print(keywords)