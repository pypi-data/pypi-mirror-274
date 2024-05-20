#!/usr/bin/env python

import os
import logging
import argparse
import json
import re
from azure_key_vault_report import azure_key_vault_report
from azure_key_vault_report import az_cmd
from message_handler import message_handler
from .slack_workflow_report import slack_workflow_report
from .teams_report import teams_report
from .post_payloads import post_payloads

########################################################################################################################


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    # The list of key vaults to check passed as command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vaults", nargs='+',
                        help="List of key vaults to check. E.g. kv-dev kv-test")

    parser.add_argument("-c", "--alert_threshold", type=int,
                        help="If set then only records that are +/- this value in days till expire/expired "
                             "will be alerted. Records will be alerted as individual Slack messages. "
                             "Summary report and other reports will not be posted.")

    parser.add_argument("-e", "--expire_threshold", type=int,
                        help="If a value (int) is set. The days to the record's Expiration Date must be below "
                             "this threshold in order to be included in the report (Default: not set).")

    parser.add_argument("-a", "--include_all", action='store_true',
                        help="Include all records in output (verbose) if provided.")

    parser.add_argument("-i", "--include_no_expiration", action='store_false',
                        help="Also include records which has no Expiration Date set.")

    parser.add_argument("-T", "--title", type=str, default="Azure Key Vault report",
                        help="The title of the message posted in Slack or MS Teams")

    parser.add_argument("-r", "--record_types", nargs='+',
                        help="List of record types to check for. E.g. certificate secret\n"
                             "Valid types are: certificate secret key\n"
                             "Default is all: certificate secret key",
                        default="certificate secret key")

    parser.add_argument("-L", "--slack_split_chars", type=int, default=3500,
                        help="Slack message above this value will be split into multiple post messages.")

    parser.add_argument("-C", "--teams_max_chars", type=int, default=17367,
                        help="The max characters the report can have due to the MS Teams payload size limits")

    parser.add_argument("-S", "--stdout_only", action='store_true',
                        help="Only print report to stdout. No post to messagehandler (Slack or MS Teams")

    parser.add_argument("-w", "--workflow_output_file", type=str, default="output.json",
                        help="The file where the full json report will be written.")

    parser.add_argument("-s", "--silence", action='store_true',
                        help="If provided the workflow will run and log, but no messages to Slack or MS Teams and "
                             "no print to stdout.")

    args = parser.parse_args()
    vaults = args.vaults
    expire_threshold = args.expire_threshold
    alert_threshold = args.alert_threshold
    include_all = args.include_all
    ignore_no_expiration = args.include_no_expiration
    title = args.title
    record_types = args.record_types
    slack_split_chars = args.slack_split_chars
    teams_max_chars = args.teams_max_chars
    stdout_only = args.stdout_only
    workflow_output_file = args.workflow_output_file
    silence = args.silence

    # Each argparse argument is logged
    for k, v in sorted(vars(args).items()):
        logging.info(f"Argument '{k}': '{v}'")

    # Exit if no vaults are specified
    if not vaults:
        logging.error("No vaults specified.")
        exit(2)

    # If only one key vault to check, ensure it is treated as a list
    if isinstance(vaults, str):
        vaults = [vaults]

    # The different kind of alert outputs are initially set to False.
    # Will be updated according to value of WEBHOOK_REPORT
    # Success is also set to False and will only be True if one or more messages are posted.
    slack_app = False
    teams_output = False
    msg_handler = None
    success = False

    # Determines if a webhook is set, and if it is for a Slack App or a Slack Workflow. If not we assume for MS Teams.
    if not WEBHOOK_REPORT:
        logging.warning("'WEBHOOK_REPORT' not provided. Report will not be posted to message handler.")
    else:
        if "slack.com/services" in WEBHOOK_REPORT:
            logging.info("Slack services webhook detected.")
            slack_app = True
        elif "slack.com" not in WEBHOOK_REPORT:
            logging.info("No slack webhook detected. Assuming post to MS Teams.")
            teams_output = True

    # Runs all the az key vaults commands and add the results to the 'az_results' list
    az_results = []
    for vault in vaults:
        az_results += az_cmd.az_cmd(vault, record_types)

    # The report is generated by using the pip package ops-py-azure-key-vault-report
    # If argument 'include_no_expiration' is not provided, then the variable 'ignore_no_expiration' is then set to True
    kv_report = azure_key_vault_report.AzureKeyVaultReport(az_results)
    kv_report.parse_results()
    kv_report.add_summary()
    kv_report.add_report(expire_threshold=expire_threshold,
                         ignore_no_expiration=ignore_no_expiration,
                         include_all=include_all,
                         teams_json=teams_output,
                         alert_threshold=alert_threshold)

    # Get the full report which will be written to file, and may be used for future references (logging / monitoring).
    # The name of the Workflow and Azure resource information are added to the json object.
    report_full = kv_report.get_report_full()
    if isinstance(report_full, dict):
        workflow_output_name = str(WORKFLOW_OUTPUT_NAME).strip().lower().replace(" ", "_")[:40]
        report_full["name"] = workflow_output_name
        report_full["repository_name"] = str(GITHUB_REPOSITORY).split("/")[-1]
        report_full["client_id"] = AZURE_CLIENT_ID
        report_full["subscription_id"] = AZURE_SUBSCRIPTION_ID
        report_full["tenant_id"] = AZURE_TENANT_ID

        # Ensure a valid filename is set. If that is not the case, then 'output.json' is used as default.
        workflow_output_file = str(workflow_output_file.lower()).replace(" ", "_")
        if not bool(re.match("^[a-z0-9_-]*$", workflow_output_file)):
            workflow_output_file = "output.json"

        # Write full report as json to file
        with open(workflow_output_file, 'w') as f:
            json.dump(report_full, f)

    # If the 'silence' argument is provided, then we are done once the json output file is written
    if silence:
        return

    # If the 'stdout_only' argument is provided, the plain text markdown reports are printed to stdout, and then exit.
    # If 'teams_output', the 'stdout_only' is handled by the 'teams_alert' function instead.
    if stdout_only and not teams_output:
        report = kv_report.get_report_summary_markdown()
        print(title)
        print(report)
        return

    # Initializes the Message Handler
    if WEBHOOK_REPORT:
        msg_handler = message_handler.MessageHandler(WEBHOOK_REPORT)

    # If to alert
    if isinstance(alert_threshold, int):
        payloads = None

        # If the webhook is previously determined to be an MS Teams webhook, then get the teams alert payloads
        if teams_output:
            payloads = kv_report.get_teams_payloads(title, alert=True)

        # If the webhook is previously determined to be a Slack App webhook, then get the slack alert payloads
        if slack_app:
            payloads = kv_report.get_slack_payloads(title, max_chars=slack_split_chars, alert=True)

        # If payloads, then post the payload by calling the post_payloads function
        if payloads and msg_handler:
            success = post_payloads(msg_handler, payloads)

        # If no payloads, then just log
        if (slack_app or teams_output) and not payloads and message_handler:
            msg = "No records to alert on detected."
            logging.error(msg)

        # If alert and Slack Workflow, then log and post message about that is not supported
        if not slack_app and not teams_output and not payloads and message_handler:
            error_msg = "Posting individual critical messages to Slack Workflow is not supported."
            logging.error(error_msg)
            success = slack_workflow_report(msg_handler, posts=[(f"ERROR - {title}", error_msg)])

    # if not alert, then report
    else:
        payloads = None

        # If the webhook is previously determined to be an MS Teams webhook, the teams_report function is called
        # which also will post the report message
        if teams_output:
            success = teams_report(title, kv_report, teams_max_chars, stdout_only=stdout_only, msg_handler=msg_handler)

        # If the webhook is previously determined to be a Slack App webhook, then get the slack report payloads
        if slack_app:
            payloads = kv_report.get_slack_payloads(title, max_chars=slack_split_chars)

        # If payloads, the slack_post function is called to post the report payloads
        if payloads and msg_handler:
            success = post_payloads(msg_handler, payloads)

        # If Slack Workflow, then get the then get the slack report Workflow payloads
        if not slack_app and not teams_output and msg_handler:
            posts = kv_report.get_slack_payloads(title, max_chars=slack_split_chars, app=False)
            if posts:
                # The slack_post function is called to post the Slack Workflow reports payloads
                success = slack_workflow_report(msg_handler, posts=posts)

    # If success and 'WEBHOOK_NOTIFY' is provided
    # an additional notify will be posted to the 'WEBHOOK_NOTIFY' webhook
    if success and WEBHOOK_NOTIFY:
        logging.info(f"Trigger additional alert about new report message(s)...")
        alert = message_handler.MessageHandler(WEBHOOK_NOTIFY)
        alert.post_payload()


########################################################################################################################


if __name__ == '__main__':
    # The actual report will be posted to the webhook exported in
    # the following environment variable
    WEBHOOK_REPORT = os.getenv("WEBHOOK_REPORT")

    # When all the reports have been posted, an additional POST is performed
    # to the webhook exported in following environment variable:
    WEBHOOK_NOTIFY = os.getenv("WEBHOOK_NOTIFY")

    # The value of the name key in the full json logfile
    WORKFLOW_OUTPUT_NAME = os.getenv("WORKFLOW_OUTPUT_NAME", "")

    # The value of the github_repo name key in the full json logfile
    GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY", "")

    # These Azure environment variables will be used in the full json logfile
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")

    main()
