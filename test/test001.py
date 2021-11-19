import sys
sys.path.append('../')

from encrypted import EncryptCore, create_private_key, create_public_key
from encrypted.utils import YamlFile, de_public_key

if __name__ == '__main__':

    pwd = '123456'

    status_keys_plaintext = "6x*bUITKm9LnVDYPlk&h7gIQ@-K+WSiMdhFTNV4Un&%0CX%FNQsyxdB!)zpoC5f9uAQ_(1QoxV8WkkqdXUwpcX^JeuOBGJ*3j_ue"
    dynamic_keys_plaintext = "+Vflf@*GW(kt)rahjbXtMC3ye)QjRFJIq%aOt5PsaUVhg%&TmGWw(cE%k)Th86(#5dK3noH5XJ@B!lw!oqAGl-EkYQkoF6MrMOWY"
    public_key_plaintext = "eCW5rd#NUKJZS5%vXpqIM2!W!Bw$FC9I"

    # status_key = str2ASCII(status_keys_plaintext)
    # dynamic_key = dyn_int_list

    private_key = create_private_key(status_keys_plaintext, dynamic_keys_plaintext)
    
    print('private_key: ', private_key)

    public_key = create_public_key(public_key_plaintext, private_key) # str
    public_key_pt = de_public_key(public_key, private_key) # str

    print('public_key: ', public_key)
    print('public_key_pt', public_key_pt)

    ec = EncryptCore(public_key, private_key)

    en_pwd = ec.encode(pwd)
    de_pwd = ec.decode(en_pwd)

    print(en_pwd)
    print(de_pwd)
