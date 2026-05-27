"""Policy validators."""


class Policy:
    """Base policy class."""
    
    @staticmethod
    def exact_match(field: str, value: str):
        """
        Policy that requires exact field match.
        
        Example:
            policy = Policy.exact_match("status", "pending")
            # Only allows data where status == "pending"
        """
        class ExactMatchPolicy:
            def __init__(self, field, value):
                self.field = field
                self.value = value
            
            def validate(self, data, *args, **kwargs):
                if isinstance(data, dict):
                    return data.get(self.field) == self.value
                return False
        
        return ExactMatchPolicy(field, value)
