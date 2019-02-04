import sys
import speech_recognition as sr

sys.path.append('../tagger/')
sys.path.append('../')
import tagger
import synset

# obtain audio from the microphone
r = sr.Recognizer()
k_nearest = 10

with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

query = ""
# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    query = r.recognize_google(audio)
    print("Google Speech Recognition thinks you said: " + query)
    print()
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


result = tagger.clean_tokens(query)
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
