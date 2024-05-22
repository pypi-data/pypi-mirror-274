class StiEventArgs:

    event: str = None
    """Name of the current event."""
    
    sender: object = None
    """The component that sent the request."""


### Private

    def __populateVars(self, obj: object):
        attributes = [attr for attr in dir(self) if not attr.startswith('_') and attr != 'sender']
        for attr in attributes:
            if hasattr(obj, attr):
                setattr(self, attr, getattr(obj, attr))


### Constructor

    def __init__(self, obj: object = None):
        if (obj != None):
            self.__populateVars(obj)