from teradatamlspk.ml.util import chisquaretest
ChiSquareTest = type("ChiSquareTest", (), {"test": staticmethod(chisquaretest)})