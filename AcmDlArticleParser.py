class AcmDlArticleParser:
    mode_layout = 'flat'
    exp_format = 'bibtex'
    domain = 'https://dl.acm.org/'
    article = 'citation.cfm?id={0}&'
    parametrs = 'preflayout={0}'
    url = domain + article + parametrs

    def __init__(self):
        self.id = None