#mapping of op_code and the instruction.
op_code ={
    "000011":"jal",  "000000":"addu",  "000100":"beq",  "101011":"sw",  "001000":"addi",  "000010":"j",
    "100011":"lw",  "000000":"sll",  "000000":"slt",  "000101":"bne",  "000000":"add",  "000000":"jr",
    "001101":"ori",  "001001":"addiu",  "001111":"lui", "000000":"sub"
}

#Program 1 is the sorting program. Program 2 is the factorial program.

#register file for the factorial program.
#PROGRAM 2
register ={
    "01000":" ",   "01001":" ",   "01010":" ",   "01011":" ",   "01100":" ",
    "01101":" ",   "01110":" ",   "01111":" ",   "11000":268501184,   "11001":268501224,
    "10000":" ",   "10001":" ",   "10010":" ",   "10011":" ",   "10100":" ",
    "10101":" ",   "10110":" ",   "10111":" ",   "11111":" ",   "00010":" ",
    "00000":0,   "00001":" "
}

#register file for the sorting program.
#PROGRAM 1
# register ={
#     "01000":" ",   "01001":6,   "01010":268501184,   "01011":268501224,   "01100":" ",
#     "01101":" ",   "01110":" ",   "01111":" ",   "11000":" ",   "11001":" ",
#     "10000":" ",   "10001":" ",   "10010":" ",   "10011":" ",   "10100":" ",
#     "10101":" ",   "10110":" ",   "10111":" ",   "11111":" ",   "00010":" ",
#     "00000":0,   "00001":" "
# }

#fuction code for the r type instructions.
fun_code ={
    "100000":"add",  "100001":"addu",  "100010":"sub",  "100100":"and",  "100101":"or",  "101010":"slt", "001000":"jr",
    "000000":"sll"
}

#instruction memory for the sorting program.
#PROGRAM 1
# instruction_mem ={  
#     4194380: "00000000000010110100000000100001",
#     4194384: "00000000000000001011100000100001",
#     4194388: "00100000000101100000000000000001",
#     4194392: "00000001001101101011000000100010",
#     4194396: "00010010111010010000000000000110",
#     4194400: "10001101010101010000000000000000",
#     4194404: "10101101011101010000000000000000",
#     4194408: "00100001010010100000000000000100",
#     4194412: "00100001011010110000000000000100",
#     4194416: "00100010111101110000000000000001",
#     4194420: "00001000000100000000000000010111",
#     4194424: "00000000000010000101100000100001",
#     4194428: "00000000000000001011100000100001",
#     4194432: "00010010111101100000000000011000",
#     4194436: "00000000000101110110000000100001",
#     4194440: "00100010111011010000000000000001",
#     4194444: "00010001101010010000000000001011",
#     4194448: "00000000000011001100000010000000",
#     4194452: "00000001011110001100000000100000",
#     4194456: "10001111000100000000000000000000",
#     4194460: "00000000000011011100100010000000",
#     4194464: "00000011001010111100100000100000",
#     4194468: "10001111001100010000000000000000",
#     4194472: "00000010001100000000100000101010",
#     4194476: "00010100001000000000000000000001",
#     4194480: "00000000000011010110000000100001",
#     4194484: "00100001101011010000000000000001",
#     4194488: "00001000000100000000000000100011",
#     4194492: "00000000000011000111100010000000",
#     4194496: "00000001011011110111100000100000",
#     4194500: "00000000000101110111000010000000",
#     4194504: "00000001110010110111000000100000",
#     4194508: "10001101111100100000000000000000",
#     4194512: "10001101110101000000000000000000",
#     4194516: "10101101110100100000000000000000",
#     4194520: "10101101111101000000000000000000",
#     4194524: "00100010111101110000000000000001",
#     4194528: "00001000000100000000000000100000",
#     4194532: "00000000000010000101100000100001",
# }


#instruction memory for the factorial program.
#PROGRAM 2
instruction_mem = { 
    4194356:"10001111000010000000000000000000",  
    4194360:"00100000000010110000000000000001",  
    4194364:"00000000000010000100100000100001", 
    4194368:"00100001000010101111111111111111",  
    4194372:"00010001010000000000000000000111", 
    4194376:"00100001010011000000000000000000", 
    4194380:"00100001001011010000000000000000", 
    4194384:"00100001010010101111111111111111",  
    4194388:"00010001100010111111111111111011",  
    4194392:"00100001100011001111111111111111",  
    4194396:"00000001001011010100100000100000",  
    4194400:"00010000000000001111111111111100",  
    4194404:"10101111001010010000000000000000"
}

data_mem = {
    268501184: 5,
    268501188: -40,
    268501192: -9,
    268501196: 0,
    268501200: 5,
    268501204: 7,
    268501208:'',
    268501212:'',
    268501216:'',
    268501220:'',
    268501224:'',
    268501228:'',
    268501232:'',
    268501236:'',
    268501240:'',
    268501244:'',
    268501248:'',
    268501252:'',
    268501256:'',
}

#PC = 4194380  #for program 1
PC = 4194356   #for program 2
clk1 = 0
clk2 = 0
clk3 = 0
clk4 = 0
clk5 = 0

#fuction returns the 2's complement. This is used to convert the negative binary offset of the beq and bne to integers.
def twos_complement(binary_str):
    # Invert all bits
    inverted_str = ''.join('1' if bit == '0' else '0' for bit in binary_str)
    # Add 1 to the inverted binary number
    result = bin(int(inverted_str, 2) + 1)[2:]
    return int(result, 2)

def is_negative(binary_str):
    return binary_str[0] == '1'

def sign_extend(str): #function to perform sign extend of 16 bit to 32 bit
    # Checking of the most significant bit
    msb = str[0]
    # If MSB is 0, perform zero extension
    if msb == '0':
        return '0' * 16 + str
    # If MSB is 1, perform sign extension
    elif msb == '1':
        return '1' * 16 + str

#function to fetch instruction.
def fetch(pc):
    
    global PC
    instr = instruction_mem[pc]
    #PC = int(PC, 2) #converts the binary string PC to an integer
    PC += 4
    print("PC:",PC)
    #PC = format(PC_int, '032b') #converts the result back to a 32-bit binary string
    decode(instr)
    global clk1
    clk1 += 1

#function that checks the op_code and returns the control signals.
def control(instr):
    RegDst = None
    Branch_eq = None
    Branch_neq = None
    MemRead = None
    MemtoReg = None
    MemWrite = None
    ALUSrc = None
    RegWrite = None
    Jmp = None
    ALUCtrl = None
    op = instr[0:6]
    if(op == "000000"):
        #print("branch")
        RegDst = 1
        Branch_eq = 0
        Branch_neq = 0
        MemRead = 0
        MemtoReg = 0
        MemWrite = 0
        ALUSrc = 0
        RegWrite = 1
        Jmp = 0
        funct = instr[26:]
        if(funct == "100000" or funct == "100001"): 
            ALUCtrl = "010" #add and addu
        elif(funct == "100010"):
            ALUCtrl = "011" #sub
        elif(funct == "101010"):
            ALUCtrl = "100" #slt
        elif(funct == "100100"):
            ALUCtrl = "000" #and
        elif(funct == "100101"):
            ALUCtrl = "001" #or
        elif(funct == "000000"):
            ALUCtrl = "101" #sll
        elif(funct == "001000"):
            ALUCtrl = "110" #jr
    if(op == "100011"):#lw
        RegDst = 0
        Branch_eq = 0
        Branch_neq = 0
        MemRead = 1
        MemtoReg = 1
        MemWrite = 0
        ALUSrc = 1
        RegWrite = 1
        Jmp = 0
        ALUCtrl = "010"
    if(op == "101011"):#sw
        RegDst = "x"
        Branch_eq = 0
        Branch_neq = 0
        MemRead = 0
        MemtoReg = "x"
        MemWrite = 1
        ALUSrc = 1
        RegWrite = 0
        Jmp = 0
        ALUCtrl = "010"
    if(op == "001000"):#addi
        #print("ctrl")
        RegDst = 0
        Branch_eq = 0
        Branch_neq = 0
        MemRead = 0
        MemtoReg = 0
        MemWrite = 0
        ALUSrc = 1
        RegWrite = 1
        Jmp = 0
        ALUCtrl = "010"
    if(op == "000100" or op == "000101"):#beq and #bne
        RegDst = "x"
        if(op == "000100"):
            Branch_eq = 1
            Branch_neq = 0
        elif(op == "000101"):
            Branch_neq = 1
            Branch_eq = 0
        MemRead = 0
        MemtoReg = "x"
        MemWrite = 0
        ALUSrc = 0
        RegWrite = 0
        Jmp = 0
        ALUCtrl = "011"
    if(op == "000010"):#j
        RegDst = "x"
        Branch_eq = "x"
        Branch_neq = "x"
        MemRead = 0
        MemtoReg = "x"
        MemWrite = 0
        ALUSrc = "x"
        RegWrite = 0
        Jmp = 1
        ALUCtrl = "111"
    return [RegDst, Branch_eq, MemRead, MemtoReg, MemWrite, ALUSrc, RegWrite, Jmp, ALUCtrl, Branch_neq]

#function to decode the instruction.
def decode(instr):
    offset = None
    addr = None
    read_data2 = None
    write_reg = None
    ctrl_sig = control(instr)
    if(instr[0:6] == "000000" and instr[26:] == "000000"):  #for sll instruction.
        rt = register[instr[11:16]]     #rs is zero register. 
        shamt = instr[21:26]
        shamt = int(shamt, 2)
        write_reg = instr[16:21]
        execute(rt, shamt, offset, write_reg, addr,ctrl_sig)
    read_data1 = register[instr[6:11]] #reading content from rs register.
    if(ctrl_sig[0] == 1):#Reg_Dst is 1 write reg is the rd register.
        write_reg = instr[16:21] 
    elif(ctrl_sig[0] == 0): #Reg_Dst is 0 write reg is rt register.
        write_reg = instr[11:16]
    else:
        write_reg = "-1" #if reg_dst is 'X'
    if(ctrl_sig[5] == 0): #r-type bne and beq the ALU_Src is 0
        read_data2 = register[instr[11:16]] #reading content from rt register.
        if(ctrl_sig[1] == 1 or ctrl_sig[9] == 1):
            if(is_negative(instr[16:])):
                offset = -1*(twos_complement(instr[16:]))
            else:
                offset = sign_extend(instr[16:])
                offset = int(offset, 2)
    elif(ctrl_sig[5] == 1): #lw and sw and addi
        read_data2 = register[instr[11:16]]   #sw reading data from rt.
        if(is_negative(instr[16:])):
            offset = -1*(twos_complement(instr[16:]))
        else:
            offset = sign_extend(instr[16:])
            offset = int(offset, 2)
    if(ctrl_sig[7] == 1):   #for jump instruction.
        addr = "0000" + instr[6:] + "00"    #address.
    if(ctrl_sig[8] != "101"):   #executing only when when alu_op is not of sll instruction.
        execute(read_data1, read_data2, offset, write_reg, addr, ctrl_sig)
    global clk2
    clk2 += 1

def execute(data1, data2, offset, write_reg, addr, ctrl_sig):
    write_data = None
    alu_res = None
    global PC
    if(ctrl_sig[8] == "010"): #lw sw and addi and r type.
        if(ctrl_sig[5] == 1):
            alu_res = data1 + offset #lw, sw, addi
            write_data = data2 #needed only for sw
        elif(ctrl_sig[5] == 0):
            alu_res = data1 + data2 #r type.
    elif(ctrl_sig[8] == "011"): #sub
        alu_res = data1 - data2
        if(alu_res == 0 and ctrl_sig[1] == 1):#beq
            offset = offset * 4
            PC = offset + PC
        elif(alu_res != 0 and ctrl_sig[9] == 1):#bne
            offset = offset * 4
            PC = offset + PC
    elif(ctrl_sig[8] == "000"): #and
        alu_res = data1 & data2
    elif(ctrl_sig[8] == "001"): #or
        alu_res = data1 | data2
    elif(ctrl_sig[8] == "100"): #slt
        if(data1 < data2):
            alu_res = 1
        else:
            alu_res = 0
    elif(ctrl_sig[8] == "101"): #sll
        alu_res = data1 << data2
    if(ctrl_sig[7] == 1):
        PC = int(addr, 2)
    mem(alu_res, write_data, write_reg, ctrl_sig)
    global clk3
    clk3 += 1

def mem(alu_res, write_data, write_reg, ctrl_sig):
    read_data = None
    if(ctrl_sig[2] == 1): #lw MemRead is 1.
        read_data = data_mem[alu_res]
        
    if(ctrl_sig[4] == 1): #sw MemWrite is 1.
        data_mem[alu_res] = write_data
    write_back(read_data, alu_res, write_reg, ctrl_sig)
    global clk4
    clk4 += 1

def write_back(read_data, alu_res, write_reg, ctrl_sig):
    if(ctrl_sig[3] == 0):   #memtoreg for r type is 0 
        register[write_reg] = alu_res

    if(ctrl_sig[3] == 1):   #memtoreg for lw is 1.
        register[write_reg] = read_data
    global clk5
    clk5 += 1


#PROGRAM 2  
while(PC != 4194408):
      fetch(PC)

#PROGRAM 1
#while(PC != 4194532):
#    fetch(PC)
print("\n")
print("Data Memory:")
for key, val in data_mem.items():
   print(f"{key} : {val}")
print("\n")
print("Register file;")
for key, val in register.items():
   print(f"{key} : {val}")

print("fetch stage:",clk1)
print("decode stage:",clk2)
print("execute stage:",clk3)
print("memory stage:",clk4)
print("writeback stage:",clk5)
print("Total number of clock cycles = ", clk1 + clk2 + clk3 + clk4 + clk5)









    