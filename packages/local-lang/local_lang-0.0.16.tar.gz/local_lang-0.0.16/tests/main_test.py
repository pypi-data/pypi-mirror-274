#  Copyright (c) 2024 pieteraerens.eu
#  All rights reserved.
#  The file main_test.py is a part of localisation.
#  Created by harrypieteraerens
#  Created: 4/28/24, 1:33 AM
#  Last modified: 4/28/24, 1:33 AM

# from locallang import LangInit
#
#
# localisation = LangInit()
#
# local = localisation.get_localisation("en_us")
#
# print(local.hello)
#
# local = localisation.get_localisation("fr_be")
#
# print(local.hello)


from locallang import LangInit

lang_init = LangInit()

lang_init.reload_localization()
