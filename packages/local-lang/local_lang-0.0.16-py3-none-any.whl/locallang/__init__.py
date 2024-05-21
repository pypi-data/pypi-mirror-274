#  Copyright (c) 2024 pieteraerens.eu
#  All rights reserved.
#  The file __init__.py is a part of localisation.
#  Created by harrypieteraerens
#  Created: 4/28/24, 2:14 AM
#  Last modified: 4/28/24, 2:14 AM

from locallang.lang_init import LangInit

try:
    from local.localisation import Localisation
except ImportError:
    pass

__version__ = "0.0.16"
__all__ = ["LangInit", "Localisation", "getLocalisation"]


def getLocalisation(local: str):
    """
    Get the localization object

    :param local:
    :return:
    """
    try:
        from local.localisation import Localisation
        return Localisation(local.replace("-", "_"))
    except ImportError:
        return None
