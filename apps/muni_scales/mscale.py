from django.utils.encoding import force_unicode

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
        return force_unicode("M%s" % self.number or u'M')

    def __eq__(self, other):
        return self.number == other.number

    def __ne__(self, other):
        return not self.__eq__(other)

    def __cmp__(self, other):
        return cmp(self.number, other.number)

    def __hash__(self):
        return hash(unicode(self))
    
        
MSCALES = {}

for level in Mscale.levels:
    m = Mscale(number = level,
               underground = "",
               slope = "",
               obstacles = ["a", "b"],
               characteristics = ["a","b"]
               )
    MSCALES[level] = m
    
MSCALE_CHOICES = tuple((m, "M %s" % str(m).replace(".0","")) for m in Mscale.levels)
