from satisfaction_lambda import customer_satisfaction
from emotion_recognition import SatisfactionScore


#IMAGES WHICH THE FACE API WORKS WITH
#url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/David_Schwimmer_2011.jpg/800px-David_Schwimmer_2011.jpg'


#IMAGES WHICH THE FACE API DOES NOT WORK WITH
#url = 'https://themoscowtimes.com/static/uploads/publications/2017/1/13/0340fe7a6ad14db2be0587e86c83e947.jpg'
#url = 'https://i.dailymail.co.uk/i/pix/2017/07/18/14/427394C200000578-4707164-Happy_people_are_healthier_Some_65_percent_of_relevant_studies_f-m-21_1500384450707.jpg'


def jankyCSS(url):
    satisfaction = SatisfactionScore()
    raw_results = satisfaction.detect_from_url(url)
    results = raw_results[0]["faceAttributes"]["emotion"]

    sum = 0
    count = 0
    for key, value in results.items():
        sum += value
        count += 1

    return (sum/count) * 100

    