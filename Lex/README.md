# Lex

## ボット作成

```Bash
aws lexv2-models create-bot `--bot-name yrikita-lex-kakezan `
--description '掛け算九九の練習' `
--role-arn arn:aws:iam::706357943586:role/service-role/lex_kakezan-role-n39aaojq `
--data-privacy childDirected=true `
--idle-session-ttl-in-seconds 300
```

## 言語を追加

```Bash
aws lexv2-models create-bot-locale `
--bot-id BX9VI6CHL1 `
--bot-version DRAFT `
--locale-id ja_JP `
--nlu-intent-confidence-threshold 0.8 `
--voice-settings voiceId=Takumi

```

## インテント作成

```Bash
aws lexv2-models create-intent --bot-id BX9VI6CHL1 --bot-version DRAFT --locale-id ja_JP `
--intent-name 1 `
--description '一の段の練習' `
--sample-utterances utterance=1の段 utterance=いちのだん utterance=1 utterance=いち

```

## スロット作成

```Bash
aws lexv2-models create-slot --bot-id BX9VI6CHL1 --bot-version DRAFT --locale-id ja_JP --intent-id APMFP7KW19 `
--slot-name 11 `
--slot-type-id AMAZON.Number `
--value-elicitation-setting file://C:\Users\yrikita\Documents\Study\aws\AWSStudy\Lex\slot.json

```
