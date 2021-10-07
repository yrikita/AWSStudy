import boto3
import time
import sys

client = boto3.client('lexv2-models')

CONV_YOMI1 =  {"1": "いん", "2" : "に", "3": "さん", "4": "し", "5": "ご", "6":"ろく","7": "しち", "8":"はち","9":"く"}
CONV_YOMI2 =  {"1": "いち", "2" : "に", "3": "さん", "4": "し", "5": "ご", "6":"ろく","7": "しち", "8":"はち","9":"く"}
CONV_HIRAGANA =  {"1": "いち", "2" : "に", "3": "さん", "4": "よん", "5": "ご", "6":"ろく","7": "しち", "8":"はち","9":"きゅう"}
CONV_KANJI =  {"1": "一", "2" : "二", "3": "三", "4": "四", "5": "五", "6":"六","7": "七", "8":"八","9":"九"}

BOT_ID = "BX9VI6CHL1"
BOT_VERSION = "DRAFT"
BOT_LOCALE = "ja_JP"

def main():

    createLocale()

    checkLocale()

    print('Intentを作成します')
    for i in range(1,10):
        intentId = createIntent(str(i))

        slotPriorities = []
        for j in range(1,10):
            slotId = createSlot(intentId, str(i), str(j))
            slotPriorities.append(dict(priority=j, slotId=slotId))
        
        updateIntent(intentId, str(i), slotPriorities)


    print('botを構築します')
    response = client.build_bot_locale(
        botId=BOT_ID,
        botVersion=BOT_VERSION,
        localeId=BOT_LOCALE
    )
    print(response)
    checkLocale()

def createLocale():
    print('Localeを作成します')
    response = client.create_bot_locale(
        botId=BOT_ID,
        botVersion=BOT_VERSION,
        localeId=BOT_LOCALE,
        nluIntentConfidenceThreshold=0.8,
        voiceSettings={
            'voiceId': 'Takumi'
        }
    )
    print(response)

def checkLocale():
    for i in range(10):
        response = client.describe_bot_locale(
            botId=BOT_ID,
            botVersion=BOT_VERSION,
            localeId=BOT_LOCALE,
        )
        print(response['botLocaleStatus'])

        if response['botLocaleStatus'] == 'Creating':
            time.sleep(5)
            continue
        elif response['botLocaleStatus'] == 'Building':
            time.sleep(5)
            continue
        elif response['botLocaleStatus'] == 'Built':
            break
        elif response['botLocaleStatus'] == 'NotBuilt':
            break
        elif response['botLocaleStatus'] == 'Failed':
            print('Error: botLocaleStatus failed', file=sys.stderr)
            sys.exit(1)
        else:
            print('Error:' + response['botLocaleStatus'] , file=sys.stderr)
            sys.exit(1)


def createIntent(intentName):
    print(intentName+"の段作成中")
    response = client.create_intent(
        botId=BOT_ID,
        botVersion=BOT_VERSION,
        localeId=BOT_LOCALE,
        intentName=intentName
    )

    return response["intentId"]
    

def createSlot(intentId, slot1, slot2):
    response = client.create_slot(
        botId=BOT_ID,
        botVersion=BOT_VERSION,
        localeId=BOT_LOCALE,
        intentId=intentId,
        slotName= slot1 + slot2,
        slotTypeId='AMAZON.Number',
        valueElicitationSetting={
            'slotConstraint': 'Required',
            'promptSpecification': {
                'messageGroups': [
                    {
                        'message': {
                            'plainTextMessage': {
                                'value': CONV_YOMI1[slot1] + CONV_YOMI2[slot2] + 'が？'
                            }
                        }
                    }
                ],
                'maxRetries': 4,
                'allowInterrupt': True
            }
        }
    )
    return response['slotId']

def updateIntent(intentId, intentName, slotPriorities):

    response = client.update_intent(
        botId=BOT_ID,
        botVersion=BOT_VERSION,
        localeId=BOT_LOCALE,
        intentId=intentId,
        intentName=intentName,
        description=CONV_KANJI[intentName] + 'の段の練習',
        sampleUtterances=[
            {
                'utterance': CONV_KANJI[intentName] + 'の段'
            },
            {
                'utterance': CONV_HIRAGANA[intentName] + 'のだん'
            },
            {
                'utterance': CONV_HIRAGANA[intentName]
            },
            {
                'utterance': intentName
            },
        ],
        dialogCodeHook={
            'enabled': False
        },
        fulfillmentCodeHook={
            'enabled': True
        },
        intentClosingSetting={
            'closingResponse': {
                'messageGroups': [
                    {
                        'message': {
                            'plainTextMessage': {
                                'value': 'おわり'
                            },
                        },
                    },
                ],
                'allowInterrupt': True
            },
            'active': True
        },
        slotPriorities=slotPriorities
    )
    print("updateIntent")
    print(response)


if __name__ == "__main__":
    main()