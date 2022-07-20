class RCFilter:
    
    def __init__(self, cuttOff, sampleTime) -> None:

        RC = 1.0 / (6.28318530717 * cuttOff)

        self.coff = []
        self.prev = []
        self.out = []

        self.coff.append(sampleTime / (RC + sampleTime))
        self.coff.append(RC / (sampleTime + RC))

        self.prev.append(0.0)
        self.prev.append(0.0)
        self.prev.append(0.0)

        self.out.append(0.0)
        self.out.append(0.0)
        self.out.append(0.0)

    def RCFilter_Update(self, inp):

        self.out[0] = (inp[0] * self.coff[0]) + (self.prev[0] * self.coff[1])
        self.out[1] = (inp[1] * self.coff[0]) + (self.prev[1] * self.coff[1])
        self.out[2] = (inp[2] * self.coff[0]) + (self.prev[2] * self.coff[1])    

        self.prev[0] = self.out[0]
        self.prev[1] = self.out[1]
        self.prev[2] = self.out[2]

        return (self.out[0], self.out[1], self.out[2])