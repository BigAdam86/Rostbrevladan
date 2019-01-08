import smtplib, ssl
import speech_recognition as sr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Record Audio
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    
    audio = r.listen(source)
 
# Speech recognition using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    voice_message = r.recognize_google(audio, language="sv-SE")
    print("You said: " + voice_message)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


sender_email = "xxxxxxxxx"
receiver_email = "xxxxxxxx"
password = "xxxxxxxxx"

message = MIMEMultipart("alternative")
message["Subject"] = "Meddelande från Röstbrevlådan"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = voice_message

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)

# Create secure connection with server and send email
try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    print("Email sent")
except:
    print("Error Sending Email")