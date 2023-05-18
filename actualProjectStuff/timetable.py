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
        return f"Block A: {self.blockA}\
            \nBlock {self.blockB}\
            \nBlock {self.blockC}\
            \nBlock {self.blockD}\
            \nBlock {self.blockE}\
            \nBlock {self.blockF}\
            \nBlock {self.blockG}\
            \nBlock {self.blockH}"