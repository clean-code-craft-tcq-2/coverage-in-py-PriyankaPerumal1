coolingLimit = {
  'PASSIVE_COOLING'     : {
    'lowerLimit'  : 0,
    'upperLimit'  : 35
    },
  'HI_ACTIVE_COOLING'   : {
    'lowerLimit'  : 0,
    'upperLimit'  : 45
    },
  'MED_ACTIVE_COOLING'  : {
    'lowerLimit'  : 0,
    'upperLimit'  : 40}
}

alertMessages = {
  'TOO_LOW'   : 'too low',
  'TOO_HIGH'  : 'too high',
  'NORMAL'  : ''
}

def infer_breach(value, lowerLimit, upperLimit):
  if value < lowerLimit:
    return 'TOO_LOW'
  if value > upperLimit:
    return 'TOO_HIGH'
  return 'NORMAL'

def classify_temperature_breach(coolingType, temperatureInC):
  if coolingType in coolingLimit:
    lowerLimit = coolingLimit[coolingType]['lowerLimit']
    upperLimit = coolingLimit[coolingType]['upperLimit']
  else:
    print('no such cooling type')
    return 'no such cooling type'
  
  return infer_breach(temperatureInC, lowerLimit, upperLimit)

def send_to_controller(breachType):
  controllerMsg = ''
  if alertMessages[breachType] is not '':
    header = 0xfeed
    controllerMsg = f'{header}, {breachType}'
    print(controllerMsg)
  return controllerMsg

def send_to_email(breachType):
  emailMsg = ''
  if alertMessages[breachType] is not '':
    recepientsList = ['a.b@c.com','c.a@b.com']
    recepients = ', '.join(recepientsList)
    emailMsg = f'To: {recepients}\nHi, the temperature is '+ alertMessages[breachType]
    print(emailMsg)
  return emailMsg

alertTargets = {
  'TO_CONTROLLER' : send_to_controller,
  'TO_EMAIL' : send_to_email
}

def check_and_alert(alertTarget, batteryChar, temperatureInC):
  breachType =\
    classify_temperature_breach(batteryChar['coolingType'], temperatureInC)
  if alertTarget in alertTargets:
    return alertTargets[alertTarget](breachType)
  else:
    print('no such alert target available')
    return 'no such alert target available'
