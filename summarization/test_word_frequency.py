from WordFrequencySummarization import WordFrequencySummarization

ob = WordFrequencySummarization()

with open('/Users/shashanks./college/semester-8/Software-Engineering/project/summarize/inp1.txt', 'r') as f:
    text = f.read()

summary = ob.summarize(text)
print(summary)