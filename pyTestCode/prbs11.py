#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Do prbs11 calculation

Command input  format:
    output unit n, datain ,format(0:8bit 1:12bit)
"""
import sys
import colorama
from colorama import init,Fore,Back,Style
init(autoreset=True)
class bitCalculate(): 
    def __init__(self): 
        pass
        
    def getBitVal(self,datain, index): 
        """
        brief:git bit value 
        
        :param datain: input data
        :param index: bit value
        :returns: bit value 0 or 1
        """
        if datain & (1 << index):
            return 1
        else:
            return 0
        
    def getBitsVal(self,datain,bitEnd,bitStr):
        dataout = 0
        for n in range(bitStr,bitEnd+1):
            dataout += datain & (1 << n)
        dataout >>= bitStr
        return dataout 

    def setBitVal(self,datain, index, val):
        """
        brief: change bit value
        
        :param datain: original data
        :param index:  bit position ,index 0 from right
        :param val:    set bit value
        :returns: new data after bit change
        """
        if val:
            datain = datain | (1 << index)
            return datain 
        else:
            datain & ~(1 << index)
            return datain
        
    def setBitsVal(self,datain,bitEnd,bitStr,val):
        pass
        
    def prbs11(self,datain):
        data = (self.getBitsVal(datain,9,0)<<1) + (self.getBitVal(datain,8)^self.getBitVal(datain,10))
        return data
        
    def prbs11WithFormat(self,datain,format = 0): 
        """
        brief: calculate prbs11 and get port0 value and port 1 value and prbs11_12 for next calculation
        
        :param datain: datain to do the first calculation
        :param foramt: 0: output get lower 8 bit data; 1:output get 12bit data
        :returns: port0=>loop to get 12 prbs data, git each prbs data's bit 0
                  port0=>loop to get 12 prbs data, git each prbs data's bit 1
        """
        prbs11_01 = self.prbs11(datain)
        prbs11_02 = self.prbs11(prbs11_01)
        prbs11_03 = self.prbs11(prbs11_02)
        prbs11_04 = self.prbs11(prbs11_03)
        prbs11_05 = self.prbs11(prbs11_04)
        prbs11_06 = self.prbs11(prbs11_05)
        prbs11_07 = self.prbs11(prbs11_06)
        prbs11_08 = self.prbs11(prbs11_07)
        prbs11_09 = self.prbs11(prbs11_08)
        prbs11_10 = self.prbs11(prbs11_09)
        prbs11_11 = self.prbs11(prbs11_10)
        prbs11_12 = self.prbs11(prbs11_11)
        port0 =  (self.getBitVal(prbs11_11,0)<<11) +\
            (self.getBitVal(prbs11_10,0)<<10) + \
            (self.getBitVal(prbs11_09,0)<<9 )+ \
            (self.getBitVal(prbs11_08,0)<<8 )+ \
            (self.getBitVal(prbs11_07,0)<<7 )+ \
            (self.getBitVal(prbs11_06,0)<<6 )+ \
            (self.getBitVal(prbs11_05,0)<<5 )+ \
            (self.getBitVal(prbs11_04,0)<<4 )+ \
            (self.getBitVal(prbs11_03,0)<<3 )+ \
            (self.getBitVal(prbs11_02,0)<<2 )+ \
            (self.getBitVal(prbs11_01,0)<<1 )+ \
            (self.getBitVal(datain,0))  
        port1 =  (self.getBitVal(prbs11_11,1)<<11) +\
            (self.getBitVal(prbs11_10,1)<<10) + \
            (self.getBitVal(prbs11_09,1)<<9 )+ \
            (self.getBitVal(prbs11_08,1)<<8 )+ \
            (self.getBitVal(prbs11_07,1)<<7 )+ \
            (self.getBitVal(prbs11_06,1)<<6 )+ \
            (self.getBitVal(prbs11_05,1)<<5 )+ \
            (self.getBitVal(prbs11_04,1)<<4 )+ \
            (self.getBitVal(prbs11_03,1)<<3 )+ \
            (self.getBitVal(prbs11_02,1)<<2 )+ \
            (self.getBitVal(prbs11_01,1)<<1 )+ \
            (self.getBitVal(datain,1))
        if format:
            print("port0 prbs11: {:#04x}".format(port0& 0x0fff))
            print("port1 prbs11: {:#04x}\n".format(port1& 0x0fff))
        else:
            print("port0 prbs11: {:#04x}".format(port0& 0x00ff))
            print("port1 prbs11: {:#04x}\n".format(port1& 0x00ff))
        dataNextIn = prbs11_12
        return port0,port1,dataNextIn  
    
    def prbs11FinalOut(self,outCnt,datain,format=0):
        """
        brief: get outCnt output datas (include port0 and port1)
        
        :param outCnt: how many datas want to output
        :param datain: the first data to do prbs11 calculation
        :returns none
        """        
        if(format):
            print(Back.GREEN + Fore.YELLOW + f"12bit data format of prbs11 data total {outCnt}")
        else:
            print(Back.GREEN + Fore.YELLOW + f"8bit data format of prbs11 data total {outCnt}")
        for i in range(0,outCnt):
            print(f"{i}:")
            _,_,datain = self.prbs11WithFormat(datain,format)
        return None

if __name__ == '__main__':
    a = bitCalculate()
    a.prbs11FinalOut(10,0x7ff)
    a.prbs11FinalOut(10,0x7ff,1)