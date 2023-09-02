import speech_recognition as sr
import pyttsx3
import openai

openai.api_key = "openai key"

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the voice engine
voice_engine = pyttsx3.init()

#Voice type: 0: K, 1: female, 2: male
voices = voice_engine.getProperty('voices') 
voice_engine.setProperty('voice', voices[0].id)
voice_engine.setProperty('rate', 170)
		

# Function to convert text to speech
def SpeakText(user_text,command):
	
	#Save an sound file to answer.
	voice_engine.save_to_file(command, '/answer.mp3')

	#Speach
	voice_engine.say(command)

	voice_engine.runAndWait()
	
	

def main():

	# Loop infinitely
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source, duration=0.2)

		while True:
	
			try:
				print('listen...')

				#listens for the user's input
				user_audio = r.listen(source)
				
				# Using google to recognize audio
				user_text = r.recognize_google(user_audio)
				user_text = user_text.lower()

				print("Did you say: ",user_text)
			
				completion = openai.ChatCompletion.create(
					model="gpt-3.5-turbo",
					messages=[
					{"role": "user", "content": user_text}
					]
				)

				#Print the message from ChatGPT
				print(completion.choices[0].message.content)

				SpeakText(user_text,completion.choices[0].message.content)

			
			except sr.RequestError as e:
				print("Could not request results; {0}".format(e))
		
			except sr.UnknownValueError:
				print("unknown error occurred")

if __name__ == "__main__":
    main()
