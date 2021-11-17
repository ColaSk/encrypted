
import hashlib
from rsa import transform

def get_private_key(status_keys, dynamic_keys, salt=b'boonray'):
    """Access to the private key

    Args:
        status_keys (list [int, ]): [1,2,3]
        dynamic_keys (list [int, ]): [4,5,6]
        salt (bytes, optional): [description]. Defaults to b'boonray'.

    Returns:
        [int]: [description]
    """
    assert len(status_keys) == len(dynamic_keys)

    xor_rt = [status_keys[i]^dynamic_keys[i] for i in range(len(dynamic_keys))]
    root_material = b"".join([ transform.int2bytes(i) for i in xor_rt])
    root_key = hashlib.pbkdf2_hmac('sha256', root_material, salt, 1000)
    return transform.bytes2int(root_key)