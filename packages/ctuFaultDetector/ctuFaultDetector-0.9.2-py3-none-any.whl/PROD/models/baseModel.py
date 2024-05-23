

class baseModel():
    def __init__(self, learning_threshold, name) -> None:
        self.learn_from_signal = False
        self.magnitude = 0
        self.learning_threshold = learning_threshold
        self.name = name

    def freeze(self):
        self.learn_from_signal = False
        print("INFO: Model is frozen (not learning from new inputs).")
    
    def unfreeze(self):
        self.learn_from_signal = True
        print("INFO: Model is frozen (not learning from new inputs).")
    
    def __repr__(self):
        return f"""
            Classifier: {self.name}
            Learning status: {"learning from new signals" if self.learn_from_signal else "frozen"}
            N_of signals trained: {self.magnitude}
            Learning threshold: {self.learning_threshold}
            """