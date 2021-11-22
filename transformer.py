# -----------------------------------------------------------------------------
# Raymond Wei 2021-11-22
# --------------------
# Purpose: building up message transformation/encoding/decoding.
#          because unicode-encoded strings seem to have issues when
#          being mqtt/tcp-ip transferred.
# --------------------------------------------------------------
import base64
import pdb, pprint

pp = pprint.PrettyPrinter(indent=4)

# msg: "# abc ວັນນະຄະດີ => 魏建池"
def b64string(msg):
    b64bytes = base64.b64encode(msg.encode('utf-8'))
    
    # 'IyBhYmMg4Lqn4Lqx4LqZ4LqZ4Lqw4LqE4Lqw4LqU4Lq1ID0+IOmtj+W7uuaxoA=='
    return b64bytes.decode('ascii')
    
# msg: 'IyBhYmMg4Lqn4Lqx4LqZ4LqZ4Lqw4LqE4Lqw4LqU4Lq1ID0+IOmtj+W7uuaxoA=='
def ascii2utf8(msg):    # msg is a base64-ascii-string
    _64bytes = msg.encode('ascii')   # turn it to a byte-string
    bytes = base64.b64decode(_64bytes)

    # back to "# abc ວັນນະຄະດີ => 魏建池"
    return bytes.decode('utf-8')

class Transformer:
    def __init__(self):
        pass

    def convert_msg2b64(self, msg):
        " text contained in msg be converted to bas64-ASCII-string"
        if type(msg) == type({}):
            return self.convert_dict(msg)
        if type(msg) == type([]):
            return self.convert_list(msg)
        if type(msg) == type(""):
            return b64string(msg)
        return msg  # int, float, double

    def convert_list(self, msg):
        " text contained in msg be converted to bas64-ASCII-string"
        lst = []
        for e in msg:
            lst.append(self.convert_msg2b64(e))
        return lst

    def convert_dict(self, dic):
        " text contained in msg be converted to bas64-ASCII-string"
        dicx = {}
        for k, v in dic.items():
            dicx[k] = self.convert_msg2b64(v)
        return dicx

    def convert_back_msg(self, msg):
        " strings in msg are base64-ASCII strings. Convert them back "
        if type(msg) == type({}):
            return self.convert_back_dict(msg)
        if type(msg) == type([]):
            return self.convert_back_list(msg)
        if type(msg) == type(""):
            return ascii2utf8(msg)
        return msg

    def convert_back_dict(self, msg):
        " strings in msg are base64-ASCII strings. Convert them back "
        dicx = {}
        for k, v in msg.items():
            if type(v) == type({}):
                dicx[k] = self.convert_back_dict(v)
            elif type(v) == type([]):
                dicx[k] = self.convert_back_list(v)
            elif type(v) == type(""):
                dicx[k] = ascii2utf8(v)
            else:
                dicx[k] = v
        return dicx

    def convert_back_list(self, msg):
        " strings in msg are base64-ASCII strings. Convert them back "
        lst = []
        for e in msg:
            if type(e) == type({}):
                lst.append(self.convert_back_dict(e))
            elif type(e) == type([]):
                lst.append(self.convert_back_list(e))
            elif type(e) == type(""):
                lst.append(ascii2utf8(e))
            else:
                lst.append(e)
        return lst

    def get_sample_data(self):
        return {
            # Lao-language string mixed with English abc
            "name1": "abc ວັນນະຄະດີ ",
            "name2": {
                "name2-1": {
                    "m1": "hello",      # pure English/ASCII string
                    "m2": 12.34,
                    # Chinese mixed with English abc and a Russian string
                    "m3": "abc魏建池 английский",
                    "m4": 321
                }
            }
        }

def main():
    transformer = Transformer()

    # pdb.set_trace()
    print("original dict:")
    print("-"*80)
    pp.pprint(transformer.get_sample_data())
    print()
    input("hit return\n")
    trxdic = transformer.convert_msg2b64(transformer.get_sample_data())
    print(f"transformed dict:")
    print("-"*80)
    pp.pprint(trxdic)
    input("hit return")
    oridic = transformer.convert_back_msg(trxdic)
    print()
    print("back-transformed dict:")
    print("-"*80)
    pp.pprint(oridic)

if __name__ == '__main__':
    main()
