
import hashlib
from rsa import transform

static_ = "uYdMvnFxS$KTjb8C9f)Z7_yeKSzn-iYW)BodWsZ4$g5OZThwl5)FSx$zfiYj6!oqfhd2FeIKsmRO+hNqJAKY_AGFdbnym8^CDwM%"

static_int_list = [117, 89, 100, 77, 118, 110, 70, 120, 83, 36, 75, 84, 106, 98, 56, 67, 57, 102, 41, 90, 55, 95, 121,
                   101, 75, 83, 122, 110, 45, 105, 89, 87, 41, 66, 111, 100, 87, 115, 90, 52, 36, 103, 53, 79, 90, 84,
                   104, 119, 108, 53, 41, 70, 83, 120, 36, 122, 102, 105, 89, 106, 54, 33, 111, 113, 102, 104, 100, 50,
                   70, 101, 73, 75, 115, 109, 82, 79, 43, 104, 78, 113, 74, 65, 75, 89, 95, 65, 71, 70, 100, 98, 110,
                   121, 109, 56, 94, 67, 68, 119, 77, 37]

random_int = [42, 105, 100, 73, 35, 108, 94, 87, 54, 121, 78, 106, 75, 102, 86, 81, 74, 109, 112, 106, 84, 36, 43, 106,
              79, 113, 100, 45, 50, 121, 108, 82, 53, 87, 78, 117, 42, 72, 100, 55, 65, 42, 77, 67, 56, 100, 88, 98,
              113, 64, 36, 79, 79, 84, 104, 66, 102, 57, 37, 70, 75, 88, 53, 73, 80, 85, 76, 112, 121, 36, 73, 73, 114,
              49, 104, 79, 79, 88, 95, 99, 35, 70, 53, 70, 50, 74, 111, 86, 68, 51, 105, 65, 117, 95, 74, 54, 120, 78,
              72, 78]

salt = b"boonray"


def gen_root_secret_key_str():

    result_int_list = [static_int_list[i]^random_int[i] for i in range(len(random_int))]
    root_material = b"".join([ transform.int2bytes(i) for i in result_int_list])
    encryption_result = hashlib.pbkdf2_hmac('sha256', root_material, salt, 1000)
    # root_secret_key = binascii.hexlify(encryption_result).decode("utf-8")
    return transform.bytes2int(encryption_result)