import codecs

N = 150000
file = codecs.open("data/wiki-news-300d-1M.vec", "r", encoding='utf-8', errors='ignore')
file1 = codecs.open("data/wiki-short1.vec", "w", encoding='utf-8', errors='ignore')
ct = 0
for i in range(N):
    try:
        line = file.readline()
        file1.write(line)
    except:
        print("Error at ", i)
        ct += 1
file.close()
file1.close()
print(ct)
