########################################################################
# Malachi Tolman
# @tolman42
# rev.4.April.2016
########################################################################
#
# See class description
#
# I am changing the code to show how git works.
#
########################################################################

class batch_class:
    """
    This represents the bundle of SNM that gets passed from module to module.

    Most of the time (for now), it's simply the batch of U and TRU that gets brought in from 
    the storage buffer.  But it also gets used as the heel in the melter, which is the melted alloy that builds
    up over time.

    #######
    # Variables 
    #######
    weight = amount of SNM in batch (kg)

    description = string to aid in keeping track of what the batch is during logging (ie "batch" vs "heel")
    """

    def __init__(self,weight,description):
        self.weight = weight
        self.description = description

    def add_weight(self,weight_2add):
        """
        Routine that changes the state variable.  Can add a negative weight is weight is lost.
        """
        self.weight = self.weight + weight_2add
