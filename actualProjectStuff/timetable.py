class Timetable:
    def __init__(self, blockA, blockB, blockC, blockD, blockE, blockF, blockG, blockH):
        self.blockA = blockA
        self.blockB = blockB
        self.blockC = blockC
        self.blockD = blockD
        self.blockE = blockE
        self.blockF = blockF
        self.blockG = blockG
        self.blockH = blockH

    def __str__(self):
        return f"Block A: {self.blockA}\nBlock B: {self.blockB}\nBlock C: {self.blockC}\nBlock D: {self.blockD}\nBlock E: {self.blockE}\nBlock F: {self.blockF}\nBlock G: {self.blockG}\nBlock H: {self.blockH}"