from factory.fuzzy import BaseFuzzyAttribute, FuzzyInteger, FuzzyChoice


class FuzzyPhoneNumber(BaseFuzzyAttribute):
    def prefix(self):
        return FuzzyChoice(["07", "+447"]).fuzz()

    def fuzz(self):
        return self.prefix() + str(FuzzyInteger(low=100000000, high=999999999).fuzz())


class FuzzyStringInteger(FuzzyInteger):
    def fuzz(self):
        return str(super().fuzz())
