# Pipelined-and-Non-Pipelined-Processor

Processor without pipelining:
● Program 1 is the sorting program. Program 2 is the factorial
program.
● We created a mapping of op_code and the instruction, register
file for both the programs, function code mapping for the r type
instruction, instruction memory for both the programs and the
data memory.
● Set the PC to the starting PC in the instruction memory for both
the program.
● clk 1 is the clock cycle for the fetch stage, similarly clk2 for
decode, clk 3 for execute, clk4 for the memory, clk5 for the
writeback.
● two _complement function is written to convert the negative
binary offset of the beq and bne to integer.
● Sign extend function perform sign extend of the 16 bit to 32 bit.
● Control signal function: takes in the instruction as the parameter
and returns the control signal of the given instruction by
checking the op code of the instruction.
● Fetch function: reads the instruction from the instruction
memory with the help of the pc parameter. Pc is incremented.
Decode function is called.
● Decode function: decoding the instruction based on the
op_code. Reading content from the rs register in read_data1. If
the instruction is sll then rs is zero register. Rt register is read
from the register file. Shamt field is converted into integer.
Execute function is called with parameters rt, shamt, offset,
write_reg, addr,ctrl_sig. If the reg_dst is 0 (lw and sw) write
destination is rt. reg_dst is 1 (r type ) write destination is rd. If
the alu_src is `1 then the instruction is lw or sw. Reading
content from the rt register in read_data2. Calculating the
address for the jump instruction. Execute function is called with
parameters read_data1, read_data2, offset, write_reg, addr,
ctrl_sig.
● Execute function: based on the ALU_ctrl we are performing the
add, sub, or, slt, sll. For lw and sw we are performing add to
calculate the memory address. For bne and beq we are
performing the sub operation and if condition is satisfied we are
updating the global pc. Memory function is called with the
parameters alu_res, write_data, write_reg, ctrl_sig.
● Memory function: memread is 1 for lw. Reading data from
memory. Writedata is 1 for sw. Writing to the memory. Calling
the write_back function with parameter read_data, alu_res,
write_reg, ctrl_sig.
● Write_back function: memtoreg is 0 for r type. Writing alu_res to
the write register. Memtoreg is 1 for lw. Writing data form the
memory to the write register.
2. Processor with Pipeline:
● Program 1 is the sorting program. Program 2 is the factorial
program.
● We created a mapping of op_code and the instruction, register
file for both the programs, function code mapping for the r type
instruction, instruction memory for both the programs and the
data memory.
● Set the PC to the starting PC in the instruction memory for both
the program.
● clk 1 is the clock cycle for the fetch stage, similarly clk2 for
decode, clk 3 for execute, clk4 for the memory, clk5 for the
writeback.
● We are creating pipelined register lists IF_ID, ID_EX, EX_MEM,
MEM_WB to replicate the actual pipelined register of a mips
pipelined processor.
● Control signal function: takes in the instruction as the parameter
and returns the control signal of the given instruction by
checking the op code of the instruction.
● To implement the pipelined flow of the execution of the stages
we are maintaining queues IF, ID, Ex, MEM, WB.
● Initially the IF queue is loaded with all the instructions.
● Fetch function : Each instruction is fetched from the IF queue
and the IF_ID pipelined register is updated with the PC and the
control signals. It is then passed to the ID stage. \
● Decode function: Taking the pc value front the IF_ID pipelined
register the decode operation is performed similar to the non
pipelined program.
● Forwarding_unit function: This function represents the
forwarding unit of a mips pipelined processor and generates
forwarding signals checking the various dependencies like EX
hazard, MEM hazard, lw followed by sw, lw / addi followed by r
type. This function is called in the decode stage.
● Control hazard: This function is used to flush the pipeline and
update it with new instructions in case of branch taken.
● Hazard detection unit: for lw followed by r type it identifies if
there is a need to stall. We are passing a string nop in the IF
queue, if it is encountered we are not doing anything.
● Execute : It is similar to one non-pipelined register except here
we are taking the values either from the pipelined registers or
the forwarded values in case of dependencies. For jump
instruction we are clearing the IF queue and pushing the
instructions starting from the target address.
● Mem and Write back: similar to the non-pipelined processor.
Here in Mem we are handling the lw followed by sw
dependencies.
● After each stage the pipelined register values are updated and
passed to the next stage.
