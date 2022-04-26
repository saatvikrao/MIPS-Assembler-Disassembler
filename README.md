# Assembler-Disassembler

### Contributors: Saatvik Rao, Sahil Agrawal, Medhansh Singh, Madhav Kanda 

Our project consists of two parts. The first part involves implementing a MIPS assembler that takes assembly code as input and produces the corresponding machine code as output. The second part consists of implementing a MIPS disassembler by producing the MIPS assembly code corresponding to the machine code given as input by the user. This machine code need not be the previously assembled code.
#####
❖ Assembler: We have written a program to translate assembly language code to machine language code. The resulting machine code is in the same format as the input for our disassembler program, i.e., the output is a set of lines, each containing 32 bits of single machine instruction. 

❖ Disassembler: We have written a program that takes in strings representing a machine code and writes out the corresponding assembly language instructions. 


## Guidelines

final_code.py is the final program that the user needs to run. assembly.txt is an example assembly code input. The user can decide to give the desirable input inside the aseembly.txt file. So, for the project, the user needs only two files at the start of the program and as the program progresses a MachineCode.txt file is created which stores the machine code for the given input. Later on, the user is asked if they want to convert back to the assembly. Depending on their answer, machine code is given output. 
