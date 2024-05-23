
class PhoneNumberValidator:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.api_url = "https://api.numlookupapi.com/v1/validate/"
        
    def validate(self, phone_number: str, country_code: str = None) -> bool:
        if not phone_number:
            raise ValueError("Phone Number cannot be empty!")
        return True