

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
    features = [
        'sentiment',
        'word_count',
        'pos_CC',
        'pos_CD',
        'pos_DT',
        'pos_EX',
        'pos_FW',
        'pos_IN',
        'pos_JJ',
        'pos_JJR',
        'pos_JJS',
        'pos_LS',
        'pos_MD',
        'pos_NN',
        'pos_NNS',
        'pos_NNP',
        'pos_NNPS',
        'pos_PDT',
        'pos_POS',
        'pos_PRP',
        'pos_PRP$',
        'pos_RB',
        'pos_RBR',
        'pos_RBS',
        'pos_RP',
        'pos_TO',
        'pos_UH',
        'pos_VB',
        'pos_VBD',
        'pos_VBG',
        'pos_VBN',
        'pos_VBP',
        'pos_VBZ',
        'pos_WDT',
        'pos_WP',
        'pos_WP$',
        'pos_WRB',
        'et_Anatomy',
        'et_Award',
        'et_Broadcaster',
        'et_Company',
        'et_Crime',
        'et_Drug',
        'et_EmailAddress',
        'et_Facility',
        'et_GeographicFeature',
        'et_HealthCondition',
        'et_Hashtag',
        'et_IPAddress',
        'et_JobTitle',
        'et_Location',
        'et_Movie',
        'et_MusicGroup',
        'et_NaturalEvent',
        'et_Organization',
        'et_Person',
        'et_PrintMedia',
        'et_Quantity',
        'et_Sport',
        'et_SportingEvent',
        'et_TelevisionShow',
        'et_TwitterHandle',
        'et_Vehicle'
    ]

    dataset_size = 22611
