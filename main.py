import random #String,integer,.. within range is going to be printed indivially
import smtplib#To send Mails to login in mail
import imghdr#To attach an image
import socket#To connect a server
from email.message import EmailMessage #It is used for From,To,adresss
# PIL module is used to extract
# pixels of image and modify it
from PIL import Image #To create and to opean, to copy an image

def getKey(text):
	try:
		d = " #DivideWOkey#"
		key = text[text.index(d) + len(d):]
		return str("The given image Doesn't Require a Key to Decrypt")
	except ValueError:
		d = " #DivideWkey#"
		key = text[text.index(d) + len(d):]
		return str("the Key for the image is "+str(key))
# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
	# list of binary codes
	# of given data
		newd = []
		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd
# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pixel, data):
	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pixel)
	for i in range(lendata):
		# Extracting 3 pixels at a time
		pixel = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]
		# Pixel value should be made
		# odd for 1 and even for 0
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pixel[j]% 2 != 0):
				pixel[j] -= 1
			elif (datalist[i][j] == '1' and pixel[j] % 2 == 0):
				if(pixel[j] != 0):
					pixel[j] -= 1
				else:
					pixel[j] += 1
		if (i == lendata - 1):
			if (pixel[-1] % 2 == 0):
				if(pixel[-1] != 0):
					pixel[-1] -= 1
				else:
					pixel[-1] += 1
		# Eighth pixel of every set tells
		# whether to stop ot read further.
		# 0 means keep reading; 1 means thec
		# message is over.
		else:
			if (pixel[-1] % 2 != 0):
				pixel[-1] -= 1
		pixel = tuple(pixel)#The tuple() function is a built-in function in Python that can be used to create a tuple.
		# A tuple is an immutable sequence type. Parameters: This function accepts a single parameter iterable (optional).
		# It is an iterable(list, range etc..) or an iterator object.
		yield pixel[0:3]#yield is used return the multiple value instead rturn method
		yield pixel[3:6]
		yield pixel[6:9]
def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)
	for pixel in modPix(newimg.getdata(), data):
		# Putting modified pixels in the new image
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1
def sendEmail(img):
	img2 = img
	try:
		img = Image.open(img, 'r')
	except FileNotFoundError:
		print("Image you have entered is not found in the folder.\nPlease try again...\n")
		main()
	except:
		print("Can't get the image please choose an image\nPlease try again...\n")
		main()
	emaitype = input("Login with:\n1. Personal Mail-id\n2. Auto Login\n")
	if(emaitype == "1"):
		Sender_Email = input("Enter the Email-id: ")
		Password = input("Enter the password: ")
		Reciever_Email = input("Enter the email-id of the recipient you wish to send: ")

	else:
		Sender_Email = "image.steganography01@gmail.com"
		Password = "Image@123"
		Reciever_Email = input("Enter the email-id of the recipient you wish to send: ")
	sendk = input("Would you like to send the key to recipient(y/n)? ")
	if(sendk == "y" or sendk == "Y"):
		t = decode(img2)
		msg = getKey(t)
		check = input("You got this message: "+msg+"\n Would you like to print this message in mail(y/n)? ")
		if(check == "y" or check == "Y"):
			mmsg ="and " + msg
		else:
			mmsg = ""
	else:
		mmsg = ""
	newMessage = EmailMessage()
	newMessage['Subject'] = "Image"
	newMessage['From'] = Sender_Email
	newMessage['To'] = Reciever_Email
	newMessage.set_content('You got an Image '+mmsg)
	with open(img2, 'rb') as f:
		image_data = f.read()
		image_type = imghdr.what(f.name)
		image_name = f.name
	newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
	try:
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
			smtp.login(Sender_Email, Password)
			smtp.send_message(newMessage)
	except socket.gaierror:
		print("No Internet Connection\n Please connect to Internet and try again")
		sendEmail(img)
	except smtplib.SMTPAuthenticationError:
		print("Please check username/password and try again")
		sendEmail(img)
	except smtplib.SMTPRecipientsRefused:
		print("You have entered Invalid Recipient address please check address and try again")
		sendEmail(img)
	print("Email sent successfully \nPlease check your email")
def encryptDat(shift,text):
    encryption = ""
    for c in text:#Dividing Strig into a Single Letters
        # check if character is an uppercase letter
        if c.isupper():#ord(char) is used to find the ascii values
            if(c != ' ' and not(ord(c) >=48 and ord(c) <= 57) and not(ord(c)>=33 and ord(c)<=47) and not(ord(c) >= 58 and ord(c) <= 64)):
                c_index = ord(c) - ord("A")#65
                # perform the shift
                new_index = (c_index + shift) % 26
                # convert to new character
                new_unicode = new_index + ord("A")
                new_character = chr(new_unicode)#char(ascii value) will a Character
                # append to encrypted string
                encryption += new_character
            elif (ord(c) >= 48 and ord(c) <= 57):#Check the numbers
                encryption += str(9 - int(c))
            elif (c == ' '):
                encryption += "^"
			#Checking Speacial Characters
            elif (ord(c) >= 33 and ord(c) <= 47):
                encryption += c
            elif (ord(c) >= 58 and ord(c) <= 64):
                encryption += c
        else:
            if (c != ' ' and not(ord(c) >=48 and ord(c) <= 57) and not(ord(c)>=33 and ord(c)<=47) and not(ord(c) >= 58 and ord(c) <= 64)):
                c_index = ord(c) - ord("a")
                # perform the shift
                new_index = (c_index + shift) % 26
                new_unicode = new_index + ord("a")#97
                new_character = chr(new_unicode)
                encryption = encryption + new_character
            elif (ord(c) >= 48 and ord(c) <= 57):
                encryption += str(9 - int(c))
            elif (c == ' '):
                encryption +=  "^"
            elif ((ord(c) >= 33 and ord(c) <= 47)):
                encryption += c
            elif (ord(c) >= 58 and ord(c) <= 64):
                encryption += c
    print("Plain text:", text)
    return encryption
def decrypDat(shift,encrypted_text):
    plain_text = ""
    for c in encrypted_text:
        # check if character is an uppercase letter
        if c.isupper():
            if(c != "^" and not(ord(c) >=48 and ord(c) <= 57) and not(ord(c)>=33 and ord(c)<=47) and not(ord(c)>=58 and ord(c)<=64)):
                # find the position in 0-25
                c_unicode = ord(c)
                c_index = ord(c) - ord("A")
                # perform the negative shift
                new_index = (c_index - shift) % 26
                # convert to new character
                new_unicode = new_index + ord("A")
                new_character = chr(new_unicode)
                # append to plain string
                plain_text = plain_text + new_character
            elif (ord(c) >= 48 and ord(c) <= 57):
                plain_text += str(-(int(c) - 9))
            elif (c == '^'):
                plain_text += " "
            elif ((ord(c) >= 33 and ord(c) <= 47)):
                plain_text += c
            elif (ord(c) >= 58 and ord(c) <= 64):
                plain_text += c
        else:
            if (c != "^" and not(ord(c) >=48 and ord(c) <= 57) and not(ord(c)>=33 and ord(c)<=47) and not(ord(c)>=58 and ord(c)<=64)):
                # find the position in 0-25
                c_unicode = ord(c)
                c_index = ord(c) - ord("a")
                # perform the negative shift
                new_index = (c_index - shift) % 26
                # convert to new character
                new_unicode = new_index + ord("a")
                new_character = chr(new_unicode)
                # append to plain string
                plain_text = plain_text + new_character
            elif (ord(c) >= 48 and ord(c) <= 57):
                plain_text += str(-(int(c) - 9))
            elif (c == '^'):
                plain_text += " "
            elif (ord(c) >= 33 and ord(c) <= 47):
                plain_text += c
            elif (ord(c) >= 58 and ord(c) <= 64):
                plain_text += c
    return plain_text
# Encode data into image
def encode():
	img = input("Enter Image File(with .FileExtension) : ")
	try:
		image = Image.open(img, 'r')
	except FileNotFoundError:
		print("Image you have entered is not found in the folder.\nPlease try again...\n")
		encode()
	except:
		print("Can't get the image please choose an image\nPlease try again...\n")
		encode()
	data = input("Enter text to be Encrypted : ")
	Rkey = input("What you prefer:\n1. Manual Key\n2. Auto Generated Key\n")
	if(Rkey == "1"):
		key = int(input("Enter the key: "))
		if(key == 0):
			print("Cipher text and plane Text is Same\nPlease use a different key\n")
			encode()
	else:
		key = random.randint(1,9999)
		print("The Auto Generated key is: "+ str(key))#str() is used to convert the int key to String
	endata = encryptDat(key,data)#Calling encryptDat funtion passing int key and String Text data
	print("Cipher text is:"+endata)
	strkey = input("Did you want to prompt the key in Decryption(y/n)?: ")
	if(strkey == "y" or strkey == "Y"):
		data = endata + " #DivideWkey#" + str(key)
	else:
		data = endata + " #DivideWOkey#" + str(key)
	newimg = image.copy()
	encode_enc(newimg, data)
	new_img_name = input("Create the new Image File(with .FileExtension) : ")
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
	main()
# Decode the data in the image
def decode(img):
	try:
		image = Image.open(img, 'r')
	except FileNotFoundError:
		print("Image you have entered is not found in the folder.\nPlease try again...\n")
		main()
	except AttributeError:
		print("\nCan't Load the image\n Please try again...\n")
		main()
	data = ''
	imgdata = iter(image.getdata())#Get an iterator from an object.
	# In the first form, the argument must supply its own iterator, or be a sequence.
	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]
		# string of binary data
		binstr = ''
		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'
		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data
def divide(text):
	try:
		d = " #DivideWOkey#"
		endata = text.split(d)[0]
		key = text[text.index(d) + len(d):]
		print("The Cipher Text is: " + str(endata))
		return decrypDat(int(key),str(endata))
	except ValueError:
		d = " #DivideWkey#"
		endata = text.split(d)[0]
		print("The Cipher Text is: " + str(endata))
		key = text[text.index(d) + len(d):]
		key2 = input("Please Enter the key: ")
		if(key2 == key):
			return decrypDat(int(key),str(endata))
		else:
			print("Key Doesn't match\nPlease try again..")
			divide(text)
# Main Function
def main():
	a = int(input("Press to select: \n"
						"1. Encrypt\n2. Decrypt\n3. Send Image\n4. Exit the program.\n"))
	if (a == 1):
		encode()#Calling encode() function
	elif (a == 2):
		img = input("Enter Image File(with .FileExtension) : ")
		data = decode(img)#calling decode() function
		if data == ";J":
			print("Image is not Encrypted. Please Encrypt the Image")
			main()
		else:
			print("Decrypted Word : " + divide(data))#calling divide function
			main()
	elif (a == 3):
		img = input("Enter Image File you wish to send(with .FileExtension) : ")
		data = decode(img)
		if data == ';J':
			print("Image is not Encrypted. Please Encrypt the Image")
			main()
		else:
			sendEmail(img)#Calling sendEmail fuction passing the image
	elif (a == 4):
		out = input("Are you sure(y/n)? ")
		if(out == "y" or out == "Y"):
			print("You are exited from Image Steganography\n\nThank You!")
			exit()#Callig exit() function to quit the proggrame
		else :
			main()
	else:
		print("Enter correct input\nPlease try again...\n")
		main()
# Driver Code
if __name__ == '__main__' :
	print("\n:: Welcome to Image Steganography ::\n")
	# Calling main function# Calling main function
	main()
