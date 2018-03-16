This is a simple ransomware PoC. Nothing fancy, for the moment just encrypting files with AES CBC 256bit

Usage: 
```
rainy.py [-h] [-d DECRYPT]

optional arguments:
  -h, --help            show this help message and exit
  -d DECRYPT, --decrypt DECRYPT
````

The 'target' directory and all the files inside will be encrypted, feel free to put in whatever non-important files you want to test.
Does not admit subdirectories for now (In fact it will crash so please don't. I'll fix it sometime).
