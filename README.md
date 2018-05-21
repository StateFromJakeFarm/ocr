# Optical Character Recognition (OCR)
---

This program isn't remotely practical, fast, scalable, or any other buzzword you can think of, but it _is_ a potentially fun way to play around with an artificial neural network written in an awesome language and without a tangled web of dependencies.  All you'll need to run this network is a Python 3 installation and the PIL module!

All this script really does is squish/expand training images to the requested dimension, construct a network of fully-connected layers, train said network for some user-defined number of iterations (batch size is entire test set, keep it simple), and then attempt to "read" the images in our test set (classification).

## Step 1: Define the network
Denote the number of requested neurons in each layer of the network as an integer on a single line of a plaintext file, each layer being separated from the next by a space character.  Note also that the first layer is the input layer, and the last layer is the output layer, thus the input layer should have the same number of neurons as there are pixels in each training image, and the output layer should have as many neurons as there are characters to classify.  For example, in my_first_net.ann below, we create the structure of a 4-layer network with 100 input neurons (10x10 images), 2 hidden layers of 70 and 50 neurons, and 26 output neurons (26 letters in English alphabet):
```
100 70 50 26
```

Feel free to play around with different network configurations, just know that adding more layers means longer training time.

## Step 2: Train the network
Now comes the time to make our dream network a reality!  Training images have been included in this repository thanks to [this dope dataset](http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/) in PNG format in the training/trainingPNGs/ directory.  Note that the training/only_caps/ and training/justLowersPNGs/ directories simply contain subsets of the original dataset.  For our example, we will be training our network to identify capital letters with the following command:
```
$ ./ocr -l my_first_net.ann -t training/only_caps/ -d 10 -i 500 -s my_first_net.ann
```

* **-l** loads the network structure from a file (my_first_net.ann)
* **-t** specifies the images directory on which to train the network (training/only_caps/)
* **-d** sets the dimension to which the images shall be converted (all images squished to 10x10 squares)
* **-i** sets the number of training iterations (500)
* **-s** defines the path to the file to contain the trained network (we use my_first_net.ann again here, though another file could be used)

See the help text (```./ocr -h```) to see all supported command-line arguments.

The program will then set about creating the training/only_caps/only_capsFormatted/ directory where it will dump all of the formatted training images:
```
training/only_caps/I/img019-027.png --(10x10)-> training/only_capsFormatted/I53.bmp
training/only_caps/I/img019-044.png --(10x10)-> training/only_capsFormatted/I54.bmp
training/only_caps/U/img031-050.png --(10x10)-> training/only_capsFormatted/U0.bmp
```

Once all of the images have been prepared, training will commence!  Go be productive while you wait for it to finish:
```
Training images prepared
Training Iteration: 67 / 500
```

## Step 3: Test the network
This is the fun or maybe very disappointing part!  After our network is done training, we will have a save file with our virtual brain tucked away inside; let's load it and see how it performs:
```
$ ./ocr -l my_first_net.ann -r readable/words_upper/
```

* **-l** loads the trained network from the save file (my_first_net.ann)
* **-r** points to the directory containing the images to be "read" (readable/words_upper/)

Some testing images are provided in the readable/ directory.  In our example, we trained only on upper-case letters, so we'll read from the readable/words_upper/ bucket.  Here's how our network performed:
```
readable/words_upper/SOUNDS.png says: SOUNOS
readable/words_upper/TRUMP(Ryan E).png says: TTLMT
readable/words_upper/JAKEISCOOL.png says: UAKEISLOOL
readable/words_upper/MYNAMEISJ.png says: MYNAMEJSJ
readable/words_upper/LENAISKEWL(lena).png says: LENAIZKFWL
readable/words_upper/HECKA(Sean).png says: NECKM
readable/words_upper/MEMELORD(will).png says: MFMLLORD
readable/words_upper/FART(katie).png says: FART
readable/words_upper/ERIKA.png says: EMAKA
readable/words_upper/REALLYBRUH.png says: REALLYPQUH
readable/words_upper/AZL.png says: AZL
readable/words_upper/DANKME(ryan).png says: UANKME
readable/words_upper/ACTUAL.png says: ACTLAL
readable/words_upper/HEYMYNAME.png says: HEYMYUAME
readable/words_upper/BUTTHOLE(emma).png says: PUTTHOLE
readable/words_upper/ALLY(Anastasia).png says: MLLY
readable/words_upper/OKAY.png says: OKAY
readable/words_upper/HELLO.png says: HELLO
```

It's something at least!
<br>
<br>
Try making your own, more complex network with more hidden layers to improve performance.  Some example nets are provided in the saved_anns/ directory.
<br>
<br>
**NOTE:** The commit history for this repo is revolting, sorry.
