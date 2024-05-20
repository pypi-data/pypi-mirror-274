'''
| Author:   Ezio416
| Created:  2024-05-19
| Modified: 2024-05-19

- Tests for nadeo_api.core
'''

import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import src.nadeo_api.auth as auth
import src.nadeo_api.core as core


if __name__ == '__main__':
    token: auth.Token = auth.get_token(
        'core',
        # os.environ['TM_E416DEV_SERVER_USERNAME'],
        # os.environ['TM_E416DEV_SERVER_PASSWORD'],
        'fohoover@gmail.com',
        'Hu!xK8&t5AHqN5',
        'e@e416.dev / nadeo_api_py_test',
        # True
    )

    t1 = core.trophies_history(
        token,
        # '594be80b-62f3-4705-932b-e743e97882cf',
        '8f08302a-f670-463b-9f71-fbfacffb8bd1',
        5000,
        0
    )

    # time.sleep(0.5)

    # t2 = core.trophies_history(
    #     token,
    #     '594be80b-62f3-4705-932b-e743e97882cf',
    #     1000,
    #     1000
    # )

    # time.sleep(0.5)

    # t3 = core.trophies_history(
    #     token,
    #     '594be80b-62f3-4705-932b-e743e97882cf',
    #     1000,
    #     2000
    # )

    # time.sleep(0.5)

    # sum = core.trophies_last_year_summary(
    #     token,
    #     '594be80b-62f3-4705-932b-e743e97882cf'
    # )

    pass
