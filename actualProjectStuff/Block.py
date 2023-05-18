class Block:
    def __init__(self, blockID, courses):
        self.blockID = blockID
        self.courses = courses

    def __str__(self):
        blockString = f"{self.blockID}: "
        for i in self.courses:
            blockString += f"\n{i} "
        return blockString