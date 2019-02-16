@echo off
net share TEXTSEO="%1"
echo Note that if error occured, you'll have to share the manifest folder manually
echo Otherwise use directory \\localhost\TEXTSEO in Word
pause