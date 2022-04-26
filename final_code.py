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



print('Do you want to convert back to machine code? (Y/N)')
x = input();

if (x == 'N'):
    quit()

print('\n')

def hexatobin(n):
    n = "{0:08b}".format(int(n, 16))
    if len(n)<32:
        diff = 32 - len(n)
        for i in range(diff):
            n = "0" + n
    return n


def decimalToBinary28(n):
    if(n>0):
        n = "{0:b}".format(int(n))
        if len(n)<28:
            diff = 28 - len(n)
            for i in range(diff):
                n = "0" + n
        return n
    else:
        n = n * (-1)
        x = bin((1<<28)-n)
        return x[2:]


def decimalToBinary32(n):
    if(n>0):
        n = "{0:b}".format(int(n))
        if len(n)<32:
            diff = 32 - len(n)
            for i in range(diff):
                n = "0" + n
        return n
    else:
        n = n * (-1)
        x = bin((1<<32)-n)
        return x[2:]


def binaryToDecimal(n):
    n = str(n)
    if n[0] is '0': 
        return int(n, 2)
    else:
        complementOf2 = int(n[1:], 2)
        return complementOf2 - 2**15
    

functDict = {'20': {'oprtn':'add','op_format': 0},'22': {'oprtn':'sub','op_format': 0},'24': {'oprtn':'and','op_format': 0},'25': {'oprtn':'or','op_format': 0},'27': {'oprtn':'nor','op_format': 0},'2a': {'oprtn':'slt','op_format': 0},'0': {'oprtn':'sll','op_format': 1}, '2': {'oprtn':'srl','op_format': 1}}
opcodes_type = {'0': {'op_type': 'R'}, '2': {'op_type': 'J', 'oprtn': 'j'}, '3': {'op_type': 'J', 'oprtn': 'jal'},'8': {'op_type': 'I', 'oprtn': 'addi', 'op_format': 1},'d': {'op_type': 'I', 'oprtn': 'or', 'op_format': 1},'c': {'op_type': 'I', 'oprtn': 'andi', 'op_format': 1},'a': {'op_type': 'I', 'oprtn': 'slti', 'op_format': 1},'2b': {'op_type': 'I', 'oprtn': 'sw', 'op_format': 4},'23': {'op_type': 'I', 'oprtn': 'lw', 'op_format': 4},'4': {'op_type': 'I', 'oprtn': 'beq', 'op_format': 5},'5': {'op_type': 'I', 'oprtn': 'bne', 'op_format': 5}}
regi = {0: '$zero', 1: '$at', 2: '$v0',3: '$v1',4: '$a0',5: '$a1',6: '$a2',7: '$a3',8: '$t0',9: '$t1',10:'$t2',11: '$t3',12: '$t4',13: '$t5',14: '$t6',15: '$t7',16: '$s0',17: '$s1',18: '$s2',19: '$s3', 20: '$s4',21: '$s5',22: '$s6',23: '$s7',24: '$t8',25: '$t9',26: '$k0',27: '$k1',28: '$gp',29: '$sp',30: '$fp',31: '$ra'}


# getting the txt
FileAddress = input('Text file or path for Machine Code: ')
MachineCode_file = open(FileAddress, 'r')

MachineCode_arr = [];
for i in MachineCode_file:
    MachineCode_arr.append(hexatobin(i));


# initialization
iniAddr = 4194304; PC = 4194304  # initial address -> 0x00400000 = 4194304
set = []; storeAddr = []; lableTags = {} # (addresses):(labels)



for mc in MachineCode_arr:
    data = opcodes_type[hex(int(mc[0:6], 2))[2:]] 
    PC = PC + 4

    # R-type
    if (data['op_type'] == 'R'):
        funct = hex(int(mc[26:32],2))[2:]

        oprtn = functDict[funct]['oprtn']
        op_format = functDict[funct]['op_format']

        rs = regi[int(mc[6: 11], 2)]; 
        rt = regi[int(mc[11:16], 2)]; rd = regi[int(mc[16:21], 2)]; 
        shamt = int(mc[21:26], 2)
                
        if (op_format == 0): set.append([oprtn + ' ' + rd + ' ' + rs + ' ' + rt, None])
        if (op_format == 1): set.append([oprtn + ' ' + rd + ' ' + rt + ' ' + str(shamt), None])
        if (op_format == 2): set.append([oprtn + ' ' + rs, None])
        # print(set)

    # I-type
    if (data['op_type'] == 'I'):
        oprtn =  data['oprtn']
        op_format = data['op_format']

        rs = regi[int(mc[6:11], 2)]; rt = regi[int(mc[11:16], 2)]; imm = str(binaryToDecimal(mc[16:]))
        
        if (op_format == 1): set.append([oprtn + ' ' + rt + ' ' + rs + ' ' + imm, None])
        elif (op_format == 3): set.append([oprtn + ' ' + rt + ' ' + imm, None])
        elif (op_format == 4): set.append([oprtn + ' ' + rt + ' ' + imm + '(' + rs + ')',None])
        elif (op_format == 5):
            imm = int(imm)
            addr = PC + 4 * imm
            if addr not in storeAddr: storeAddr.append(addr)
            set.append([oprtn + ' ' + rs + ' ' + rt + ' ' , addr])
    
    # J-type
    if (data['op_type'] == 'J'):
        oprtn = data['oprtn']

        addr = int(mc[6:], 2) << 2 
        addr = decimalToBinary32(PC)[0:4] + decimalToBinary28(addr)
        addr = int(addr, 2)

        if addr not in storeAddr: storeAddr.append(addr)
        set.append([oprtn + ' ' , addr])
    
    # print(set)


# sort the addresses
storeAddr.sort()    


l = 0 # starting LABEL
for addr in storeAddr:
    l += 1
    lableTags[addr] = 'L' + str(l)
    


# write in output file 
result = open('assembly_code.txt', 'w') 



count = 0
printArr = []



for i in set:
    addr = iniAddr + count   # iniAddr = 4194304
    label = ''
    if lableTags.get(addr) is not None: label = lableTags.get(addr)

    sw = label + ': ' + i[0]
    
    if i[1] is None:
        if label is '':
            sw = i[0]
    else:
        if label is '':
            sw = i[0] + lableTags[i[1]]
        else:
            sw = sw + lableTags[i[1]]

    count = count + 4        
    result.write(sw + '\n')
    printArr.append(sw)


# finish
result.close()
# output file updated

# print instructions
for i in printArr:
    print(i)
   
