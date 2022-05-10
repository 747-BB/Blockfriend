class FatalSolverError(Exception):
    '''A fatal error in the captcha solving process.'''
    pass


class SolverError(Exception):
    '''An error in the captcha solving, retry the process.'''
    pass