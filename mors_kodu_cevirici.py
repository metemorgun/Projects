# -*- coding: utf-8 -*-
# 3x-29-mors_kod.py
import pygame
import time

MORSKOD = {
    'A': '.-',   'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-',  'L': '.-..', 'M': '--',   'N': '-.',  'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-',  'V': '...-', 'W': '.--',  'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.','Ç':'-.-.','ç':'-.-.ü','Ğ':'--.','ğ':'--.','İ':'..','ı':'..','Ö':'---','ö':'---',
    'Ş':'...','ş':'...','Ü':'..-','ü':'..-'  
}

turkce = {'ç': 'Ç', 'ğ': 'Ğ', 'ı': 'I', 'i': 'İ', 'ö': 'Ö', 'ş': 'Ş', 'ü': 'Ü'}
tr_lat = {'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'}

BIRIM = 0.3
UCLU = 3 * BIRIM
YEDILI = 7 * BIRIM

def buyukHarf(harf):
    if harf in turkce:
        bharf = turkce[harf]
        if bharf in tr_lat:
            return tr_lat[bharf]
    return harf.upper()

def duzenle(ystring):
    string = ystring
    keys = MORSKOD.keys()
    i = 0
    while i < len(string):
        char = buyukHarf(string[i])
        if char not in keys and char != '':
            if i == 0:
                string = 'X' + string[1:]
            else:
                string = string[:i] + 'X' + string[i + 1:]
        elif char != string[i]:
            if i == 0:
                string = char + string[1:]
            else:
                string = string[:i] + char + string[i + 1:]
        i += 1
    return string

def main():
    msg1 = " Mors Kodu Haline Getirilecek Mesaj"
    msg2 = " Mors Kodu Mesaj"
    msg = duzenle(msg1)
    pygame.mixer.init()
    pygame.init()
    morse_string = ''
    
    for char in msg:
        if char == ' ':
            morse_string += ' '
            print('{}{}'.format('', ' ' * 7))
            time.sleep(YEDILI)
        else:
            morse_string += MORSKOD[char.upper()]
            print('{}{}'.format(char.upper(), MORSKOD[char.upper()]))
            pygame.mixer.music.load('İstenilen\\Dosya\\\\Konumu\\mors_sesleri' + char.upper()+'_morse_code.ogg') # Mors seslerini içeren dosyanın konumu belirtilmelidir.
            pygame.mixer.music.play()
            time.sleep(UCLU)
    print(morse_string)
    print(msg1)
    print(msg)

if __name__ == "__main__":
    main()