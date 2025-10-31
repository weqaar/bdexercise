import hashlib

baseurl = "https://test.com/problems/"
hashmap = dict()

def main():
    urltoencode = "https://test.com/problems/design-tinyurl"
    encode(urltoencode) 
    print(">>DEBUG", hashmap)


def validateurl(url: str) -> bool:
    return True


def encode(fullurl: str) -> bool:
    hashin = hashlib.md5()
    urlhash = hashin.update(fullurl.encode(encoding="UTF-8"))
    print(">>DEBUG", urlhash.digest())
    hashmap["url"] = fullurl
    hashmap["hash"] = urlhash
    hashmap["shorturl"] = baseurl + str(urlhash)
    return True
    
def decode(shorturl: str) -> str:
    pass


if __name__ == '__main__':
    main()
