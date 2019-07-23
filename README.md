# Optical Character Recognition (OCR)
---

This program isn't remotely practical, fast, scalable, or any other buzzword you can think of, but it _is_ a potentially fun way to play around with a simple artificial neural network without needing to deal with a tangled web of dependencies.  All you need to run this program is a Python 3 interpretter and the PIL module!

All this script really does is squish/expand training images to the requested dimension, construct a network of fully-connected layers, train this network for some user-defined number of iterations (each iteration trains on entire training set, though each batch is just one image), and then attempt to "read" the images in the test set (classification).

## Step 1: Define the network
Denote the number of neurons in each layer of the network as an integer on a single line of a plaintext file, with each layer separated from the next by a space character.  Note also that the first layer is the input layer, and the last layer is the output layer, which means the input layer should have the same number of neurons as there are pixels in each training image, and the output layer should have as many neurons as there are characters to classify.  For example, in ```my_first_net.ann``` below, we create the structure of a 5-layer network with 256 input neurons (16x16 images), 3 hidden layers of 128, 64, and 32 neurons, followed by 26 output neurons (26 letters in English alphabet):
```
256 128 64 32 26
```

Feel free to play around with different network configurations.  Just be aware that adding more layers generally leads to longer training time.

## Step 2: Train the network
Training images are included in this repository thanks to [this great dataset](http://www.ee.surrey.ac.uk/CVSSP/demos/chars74k/) in PNG format within the ```training/all/``` directory.  Note that the ```training/only_uppers/``` and ```training/only_lowers/``` directories simply contain subsets of the original dataset.  For our example, we will be training our network to identify capital letters with the following command:
```
$ ./ocr -l my_first_net.ann -t training/only_uppers/ -d 16 -i 800 -s my_first_net.ann
```

* **-l** loads the network structure from a file (```my_first_net.ann```)
* **-t** specifies the images directory on which to train the network (```training/only_uppers/```)
* **-d** sets the dimension to which the images shall be converted (all images squished to 16x16 squares)
* **-i** sets the number of training iterations (800)
* **-s** defines the path to the file to contain the trained network (we use ```my_first_net.ann``` again here, though another file could be used)

See the help text (```./ocr -h```) for all supported command-line arguments.

The program will first populate the ```training/only_uppers_formatted/``` directory with all of the formatted training images:
```
training/only_uppers/T/img030-033.png --(16x16)-> training/only_uppers_formatted/T0.bmp
training/only_uppers/T/img030-005.png --(16x16)-> training/only_uppers_formatted/T1.bmp
training/only_uppers/T/img030-007.png --(16x16)-> training/only_uppers_formatted/T2.bmp
```

Once all of the images are prepared, training will begin:
```
Training images prepared
Training Iteration: 1 / 800
```
This is typically the longest part of the program's runtime, so expect to wait a while.

## Step 3: Test the network
After training finishes, the network structure, vocabulary, and weights are all written to a file.  This file can be loaded to test the network's performance:
```
$ ./ocr -l my_first_net.ann -r readable/words_upper/
```

* **-l** loads the trained network from the save file (```my_first_net.ann```)
* **-r** points to the directory containing the images to be "read" (```readable/words_upper/```)

Some testing images are provided in the ```readable/``` directory.  In our example, we trained only on upper-case letters, so we'll read from the ```readable/words_upper/``` bucket.  Here's how our network performed:
```
readable/words_upper/OKAY.png says: OKAY
readable/words_upper/DANKME.png says: UANKME
readable/words_upper/HEYMYNAME.png says: HEYPYVAME
readable/words_upper/RUNESCAPE.png says: MLNEICAPE
readable/words_upper/JAKEISCOOL.png says: JAKEISLOOL
readable/words_upper/LENAISKEWL.png says: LENAIZKEWL
readable/words_upper/ROBLOXOOF.png says: RHALBXOOF
readable/words_upper/ALLY.png says: MLLW
readable/words_upper/AZL.png says: AZL
readable/words_upper/HECKA.png says: HECKM
readable/words_upper/MYNAMEISJ.png says: MYNAMEZSJ
readable/words_upper/ERIKA.png says: ERTKA
readable/words_upper/HELLO.png says: HELLC
readable/words_upper/ACTUAL.png says: ACTLAL
readable/words_upper/MEMELORD.png says: MEMLLORD
readable/words_upper/REALLYBRUH.png says: REALLYBLUH
readable/words_upper/SOUNDS.png says: SOUNDE
```

Not amazing, but it _is_ a small, non-convolutional network.  Other example networks are provided in the ```saved_anns``` directory.