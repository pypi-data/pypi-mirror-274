from slurpit.models.basemodel import BaseModel

class Platform(BaseModel):
    def __init__(self, status: str):
        """
        Initializes a new instance of the Platform class, which inherits from BaseModel.

        Args:
            status (str): The status of the platform, indicating its current operational state.
        """
        self.status = status  # Store the platform's status
