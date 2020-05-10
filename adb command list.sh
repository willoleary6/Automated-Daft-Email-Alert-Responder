cd C:\adb\platform-tools
adb connect localhost:5555
adb shell
pm list packages -f
monkey -p com.google.android.gm -v 1
monkey -p com.daft.ie -c android.intent.category.LAUNCHER 1

input touchscreen tap 500 600

input touchscreen tap 200 100 # open folders

input touchscreen swipe 200 1000 200 400 # swipe the options to bring the inFocus

input touchscreen tap 200 600 # tap inFocus label

input touchscreen tap 500 100 # close the folder button

input touchscreen tap 1000 1000 # open daft ad