from datetime import datetime
from http import HTTPStatus
from typing import List

import requests
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import Logger
from message_local.MessageLocal import MessageLocal
from message_local.Recipient import Recipient
from python_sdk_remote.utilities import our_get_env

IS_REALLY_SEND_SMS = our_get_env('IS_REALLY_SEND_SMS', 'False').lower() in ('true', '1')

INFORU_AUTH_TOKEN = our_get_env("INFORU_AUTH_TOKEN", raise_if_not_found=IS_REALLY_SEND_SMS)
url = our_get_env("SMS_MESSAGE_INFORU_URL", raise_if_not_found=IS_REALLY_SEND_SMS)

SMS_SENDER_ID = our_get_env("SMS_SENDER_ID", default="circles")

SMS_MESSAGE_INFORU_API_TYPE_ID = 7  # For API-Management

# TODO: move to constants
SMS_INFORU_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 208
SMS_INFORU_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = "SMS_INFORU_LOCAL_PYTHON_PACKAGE"
DEVELOPER_EMAIL = "emad.a@circ.zone"
logger = Logger.create_logger(object={
    'component_id': SMS_INFORU_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': SMS_INFORU_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
})


class SMSMessageInforu(MessageLocal):
    # Don't call super().__init__(), we already have the message_local object

    def send(self, body: str = None, compound_message_dict: dict = None, recipients: List[Recipient] = None,
             cc: List[Recipient] = None, bcc: List[Recipient] = None,
             scheduled_timestamp_start: datetime = None,
             scheduled_timestamp_end: datetime = None, **kwargs) -> list[int]:
        try:
            recipients = recipients or self.get_recipients()

            for recipient in recipients:
                message = body or self.get_body_text_after_template_processing(recipient)
                phone = recipient.get_normizalied_phone()
                payload = {
                    "Data": {
                        "Message": message,
                        "Recipients": [
                            {
                                "Phone": phone,
                            }
                        ],
                        "Settings": {
                            "Sender": SMS_SENDER_ID
                        }
                    }
                }

                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': INFORU_AUTH_TOKEN,
                }

                # TODO Put this call in remark and add a call to API Management Direct
                # TODO Call API Management InDirect
                if IS_REALLY_SEND_SMS:
                    response = requests.post(url, headers=headers, json=payload)

                    logger.info(f"Response Code: {response.status_code}")
                    logger.info(f"Response Content: {response.text}")

                    if response.status_code == HTTPStatus.OK:
                        logger.info(f"SMS {message} sent successfully to {phone}." + "Response: " + response.text)
                    else:
                        logger.error(
                            f"SMS {message} sending failed to {phone} with status code: {response.status_code}")

        except requests.RequestException as re:
            logger.exception(f"RequestException: {re}")
        except Exception as e:
            logger.exception(
                "An error occurred during the InforU API operation. " + f"Exception Type: {type(e).__name__}, Message: {str(e)}")
            raise
        finally:
            logger.end("SMS message send")
        return []
