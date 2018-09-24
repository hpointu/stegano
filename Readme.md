**Require python>3**

Few scripts to hide stuff in stuff for kids.

Also dumb Vigenere implementation because it's fun


**Vigenere example :**
```sh
$ # Encoding
$ echo "The Text" | python vigenere.py -k "thekey"
Moi Divm
$ # Decoding
$ echo "The Text" | python vigenere.py -k "thekey" | python vigenere.py -d -k "thekey"
The Text
```
