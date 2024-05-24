import re

#label address mappings
j_map = {'loop1': 4194348, 'loopi': 4194396, 'loop2': 4194432, 'loop3': 4194444, 'loop': 4194540 }

jal_map = {'print_int': 4194592, 'input_int': 4194576, 'print_line': 4194608, 'print_inp_int_statement': 4194648, 
            'print_out_int_statement': 4194668, 'print_inp_statement': 4194628, 'print_enter_int': 4194688}

beq_map = {'loop1end': 6, 'loopiend': 6, 'loop2end': 24, 'loop3end': 11, 'end': 6}

ori_map = {'enter_int': 157, 'out_int_statement': 101, 'inp_int_statement': 47, 'inp_statement': 2, 'next_line': 0,  }

#register mapping
register ={
    "$t0":"01000",   "$t1":"01001",   "$t2":"01010",   "$t3":"01011",   "$t4":"01100",
    "$t5":"01101",   "$t6":"01110",   "$t7":"01111",   "$t8":"11000",   "$t9":"11001",
    "$s0":"10000",   "$s1":"10001",   "$s2":"10010",   "$s3":"10011",   "$s3":"10100",
    "$s5":"10101",   "$s6":"10110",   "$s7":"10111",    "$ra":"11111",  "$v0":"00010",
    "$0":"00000",    "$1":"00001",    "$at":"00001",    "$a0":"00100"    
}

#op code mapping
op_code ={
    "jal":"000011",  "addu":"000000",  "beq":"000100",  "sw":"101011",  "addi":"001000",  "j":"000010",
    "lw":"100011",  "sll":"000000",  "slt":"000000",  "bne":"000101",  "add":"000000",  "jr":"000000",
    "ori":"001101",  "addiu":"001001",  "lui":"001111", "sub":"000000"
}

#function code mapping
fun_code ={
    "add":"100000",  "addu":"100001",  "sub":"100010",  "and":"100100",  "or":"100101",  "slt":"101010",  "jr":"001000",
    "sll":"000000", "sub": "100010"
}

#fuction to convert the assembly instruction to machine code. (binary and hex)
def assembly_machine(instruction):
    if(instruction == "syscall"):
        return "0"*28 + "1100"
    parts = instruction.split()
    op = parts[0].strip()	#storing the op code in op.
    if(op == "add" or op == "sub" or op == "addu" or op == "slt"):
        rd,rs,rt = map(lambda x : x.strip(","),parts[1:])	#storing the registers in variables.
        machine_code = op_code[op] + register[rs] + register[rt] + register[rd] + "00000" + fun_code[op]	#generating machine code.
        return machine_code

    elif(op == "sll"):
        rd,rt,shift_amt = map(lambda x : x.strip(","),parts[1:])	#storing the registers and shift amt in variables.
        shamt = format(int(shift_amt),'05b')    #converting the shift_amt into 5bit
        machine_code = op_code[op] + register["$0"] + register[rt] + register[rd] + shamt + fun_code[op]    #generating the machine code.
        return machine_code

    elif(op == "addi" or op == "ori" or op == "addiu"):
        rt,rs,immediate = map(lambda x : x.strip(","),parts[1:])    #storing the registers and immediate value in variables.
        immediate = format(int(immediate),'016b')   #converting the immediate value into 16bit
        machine_code = op_code[op] + register[rs] + register[rt] + immediate    #generating the machine code.
        return machine_code
    
    elif(op == "beq" or op == "bne"):
        rt,rs,immediate = map(lambda x : x.strip(","),parts[1:])    #storing the registers and relative address into variable.
        immediate = format(int(immediate),'016b')   #converting the relative address into 16 bit.
        machine_code = op_code[op] + register[rt] + register[rs] + immediate    #generating the machine code.
        return machine_code

    elif(op == "sw" or op == "lw"):
        rt, offset_b = map(lambda x : x.strip(","),parts[1:])   #storing the register and offset in variable.
        offset = int(offset_b.split('(')[0])
        base_r = offset_b.split('(')[1][:-1].strip()    #storing the base register in variable.
        offset = format(offset,'016b')  #converting offset to 16 bit.
        machine_code = op_code[op] + register[base_r] + register[rt] + offset    #generating the machine code.
        return machine_code

    elif(op =="lui"):
        rt,immediate = map(lambda x : x.strip(","),parts[1:])   #storing the register and immediate value in variable.
        immediate = format(int(immediate),'016b')   #converting the immediate value to 16bit
        machine_code = op_code[op] + register["$0"] + register[rt] + immediate    #generating the machine code.
        return machine_code

    elif(op == "jal" or op == "j"):
        target_add = parts[1].strip()   #storing the target address in a variable.
        target_bin = format(int(target_add),'032b')     #converting it into 32 bit binary.
        target_bin = target_bin[:-2]	#removing 2 lsb.
        target_bin = target_bin[4:]	#removing 4 msb
        machine_code = op_code[op] + target_bin    #generating the machine code.
        return machine_code

    elif(op == "jr"):
        r = parts[1].strip()	#storing the return register in the variable.
        machine_code = op_code[op] + register[r] + register["$0"] + register["$0"] + register["$0"] + fun_code[op]    #generating the machine code.
        return machine_code

#function to write output to a file
def write_to_file(code, output_file):
    with open(output_file, 'w') as file:  
        file.write('\n'.join(code))  #write list of machine code(binary and hex strings) to output file

#
def create_lines(filename):
    lines_list = [] #list to store the modified assembly instructions
    with open(filename, 'r') as f:
        lines = f.readlines()  
        
        for line in lines: #iterate through each line in the input assembly file
            line = line.strip()
            
            #skip lines that are comments, those starting with #, and data related instructions
            if line == '' or line.startswith('#') or line.startswith('.data') or line.startswith('next_line') \
                or line.startswith('inp_statement') or line.startswith('inp_int_statement') \
                or line.startswith('out_int_statement') or line.startswith('enter_int') or line.startswith('.text'):
                continue
            
            #tokenize each line by splitting the line at delimiters like ',','\s' and ':'
            tokens = re.split(r'[,\s:]+', line) 
            
            #replace the register $zero with $0 in the tokens
            for i, token in enumerate(tokens):
                if token == "$zero":
                    tokens[i] = '$0'
            #processing different kinds of instructions(pseudo instructions and label containing instructions)
            if tokens[0] == 'move':
                #convert "move" to "addu" instruction
                l = f'addu {tokens[1]} $0 {tokens[2]}' 
                lines_list.append(l)
            elif len(tokens) >= 2 and tokens[1] == 'move':
                l = f'addu {tokens[2]} $0 {tokens[3]}'
                lines_list.append(l)
            elif tokens[0] == 'bgt':
                #convert "bgt" instruction to "slt" instruction followed by "bne" instruction
                l = f'slt $1 {tokens[2]} {tokens[1]}'
                lines_list.append(l)
                l = f'bne $at $0 1'
                lines_list.append(l)
            elif len(tokens) >= 2 and tokens[1] == 'li':
                #convert "li" instruction to "addiu" instruction
                l = f'addiu {tokens[2]} $0 {tokens[3]}'
                lines_list.append(l)
            elif tokens[0] == 'la':
                #convert "la" instruction to "lui" instruction followed by "ori" instruction
                l = f'lui $at 4097'
                lines_list.append(l)
                l = f'ori $a0 $at {ori_map[tokens[2]]}'
                lines_list.append(l)
            elif tokens[0] == 'jal':
                #using address mapping to modify "jal" instruction
                l = f'jal {jal_map[tokens[1]]}'
                lines_list.append(l)
            elif tokens[0] == 'j':
                #modifying "j" instruction using address mapping
                l = f'j {j_map[tokens[1]]}'
                lines_list.append(l)
            elif len(tokens) >= 2 and tokens[1] == 'beq':
                #using address mapping to modify "beq" instruction
                l = f'beq {tokens[2]} {tokens[3]} {beq_map[tokens[4]]}'
                lines_list.append(l)
            elif len(tokens) >= 2 and tokens[1] == 'addi':
                #removing the target preceding
                l = f'addi {tokens[2]} {tokens[3]} {tokens[4]}'
                lines_list.append(l)
            elif len(tokens) >= 2 and tokens[1] == 'sll':
                #removing the preceding target for the instruction
                l = f'sll {tokens[2]} {tokens[3]} {tokens[4]}'
                lines_list.append(l)
            else:
                #keep the other instructions unchanged
                lines_list.append(' '.join(tokens))

    machine_code = [] #list to store binary strings and hex strings
    for ele in lines_list:
        hex_string = format(int(assembly_machine(ele),2), '#010x')
        machine_code.append(assembly_machine(ele) + "    " + hex_string)
        write_to_file(machine_code, "029_128_machine_code.txt")

                    
create_lines('029_128_full_template_code.asm')

