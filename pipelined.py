from queue import Queue
# Mapping of op_code and the corresponding instruction.
op_code ={
    "000011":"jal",  "000000":"addu",  "000100":"beq",  "101011":"sw",  "001000":"addi",  "000010":"j",
    "100011":"lw",  "000000":"sll",  "000000":"slt",  "000101":"bne",  "000000":"add",  "000000":"jr",
    "001101":"ori",  "001001":"addiu",  "001111":"lui", "000000":"sub"
}

#Program 1 is the sorting program. Program 2 is the factorial program.
#PROGRAM 1
#register file for the sorting program.
# register ={
#     "01000":" ",   "01001":6,   "01010":268501184,   "01011":268501220,   "01100":" ",
#     "01101":" ",   "01110":" ",   "01111":" ",   "11000":" ",   "11001":" ",
#     "10000":" ",   "10001":" ",   "10010":" ",   "10011":" ",   "10100":" ",
#     "10101":" ",   "10110":" ",   "10111":" ",   "11111":" ",   "00010":" ",
#     "00000":0,   "00001":" "
# }

#fuction code for the R type instructions.
fun_code ={
    "100000":"add",  "100001":"addu",  "100010":"sub",  "100100":"and",  "100101":"or",  "101010":"slt", "001000":"jr",
    "000000":"sll"
}

# Register file for the factorial program.
#PROGRAM 2
register ={
    "01000":5,   "01001":" ",   "01010":" ",   "01011":" ",   "01100":" ",
    "01101":" ",   "01110":" ",   "01111":" ",   "11000":" ",   "11001":268501224,
    "10000":" ",   "10001":" ",   "10010":" ",   "10011":" ",   "10100":" ",
    "10101":" ",   "10110":" ",   "10111":" ",   "11111":" ",   "00010":" ",
    "00000":0,   "00001":" "
}

# Instruction memory for the sorting program.
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
#     4194532: "00000000000010000101100000100001"
# }

# Instruction memory for the factorial program.
#PROGRAM 2
instruction_mem = {   
    4194360:"00100000000010110000000000000001",  
    4194364:"00000000000010000100100000100001", 
    4194368:"00100001000010101111111111111111",  
    4194372:"00010001010010110000000000001000", 
    4194376:"00100000000101110000000000000001",
    4194380:"00100001010011000000000000000000", 
    4194384:"00100001001011010000000000000000", 
    4194388:"00100001010010101111111111111111",  
    4194392:"00010001100010111111111111111010",  
    4194396:"00100001100011001111111111111111",  
    4194400:"00000001001011010100100000100000",  
    4194404:"00010000000000001111111111111100",  
    4194408:"10101111001010010000000000000000",
}

# Data memory
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
    268501256:''
}

clk1 = 0
clk2 = 0
clk3 = 0
clk4 = 0
clk5 = 0

IF = Queue()
ID = Queue()
EX = Queue()
MEM = Queue()
WB = Queue()
fwd = []

# Initialize the IF queue with all the instruction addresses.
for key in instruction_mem.keys():
    IF.put(key)

#pipelined registers
IF_ID = []
ID_EX = []
EX_MEM = []
MEM_WB = []

#fuction returns the 2's complement. This is used to convert the negative binary offset of the beq and bne to integers.
def twos_complement(binary_str):
    # Invert all bits
    inverted_str = ''.join('1' if bit == '0' else '0' for bit in binary_str)
    # Add 1 to the inverted binary number
    result = bin(int(inverted_str, 2) + 1)[2:]
    return int(result, 2) #integer value


# Function to check if a binary string represents a negative number.
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

# Function to fetch an instruction from the instruction memory.
def fetch(pc):
    if(pc == "nop"): #if the instruction in the instruction memory is nop, we do nothing
        ID.put("nop")
        return
    global IF_ID
    instr = instruction_mem[pc]
    print("PC:",pc)
    ctrl_sig = control(instr)
    #the pipelined register IF_ID is passed with PC and control signals
    IF_ID = [pc, ctrl_sig] 
    ID.put(IF_ID)


#function representing the control unit, where the control signals are generated based on the opcode
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
    if(op == "000000"): # r type
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

# Function to decode an instruction
def decode():
    global IF_ID
    global ID_EX
    IF_ID = ID.get()
    # If the instruction is "nop," do nothing and pass it along the pipeline.
    if(IF_ID == "nop"):
        EX.put("nop")
        return
    offset = None
    addr = None
    read_data2 = None
    write_reg = None
    instr = instruction_mem[IF_ID[0]]
    ctrl_sig = IF_ID[1]
    #sll instruction
    if(instr[0:6] == "000000" and instr[26:] == "000000"):
        rt = register[instr[11:16]]     #rs is zero register.
        shamt = instr[21:26]
        shamt = int(shamt, 2)
        write_reg = instr[16:21]
        d = {
        "rs": [instr[6:11],None], "rt": [instr[11:16],None], "rd": [instr[16:21],None]
        }
        p_c = IF_ID[0]
        sig = IF_ID[1]
        d["rs"][1] = None
        d["rt"][1] = rt
        # Store decoded information in ID_EX pipeline register.
        ID_EX = [d, sig, rt, shamt, offset, write_reg, addr, p_c]
        EX.put(ID_EX)
    #reading content from rs register.
    read_data1 = register[instr[6:11]] #rs
    if(ctrl_sig[0] == 1):#Reg_Dst is 1 write reg is the rd register.
        write_reg = instr[16:21] #rd
    elif(ctrl_sig[0] == 0):#Reg_Dst is 0 write reg is the rt register.
        write_reg = instr[11:16] #rt
    else:
        write_reg = "-1" #if reg_dst is 'X', nothing to be written back
    if(ctrl_sig[5] == 0): #r-type bne and beq the ALU_Src is 0
        read_data2 = register[instr[11:16]]
        if(ctrl_sig[1] == 1 or ctrl_sig[9] == 1): #for beq and bne
            if(is_negative(instr[16:])):
                offset = -1*(twos_complement(instr[16:]))
            else:
                offset = sign_extend(instr[16:]) #16 bit to 32 bit conversion
                offset = int(offset, 2) #converting binary string into integer value
    elif(ctrl_sig[5] == 1): #lw and sw and addi
        read_data2 = register[instr[11:16]] 
        if(is_negative(instr[16:])):
            offset = -1*(twos_complement(instr[16:]))
        else:
            offset = sign_extend(instr[16:])
            offset = int(offset, 2)
    if(ctrl_sig[7] == 1):   #for jump instruction.
        addr = "0000" + instr[6:] + "00" #appending 4 zeroes at the beginning and 2 at the end
    global clk2
    clk2 += 1
    if(ctrl_sig[8] != "101"): #when not sll instruction
        d = {
        "rs": [instr[6:11],None], "rt": [instr[11:16],None], "rd": [instr[16:21],None]
        }
        p_c = IF_ID[0]
        sig = IF_ID[1]
        d["rs"][1] = read_data1
        d["rt"][1] = read_data2
         # Store decoded information in ID_EX pipeline register.
        ID_EX = [d, sig, read_data1, read_data2, offset, write_reg, addr, p_c]
        EX.put(ID_EX)
        #checking for dependencies
        forwarding_unit()
        #cheking for control hazards incase of beq and bne instructions 
        if(instr[0:6] == "000100" or instr[0:6] == "000101"):
            control_hazard()


#function representing the forwarding unit of the processor, generates forwarding signals checking the dependencies
def forwarding_unit():
    global fwd
    global EX_MEM
    global ID_EX
    global MEM_WB
    fwdA = None
    fwdB = None
    #Mem hazard
    if(len(MEM_WB) > 0 and len(ID_EX) > 0 and MEM_WB[1][6]):
        dict1 = MEM_WB[0]
        dict2 = ID_EX[0]
        if(dict1["rd"][0] != "00000" and (dict1["rd"][0] == dict2["rs"][0])):
            fwdA = "01"
        if(dict1["rd"][0] != "00000" and (dict1["rd"][0] == dict2["rt"][0])):
            fwdB = "01"
    #EX hazard
    if(len(EX_MEM) > 0 and len(ID_EX) > 0 and EX_MEM[1][6]):
        dict1 = EX_MEM[0]
        dict2 = ID_EX[0]
        if((EX_MEM)[1][0] == 0 and EX_MEM[1][2] == 0 and dict1["rt"][0] != "00000" and (dict1["rt"][0] == dict2["rs"][0])):
            fwdA = "11" #addi
        if((EX_MEM)[1][0] == 0 and EX_MEM[1][2] == 0 and dict1["rt"][0] != "00000" and (dict1["rt"][0] == dict2["rt"][0])):
            fwdB = "11" #addi
        if(dict1["rd"][0] != "00000" and (dict1["rd"][0] == dict2["rs"][0])):
            fwdA = "10"
        if(dict1["rd"][0] != "00000" and (dict1["rd"][0] == dict2["rt"][0])):    
            fwdB = "10"
    #hazard in the case of instruction lw followed by sw
    if(len(MEM_WB) > 0 and len(EX_MEM) > 0 and (MEM_WB[0]["rt"][0] == EX_MEM[0]["rt"][0]) and (EX_MEM[1][4] == 1)):
        fwdA = "00"
    fwd =  [fwdA,fwdB]

#function to check if there is a need to stall
def hazard_detection_unit():
    #stall in the case of lw followed by r type instruction
    ID_EX = EX.queue[0]
    instr = instruction_mem[IF_ID[0]]
    d = {
        "rs": [instr[6:11],None], "rt": [instr[11:16],None], "rd": [instr[16:21],None], "offset": [offset]
    }
    if(ID_EX[1][2] and ((ID_EX[0]["rt"][0] == d["rs"][0]) or (ID_EX[0]["rt"][0] == d["rt"][0]))):
         IF.put("nop")
    

def execute():
    global ID_EX
    global EX_MEM
    global MEM_WB
    global fwd
    ID_EX = EX.get()
    if(ID_EX == "nop"):#do nothing inacse of nop
        MEM.put("nop")
        return
    d = ID_EX[0]
    data1 = ID_EX[2]
    data2 = ID_EX[3]
    offset = ID_EX[4]
    write_reg = ID_EX[5]
    addr = ID_EX[6]
    ctrl_sig = ID_EX[1]
    write_data = None
    alu_res = None
    '''conditions to check if we need to take values from the pipeline register of the corresponding 
    stage or take the forwarded values from other pipelines based on the signals generated by forwarding unit'''
    if(((ctrl_sig[8] == "010" and ctrl_sig[5] == 0) or ctrl_sig[8] == "011" or ctrl_sig[8] == "101" or ctrl_sig[8] == "000" or ctrl_sig[8] == "001" or ctrl_sig[8] == "100") and len(fwd) > 0):
        if(fwd[0] == "11"):
            data1 = EX_MEM[0]["rt"][1]
        if(fwd[1] == "11"):
            data2 = EX_MEM[0]["rt"][1]
            #print("sub data2", data2)
        if(fwd[0] == "10"):
            data1 = EX_MEM[0]["rd"][1]
            #print("data1 of add after sll", data1)
        if(fwd[0] == "01"):
             data1 = MEM_WB[0]["rd"][1]
            #print("data1 after mem", data1)
        if(fwd[1] == "10"):
            data2 = EX_MEM[0]["rd"][1]
        if(fwd[1] == "01"):
             data2 = MEM_WB[0]["rd"][1]
    p_c = ID_EX[7]
    if(ctrl_sig[8] == "010"):
        if(ctrl_sig[5] == 1 ):
            if(len(fwd) > 0 and fwd[0] == "10"):
                data1 = EX_MEM[0]["rd"][1] #take forwarded values incase of
            elif(len(fwd) > 0 and fwd[0] == "01" ):
                data1 = MEM_WB[0]["rt"][1]
            alu_res =  data1 + offset #lw, sw, addi
            if(ctrl_sig[3] == 0):
                d["rt"][1] = alu_res
            write_data = data2 #needed only for sw
        elif(ctrl_sig[5] == 0):
            alu_res = data1 + data2 #r
            d["rd"][1] = alu_res
    elif(ctrl_sig[8] == "011"): #sub
        alu_res = data1 - data2
        d["rd"][1] = alu_res
    elif(ctrl_sig[8] == "000"): #and
        alu_res = data1 & data2
        d["rd"][1] = alu_res
    elif(ctrl_sig[8] == "001"): #or
        alu_res = data1 | data2
        d["rd"][1] = alu_res
    elif(ctrl_sig[8] == "100"): #slt
        if(data1 < data2):
            alu_res = 1
            d["rd"][1] = alu_res
        else:
            alu_res = 0
            d["rd"][1] = alu_res
        #print("$s0", register["10000"])
        #print("$s1",register["10001"])
    elif(ctrl_sig[8] == "101"): #sll
        #data2 = int(data2, 2)
        #print("in sll", data1)
        #print("in sll", data2)
        alu_res = data1 << data2
        d["rd"][1] = alu_res
    if(ctrl_sig[7] == 1):
        x = int(addr, 2)
        while not IF.empty(): #pipeline flush
            IF.get()
        while not ID.empty(): #pipeline flush
            ID.get()
        #update the If with new instructions as per the jump instruction's target address 
        last_instr = list(instruction_mem.keys())[-1]
        while(x <= last_instr):
            IF.put(x)
            x += 4
    EX_MEM = [d, ctrl_sig, alu_res, write_data, write_reg, p_c]
    MEM.put(EX_MEM)

#function to identify the control hazards incase of beq and bne instructions
def control_hazard():
    ID_EX = EX.queue[0]
    global EX_MEM
    d = ID_EX[0]
    data1 = d["rs"][1]
    data2 = d["rt"][1]
    d2 = EX_MEM[0] #for the hazard when r type followed by beq 
    if(IF_ID[1][9] == 1 or IF_ID[1][1] == 1):
        if(fwd[0] == "10"):
            data1 = d2["rd"][1]
        if(fwd[1] == "10"):
            data2 = d2["rd"][1]
        if(fwd[0] == "11"):
            data1 = d2["rt"][1]
        if(fwd[1] == "11"):
            data2 = d2["rt"][1]
        alu_res = data1 - data2
        if(alu_res == 0 and IF_ID[1][1] == 1):#beq
            offset = ID_EX[4] * 4 
            x = offset + ID_EX[7]
            x = x + 4
            #in case of control hazard(when condition is satisfied) in beq, flush the pipeline
            while not IF.empty(): #pipeline flush
                IF.get()
            #and then update the pipeline with new instructions
            last_instr = list(instruction_mem.keys())[-1]
            while(x <= last_instr):
                IF.put(x)
                x += 4
        elif(alu_res != 0 and IF_ID[1][9] == 1):#bne
            offset = ID_EX[4] * 4
            x = offset + ID_EX[7]
            x = x + 4
            while not IF.empty():  #pipeline flush
                IF.get()
            last_instr = list(instruction_mem.keys())[-1]
            while(x <= last_instr):
                IF.put(x)
                x += 4

def mem():
    global MEM_WB
    global EX_MEM
    global fwd
    EX_MEM = MEM.get()
    if(EX_MEM == "nop"):#if nop do nothing
        WB.put("nop")
        return
    #extract the values required from pipelined registers
    read_data = None
    alu_res = EX_MEM[2]
    write_data = EX_MEM[3]
    write_reg = EX_MEM[4]
    ctrl_sig = EX_MEM[1]
    d = EX_MEM[0]
    if(ctrl_sig[2] == 1): #lw MemRead is 1.
        read_data = data_mem[alu_res]
        d["rt"][1] = read_data
    if(ctrl_sig[4] == 1): #sw MemWrite is 1.
        if(fwd[0] == "00"):
            write_data = MEM_WB[0]["rt"][1]
        data_mem[alu_res] = write_data
    d = EX_MEM[0]
    p_c = EX_MEM[5]

    MEM_WB = [d, ctrl_sig, read_data, alu_res, write_reg, p_c]
    WB.put(MEM_WB)

def write_back():
    rand = WB.get()
    if(rand == "nop"):
        return
    read_data = rand[2]
    alu_res = rand[3]
    write_reg = rand[4]
    ctrl_sig = rand[1]
    if(ctrl_sig[3] == 0):   #memtoreg for r type is 0 
        register[write_reg] = alu_res
    if(ctrl_sig[3] == 1):   #memtoreg for lw is 1.
        register[write_reg] = read_data
    # for key, val in data_mem.items():
    #      print(f"{key} : {val}")

cnt = 0
while (True):
    #keep executing the stages whenever the queues are not empty, assuming that they happen simultaneously
    if not WB.empty():
        write_back()
    if not MEM.empty():
        mem()
    if not EX.empty():
        execute()
    if not ID.empty():
        decode()
    if not IF.empty():
        fetch(IF.get())
    if(IF.empty() and ID.empty() and EX.empty() and MEM.empty() and WB.empty()): #if all queues are empty, break from the loop
        break
    cnt += 1

print("\n")
print("data Memory")
for key, val in data_mem.items():
    print(f"{key} : {val}")
print("\n")
print("Register File")
for key, val in register.items():
    print(f"{key}: {val}")
print("\n")
print("Number of clock cycles", cnt)









    