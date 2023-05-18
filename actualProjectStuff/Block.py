class Block:
    def __init__(self, blockID, courses):
        self.blockID = blockID
        self.courses = courses

    def __str__(self):
        return f"{self.blockID}: {self.courses}"