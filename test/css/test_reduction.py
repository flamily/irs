"""
Author: Joshua De los Santos
Modified: 5:55PM - 7/11/18

Description:
    Tests for valid json inputs and arbitrary non-json inputs.
"""
import pytest
from biz.css.reduction import apply_reduction


@pytest.mark.parametrize('raw_results', [
    ([{
        'faceId': '3f839179-344a-4a03-a8e3-2022db271033',
        'faceRectangle': {
            'top': 219,
            'left': 247,
            'width': 297,
            'height': 297},
        'faceAttributes': {
            'glasses': 'NoGlasses',
            'emotion': {
                'anger': 0.001,
                'contempt': 0.002,
                'disgust': 0.002,
                'fear': 0.0,
                'happiness': 0.058,
                'neutral': 0.935,
                'sadness': 0.001,
                'surprise': 0.001}}}]),

    ([{
        'faceRectangle': {'top': 159, 'left': 117, 'width': 95, 'height': 95},
        'faceAttributes': {
            'glasses': 'NoGlasses',
            'emotion': {
                'anger': 0.002,
                'contempt': 0.0,
                'disgust': 0.014,
                'fear': 0.0,
                'happiness': 0.99,
                'neutral': 0.001,
                'sadness': 0.001,
                'surprise': 0.001}}}]),

    ([{
        'faceId': '3f839179-344a-4a03-a8e3-2022db271033',
        'faceAttributes': {
            'glasses': 'NoGlasses',
            'emotion': {
                'anger': 0.096,
                'contempt': 0.003,
                'disgust': 0.682,
                'fear': 0.004,
                'happiness': 0.008,
                'neutral': 0.002,
                'sadness': 0.211,
                'surprise': 0.001}}}]),

    ([{
        'faceId': '8cfb06b4-bbdb-42ca-a78b-962908895704',
        'faceRectangle': {'top': 55, 'left': 16, 'width': 74, 'height': 74},
        'faceAttributes': {
            'glasses': 'NoGlasses',
            'emotion': {
                'anger': 0.107,
                'contempt': 0.005,
                'disgust': 0.0,
                'fear': 0.0,
                'happiness': 0.0,
                'neutral': 0.84,
                'sadness': 0.047,
                'surprise': 0.0}}}, {
                    'faceId': '5727a8ce-0181-4ad9-a236-99d21d734bfe',
                    'faceRectangle': {
                        'top': 191,
                        'left': 114,
                        'width': 74,
                        'height': 74},
                    'faceAttributes': {
                        'glasses': 'NoGlasses',
                        'emotion': {
                            'anger': 0.0,
                            'contempt': 0.0,
                            'disgust': 0.0,
                            'fear': 0.0,
                            'happiness': 0.0,
                            'neutral': 0.996,
                            'sadness': 0.001,
                            'surprise': 0.003}}}, {
                                'faceId':
                                    'f19b5217-2094-4d72-9803-ca8d276',
                                'faceRectangle': {
                                    'top': 42,
                                    'left': 111,
                                    'width': 74,
                                    'height': 74},
                                'faceAttributes': {
                                    'glasses': 'NoGlasses',
                                    'emotion': {
                                        'anger': 0.825,
                                        'contempt': 0.0,
                                        'disgust': 0.003,
                                        'fear': 0.056,
                                        'happiness': 0.006,
                                        'neutral': 0.0,
                                        'sadness': 0.103,
                                        'surprise': 0.008}}}, {
                                            'faceId':
                                                '46fdb-b4df-4186-82b7-d0194',
                                            'faceRectangle': {
                                                'top': 193,
                                                'left': 17,
                                                'width': 72,
                                                'height': 72},
                                            'faceAttributes': {
                                                'glasses': 'NoGlasses',
                                                'emotion': {
                                                    'anger': 0.0,
                                                    'contempt': 0.0,
                                                    'disgust': 0.0,
                                                    'fear': 0.0,
                                                    'happiness': 1.0,
                                                    'neutral': 0.0,
                                                    'sadness': 0.0,
                                                    'surprise': 0.0}}}]),
    ([{
        'faceId': '68581599-6228-42a2-b16d-1f651918df08',
            'faceRectangle': {
                'top': 269,
                'left': 604,
                'width': 173,
                'height': 173},
            'faceAttributes': {
                'glasses': 'NoGlasses',
                'emotion': {
                    'anger': 0.003,
                    'contempt': 0.049,
                    'disgust': 0.0,
                    'fear': 0.0,
                    'happiness': 0.0,
                    'neutral': 0.6,
                    'sadness': 0.346,
                    'surprise': 0.0}}}]),

    ([{
        'faceId': 'e0c5a991-398b-42df-ad6b-f914384f8fd6',
            'faceRectangle': {
                'top': 250,
                'left': 582,
                'width': 171,
                'height': 171},
            'faceAttributes': {
                'glasses': 'NoGlasses',
                'emotion': {
                    'anger': 0.002,
                    'contempt': 0.064,
                    'disgust': 0.0,
                    'fear': 0.0,
                    'happiness': 0.0,
                    'neutral': 0.571,
                    'sadness': 0.362,
                    'surprise': 0.0}}}]),
])
def test_json_input(raw_results):
    """Input valid azure json data"""
    prediction = apply_reduction(raw_results)
    assert prediction >= 0
    assert prediction <= 100


@pytest.mark.parametrize('raw_results', [
    ([]),
    (''),
    (['arbitraryurl.com.au']),
    (27),
])
def test_bad_json_input(raw_results):
    """Input non-json data"""
    prediction = apply_reduction(raw_results)
    assert prediction == -1
