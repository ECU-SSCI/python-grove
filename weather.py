from gc import collect
from microbit import i2c
from math import pow
from utime import ticks_us

BME280_ADDRESS = (0x76)

collect()
i2c.init()

class Weather():
    def __init__(self):
        while (self.read(0xD0) != 0x60):
            print('BME280 not ready...')
            sleep(1000)
        print('Si1145 preparing...')
        self.lastSample = 0
        self.currentRawData = bytearray(8)
        self.adc_T = 0
        self.adc_H = 0
        self.adc_P = 0
        self.vP1 = 0
        self.vP2 = 0
        self.vP3 = 0
        self.vH1 = 0
        self.dig_T1 = self.read(0x88, 16)
        self.dig_T2 = self.read(0x8A, 16, True)
        self.dig_T3 = self.read(0x8C, 16, True)
        self.dig_P1 = self.read(0x8E, 16)
        self.dig_P2 = self.read(0x90, 16, True)
        self.dig_P3 = self.read(0x92, 16, True)
        self.dig_P4 = self.read(0x94, 16, True)
        self.dig_P5 = self.read(0x96, 16, True)
        self.dig_P6 = self.read(0x98, 16, True)
        self.dig_P7 = self.read(0x9A, 16, True)
        self.dig_P8 = self.read(0x9C, 16, True)
        self.dig_P9 = self.read(0x9E, 16, True)
        self.dig_H1 = self.read(0xA1)
        self.dig_H2 = self.read(0xE1, 16, True)
        self.dig_H3 = self.read(0xE3)
        self.dig_H4 = (self.read(0xE4) << 4) | (0x0F & self.read(0xE4 + 1))
        self.dig_H5 = (self.read(0xE5 + 1) << 4) | (0x0F & self.read(0xE5) >> 4)
        self.dig_H6 = self.read(0xE7)
        i2c.write(BME280_ADDRESS, bytearray([0xF2, 0x01]))
        i2c.write(BME280_ADDRESS, bytearray([0xF4, 0x27]))
        self.t_fine = 0
        print('Si1145 ready!')
        collect()
    def read(self, reg, num_bits=8, signed=False, le=False):
        i2c.write(BME280_ADDRESS, bytearray([reg]))
        b = bytearray(int(num_bits/8))
        b = i2c.read(BME280_ADDRESS, int(num_bits/8))
        n = 0
        for x in reversed(b):
            n <<= 8
            n |= x
        if signed:
            mask = 2**(num_bits - 1)
            n = -(n & mask) + (n & ~mask)
        return n
    def getRawData(self):
        if ticks_us() - self.lastSample > 10000:
            while (self.read(0xF3) & 0x08):
                t = ticks_us()
                while t - ticks_us() > 2:
                    pass
            self.lastSample = ticks_us()
            i2c.write(BME280_ADDRESS, bytearray([0xF7]))
            self.currentRawData = i2c.read(BME280_ADDRESS, 8)
    def getTemperature(self):
        self.getRawData()
        self.adc_T = ((self.currentRawData[3] << 16) | (self.currentRawData[4] << 8) | self.currentRawData[5]) >> 4
        self.t_fine = ((((self.adc_T >> 3) - (self.dig_T1 << 1)) * self.dig_T2) >> 11) + ((((((self.adc_T >> 4) - self.dig_T1) * ((self.adc_T >> 4) - self.dig_T1)) >> 12) * self.dig_T3) >> 14)
        return ((self.t_fine * 5 + 128) >> 8)/100
    def getPressure(self):
        self.getRawData()
        self.adc_P = ((self.currentRawData[0] << 16) | (self.currentRawData[1] << 8) | self.currentRawData[2]) >> 4
        if self.t_fine == 0:
            self.getTemperature()
        self.vP1 = self.t_fine - 128000
        self.vP2 = self.vP1 * self.vP1 * self.dig_P6
        self.vP2 = self.vP2 + ((self.vP1*self.dig_P5)<<17)
        self.vP2 = self.vP2 + ((self.dig_P4)<<35)
        self.vP1 = ((self.vP1 * self.vP1 * self.dig_P3)>>8) + ((self.vP1 * self.dig_P2)<<12)
        self.vP1 = ((((1)<<47)+self.vP1))*(self.dig_P1)>>33
        if self.vP1 == 0:
            return 0
        self.vP3 = 1048576-self.adc_P
        self.vP3 = (((self.vP3<<31)-self.vP2)*3125)//self.vP1
        self.vP1 = ((self.dig_P9) * (self.vP3>>13) * (self.vP3>>13)) >> 25
        self.vP2 = ((self.dig_P8) * self.vP3) >> 19
        self.vP3 = ((self.vP3 + self.vP1 + self.vP2) >> 8) + ((self.dig_P7)<<4)
        return (self.vP3 & ((1 << 32) - 1)) / 256
    def getHumidity(self):
        self.getRawData()
        self.adc_H = (self.currentRawData[6] << 8) | self.currentRawData[7]
        if self.t_fine == 0:
            self.getTemperature()
        self.vH1 = self.t_fine - 76800
        self.vH1 = (((((self.adc_H << 14) - (self.dig_H4 << 20) - (self.dig_H5 * self.vH1)) + 16384) >> 15) * (((((((self.vH1 * self.dig_H6) >> 10) * (((self.vH1 * self.dig_H3) >> 11) + 32768)) >> 10) + 2097152) * self.dig_H2 + 8192) >> 14))
        self.vH1 = (self.vH1 - (((((self.vH1 >> 15) * (self.vH1 >> 15)) >> 7) * self.dig_H1) >> 4))
        self.vH1 = 0 if self.vH1 < 0 else self.vH1
        self.vH1 = 419430400 if self.vH1 > 419430400 else self.vH1
        return ((self.vH1>>12) & ((1 << 32) - 1)) / 1024.0
    def calcAltitude(self, pressure):
        return (1.0 - pow((pressure / 101325), 0.190263095808885)) / 0.0000225577