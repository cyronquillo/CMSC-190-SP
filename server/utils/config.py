

class DataDetails():

    filenames = {
        'first_debate_1960':
            {
                'candidates': ["SENATOR KENNEDY", "MR. NIXON", "MR. KENNEDY"]
            },
        'first_debate_1976':
            {
                'candidates': ['MR. CARTER', 'MR. FORD']
            },
        'first_debate_1980':
            {
                'candidates': ['REP. JOHN B. ANDERSON', 'GOV. RONALD REAGAN', 'REAGAN', 'ANDERSON']
            },
        'first_debate_1984':
            {
                'candidates': ['MR. MONDALE', 'THE PRESIDENT']
            },
        'first_debate_1988':
            {
                'candidates': ['BUSH', 'DUKAKIS']
            },
        'first_debate_1992':
            {
                'candidates': ['CLINTON', 'BUSH', 'PEROT']
            },
        'first_debate_1996':
            {
                'candidates': ['CLINTON', 'DOLE']
            },
        'first_debate_2000':
            {
                'candidates': ['GORE', 'BUSH']
            },
        'first_debate_2004':
            {
                'candidates': ['BUSH', 'KERRY']
            },
        'first_debate_2008':
            {
                'candidates': ['OBAMA', 'MCCAIN']
            },
        'first_debate_2012':
            {
                'candidates': ['OBAMA', 'ROMNEY']
            },
        'first_debate_2016':
            {
                'candidates': ['TRUMP', 'CLINTON']
            },

        'second_debate_1960':
            {
                'candidates': ['MR. NIXON', 'MR. KENNEDY']
            },
        'second_debate_1976':
            {
                'candidates': ['MR. CARTER', 'MR. FORD']
            },
        'second_debate_1980':
            {
                'candidates': ['MR. CARTER', 'MR. REAGAN']
            },
        'second_debate_1984':
            {
                'candidates': ['MR. MONDALE', 'THE PRESIDENT']
            },
        'second_debate_1988':
            {
                'candidates': ['BUSH', 'DUKAKIS']
            },
        'second_debate_1992':
            {
                'candidates': ['CLINTON', 'BUSH', 'PEROT']
            },
        'second_debate_1996':
            {
                'candidates': ['CLINTON', 'DOLE']
            },
        'second_debate_2000':
            {
                'candidates': ['GORE', 'BUSH']
            },
        'second_debate_2004':
            {
                'candidates': ['BUSH', 'KERRY']
            },
        'second_debate_2008':
            {
                'candidates': ['OBAMA', 'MCCAIN']
            },
        'second_debate_2012':
            {
                'candidates': ['OBAMA', 'ROMNEY']
            },
        'second_debate_2016':
            {
                'candidates': ['Trump', 'Clinton']
            },

        'third_debate_1960':
            {
                'candidates': ['MR. NIXON', 'MR. KENNEDY']
            },
        'third_debate_1976':
            {
                'candidates': ['MR. CARTER', 'MR. FORD']
            },
        'third_debate_1992':
            {
                'candidates': ['CLINTON', 'BUSH', 'PEROT']
            },
        'third_debate_2000':
            {
                'candidates': ['GORE', 'BUSH']
            },
        'third_debate_2004':
            {
                'candidates': ['BUSH', 'KERRY']
            },
        'third_debate_2008':
            {
                'candidates': ['OBAMA', 'MCCAIN']
            },
        'third_debate_2012':
            {
                'candidates': ['OBAMA', 'ROMNEY']
            },
        'third_debate_2016':
            {
                'candidates': ['Trump', 'Clinton']
            },

        'fourth_debate_1960':
            {
                'candidates': ['MR. NIXON', 'MR. KENNEDY']
            }
    }

    API_KEY = {
        'version': '2018-03-16',
        'username': '00623d9d-8736-4e79-8510-b18ca795bf08',
        'password': 'VpOJpCqQclrq'
    }
    extras = [
        '(Applause)',
        '[ applause ]',
        '(APPLAUSE)',
        '[ Applause ]',
        '[Applause]',
        '[applause]',
        '[Arabian]',

        '(Scattered applause)',
        '(Boos and applause)',
        '(Cheers and Applause)',
        '(Laughter, applause)',
        '(Laughter, scattered applause)',
        '(Laughter, boos)',
        '(Laughter and applause)',
        '(CHEERS AND APPLAUSE)',

        '(Laughter)',
        '(Laughter.)',
        '(laughter)'
        '(LAUGHTER)',
        '[Laughter]',
        '(Laughs)',
        '[laughter]',

        '(barely audible)',
        '(continuing)',
        '(CROSSTALK)',
        '[Interruption]',
        '(phonetic)',
        '(Audience: "No.")',
        '[cross talk]',
        '(chuckle)',
        'â€“',
        '[Groan]',
        '(Inaudible)',
        '(inaudible)',
        '(OFF-MIKE)',
        '(sic)',
        '(ph)',
        '(A)',
        '(GOVERNOR CARTER: Yes.)',
        '(upi)',
        '(Reuters)',
        '(CNN)',
        '[twenty-seven-minute delay]'
    ]

    feature_size = 63
    classification = 2
    features = {
        'sentiment': 0,
        'word_count': 1,
        'pos_CC': 2,
        'pos_CD': 3,
        'pos_DT': 4,
        'pos_EX': 5,
        'pos_FW': 6,
        'pos_IN': 7,
        'pos_JJ': 8,
        'pos_JJR': 9,
        'pos_JJS': 10,
        'pos_LS': 11,
        'pos_MD': 12,
        'pos_NN': 13,
        'pos_NNS': 14,
        'pos_NNP': 15,
        'pos_NNPS': 16,
        'pos_PDT': 17,
        'pos_POS': 18,
        'pos_PRP': 19,
        'pos_PRP$': 20,
        'pos_RB': 21,
        'pos_RBR': 22,
        'pos_RBS': 23,
        'pos_RP': 24,
        'pos_TO': 25,
        'pos_UH': 26,
        'pos_VB': 27,
        'pos_VBD': 28,
        'pos_VBG': 29,
        'pos_VBN': 30,
        'pos_VBP': 31,
        'pos_VBZ': 32,
        'pos_WDT': 33,
        'pos_WP': 34,
        'pos_WP$': 35,
        'pos_WRB': 36,
        'et_Anatomy': 37,
        'et_Award': 38,
        'et_Broadcaster': 39,
        'et_Company': 40,
        'et_Crime': 41,
        'et_Drug': 42,
        'et_EmailAddress': 43,
        'et_Facility': 44,
        'et_GeographicFeature': 45,
        'et_HealthCondition': 46,
        'et_Hashtag': 47,
        'et_IPAddress': 48,
        'et_JobTitle': 49,
        'et_Location': 50,
        'et_Movie': 51,
        'et_MusicGroup': 52,
        'et_NaturalEvent': 53,
        'et_Organization': 54,
        'et_Person': 55,
        'et_PrintMedia': 56,
        'et_Quantity': 57,
        'et_Sport': 58,
        'et_SportingEvent': 59,
        'et_TelevisionShow': 60,
        'et_TwitterHandle': 61,
        'et_Vehicle': 62
    }

    dataset_size = 22611
