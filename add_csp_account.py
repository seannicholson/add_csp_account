##############################################################################
# Halo API Add CSP Account
# Author: Sean Nicholson
# Version 1.0.0
# Date 07.11.2018
# v 1.0.0 - initial release
##############################################################################


import cloudpassage, csv, uuid, yaml



def create_api_session(session):
    config_file_loc = "cloudpassage.yml"
    config_info = cloudpassage.ApiKeyManager(config_file=config_file_loc)
    session = cloudpassage.HaloSession(config_info.key_id, config_info.secret_key)
    return session



def read_accounts_csv(csvFile):
    with open(csvFile, 'rb') as f:
        reader = csv.DictReader(f)
        cspAccounts = list(reader)
    return cspAccounts

def add_csp_accounts(session, csvFile):
    cspAccounts = read_accounts_csv(csvFile)
    with open('cloudpassage.yml') as config_settings:
        script_options_info = yaml.load(config_settings)
        home_group = script_options_info['defaults']['home_group_id']
        roleArn = script_options_info['defaults']['role_arn']
        externalId = str(script_options_info['defaults']['externalId'])
    AddCspAccount = cloudpassage.HttpHelper(session)
    for account in cspAccounts:
        if account['account_name']:
            payload = {"external_id": str(externalId), "role_arn": str(roleArn), "sns_arn": account['sns_arn'], "group_id": home_group, "csp_account_type": account['account_type'],"account_display_name": account['account_name']}
        else:
            payload = {"external_id": str(externalId), "role_arn": str(roleArn), "sns_arn": account['sns_arn'], "group_id": home_group, "csp_account_type": account['account_type']}

        #print payload
        AddCspAccount.post("/v1/csp_accounts", payload)
        print "Added CSP Account {0} to Halo Cloud Secure\n".format(account['account_id'])



if __name__ == "__main__":
    with open('cloudpassage.yml') as config_settings:
        script_options_info = yaml.load(config_settings)
        aws_account_csv = script_options_info['defaults']['aws_account_csv']
    api_session = None
    api_session = create_api_session(api_session)
    add_csp_accounts(api_session, aws_account_csv)
