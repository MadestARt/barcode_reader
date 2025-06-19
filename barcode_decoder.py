# Минимальный декодер Code‑128 без комментариев и аннотаций

PATTERNS=(
"11011001100","11001101100","11001100110","10010011000","10010001100","10001001100",
"10011001000","10011000100","10001100100","11001001000","11001000100","11000100100",
"10110011100","10011011100","10011001110","10111001100","10011101100","10011100110",
"11001110010","11001011100","11001001110","11011100100","11001110100","11101101110",
"11101001100","11100101100","11100100110","11101100100","11100110100","11100110010",
"11011011000","11011000110","11000110110","10100011000","10001011000","10001000110",
"10110001000","10001101000","10001100010","11010001000","11000101000","11000100010",
"10110111000","10110001110","10001101110","10111011000","10111000110","10001110110",
"11101110110","11010001110","11000101110","11011101000","11011100010","11011101110",
"11101011000","11101000110","11100010110","11101101000","11101100010","11100011010",
"11101111010","11001000010","11110001010","10100110000","10100001100","10010110000",
"10010000110","10000101100","10000100110","10110010000","10110000100","10011010000",
"10011000010","10000110100","10000110010","11000010010","11001010000","11110111010",
"11000010100","10001111010","10100111100","10010111100","10010011110","10111100100",
"10011110100","10011110010","11110100100","11110010100","11110010010","11011011110",
"11011110110","11110110110","10101111000","10100011110","10001011110","10111101000",
"10111100010","11110101000","11110100010","10111011110","10111101110","11101011110",
"11110101110","11010000100","11010010000","11010011100","11000111010")

START_A,START_B,START_C=103,104,105
STOP=106
SYM_LEN=11

ASCII_A={i:chr(i) for i in range(32)}
ASCII_A.update({i:chr(i + 64) for i in range(32, 96)})
ASCII_B={i:chr(i + 32) for i in range(96)}

SPECIAL_REPR={96: "<FNC3>", 97: "<FNC2>", 101: "<FNC4>", 100: "<FNC4>", 102: "<FNC1>"}

PAT2VAL={p:i for i,p in enumerate(PATTERNS)}

class BarcodeDecoder:
    def __init__(self,data_binary,strict_checksum=True):
        if set(data_binary)-{"0","1"}:raise ValueError
        self._bits=data_binary.strip("0")
        self._strict=strict_checksum

    def decode(self):
        v=self.bits_to_values()
        self.check_checksum(v)
        return self.vals_to_str(v)

    def bits_to_values(self):
        syms=[self._bits[i:i + SYM_LEN] for i in range(0, len(self._bits), SYM_LEN)]
        vals=[]
        for s in syms:
            x=PAT2VAL.get(s)
            if x is None:break
            vals.append(x)
            if x==STOP:break
        if not vals or vals[-1]!=STOP:raise ValueError
        return vals

    def check_checksum(self, vals):
        if len(vals)<4:raise ValueError
        c=vals[0]+sum((i+1)*v for i,v in enumerate(vals[1:-2]))
        if c%103!=vals[-2]:
            if self._strict:raise ValueError
            print("checksum error")

    def vals_to_str(self, vals):
        it=iter(vals)
        s=next(it)
        if s==START_A:cur= "A"
        elif s==START_B:cur= "B"
        elif s==START_C:cur= "C"
        else:raise ValueError
        out=[];shift=False
        for v in list(it)[:-2]:
            if cur in {"A","B"} and v==98:
                shift=True;continue
            if v in {99,100,101}:
                cur={99:"C",100:"B",101:"A"}[v];continue
            if v in SPECIAL_REPR:
                out.append(SPECIAL_REPR[v]);continue
            eff=("B" if cur=="A" else "A") if shift else cur
            shift=False
            if eff=="C":
                if v>99:raise ValueError
                out.append(f"{v:02d}")
            elif eff=="A":
                if v<=95:out.append(ASCII_A[v])
                else:raise ValueError
            else:
                if v<=95:out.append(ASCII_B[v])
                else:raise ValueError
        return "".join(out)
