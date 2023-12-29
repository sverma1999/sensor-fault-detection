import sys


# function to get error message with line number and file name
def error_message_detail(error, error_detail: sys):
    # Loads the tuple returned by sys.exc_info() into three variables, we are interested in the third variable which is the traceback object.
    _, _, exc_tb = error_detail.exc_info()

    # we get the file name from the traceback object
    file_name = exc_tb.tb_frame.f_code.co_filename

    # we create the error message with the file name, line number and error message
    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message


class SensorException(Exception):
    def __init__(self, error_message, error_detail):
        """
        :param error_message: error message in string format
        """
        # we are passing the error message to the parent class 'Exception', to initialize the exception with the provided error message.
        super().__init__(error_message)

        # we call the function to get the error message with line number and file name
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    # we are overriding the __str__ method to return the error message
    def __str__(self):
        return self.error_message
