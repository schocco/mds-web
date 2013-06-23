# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
    
class CalcBase(object):
    _interval_borders = (0,2,8,10)
    @staticmethod
    def get_boundaries(value, lst, max_pts=10):
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
                ps = tuple(float(p) * max_pts / 10 for p in CalcBase._interval_borders[idx:idx+2])
                return ps + lst[idx:idx+2]
    
    @staticmethod 
    def get_criteria_score(value, lst, max_pts=10):
        '''
        :returns: a tuple with an explanation and the actual score. The explanation
                  describes how the score was calculated.
        :rtype: tuple(str,int)
        '''
        # return min when value lower than first listvalue
        if(value <= lst[0]):
            explanation = _("The value (%s) is smaller than the first interval point %s" % (value, lst[0]))
            return explanation, CalcBase._interval_borders[0] * float(max_pts) / 10
        # return max when value higher than last listvalue
        if(value >= lst[-1]):
            explanation = _("The value (%s) exceeds the last interval point %s" % (value, lst[-1]))
            return explanation, CalcBase._interval_borders[-1] * float(max_pts) / 10
        if(value in lst):
            index = lst.index(value)
            explanation = _("The value (%s) matches an interval point" % value)
            return explanation, CalcBase._interval_borders[index] * float(max_pts) / 10
        #otherwise calculate, using the interval borders
        p0, p1, i0, i1 = UXC.get_boundaries(value, lst, max_pts)
        result = float(p1 - p0) / (i1 - i0) * (value - i0) + p0
        result = round(result,1)
        explanation = _("The score was determined by linear interpolation. The value is in "
                        + "between %s and %s, so that the score has to be in between %s and %s" % (i0, i1, p0, p1))
        return explanation, result
    
class UDH(CalcBase):
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
    
class UXC(CalcBase):
    '''
    Shows scores assigned to each UXC scale criteria for
    better transparency/understandability of the calculated
    result.
    '''
    _interval_borders = (0,2,8,10)
    _max_total_points = 40
    
    _total_length = (0,10,25,40)
    _total_length_max_pts = 15
    _total_ascent = (0,200,800,1500) #interval borders in meters
    _total_ascent_max_pts = 7.5
    _max_slope = (0,10,25,30)
    _max_slope_max_pts = 5
    _max_difficulty = (0,1,2.5,4)
    _max_difficulty_max_pts = 5
    _avg_difficulty = (0,0.5,1,2)
    _avg_difficulty_max_pts = 7.5

    def __init__(self, obj):
        '''
        :param obj: an instance of the UDHScale model
        '''
        self.obj = obj
        self.__total_length = obj.total_length
        self.__total_ascent = obj.total_ascent
        self.__max_slope = obj.maximum_slope_uh
        self.__max_difficulty = obj.maximum_difficulty
        self.__avg_difficulty = obj.average_difficulty
        
    
    def get_total_length(self):
        length = float(self.__total_length) / 1000 #km instead of meters
        max_pts = UXC._total_length_max_pts
        calc = {'value': self.__total_length}
        calc['explanation'], calc['result'] = UXC.get_criteria_score(length, UXC._total_length, max_pts)
        return calc

    def get_total_ascent(self):
        ascent = float(self.__total_ascent)
        max_pts = UXC._total_ascent_max_pts
        calc = {'value': self.__total_ascent}
        calc['explanation'], calc['result'] = UXC.get_criteria_score(ascent, UXC._total_ascent, max_pts)
        return calc

    def get_max_slope(self):
        slope = self.__max_slope
        max_pts = UXC._max_slope_max_pts
        calc = {'value': self.__max_slope}
        calc['explanation'], calc['result'] = UXC.get_criteria_score(slope, UXC._max_slope, max_pts)
        return calc


    def get_max_difficulty(self):
        diff = self.__max_difficulty.number
        max_pts = UXC._max_difficulty_max_pts
        calc = {'value': self.__max_difficulty}
        calc['explanation'], calc['result'] = UXC.get_criteria_score(diff, UXC._max_difficulty, max_pts)
        return calc


    def get_avg_difficulty(self):
        diff = self.__avg_difficulty.number
        max_pts = UXC._avg_difficulty_max_pts
        calc = {'value': self.__avg_difficulty}
        calc['explanation'], calc['result'] = UXC.get_criteria_score(diff, UXC._avg_difficulty, max_pts)
        return calc
    
    def get_total_score(self):
        score = self.total_length['result'] + self.total_ascent['result']
        score += self.max_slope['result'] + self.max_difficulty['result']
        score += self.avg_difficulty['result']
        return int(round(score))
    
    total_length = property(get_total_length, None, None, None)
    total_ascent = property(get_total_ascent, None, None, None)
    max_slope = property(get_max_slope, None, None, None)
    max_difficulty = property(get_max_difficulty, None, None, None)
    avg_difficulty = property(get_avg_difficulty, None, None, None)
    total_score = property(get_total_score, None, None, None)
