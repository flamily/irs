import cognitive_face as CF
import locale

class SatisfactionScore:
	def __init__(self, location='australiaeast'):
		self._base_url = "https://%s.api.cognitive.microsoft.com/face/v1.0/" % location
		KEY = '850b8b8a63a04e888601d6acbf6fb172'
		self._cognitive_face = CF
		self._cognitive_face.Key.set(KEY)
		self._cognitive_face.BaseUrl.set(self._base_url)

	def detect_from_url(self, url):
		return self.detect(url)

	def detect_from_local_file(self, filepath):
		#with open(filepath, "rb") as image:
	#		image_as_bytes = image.read()
		locale.getdefaultlocale()

		f = open(filepath, "rb")
		image_as_bytes = f.read()
		f.close()

		return self.detect(image_as_bytes)

	def detect(self, image, face_id=True, landmarks=False, attributes='emotion, glasses'):
		return self._cognitive_face.face.detect(image, face_id, landmarks, attributes)


if __name__ == "__main__":
	css = SatisfactionScore()

	#print(css.detect_from_url('https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'))

	print(css.detect_from_local_file("face.jpg"))