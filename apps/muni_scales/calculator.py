# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
    
    
#s(x) = p
#i1 −i0 (x − i0 ) + p0
#p0 represents the lower boundary of the available points. For the first interval this is
#always 0.
#p1 represents the upper boundary of the available points.
#i0 represents the lower boundary of the criteria measure.
#i1 represents the upper boundary of the criteria measure.
#x represents the criteria input for which the score should be determined.

class UDH(object):
    '''
    Shows scores assigned to each scale criteria for
    better transparency/understandability of the calculated
    result.
    '''
    _interval_borders = (0,2,8,10)
    _max_criteria_points = 10
    _max_total_points = 40
    _formula = "s(x) = p1-p0/ i1 −i0 * (x − i0 ) + p0"
    # Total Length (0-10 points) The total length of the trail in km
    # 0/2/8/10 points given to 0/1/4/8 km
    _total_length = (0,1,4,8)
    #Average Slope (0-10 points) The total height difference divided by total length of the
    #trail: 0/2/8/10 points given to 0/10/25/35 %
    _avg_slope = (0,10,25,35)
    #Maximum Difficulty (0-10 points) The rating of the most difficult section of the trail
    #using the M scale: 0/2/8/10 points given to M 0/2/3.5/5
    _max_difficulty = (0,2,3.5,5)
    #Average Difficulty (0-10 points) The average difficulty rating of the trail using the M
    #scale, 0/2/8/10 points given to M 0/1/2.5/3.5
    _avg_difficulty = (0,1,2.5,3.5)

    def __init__(self, obj):
        '''
        :param obj: an instance of the UDHScale model
        '''
        self.obj = obj
        self.__total_length = obj.total_length
        self.__avg_slope = obj.average_slope
        self.__max_difficulty = obj.maximum_difficulty
        self.__avg_difficulty = obj.average_difficulty

    @staticmethod
    def get_boundaries(value, lst):
        '''
        determines the position of the value in the provided
        list and returns the matching borders of the points list.
        p0 represents the lower boundary of the available points. 
        p1 represents the upper boundary of the available points.
        i0 represents the lower boundary of the criteria measure.
        i1 represents the upper boundary of the criteria measure.
        
        :returns: a tuple with 4 elements: (p0, p1, i0, i1)
        '''
        for idx, val in enumerate(lst):
            if value > val and value < lst[idx+1]:
                return UDH._interval_borders[idx:idx+2] + lst[idx:idx+2]
    
    @staticmethod 
    def get_criteria_score(value, lst):
        '''
        :returns: a tuple with an explanation and the actual score. The explanation
                  describes how the score was calculated.
        :rtype: tuple(str,int)
        '''
        # return min when value lower than first listvalue
        if(value <= lst[0]):
            explanation = _("The value (%s) is smaller than the first interval point %s" % (value, lst[0]))
            return explanation, UDH._interval_borders[0]
        # return max when value higher than last listvalue
        if(value >= lst[-1]):
            explanation = _("The value (%s) exceeds the last interval point %s" % (value, lst[-1]))
            return explanation, UDH._interval_borders[-1]
        if(value in lst):
            index = lst.index(value)
            explanation = _("The value (%s) matches an interval point" % value)
            return explanation, UDH._interval_borders[index]
        #otherwise calculate, using the interval borders
        p0, p1, i0, i1 = UDH.get_boundaries(value, lst)
        result = float(p1 - p0) / (i1 - i0) * (value - i0) + p0
        result = round(result,2)
        explanation = _("The score was determined by linear interpolation. The value is in "
                        + "between %s and %s, so that the score has to be in between %s and %s" % (i0, i1, p0, p1))
        return explanation, result

    def get_total_length(self):
        calc = {'value': self.__total_length}
        length_km = float(self.__total_length)/1000
        calc['explanation'], calc['result'] = UDH.get_criteria_score(length_km, UDH._total_length)
        return calc

    def get_avg_slope(self):
        calc = {'value': self.__avg_slope}
        calc['explanation'], calc['result'] = UDH.get_criteria_score(self.__avg_slope, UDH._avg_slope)
        return calc


    def get_max_difficulty(self):
        calc = {'value': self.__max_difficulty}
        calc['explanation'], calc['result'] = UDH.get_criteria_score(self.__max_difficulty.number, UDH._max_difficulty)
        return calc


    def get_avg_difficulty(self):
        calc = {'value': self.__avg_difficulty}
        calc['explanation'], calc['result'] = UDH.get_criteria_score(self.__avg_difficulty.number, UDH._avg_difficulty)
        return calc
    
    def get_total_score(self):
        score = self.total_length['result'] + self.avg_slope['result'] + self.max_difficulty['result'] + self.avg_difficulty['result']
        return int(round(score))

    total_length = property(fget=get_total_length, doc="")
    avg_slope = property(fget=get_avg_slope, doc="")
    max_difficulty = property(fget=get_max_difficulty, doc="max_difficulty's docstring")
    avg_difficulty = property(fget=get_avg_difficulty, doc="avg_difficulty's docstring")
    total_score = property(fget=get_total_score, doc="the total score of the trail")
        
