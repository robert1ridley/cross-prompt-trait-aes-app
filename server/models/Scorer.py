import random

class Scorer():
    def __init__(self):
        pass

    def get_scores(self):
        labels = ["Overall", "Content", "Organization", "Word Choice", "Sentence Fluency", "Conventions"]
        scores = [random.randint(1, 101) for label in labels]
        return {
            'labels': labels,
            'scores': scores
        }