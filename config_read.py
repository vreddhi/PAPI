import configparser
import json


config = configparser.ConfigParser()
config.read('property_config.txt', encoding=None)
ENV = "stage"

rule_names = config['RULE_ORDER']['Order'].split(',')

for ruleName in rule_names:
    ruleName = str(ruleName).strip()
    name = config[ruleName]['name']
    child_rule = config[ruleName]['child_rule']
    criteria_details = config[ruleName]['criteria_details']
    criteria_names = config[ruleName]['criteria_names']
