Muni Difficulty Scale - Web Project
###################################


This is the Django based web project for the Muni Difficulty Scale as defined by
the muni committee members of the International Unicycling Federation
(`IUF <http://iufinc.org>`_).

The Muni Difficulty Scale is a difficulty measuring approach for mountain
unicycling tracks. The difficulty description consists of a technical component
(M-Scale) and a discipline specific component (UDH for downhill or UXC for
cross country).


Planned features
****************

- Informing about the difficulty scale
- Internationalization
- Online calculator to determine scores
- GPX track import as alternative data entry method for the calculator
- Storing trails and their associated difficulty ratings, so that they can be
  referenced by event hosts to inform their participants
- Public RESTful API for read access


Requirements
************

- Python packages as listed in requirements.txt (created via PIP)
- PostGIS instance
- GDAL


References
************

publication, describing the difficulty scale:
  https://github.com/iuf/muni-difficulty-scale






