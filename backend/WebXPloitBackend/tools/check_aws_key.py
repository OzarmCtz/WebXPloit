# EXEMPLE OF RUNNING : python .\run.py AKLIASOMETHING PASSWORD
import datetime
import boto3
import sys
import botocore


class CheckAwsKeyAndSes:
    def __init__(self):
        self.regions = [
            "us-east-2",
            "us-east-1",
            "us-west-1",
            "us-west-2",
            "af-south-1",
            "ap-southeast-3",
            "ap-south-1",
            "ap-northeast-3",
            "ap-northeast-2",
            "ap-southeast-1",
            "ap-southeast-2",
            "ap-northeast-1",
            "ca-central-1",
            "eu-central-1",
            "eu-west-1",
            "eu-west-2",
            "eu-south-1",
            "eu-west-3",
            "eu-north-1",
            "il-central-1",
            "me-south-1",
            "sa-east-1",
        ]
        akia_key = sys.argv[1]
        akia_password = sys.argv[2]

        self.session = boto3.Session(
            aws_access_key_id=akia_key, aws_secret_access_key=akia_password
        )

    def run(self):
        if not self.check_aws_credentials(self.session):
            sys.exit(1)
        table_data = []
        for region in self.regions:
            client = self.session.client("sesv2", region_name=region)
            try:
                response = client.get_account()
                enforcement_status = response.get("EnforcementStatus", "Unavailable")
                sending_eneabled = response.get("SendingEnabled", "Unavailable")

                # Accéder au sous-dictionnaire 'SendQuota' pour 'Max24HourSend' et 'SentLast24Hours'
                max_24_hour_send = response["SendQuota"].get(
                    "Max24HourSend", "Unavailable"
                )
                sent_last_24_hours = response["SendQuota"].get(
                    "SentLast24Hours", "Unavailable"
                )

                table_data.append(
                    {
                        "Region": region,
                        "EnforcementStatus": enforcement_status,
                        "Max24HourSend": max_24_hour_send,
                        "SentLast24Hours": sent_last_24_hours,
                        "SendingEnabled": sending_eneabled,
                    }
                )
            except botocore.exceptions.ClientError as e:
                error_code = e.response["Error"]["Code"]
                if error_code == "AccessDeniedException":
                    print(f"AccessDeniedException : {e}")
                    break
                else:
                    print(
                        f"An error occurred when fetching information for region {region}: {e}"
                    )

        # Afficher les informations sous forme de tableau
        print(
            f"{'Region':<15}{'EnforcementStatus':<20}{'Max24HourSend':<15}{'SendingEnabled':<15}{'SentLast24Hours'}"
        )

        for data in table_data:
            print(
                f"{data['Region']:<15}{data['EnforcementStatus']:<20}{data['Max24HourSend']:<15}{data['SendingEnabled']:<15}{data['SentLast24Hours']}"
            )

        now = datetime.datetime.now()
        heure_formattee = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nAws Key checked at : {heure_formattee}")

    def check_aws_credentials(self, session):
        try:
            sts = session.client("sts")
            account_id = sts.get_caller_identity()["Account"]
            print(f"Successfully authenticated with account ID: {account_id}")
            return True
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "SignatureDoesNotMatch":
                print(
                    "The provided AWS credentials are incorrect. Please check your Access Key ID and Secret Access Key."
                )
            else:
                print(f"An unexpected error occurred: {e}")
            return False


CheckAwsKeyAndSes().run()
