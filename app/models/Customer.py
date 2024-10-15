class Customer:
    def __init__(self, custId: int, custName: str, from_location: str, to_location: str):
        self.custId = custId
        self.custName= custName
        self.from_location = from_location
        self.to_location = to_location

    def getCustName(self) -> str:
        return self.custName

    def getCustId(self) -> int:
        return self.custId
