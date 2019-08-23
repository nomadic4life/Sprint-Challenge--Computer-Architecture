"""CPU functionality."""

import sys
from datetime import datetime


class CPU:
    """Main CPU class."""
    instructions = {
        0b00000000: 'NOP',
        0b00000001: 'HLT',
        0b00010001: 'RET',
        0b00010011: 'IRET',
        0b01000101: 'PUSH',
        0b01000110: 'POP',
        0b01000111: 'PRN',
        0b01001000: 'PRA',
        0b01010000: 'CALL',
        0b01010010: 'INT',
        0b01010100: 'JMP',
        0b01010101: 'JEQ',
        0b01010110: 'JNE',
        0b01010111: 'JGT',
        0b01011000: 'JLT',
        0b01011001: 'JLE',
        0b01011010: 'JGE',
        0b01100101: 'INC',
        0b01100110: 'DEC',
        0b01101001: 'NOT',
        0b10000010: 'LDI',
        0b10000011: 'LD',
        0b10000100: 'ST',
        0b10100000: 'ADD',
        0b10100001: 'SUB',
        0b10100010: 'MUL',
        0b10100011: 'DIV',
        0b10100100: 'MOD',
        0b10100111: 'CMP',
        0b10101000: 'AND',
        0b10101010: 'OR',
        0b10101011: 'XOR',
        0b10101100: 'SHL',
        0b10101101: 'SHR'
    }

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0b00000000] * 256
        self.reg = [0b00000000] * 8
        self.pc = 0
        self.ir = 0
        self.fl = 0
        self.mar = 0
        self.mdr = 0
        self.isr = 0
        self.imr = 0
        self.sp = 0x07
        self.reg[self.sp] = 0xf4

        self.halted = False
        self.dintr = False
        self.ts = datetime.now().timestamp()

        self.dispatch = {
            'NOP': self.exec_nop,
            'HLT': self.exec_hlt,
            'RET': self.exec_ret,
            'IRET': self.exec_iret,
            'PUSH': self.exec_push,
            'POP': self.exec_pop,
            'PRN': self.exec_prn,
            'PRA': self.exec_pra,
            'CALL': self.exec_call,
            # 'INT': self.exec_int,
            'JMP': self.exec_jmp,
            'JEQ': self.exec_jeq,
            'JNE': self.exec_jne,
            # 'JGT': self.exec_jgt,
            # 'JLT': self.exec_jlt,
            # 'JLE': self.exec_jle,
            # 'JGE': self.exec_jge,
            # 'INC': self.exec_inc,
            # 'DEC': self.exec_dec,
            # 'NOT': self.exec_not,
            'LDI': self.exec_ldi,
            # 'LD': self.exec_ld,
            'ST': self.exec_st,
            'ADD': self.exec_add,
            # 'SUB': self.exec_sub,
            'MUL': self.exec_mul,
            # 'DIV': self.exec_div,
            # 'MOD': self.exec_mod,
            'CMP': self.exec_cmp,
            # 'AND': self.exec_and,
            # 'OR': self.exec_or,
            # 'XOR': self.exec_xor,
            # 'SHL': self.exec_shl,
            # 'SHR': self.exec_shr
        }

    def exec_nop(self, operand=None):
        pass

    def exec_hlt(self, operand=None):
        self.halted = True

    def exec_ldi(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.reg[a] = b

    def exec_prn(self, operand):
        a = operand["operand_a"]
        print(self.reg[a])

    def exec_mul(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.alu('MUL', a, b)

    def exec_push(self, operand):
        a = operand["operand_a"]
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[a], self.reg[self.sp])

    def exec_pop(self, operand=None):
        print(operand)
        a = operand["operand_a"]
        self.reg[a] = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    def exec_ret(self, operand=None):
        address = {"operand_a": 0x04}
        self.exec_pop(address)
        self.pc = self.reg[0x04] + 1

    def exec_call(self, operand):
        a = operand["operand_a"]
        address = {"operand_a": 0x04}
        self.reg[0x04] = self.pc + 1
        self.exec_push(address)
        self.pc = self.reg[a]

    def exec_jmp(self, operand):
        a = operand["operand_a"]
        self.pc = self.reg[a]

    def exec_add(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.alu('ADD', a, b)

    def exec_sub(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.alu('SUB', a, b)

    def exec_div(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        if b != 0:
            self.alu('MOD', a, b)
        else:
            print('cannot divide by 0')
            self.halted = True

    def exec_mod(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        if b != 0:
            self.alu('MOD', a, b)
        else:
            print('cannot divide by 0')
            self.halted = True

    def exec_st(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.ram_write(self.reg[b], self.reg[a])

    def exec_and(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.alu('AND', a, b)

    def exec_or(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.alu('OR', a, b)

    def exec_xor(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.alu('XOR', a, b)

    def exec_not(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.alu('NOT', a, b)

    def exec_shl(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.alu('SHL', a, b)

    def exec_shr(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.alu('SHR', a, b)

    def exec_addi(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.alu('ADDI', a, b)

    def exec_iret(self, operand=None):
        address = {"operand_a": 0x06}
        self.exec_pop(address)
        address = {"operand_a": 0x05}
        self.exec_pop(address)
        address = {"operand_a": 0x04}
        self.exec_pop(address)
        address = {"operand_a": 0x03}
        self.exec_pop(address)
        address = {"operand_a": 0x02}
        self.exec_pop(address)
        address = {"operand_a": 0x01}
        self.exec_pop(address)
        address = {"operand_a": 0x00}
        self.exec_pop(address)
        self.fl = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        self.dintr = False

    def exec_pra(self, operand):
        print(operand)
        a = operand["operand_a"]
        print(chr(self.ram_read(self.reg[a])))

    def exec_cmp(self, operand):
        a = operand["operand_a"]
        b = operand["operand_b"]
        self.alu('CMP', a, b)

    def exec_jeq(self, operand):
        a = operand["operand_a"]
        self.pc = self.reg[a] if self.fl == 1 else self.pc+2

    def exec_jne(self, operand):
        a = operand["operand_a"]
        self.pc = self.reg[a] if self.fl != 1 else self.pc+2

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) != 2:
            print("Error: wrong number of arguments")
            sys.exit()

        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                tmp = line.split('#', 1)[0].strip()
                if tmp:
                    self.ram_write(int(tmp, 2), address)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'ADDI':
            self.reg[reg_a] += reg_b
        elif op == 'SUB':
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'DIV':
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == 'MOD':
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == 'NOT':
            self.reg[reg_a] = not self.reg[reg_b]
        elif op == 'AND':
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == 'OR':
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == 'XOR':
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == 'DEC':
            self.reg[reg_a] -= 1
        elif op == 'INC':
            self.reg[reg_a] += 1
        elif op == 'SHL':
            self.reg[reg_a] <<= self.reg[reg_b]
        elif op == 'SHR':
            self.reg[reg_a] >>= self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 2
            else:
                self.fl = 4
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            if datetime.now().timestamp() - self.ts >= 1:
                self.ts = datetime.now().timestamp()
                self.reg[self.isr] += 0b00000001

            self.ir = self.pc
            num_operands = (self.ram_read(self.ir) >> 6) & 0b11
            set_pc = (self.ram_read(self.ir) >> 4) & 0b0001

            if self.ram_read(self.ir) in self.instructions:

                intstruction = self.ram_read(self.ir)
                operands = {
                    "operand_a": None,
                    "operand_b": None
                }

                if num_operands > 0:

                    value = self.ram_read(self.ir + 1)
                    operands["operand_a"] = value

                if num_operands > 1:

                    value = self.ram_read(self.ir + 2)
                    operands["operand_b"] = value

                self.dispatch[self.instructions[intstruction]](operands)

            else:
                print('Error: incorrect opcode. Exiting LS8')
                sys.exit()

            if set_pc == 0:
                self.pc += num_operands + 1

    def ram_read(self, address):
        self.mar = address
        return self.ram[address]

    def ram_write(self, value, address):
        self.mar = address
        self.mdr = value
        self.ram[address] = value
