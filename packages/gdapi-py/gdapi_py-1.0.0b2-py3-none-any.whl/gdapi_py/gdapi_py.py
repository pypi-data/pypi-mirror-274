import hashlib
import requests
import base64
import itertools
import random
from string import ascii_letters, digits
import re

class gdapi:
    def __init__(self, username, password, dbprefix = "http://www.boomlings.com/database"):
        self.dbprefix = dbprefix
        self.udid = self.__generate_udid()
        self.uuid = self.__generate_uuid()
        self.gjp2 = self.__encode_gjp2(password)
        data = {
            "userName": username,
            "gjp2": self.gjp2,
            "secret": "Wmfv3899gc9",
            "udid": self.udid
        }
        request = requests.post(f"{self.dbprefix}/accounts/loginGJAccount.php", headers={"User-Agent": ""}, data=data)
        match = re.match(r"(\d+),(\d+)", request.text)
        if match:
            self.accountid = int(match.group(1))
            self.userid = int(match.group(2))
            self.username = username
            self.password = password
        else:
            raise RuntimeError("Failed to login to account. Please verify the account details.")

    @staticmethod
    def __xor_cipher(string: str, key: str):
        return ("").join(chr(ord(x) ^ ord(y)) for x, y in zip(string, itertools.cycle(key)))

    def __encode_gjp(self, password: str):
        encoded = self.__xor_cipher(password, "37526")
        encoded_base64 = base64.b64encode(encoded.encode()).decode()
        encoded_base64 = encoded_base64.replace("+", "-")
        encoded_base64 = encoded_base64.replace("/", "_")
        return encoded_base64

    def __decode_gjp(self, gjp: str):
        decoded_base64 = base64.b64decode(gjp.encode()).decode()
        decoded = self.__xor_cipher(decoded_base64, "37526")
        return decoded

    @staticmethod
    def __encode_gjp2(password: str) -> str:
        salt = "mI29fmAnxgTs"
        hash_object = hashlib.sha1((password + salt).encode())
        gjp2 = hash_object.hexdigest()
        return gjp2

    @staticmethod
    def __is_gjp2_valid(stored_gjp2: str, password: str) -> bool:
        salt = "mI29fmAnxgTs"
        hash_object = hashlib.sha1((password + salt).encode())
        gjp2 = hash_object.hexdigest()
        return gjp2 == stored_gjp2

    @staticmethod
    def __generate_rs(n):
        return "".join(random.choices(ascii_letters + digits, k=n))

    @staticmethod
    def __generate_udid(start = 100_000, end = 100_000_000):
        return "S" + str(random.randint(start, end))

    @classmethod
    def __generate_uuid(self, parts = (8, 4, 4, 4, 10)):
        return "-".join(map(self.__generate_rs, parts))

    def __generate_chk(self, values = [], key: str = "", salt: str = "") -> str:
        values.append(salt)

        string = ("").join(map(str, values))

        hashed = hashlib.sha1(string.encode()).hexdigest()
        xored = self.__xor_cipher(hashed, key)
        final = base64.urlsafe_b64encode(xored.encode()).decode()

        return final

    def post_account_comment(self, comment: str):
        data = {
            "secret": "Wmfd2893gb7",
            "gjp2": self.gjp2,
            "gameVersion": "22",
            "comment": base64.b64encode(comment.encode('utf-8')).decode('utf-8'),
            "binaryVersion": "40",
            "accountID": self.accountid
        }
        request = requests.post(f"{self.dbprefix}/uploadGJAccComment20.php", headers={"User-Agent": ""}, data=data)
        if re.match(r'^\d{8,}$', request.text):
            return True, request.text
        else:
            return False, request.text

    def post_level_comment(self, comment: str = "", levelid: str = "", percent: str = "0"):
        data = {
            "gameVersion": "22",
            "binaryVersion": "40",
            "accountID": self.accountid,
            "gjp2": self.gjp2,
            "userName": self.username,
            "comment": base64.b64encode(comment.encode('utf-8')).decode('utf-8'),
            "secret": "Wmfd2893gb7",
            "levelID": str(levelid),
            "percent": str(max(min(int(percent), 100), 0))
        }
        chk_values = [
            data['userName'],
            data['comment'],
            data['levelID'],
            data['percent'],
            "0xPT6iUrtws0J"
        ]
        chk = self.__generate_chk(chk_values, key="29481")
        data['chk'] = chk
        #a2lsbCBtZQ

        request = requests.post(f"{self.dbprefix}/uploadGJComment21.php", headers={"User-Agent": ""}, data=data)
        if re.match(r'^\d{7,}$', request.text):
            return True, request.text
        else:
            return False, request.text

    def post_user_message(self, subject: str = "", body: str = "", toaccountid = 0):
        data = {
            "gameVersion": "22",
            "binaryVersion": "40",
            "accountID": self.accountid,
            "toAccountID": toaccountid,
            "subject": base64.b64encode(subject.encode('utf-8')).decode('utf-8'),
            "body": base64.b64encode(self.__xor_cipher(body, "14251").encode('utf-8')).decode('utf-8'), #url safe encoding, its weird.
            "gjp2": self.gjp2,
            "secret": "Wmfd2893gb7"
        }

        request = requests.post(f"{self.dbprefix}/uploadGJMessage20.php", headers={"User-Agent": ""}, data=data)
        if request.text == "1":
            return True
        else:
            return False

    def post_user_friend_request(self, comment: str = "", toaccountid = 0):
        data = {
            "gameVersion": "22",
            "binaryVersion": "40",
            "accountID": self.accountid,
            "toAccountID": toaccountid,
            "comment": base64.b64encode(comment.encode('utf-8')).decode('utf-8'),
            "gjp2": self.gjp2,
            "secret": "Wmfd2893gb7"
        }

        request = requests.post(f"{self.dbprefix}/uploadFriendRequest20.php", headers={"User-Agent": ""}, data=data)
        if request.text == "1":
            return True
        else:
            return False