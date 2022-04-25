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
                
        if (op_format == 0): set.append([oprtn + ' ' + rd + ' ' + rs + ' ' + rt, -1])
        if (op_format == 1): set.append([oprtn + ' ' + rd + ' ' + rt + ' ' + str(shamt), -1])
        if (op_format == 2): set.append([oprtn + ' ' + rs, -1])
        # print(set)

    # I-type
    if (data['op_type'] == 'I'):
        oprtn =  data['oprtn']
        op_format = data['op_format']

        rs = regi[int(mc[6:11], 2)]; rt = regi[int(mc[11:16], 2)]; imm = str(binaryToDecimal(mc[16:]))
        
        if (op_format == 1): set.append([oprtn + ' ' + rt + ' ' + rs + ' ' + imm, -1])
        elif (op_format == 3): set.append([oprtn + ' ' + rt + ' ' + imm, -1])
        elif (op_format == 4): set.append([oprtn + ' ' + rt + ' ' + imm + '(' + rs + ')',-1])
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
    label = 'x'
    if lableTags.get(addr) is not None: label = lableTags.get(addr)

    sw = label + ': ' + i[0]
    if (i[1] == -1 and label[0] != 'L'):
        sw = i[0]
    elif (label[0] == 'L'):
        sw = sw + lableTags[i[1]]
    else:
        sw = i[0] + lableTags[i[1]]


    result.write(sw + '\n')
    printArr.append(sw)  
    count = count + 4        

# finish
result.close()
# output file updated

# print instructions
for i in printArr:
    print(i)
   
 
