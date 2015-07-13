# -*- coding: utf-8 -*-
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _


class Mscale(object):
    """
    M scale, describing the difficultiy of a single muni trail section.
    """
    levels = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)

    def __init__(self, *args, **kwargs):
        """
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
        """
        self.number = float(kwargs.pop(u"number", 0))
        self.underground = kwargs.pop(u"underground", "")
        self.slope = kwargs.pop(u"slope", "")
        self.obstacles = kwargs.pop(u"obstacles", [])
        self.characteristics = kwargs.pop(u"characteristics", [])

    def __unicode__(self):
        return force_unicode(u"M%s" % self.number or u'M')

    def __str__(self):
        return str(self.__unicode__())

    def __eq__(self, other):
        if isinstance(other, Mscale):
            return self.number == other.number
        elif isinstance(other, (int, float)):
            return self.number == other
        else:
            return False
            # raise TypeError(u"Cannot compare Mscale object with %s" % str(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __cmp__(self, other):
        """
        Also allows comparisons between mscale instances and numbers.
        """
        if (isinstance(other, Mscale)):
            return cmp(self.number, other.number)
        elif (isinstance(other, int) or isinstance(other, float)):
            return cmp(self.number, other)
        else:
            raise TypeError(_(u"Cannot compare Mscale object with {0}").format(other))

    def __hash__(self):
        return hash(unicode(self))


MSCALES = {}

MSCALES[0] = Mscale(number=0.0,
                    underground=_(u"pavement or solid soil/compact gravel"),
                    slope="< 20 %",
                    obstacles=[_(u"no obstacles")],
                    characteristics=[_(u"90° turns within > 2 m and with slope < 10 %")]
                    )
MSCALES[0.5] = Mscale(number=0.5)

MSCALES[1] = Mscale(number=1.0,
                    underground=_(u"partly loose soil/gravel"),
                    slope="< 40 %",
                    obstacles=[_(u"small obstacles, approx. 5cm high (small stones, flat roots)"),
                               _(u"single 15 cm steps")],
                    characteristics=[_(u"90° turn within > 1 m and with slope < 20 %")]
                    )

MSCALES[1.5] = Mscale(number=1.5)

MSCALES[2] = Mscale(number=2.0,
                    underground=_(u"loose soil/gravel"),
                    slope="< 60 %",
                    obstacles=[_(u"obstacles, approx. 10 cm high (stones, roots"),
                               _(u"single 30 cm steps")
                               ],
                    characteristics=[_(u"90° turn within > 0.5 m and with slope < 30 %")]
                    )

MSCALES[2.5] = Mscale(number=2.5)

MSCALES[3] = Mscale(number=3.0,
                    underground=_(u"loose soil with loose stones (size of few cm)"),
                    slope="< 80 %",
                    obstacles=[_(u"obstacles that are approx 20cm high (stones, roots)"),
                               _(u"several irregular steps, approx. 20 cm each"),
                               _(u"drops < 1 m"),
                               _(u"gaps < 0.5 m")],
                    characteristics=[_(u"135° turn within ~ 0.5 m and with slope < 40 %")]
                    )

MSCALES[3.5] = Mscale(number=3.5)

MSCALES[4] = Mscale(number=4.0,
                    underground=_(u"very loose/slippery soil with loose stones (size of several cm)"),
                    slope="< 100 %",
                    obstacles=[_(u"big obstacles (stones, logs ~ 30 cm)"),
                               _(u"several irregular steps ~ 30 cm each"),
                               _(u"drops < 1.5 m"),
                               _(u"gaps < 1 m")],
                    characteristics=[_(u"135° turn within ~ 0.5 m and with slope < 60 %")]
                    )

MSCALES[4.5] = Mscale(number=4.5)

MSCALES[5] = Mscale(number=5.0,
                    underground=_(u"very loose/slippery soil with loose stones (size of several cm)"),
                    slope="> 100 %",
                    obstacles=[_(u"very big obstacles (stones, logs ~ 40 cm)"),
                               _(u"several irregular steps ~ 40 cm each"),
                               _(u"drops > 1.5 m, gaps > 1 m")],
                    characteristics=[_(u"135° turn within ~ 0.5 m and with slope < 80 %")]
                    )

MSCALE_CHOICES = tuple((m, "M %s" % str(m).replace(".0", "")) for m in Mscale.levels)
