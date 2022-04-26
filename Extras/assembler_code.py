from bitstring import BitArray

def hexatobin(n):
    n = "{0:08b}".format(int(n, 16))
    if len(n)<32:
        diff = 32 - len(n)
        for i in range(diff):
            n = "0" + n
    return n

def binToHexa(n):
    num = int(n, 2)
    hex_num = hex(num)
    hex_num = hex_num[2:]
    if len(hex_num)<8:
        diff = 8 - len(hex_num)
        for i in range(diff):
            hex_num = "0" + hex_num
    hex_num = "0x" + hex_num
    return(hex_num)

def decimalToBinary(n):
    n = "{0:b}".format(int(n))
    if len(n)<5:
        diff = 5-len(n)
        for i in range(diff):
            n = "0" + n
    return n

def decimalToBinary_I(n):
    n = int(n)
    if(n>0):
        n = "{0:b}".format(int(n))
        if len(n)<16:
            diff = 16-len(n)
            for i in range(diff):
                n = "0" + n
        return n
    else:
        n = n * (-1)
        x = bin((1<<16)-n)
        return x[2:]

def decimalToBinary_J(n):
    n = int(n)
    if(n>0):
        n = "{0:b}".format(int(n))
        if len(n)<26:
            diff = 26-len(n)
            for i in range(diff):
                n = "0" + n
        return n
    else:
        n = n * (-1)
        x = bin((1<<32)-n)
        return x[2:]

def dec2bin(dec, n_bits):
    if int(dec) < 0:
        dec = int(dec)
        b = BitArray(int=dec,length=n_bits)
        return b.bin
    else:
        return bin(int(dec))[2:].zfill(n_bits)

def binaryToDecimal(n):
    return int(n,2)

R_type = { "add":"100000", "sub":"100010", "jr":"001000", "slt":"101010", "and":"100100", "or":"100101", "nor":"100111", "srl":"000010", "sll":"000000"}
I_type = {"addi":"001000", "beq":"000100", "bne":"000101", "lw":"100011", "lhw":"100001", "lb":"100000", "sw":"101011", "shw":"101001", "sb":"101000"}
J_type = {"j":"000010", "jal":"000011"}
regi = {"$0":"00000","$at":"00001", "$v0":"00010", "$v1":"00011", "$a0":"00100", "$a1":"00101", "$a2":"00110", "$a3":"00111", "$t0":"01000", "$t1":"01001", "$t2":"01010", "$t3":"01011", "$t4":"01100", "$t5":"01101", "$t6":"01110", "$t7":"01111", "$s0":"10000", "$s1":"10001", "$s2":"10010","$s3":"10011", "$s4":"10100","$s5":"10101", "$s6":"10110", "$s7":"10111", "$t8":"11000", "$t9":"11001", "$k0":"11010", "$k1":"11011", "$gp":"11100", "$sp":"11101", "$fp":"11110", "$ra":"11111"}
load_store = ["lw", "lhw", "lb", "sw", "shw", "sb"]


FileAddress = input('Text file or path for the Assembly Code: ')
AssemblyCode_file = open(FileAddress, 'r')

result = []
set = []
for mipscode in AssemblyCode_file:
    inst = [ i for i in mipscode.split()]
    if len(inst) < 5 and 'j' not in inst:
        inst.insert(0,-1)
    set.append(inst)

for i in range(len(set)):
    # inst = [ i for i in input().split() ]
    # if len(inst) < 5 and 'j' not in inst:
    #     inst.insert(0,-1)
    # instruction_set.append(inst)
    # print(instruction_set)
    # print(inst)
    if set[i][1] in R_type:
        n = "000000"
        if set[i][1] == "sll" or set[i][1] == "srl":
            shamt = decimalToBinary(set[i][4])
            rs  = "00000"
            rt  = regi[set[i][3]]
            rd = regi[set[i][2]]
        elif set[i][1] == "jr":
            rs = regi[set[i][2]]
            rt = "00000"
            rd = "00000"
            shamt =  "00000"
        else:
            shamt = "00000"
            rs  = regi[set[i][3]]
            rt  = regi[set[i][4]]
            rd = regi[set[i][2]]
        funct = R_type[set[i][1]]
        n = n + rs + rt + rd + shamt + funct
        # print(n) 
        result.append(n)
    if set[i][1] in I_type:
        n = I_type[set[i][1]]
        if set[i][1] == "addi":
            rs = regi[set[i][3]]
            rt = regi[set[i][2]]
            imm = decimalToBinary_I(set[i][4])
        if set[i][1] in load_store:
            rt  = regi[set[i][2]]
            temp = set[i][3].split('(')
            imm = decimalToBinary_I(temp[0])
            rs_temp = temp[1].split(')')
            rs = regi[rs_temp[0]]
        if set[i][1] == "beq" or set[i][1] == "bne":
            rs = regi[set[i][2]]
            rt = regi[set[i][3]]
            index_f = -1
            for j in range(len(set)):
                if set[j][0] == set[i][4] + ':':
                    index_f = j
                    break
            offset = decimalToBinary_I(index_f-i-1)
            imm = offset
        n = n + rs + rt + imm
        # print(n)
        result.append(n)
    if set[i][0] in J_type:
        n = J_type[set[i][0]]
    # address = decimalToBinary_J(set[i][21])
        index_f = -1
        for j in range(len(set)):
            if set[j][0] == set[i][1] + ':':
                index_f = j
                break
        # print(index_f)
        address = dec2bin(index_f*4+4194304,32)
        address = address[4:]
        address = int(address,2)
        address = address/4
        address = dec2bin(address,26)
        n = n + address
        # print(n)
        result.append(n)
        
disassembledCode = open('MachineCode.txt','w')

for i in result:
    i = binToHexa(i)
    print(i)
    disassembledCode.write(i+'\n')

disassembledCode.close()
