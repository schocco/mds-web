class Mscale(object):
    '''
    M scale, describing the difficultiy of a single muni trail section.
    '''
    levels = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)

    def __init__(self, *args, **kwargs):
        '''
        initial values can be provided via kwargs.
        
        :param number: difficulty level, e.g. 2 for M2
        :type number: int
        :param underground: description of the trail underground
        :type underground: str.
        :param slope: slope
        :param obstacles: list of obstacles
        :type obstacles: list
        :param characteristics: list of other characteristics 
                                that describe the trail section
        :type characteristics: list
        '''
        self.number = kwargs.pop("number", 0)
        self.underground = kwargs.pop("underground", "")
        self.slope = kwargs.pop("slope", "")
        self.obstacles = kwargs.pop("obstacles", [])
        self.characteristics = kwargs.pop("characteristics", [])
    def __unicode__(self):
        return "M%s" % self.number
    
        
MSCALES = {}

for level in Mscale.levels:
    m = Mscale(number = level,
               underground = "",
               slope = "",
               obstacles = ["a", "b"],
               characteristics = ["a","b"]
               )
    MSCALES[level] = m
    
