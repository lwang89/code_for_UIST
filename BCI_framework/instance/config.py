EXPERIMENT_PARAMETERS = [
    {
        "experimentID": 0,                                      # int
        "experimentName": "Test Nback visual using no device",   # string
        "experimentCreator": "Ben",                             # string
        "experimentDescription": "Test Visual n-back experiment",      # string
        "boosted_devices": [],                                  # ["fnirs"], ["muse"], or [].
        "introductionVideoPath": "nback/general_intro_audio.mp4",
        "receiverCalibrationStart": 3,                          # int temprorally used for fnirs data preporcessing, wait for a while to start
        "receiverCalibrationDuration": 20,                      # int temprorally used for fnirs data preporcessing, wait for a while to start
        "sessionParameters": 
        [
            {
                "sessionID": "0_1",
                "sessionType": "train",
                "sessionRestDuration": 20,
                "serials": [
                    {
                        "serialID": "0_1_1",
                        "introduction": {
                            "duration": 5,
                            "content": "This is a 0-back task. Every number is a target number.",
                            "img_url": 'nback/0_back.png',
                            "audio_url": "nback/intro_0_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [9, 2, 1, 6, 5, 3, 7, 8, 1, 4],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 0},
                        },
                    },
                    {
                        "serialID": "0_1_2",
                        "introduction": {
                            "duration": 10,
                            "content": "This is a 1-back task. A number is a target if it is identical to the previous number.",
                            "img_url": 'nback/1_back.png',
                            "audio_url": "nback/intro_1_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [1, 4, 4, 2, 5, 2, 9, 2, 7, 2],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 1},
                        },
                    },
                ],
            },
            {
                "sessionID": "0_2",
                "sessionType": "test",
                "sessionRestDuration": 20,
                "serials": [
                    {
                        "serialID": "0_2_1",
                        "introduction": {
                            "duration": 5,
                            "content": "This is a 2-back task. A number is a target if it is identical to the number 2 steps back.",
                            "img_url": 'nback/2_back.png',
                            "audio_url": "nback/intro_2_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [2, 3, 6, 8, 6, 2, 4, 4, 4, 2],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 2},
                        },
                    },
                    {
                        "serialID": "0_2_2",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 3-back task. A number is a target if it is identical to the number 3 steps back.",
                            "img_url": 'nback/3_back.png',
                            "audio_url": "nback/intro_3_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [3, 2, 2, 6, 2, 6, 3, 9, 2, 9],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 3},
                        },
                    },
                ],
            },
        ]
    },
    {
        "experimentID": 1,                                      # int
        "experimentName": "Nback Visual using fNIRS",           # string
        "experimentCreator": "Leon",                            # string
        "experimentDescription": "Real n-back experiment",      # string
        "boosted_devices": ["fnirs"],                           # ["fnirs"], ["muse"], or [].
        "introductionVideoPath": "nback/general_intro_visual.mp4",
        "receiverCalibrationStart": 5,                          # int temprorally used for fnirs data preporcessing, wait for a while to start
        "receiverCalibrationDuration": 20,                      # int temprorally used for fnirs data preporcessing, wait for a while to start
        "sessionParameters": 
        [
            {
                "sessionID": "1_1",
                "sessionType": "train",

                "sessionRestDuration": 20,
                "serials": [
                    {
                        "serialID": "1_1_1",
                        "introduction": {
                            "duration": 5,
                            "content": "This is a 0-back task. Every number is a target number.",
                            "img_url": 'nback/0_back.png',
                            "audio_url": "nback/intro_0_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [9, 9, 1, 9, 7, 3, 5, 1, 9, 6, 7, 9, 5, 2, 2, 1, 1, 2, 4, 7, 3, 9, 3, 7, 9, 3, 3, 1, 3, 7, 2, 2, 2, 5, 6, 7, 8, 3, 4, 6],
                            "displayDuration": 0.5,
                            "trialDuration": 2,     # The sum of display time and interval between display
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 0},
                        },
                    },
                    {
                        "serialID": "1_1_2",
                        "introduction": {
                            "duration": 10,
                            "content": "This is a 1-back task. A number is a target if it is identical to the previous number.",
                            "img_url": 'nback/1_back.png',
                            "audio_url": "nback/intro_1_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [2, 5, 9, 7, 6, 6, 1, 1, 1, 6, 6, 9, 9, 5, 5, 9, 4, 6, 6, 5, 7, 8, 5, 5, 7, 4, 4, 1, 7, 7, 7, 5, 2, 5, 7, 3, 3, 5, 9, 5],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 1},
                        },
                    },
                    {
                        "serialID": "1_1_3",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 2-back task. A number is a target if it is identical to the number 2 steps back.",
                            "img_url": 'nback/2_back.png',
                            "audio_url": "nback/intro_2_back.mp3",
                        },
                        "serialRestDuration": 30,
                        "trial": {
                            "sequence": [2, 7, 6, 8, 5, 1, 5, 5, 3, 7, 3, 4, 7, 7, 4, 9, 3, 9, 7, 9, 7, 9, 8, 4, 8, 9, 7, 1, 4, 7, 8, 7, 8, 9, 1, 9, 4, 9, 2, 9],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 2},
                        },
                    },
                    {
                        "serialID": "1_1_4",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 3-back task. A number is a target if it is identical to the number 3 steps back.",
                            "img_url": 'nback/3_back.png',
                            "audio_url": "nback/intro_3_back.mp3",
                        },
                        "serialRestDuration": 40,
                        "trial": {
                            "sequence": [2, 2, 3, 4, 5, 3, 9, 1, 3, 9, 4, 4, 3, 9, 7, 8, 5, 7, 8, 5, 9, 8, 5, 2, 8, 1, 3, 4, 1, 2, 7, 5, 9, 1, 4, 9, 1, 3, 4, 9],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 3},
                        },
                    },
                    {
                        "serialID": "1_1_5",
                        "introduction": {
                            "duration": 10,
                            "content": "This is a 1-back task. A number is a target if it is identical to the previous number.",
                            "img_url": 'nback/1_back.png',
                            "audio_url": "nback/intro_1_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [7, 5, 6, 7, 9, 2, 2, 6, 6, 2, 2, 2, 1, 7, 7, 7, 8, 8, 3, 6, 9, 4, 6, 9, 1, 1, 7, 2, 3, 4, 4, 4, 6, 6, 5, 1, 3, 9, 2, 2],
                            "displayDuration": 0.5,
                            "trialDuration": 2,     # The sum of display time and interval between display
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 1},
                        },
                    },
                    {
                        "serialID": "1_1_6",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 2-back task. A number is a target if it is identical to the number 2 steps back.",
                            "img_url": 'nback/2_back.png',
                            "audio_url": "nback/intro_2_back.mp3",
                        },
                        "serialRestDuration": 30,
                        "trial": {
                            "sequence": [1, 2, 4, 4, 4, 7, 4, 1, 7, 1, 6, 9, 1, 1, 1, 1, 3, 1, 7, 7, 5, 7, 8, 6, 9, 9, 9, 1, 7, 1, 6, 9, 9, 9, 2, 8, 2, 8, 5, 5],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 2},
                        },
                    },
                    {
                        "serialID": "1_1_7",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 3-back task. A number is a target if it is identical to the number 3 steps back.",
                            "img_url": 'nback/3_back.png',
                            "audio_url": "nback/intro_3_back.mp3",
                        },
                        "serialRestDuration": 40,
                        "trial": {
                            "sequence": [7, 6, 5, 5, 6, 5, 6, 7, 3, 6, 2, 5, 6, 1, 5, 6, 9, 6, 4, 7, 6, 6, 6, 1, 6, 2, 9, 7, 2, 2, 2, 2, 2, 2, 9, 8, 1, 1, 4, 3],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 3},
                        },
                    },
                    {
                        "serialID": "1_1_8",
                        "introduction": {
                            "duration": 5,
                            "content": "This is a 0-back task. Every number is a target number.",
                            "img_url": 'nback/0_back.png',
                            "audio_url": "nback/intro_0_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [1, 8, 2, 1, 4, 2, 4, 9, 4, 6, 4, 7, 6, 5, 1, 4, 7, 6, 3, 3, 8, 7, 9, 4, 7, 3, 1, 2, 5, 5, 2, 1, 5, 2, 5, 1, 9, 8, 8, 6],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 0},
                        },
                    },
                    {
                        "serialID": "1_1_9",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 2-back task. A number is a target if it is identical to the number 2 steps back.",
                            "img_url": 'nback/2_back.png',
                            "audio_url": "nback/intro_2_back.mp3",
                        },
                        "serialRestDuration": 30,
                        "trial": {
                            "sequence": [5, 8, 5, 2, 1, 2, 2, 2, 1, 5, 6, 2, 1, 5, 1, 3, 2, 2, 7, 8, 2, 4, 9, 4, 9, 4, 9, 6, 8, 6, 9, 6, 9, 3, 4, 6, 1, 6, 3, 7],
                            "displayDuration": 0.5,
                            "trialDuration": 2,     # The sum of display time and interval between display
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 2},
                        },
                    },
                    {
                        "serialID": "1_1_10",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 3-back task. A number is a target if it is identical to the number 3 steps back.",
                            "img_url": 'nback/3_back.png',
                            "audio_url": "nback/intro_3_back.mp3",
                        },
                        "serialRestDuration": 40,
                        "trial": {
                            "sequence": [8, 9, 1, 8, 3, 9, 1, 7, 8, 1, 9, 8, 4, 2, 8, 4, 2, 5, 6, 5, 7, 9, 8, 7, 8, 8, 2, 7, 2, 7, 8, 9, 7, 8, 9, 7, 9, 5, 3, 4],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 3},
                        },
                    },
                    {
                        "serialID": "1_1_11",
                        "introduction": {
                            "duration": 5,
                            "content": "This is a 0-back task. Every number is a target number.",
                            "img_url": 'nback/0_back.png',
                            "audio_url": "nback/intro_0_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [2, 6, 5, 1, 1, 6, 2, 8, 5, 2, 2, 3, 4, 6, 5, 3, 2, 7, 4, 8, 7, 8, 6, 7, 9, 4, 8, 9, 8, 9, 9, 2, 7, 1, 9, 9, 6, 2, 2, 5],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 0},
                        },
                    },
                    {
                        "serialID": "1_1_12",
                        "introduction": {
                            "duration": 10,
                            "content": "This is a 1-back task. A number is a target if it is identical to the previous number.",
                            "img_url": 'nback/1_back.png',
                            "audio_url": "nback/intro_1_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [5, 1, 4, 3, 7, 1, 7, 2, 2, 2, 8, 6, 8, 9, 9, 2, 8, 6, 5, 6, 5, 1, 8, 9, 9, 9, 6, 1, 1, 4, 5, 5, 7, 7, 7, 7, 1, 6, 6, 6],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 1},
                        },
                    },
                ],
            },
            {
                "sessionID": "1_2",
                "sessionType": "test",
                "sessionRestDuration": 20,
                "serials": [
                    {
                        "serialID": "1_2_1",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 3-back task. A number is a target if it is identical to the number 3 steps back.",
                            "img_url": 'nback/3_back.png',
                            "audio_url": "nback/intro_3_back.mp3",
                        },
                        "serialRestDuration": 40,
                        "trial": {
                            "sequence": [3, 2, 1, 6, 2, 1, 3, 2, 3, 3, 3, 9, 6, 3, 7, 6, 1, 9, 7, 3, 7, 8, 4, 8, 8, 4, 2, 3, 4, 9, 3, 4, 3, 3, 9, 1, 9, 5, 8, 8],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 3},
                        },
                    },
                    {
                        "serialID": "1_2_2",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 0-back task. Every number is a target number.",
                            "img_url": 'nback/0_back.png',
                            "audio_url": "nback/intro_0_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [1, 8, 9, 2, 1, 5, 6, 6, 9, 4, 5, 4, 6, 5, 2, 4, 5, 6, 2, 1, 9, 9, 2, 9, 4, 4, 7, 8, 1, 1, 5, 2, 2, 8, 3, 6, 9, 6, 8, 5],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 0},
                        },
                    },
                    {
                        "serialID": "1_2_3",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 1-back task. A number is a target if it is identical to the previous number.",
                            "img_url": 'nback/1_back.png',
                            "audio_url": "nback/intro_1_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [9, 1, 1, 1, 1, 2, 9, 3, 8, 4, 4, 8, 5, 6, 2, 2, 1, 3, 8, 8, 8, 8, 9, 2, 1, 1, 9, 4, 3, 7, 7, 4, 2, 9, 7, 8, 9, 9, 9, 5],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 1},
                        },
                    },
                    {
                        "serialID": "1_2_4",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 2-back task. A number is a target if it is identical to the number 2 steps back.",
                            "img_url": 'nback/2_back.png',
                            "audio_url": "nback/intro_2_back.mp3",
                        },
                        "serialRestDuration": 30,
                        "trial": {
                            "sequence": [4, 3, 9, 3, 9, 6, 9, 7, 9, 7, 4, 7, 6, 5, 4, 8, 5, 3, 5, 7, 5, 4, 6, 5, 5, 4, 5, 4, 5, 7, 5, 5, 2, 2, 8, 8, 7, 9, 9, 8],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 2},
                        },
                    },
                ],
            },
        ]
    },
    { 
        "experimentID": 2,                                      # int
        "experimentName": "Nback  using fNIRS",            # string
        "experimentCreator": "Leon",                            # string
        "experimentDescription": "Real n-back experiment",      # string
        "boosted_devices": ["fnirs"],                           # ["fnirs"], ["muse"], or [].
        "introductionVideoPath": "nback/general_intro_visual.mp4",
        "receiverCalibrationStart": 5,                          # int temprorally used for fnirs data preporcessing, wait for a while to start
        "receiverCalibrationDuration": 20,                      # int temprorally used for fnirs data preporcessing, wait for a while to start
        "sessionParameters": 
        [
            {
                "sessionID": "2_1",
                "sessionType": "train",

                "sessionRestDuration": 20,
                "serials": [
                    {
                        "serialID": "2_1_1",
                        "introduction": {
                            "duration": 5,
                            "content": "This is a 0-back task. Every number is a target number.",
                            "img_url": 'nback/0_back.png',
                            "audio_url": "nback/intro_0_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [9, 9, 1, 9, 7, 3, 5, 1, 9, 6, 7, 9, 5, 2, 2, 1, 1, 2, 4, 7, 3, 9, 3, 7, 9, 3, 3, 1, 3, 7, 2, 2, 2, 5, 6, 7, 8, 3, 4, 6],
                            "displayDuration": 0.5,
                            "trialDuration": 2,     # The sum of display time and interval between display
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 0},
                        },
                    },
                    {
                        "serialID": "2_1_2",
                        "introduction": {
                            "duration": 10,
                            "content": "This is a 1-back task. A number is a target if it is identical to the previous number.",
                            "img_url": 'nback/1_back.png',
                            "audio_url": "nback/intro_1_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [2, 5, 9, 7, 6, 6, 1, 1, 1, 6, 6, 9, 9, 5, 5, 9, 4, 6, 6, 5, 7, 8, 5, 5, 7, 4, 4, 1, 7, 7, 7, 5, 2, 5, 7, 3, 3, 5, 9, 5],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 1},
                        },
                    },
                    {
                        "serialID": "2_1_3",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 2-back task. A number is a target if it is identical to the number 2 steps back.",
                            "img_url": 'nback/2_back.png',
                            "audio_url": "nback/intro_2_back.mp3",
                        },
                        "serialRestDuration": 30,
                        "trial": {
                            "sequence": [2, 7, 6, 8, 5, 1, 5, 5, 3, 7, 3, 4, 7, 7, 4, 9, 3, 9, 7, 9, 7, 9, 8, 4, 8, 9, 7, 1, 4, 7, 8, 7, 8, 9, 1, 9, 4, 9, 2, 9],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 2},
                        },
                    },
                    {
                        "serialID": "2_1_4",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 3-back task. A number is a target if it is identical to the number 3 steps back.",
                            "img_url": 'nback/3_back.png',
                            "audio_url": "nback/intro_3_back.mp3",
                        },
                        "serialRestDuration": 40,
                        "trial": {
                            "sequence": [2, 2, 3, 4, 5, 3, 9, 1, 3, 9, 4, 4, 3, 9, 7, 8, 5, 7, 8, 5, 9, 8, 5, 2, 8, 1, 3, 4, 1, 2, 7, 5, 9, 1, 4, 9, 1, 3, 4, 9],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 3},
                        },
                    },
                    {
                        "serialID": "2_1_5",
                        "introduction": {
                            "duration": 10,
                            "content": "This is a 1-back task. A number is a target if it is identical to the previous number.",
                            "img_url": 'nback/1_back.png',
                            "audio_url": "nback/intro_1_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [7, 5, 6, 7, 9, 2, 2, 6, 6, 2, 2, 2, 1, 7, 7, 7, 8, 8, 3, 6, 9, 4, 6, 9, 1, 1, 7, 2, 3, 4, 4, 4, 6, 6, 5, 1, 3, 9, 2, 2],
                            "displayDuration": 0.5,
                            "trialDuration": 2,     # The sum of display time and interval between display
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 1},
                        },
                    },
                    {
                        "serialID": "2_1_6",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 2-back task. A number is a target if it is identical to the number 2 steps back.",
                            "img_url": 'nback/2_back.png',
                            "audio_url": "nback/intro_2_back.mp3",
                        },
                        "serialRestDuration": 30,
                        "trial": {
                            "sequence": [1, 2, 4, 4, 4, 7, 4, 1, 7, 1, 6, 9, 1, 1, 1, 1, 3, 1, 7, 7, 5, 7, 8, 6, 9, 9, 9, 1, 7, 1, 6, 9, 9, 9, 2, 8, 2, 8, 5, 5],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 2},
                        },
                    },
                    {
                        "serialID": "2_1_7",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 3-back task. A number is a target if it is identical to the number 3 steps back.",
                            "img_url": 'nback/3_back.png',
                            "audio_url": "nback/intro_3_back.mp3",
                        },
                        "serialRestDuration": 40,
                        "trial": {
                            "sequence": [7, 6, 5, 5, 6, 5, 6, 7, 3, 6, 2, 5, 6, 1, 5, 6, 9, 6, 4, 7, 6, 6, 6, 1, 6, 2, 9, 7, 2, 2, 2, 2, 2, 2, 9, 8, 1, 1, 4, 3],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 3},
                        },
                    },
                    {
                        "serialID": "2_1_8",
                        "introduction": {
                            "duration": 5,
                            "content": "This is a 0-back task. Every number is a target number.",
                            "img_url": 'nback/0_back.png',
                            "audio_url": "nback/intro_0_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [1, 8, 2, 1, 4, 2, 4, 9, 4, 6, 4, 7, 6, 5, 1, 4, 7, 6, 3, 3, 8, 7, 9, 4, 7, 3, 1, 2, 5, 5, 2, 1, 5, 2, 5, 1, 9, 8, 8, 6],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 0},
                        },
                    },
                    {
                        "serialID": "2_1_9",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 2-back task. A number is a target if it is identical to the number 2 steps back.",
                            "img_url": 'nback/2_back.png',
                            "audio_url": "nback/intro_2_back.mp3",
                        },
                        "serialRestDuration": 30,
                        "trial": {
                            "sequence": [5, 8, 5, 2, 1, 2, 2, 2, 1, 5, 6, 2, 1, 5, 1, 3, 2, 2, 7, 8, 2, 4, 9, 4, 9, 4, 9, 6, 8, 6, 9, 6, 9, 3, 4, 6, 1, 6, 3, 7],
                            "displayDuration": 0.5,
                            "trialDuration": 2,     # The sum of display time and interval between display
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 2},
                        },
                    },
                    {
                        "serialID": "2_1_10",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 3-back task. A number is a target if it is identical to the number 3 steps back.",
                            "img_url": 'nback/3_back.png',
                            "audio_url": "nback/intro_3_back.mp3",
                        },
                        "serialRestDuration": 40,
                        "trial": {
                            "sequence": [8, 9, 1, 8, 3, 9, 1, 7, 8, 1, 9, 8, 4, 2, 8, 4, 2, 5, 6, 5, 7, 9, 8, 7, 8, 8, 2, 7, 2, 7, 8, 9, 7, 8, 9, 7, 9, 5, 3, 4],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 3},
                        },
                    },
                    {
                        "serialID": "2_1_11",
                        "introduction": {
                            "duration": 5,
                            "content": "This is a 0-back task. Every number is a target number.",
                            "img_url": 'nback/0_back.png',
                            "audio_url": "nback/intro_0_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [2, 6, 5, 1, 1, 6, 2, 8, 5, 2, 2, 3, 4, 6, 5, 3, 2, 7, 4, 8, 7, 8, 6, 7, 9, 4, 8, 9, 8, 9, 9, 2, 7, 1, 9, 9, 6, 2, 2, 5],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 0},
                        },
                    },
                    {
                        "serialID": "2_1_12",
                        "introduction": {
                            "duration": 10,
                            "content": "This is a 1-back task. A number is a target if it is identical to the previous number.",
                            "img_url": 'nback/1_back.png',
                            "audio_url": "nback/intro_1_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [5, 1, 4, 3, 7, 1, 7, 2, 2, 2, 8, 6, 8, 9, 9, 2, 8, 6, 5, 6, 5, 1, 8, 9, 9, 9, 6, 1, 1, 4, 5, 5, 7, 7, 7, 7, 1, 6, 6, 6],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 1},
                        },
                    },
                ],
            },
            {
                "sessionID": "2_2",
                "sessionType": "test",
                "sessionRestDuration": 20,
                "serials": [
                    {
                        "serialID": "2_2_1",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 3-back task. A number is a target if it is identical to the number 3 steps back.",
                            "img_url": 'nback/3_back.png',
                            "audio_url": "nback/intro_3_back.mp3",
                        },
                        "serialRestDuration": 40,
                        "trial": {
                            "sequence": [3, 2, 1, 6, 2, 1, 3, 2, 3, 3, 3, 9, 6, 3, 7, 6, 1, 9, 7, 3, 7, 8, 4, 8, 8, 4, 2, 3, 4, 9, 3, 4, 3, 3, 9, 1, 9, 5, 8, 8],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 3},
                        },
                    },
                    {
                        "serialID": "2_2_2",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 0-back task. Every number is a target number.",
                            "img_url": 'nback/0_back.png',
                            "audio_url": "nback/intro_0_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [1, 8, 9, 2, 1, 5, 6, 6, 9, 4, 5, 4, 6, 5, 2, 4, 5, 6, 2, 1, 9, 9, 2, 9, 4, 4, 7, 8, 1, 1, 5, 2, 2, 8, 3, 6, 9, 6, 8, 5],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 0},
                        },
                    },
                    {
                        "serialID": "2_2_3",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 1-back task. A number is a target if it is identical to the previous number.",
                            "img_url": 'nback/1_back.png',
                            "audio_url": "nback/intro_1_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [9, 1, 1, 1, 1, 2, 9, 3, 8, 4, 4, 8, 5, 6, 2, 2, 1, 3, 8, 8, 8, 8, 9, 2, 1, 1, 9, 4, 3, 7, 7, 4, 2, 9, 7, 8, 9, 9, 9, 5],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 1},
                        },
                    },
                    {
                        "serialID": "2_2_4",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 2-back task. A number is a target if it is identical to the number 2 steps back.",
                            "img_url": 'nback/2_back.png',
                            "audio_url": "nback/intro_2_back.mp3",
                        },
                        "serialRestDuration": 30,
                        "trial": {
                            "sequence": [4, 3, 9, 3, 9, 6, 9, 7, 9, 7, 4, 7, 6, 5, 4, 8, 5, 3, 5, 7, 5, 4, 6, 5, 5, 4, 5, 4, 5, 7, 5, 5, 2, 2, 8, 8, 7, 9, 9, 8],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberAudio", "bigN": 2},
                        },
                    },
                ],
            },
        ]
    },
    {
        "experimentID": 3,                                      # int
        "experimentName": "Test Nback Visual using fNIRS",      # string
        "experimentCreator": "Leon",                            # string
        "experimentDescription": "Real n-back experiment",      # string
        "boosted_devices": ["fnirs"],                           # ["fnirs"], ["muse"], or [].
        "introductionVideoPath": "nback/general_intro_visual.mp4",
        "receiverCalibrationStart": 5,                          # int temprorally used for fnirs data preporcessing, wait for a while to start
        "receiverCalibrationDuration": 20,                      # int temprorally used for fnirs data preporcessing, wait for a while to start
        "sessionParameters": 
        [
            {
                "sessionID": "1_1",
                "sessionType": "train",

                "sessionRestDuration": 20,
                "serials": [
                    {
                        "serialID": "1_1_1",
                        "introduction": {
                            "duration": 5,
                            "content": "This is a 0-back task. Every number is a target number.",
                            "img_url": 'nback/0_back.png',
                            "audio_url": "nback/intro_0_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [9, 9, 1, 9, 7, 3, 5, 1, 9, 6, 7, 9, 5, 2, 2, 1, 1, 2, 4, 7, 3, 9, 3, 7, 9, 3, 3, 1, 3, 7, 2, 2, 2, 5, 6, 7, 8, 3, 4, 6],
                            "displayDuration": 0.5,
                            "trialDuration": 2,     # The sum of display time and interval between display
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 0},
                        },
                    },
                    {
                        "serialID": "1_1_2",
                        "introduction": {
                            "duration": 10,
                            "content": "This is a 1-back task. A number is a target if it is identical to the previous number.",
                            "img_url": 'nback/1_back.png',
                            "audio_url": "nback/intro_1_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [2, 5, 9, 7, 6, 6, 1, 1, 1, 6, 6, 9, 9, 5, 5, 9, 4, 6, 6, 5, 7, 8, 5, 5, 7, 4, 4, 1, 7, 7, 7, 5, 2, 5, 7, 3, 3, 5, 9, 5],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 1},
                        },
                    },
                ],
            },
            {
                "sessionID": "1_2",
                "sessionType": "test",
                "sessionRestDuration": 20,
                "serials": [
                    {
                        "serialID": "1_2_1",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 3-back task. A number is a target if it is identical to the number 3 steps back.",
                            "img_url": 'nback/3_back.png',
                            "audio_url": "nback/intro_3_back.mp3",
                        },
                        "serialRestDuration": 40,
                        "trial": {
                            "sequence": [3, 2, 1, 6, 2, 1, 3, 2, 3, 3, 3, 9, 6, 3, 7, 6, 1, 9, 7, 3, 7, 8, 4, 8, 8, 4, 2, 3, 4, 9, 3, 4, 3, 3, 9, 1, 9, 5, 8, 8],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 3},
                        },
                    },
                    {
                        "serialID": "1_2_2",
                        "introduction": {
                            "duration": 15,
                            "content": "This is a 0-back task. Every number is a target number.",
                            "img_url": 'nback/0_back.png',
                            "audio_url": "nback/intro_0_back.mp3",
                        },
                        "serialRestDuration": 20,
                        "trial": {
                            "sequence": [1, 8, 9, 2, 1, 5, 6, 6, 9, 4, 5, 4, 6, 5, 2, 4, 5, 6, 2, 1, 9, 9, 2, 9, 4, 4, 7, 8, 1, 1, 5, 2, 2, 8, 3, 6, 9, 6, 8, 5],
                            "displayDuration": 0.5,
                            "trialDuration": 2,
                            "trialParameters": {"trialType": "NBackNumberVisual", "bigN": 0},
                        },
                    },
                ],
            },
        ]
    },
]

DATA_RECEIVER_PARAMETERS = [
    {
        "name": "fnirs",
        "id": 1,
        "description": "A device to collect fnirs signal",
        "default_label": -1,
        "send_port": 1243
    },
]

FEATURE_INDEX = {
   
    'fnirs': []\
            + ['dO_I_AB', 'dD_I_AB', 'dO_phi_AB', 'dD_phi_AB']\
            + ['dO_I_CD', 'dD_I_CD', 'dO_phi_CD', 'dD_phi_CD']
}
COL_INDEX = ['label', 'chunk']


# The data receivers generate slide window raw dataset following the below protocols.
# It is useful when deploying online analysis.
RAW_DATA_SLIDE_WINDOW_PARAMETERS = [
    {"window_length": 3, "slide_interval": 2},
    {"window_length": 10, "slide_interval": 3}
]

MODEL_TRAINING_PARAMETERS = {
    ######################### Common Parameters #########################
    "n_epoch": 10,
    "train_batch_size": 165,
    "val_batch_size": 66,
    "eval_every_iteration": 5,
    "learning_rate": float(1e-2),
    "input_size": None,             # Should be auto generated
    "num_classes": 4,
    "load_mode": "personal",
    "model_class": "CNN",
    "initialized": False,
    "load_group_model_path": '/cluster/tufts/hugheslab/zhuang12/HCI/brain_data_processing-master/hz_framework_draft2_nature/fast_test_running/slided_window/group_model/CNN/group_best_model_random_seed_0.statedict',
    "gpu_index": "cuda:0",
    ######################### Model Specific Parameters #########################
    "conv1d_hidden_size": 32,
    "window_size": 5,               # Irrelative with slide window parameters
    "window_stride": 1,             # Irrelative with slide window parameters
    "linear_hidden_size": 36,

    ######################### Training File Path Parameters #########################
    "slide_window_size": 10,        # Should be same as slide window length above
    "slide_interval": 3,            # Should be same as slide window interval above
    "result_save_dir": None,        # Should be auto generated
    "train_dir": None,              # Should be auto generated
    "train_files": None,            # Should be auto generated
    "feature_index": None,          # Should be auto generated
    "col_index": None,              # Should be auto generated
    ######################### Data Features #########################
    "device": "fnirs"
}

# 
PREDICTION_SERVER_PARAMETERS = {

    "port": 1243,
    "test_session_time": 1800,

    "slide_window_size": 10,        # Should be same as slide window length above
    # we do prediction on the chunk sent from server, no need to use stride

    "test_batch_size": 1,
    "model_class": "CNN",
    "person_index": 0,              # Use which person's model to predict
    "feature_index": None,          # Should be auto generated
    ######################### Data Features #########################
    "device": "fnirs"
}

STORE_PATH = {
    "pre_experiment_path"               :   "library/storage/pre_experiment",
    "experiment_raw_data_path"          :   "library/storage/experiment/raw_data",
    "experiment_slide_window_data_path" :   "library/storage/experiment/slide_window_data",
    "experiment_preprocessed_data_path" :   "library/storage/experiment/preprocessed_data",
    "experiment_analyzed_data_path"     :   "library/storage/experiment/analyzed_data",
    "experiment_models_path"            :   "library/storage/experiment/models",
    "post_experiment_path"              :   "library/storage/post_experiment",
    "log_path"                          :   "library/storage/log"
}
