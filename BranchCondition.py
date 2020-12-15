class BranchCondition(object):
    def __init__(self, bc):
        self.condition = bc
        self.true_address = None
        self.false_address = None
    def __str__(self):
    	return self.condition + "," + str(self.true_address) + "," + str(self.false_address)



