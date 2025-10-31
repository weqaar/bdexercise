import hashlib
import io, os, sys
import validators
import json
import urllib

# Config params
baseurl = "https://test.com/problems/"
hash_length = 8
short_url_ttl = 336 # 14d
dbfile = "db.json"
# ------

hashmap = dict()

'''
Could use argparse or click for [decode -d, encode -e] params but omitting as this is a time limited exercise
'''
def main():
    defaulturltoencode = "https://test.com/problems/design-tinyurl"
    if len(sys.argv) > 1:
        urltoencode =  sys.argv[1]
    else:
        urltoencode = defaulturltoencode

    sys.exit("Invalid URL") if validators.url(urltoencode) == False else None

    encode(urltoencode)
    syncfile()

    # Decode test
    test_short_url = ["https://test.com/problems/a71bce9d", "https://test.com/problems/f50de615"]
    for surl in test_short_url:
        print(decode(surl))
    
    sys.exit(0)

def encode(fullurl: str) -> bool:
    urlhash = hashlib.sha512(fullurl.encode(encoding="UTF-8")).hexdigest()[:hash_length]
    hashmap.clear()
    hashmap[urlhash] = dict()
    hashmap[urlhash]["url"] = fullurl
    hashmap[urlhash]["shorturl"] = baseurl + str(urlhash)
    hashmap[urlhash]["ttl"] = short_url_ttl 
    return True
    
def decode(shorturl: str) -> str:
    try:
        with open(dbfile, 'r', encoding='utf-8', errors='ignore') as file:
            try:
                a_str = file.read()
                valid_json = a_str.replace("'", '"')
                filedb = json.loads(valid_json)
                filedbkeys = list(filedb.keys())

                shorturlparse = urllib.parse.urlsplit(shorturl, scheme='', allow_fragments=True)
                shorturlkey = shorturlparse.path.split('/')[-1]

                if shorturlkey in filedbkeys:
                    return filedb[shorturlkey]["url"]
            except Exception as e:
                print("Exception error:", e)
            return None
    except Exception as exc:
        return exc

def syncfile() -> bool:
    if not os.path.exists(dbfile):
        write_file(hashmap)
        return True

    with open(dbfile, 'r+', encoding='utf-8', errors='ignore') as file:
        try:
            a_str = file.read()
            valid_json = a_str.replace("'", '"')
            filedb = json.loads(valid_json)
            filedbkeys = list(filedb.keys())

            for key in hashmap.keys():
                if key not in filedbkeys:
                    filedb.update(hashmap)
                    write_file(filedb)
                else:
                    pass
            return True
        except Exception as e:
            print("Exception error:", e)
        return False

def write_file(destobj):
    with open(dbfile, 'w', encoding='utf-8') as file:
        json.dump(destobj, file)

if __name__ == '__main__':
    main()
