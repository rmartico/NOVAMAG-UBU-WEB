#     Copyright (C) 2017-2018 UBU-ICCRAM-ADMIRABLE-NOVAMAG-GA686056
#     http://crono.ubu.es/novamag
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This Program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with UBU-ICCRAM-ADMIRABLE-NOVAMAG-GA686056  see the file COPYING.  If not, see
# <http://www.gnu.org/licenses/>.

import os

# Configuration parameters in SQLAlchemy

# Change to allow the upload to Heroku with its database
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql:///novamag' # WARNING differnet names between machines #TODO
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_TRACK_MODIFICATIONS = False

# For CSRF with WTF
SECRET_KEY = 'sdflsfjlsfsdfiowfjsad37847239847239jflsjfaf28308302'