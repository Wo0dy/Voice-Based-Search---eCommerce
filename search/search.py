import sys

sys.path.append('../tagger/')
sys.path.append('../')
import tagger
import synset

k_nearest = 10

result = tagger.clean_tokens()
print()
for i in range(len(result)):
    word = result[i]['noun']
    result[i]['error'] = "none"
    nearest_words_list = synset.nearest_words(word)
    if isinstance(nearest_words_list, type("")):
        result[i]['error'] = nearest_words_list
        result[i]['list'] = []
    else:
        nearest_words_list = nearest_words_list[:k_nearest]
        result[i]['list'] = nearest_words_list

if __name__ == "__main__":
    for i in range(len(result)):
        if 'adjective' in result[i]:
            print("phrase : ", result[i]['adjective'], result[i]['noun'])
        else:
            print("phrase : ", result[i]['noun'])
        print("error : ", result[i]['error'])
        print("list : ", result[i]['list'])
        print()
