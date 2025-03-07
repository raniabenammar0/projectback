   
class EmailStatus:
    @staticmethod
    def success():
        return {
            "status": "success",
            "message": "Email sent successfully."
        }

    @staticmethod
    def error_missing_credentials():
        return {
            "status": "error",
            "message": "Missing email credentials."
        }

    @staticmethod
    def error_sending_failed(reason):
        return {
            "status": "error",
            "message": f"Failed to send email: {reason}"
        }
