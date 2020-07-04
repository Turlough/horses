class Minimiser:
    index = 0
    record = {}

    def submit(self, weight, obj):
        '''
        Weight is the the value to be minimised,
        obj is the object to which the weight is assigned
        '''
        self.record[self.index] = [weight, obj]
        self.index += 1

    def smallest(self):
        key_min = min(self.record.keys(), key=(lambda k: self.record[k][0]))
        return self.record[key_min][1]

    def reset(self):
        self.index = 0
        self.record = {}