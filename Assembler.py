import sys
import os
import string
#ParseASM is used to seperate the comand
class ParseASM(object):
    def __init__(self,line):
        self.lineL=line.strip()

    def dealLine(self):
        if self.lineL:
            ins=self.lineL.split()[0]
            if ins.startswith('@'):
                ains=ins[1:]
                if ains[0] in string.ascii_letters or ains[0]=='_':
                    global sTable
                    global Vnum
                    if ains not in sTable:
                        sTable[ains]=16+Vnum
                        Vnum=Vnum+1
                    else:
                        pass
                    return str(sTable[ains])
                else:
                    return ains
            elif '=' in ins:
                index=ins.index('=')
                des=ins[0:index]
                cmp=ins[index+1:]
                jmp=''
                return (des,cmp,jmp)
            elif ';' in ins:
                des=''
                cmp=ins.split(';')[0]
                jmp=ins.split(';')[1]
                return (des,cmp,jmp)
            else:
                return 0
        else:
            return 0

class coderASM(object):
    def __init__(self, ins):
        self.elements=ins

    def desBin(self,des):
        if des=='':
            return '000'
        elif des=='M':
            return '001'
        elif des=='D':
            return '010'
        elif des=='MD':
            return '011'
        elif des=='A':
            return '100'
        elif des=='AM':
            return '101'
        elif des=='AD':
            return '110'
        elif des=='AMD':
            return '111'

    def cmpBin(self,cmp):
        if 'M' in cmp:
            a='1'
            M_index=cmp.index('M')
            cmp_sub=cmp[0:M_index]+'S'+cmp[M_index+1:]
        elif 'A' in cmp:
            a='0'
            A_index=cmp.index('A')
            cmp_sub=cmp[0:A_index]+'S'+cmp[A_index+1:]
        else:
            #a='0'
            cmp_sub=cmp
 

        if cmp_sub=='0':
            return '0101010'
        elif cmp_sub=='1':
            return '0111111'
        elif cmp_sub=='-1':
            return '0111010'
        elif cmp_sub=='D':
            return '0001100'
        elif cmp_sub=='S':
            return a+'110000'
        elif cmp_sub=='!D':
            return '0001101'
        elif cmp_sub=='!S':
            return a+'110001'
        elif cmp_sub=='-D':
            return '0001111'
        elif cmp_sub=='-S':
            return a+'110011'
        elif cmp_sub=='D+1':
            return '0011111'
        elif cmp_sub=='S+1':
            return a+'110111'
        elif cmp_sub=='D-1':
            return '0001110'
        elif cmp_sub=='S-1':
            return a+'110010'
        elif cmp_sub=='D+S':
            return a+'000010'
        elif cmp_sub=='D-S':
            return a+'010011'
        elif cmp_sub=='S-D':
            return a+'000111'
        elif cmp_sub=='D&S':
            return a+'000000'
        elif cmp_sub=='D|S':
            return a+'010101'

    def jmpBin(self,jmp):
        if jmp=='':
            return '000'
        elif jmp=='JGT':
            return '001'
        elif jmp=='JEQ':
            return '010'
        elif jmp=='JGE':
            return '011'
        elif jmp=='JLT':
            return '100'
        elif jmp=='JNE':
            return '101'
        elif jmp=='JLE':
            return '110'
        elif jmp=='JMP':
            return '111'


    def code(self):
        elements=self.elements
        if elements:
            if type(elements)==type('str'):
                binary=str(bin(int(elements)))
                zero_num=16-(len(binary)-2)
                return zero_num*'0'+ binary[2:]
            else:
                des=self.desBin(elements[0])
                cmp=self.cmpBin(elements[1])
                jmp=self.jmpBin(elements[2])
                cins='111'+cmp+des+jmp
                return cins
        else:
            return 0



if __name__=="__main__":
    path=os.path.dirname(os.path.abspath(__file__))
    filename=sys.argv[1]
    f=open(path+'\\'+filename)
    f_output=open(path+'\\'+filename.split('.')[0]+'.hack','w')
    sTable={'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4, 'SCREEN':16384, 'KBD':24576}
    Vnum=0
    counter=-1
    for i in range(16):
        preSymbol='R'+str(i)
        sTable[preSymbol]=i

    for line in f:
        lineL=line.strip()
        if lineL and (not lineL.startswith('/')) and (not lineL.startswith('(')):
            counter+=1
        if lineL.startswith('('):
            right_index=lineL.index(')')
            label=lineL[1:right_index]
            if label not in sTable:
                sTable[label]=counter+1
            else:
                pass
        else:
            pass

    f.seek(0)

    for line in f:
        parser=ParseASM(line)
        ins=parser.dealLine()
        coder=coderASM(ins)
        output=coder.code()
        if output:
            f_output.write(output+'\n')

