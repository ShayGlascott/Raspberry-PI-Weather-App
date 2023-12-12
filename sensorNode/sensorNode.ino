#include <Wire.h>
#include <SparkFunBME280.h>
#include <SparkFunCCS811.h>

#define CCS811_ADDR 0x5B
#define LIGHTSENSORPIN A0
#define STATUSLEDPIN 2

CCS811 myCCS811(CCS811_ADDR);
BME280 myBME280;

bool isConnected = false;
unsigned long millisWhenConnected;
unsigned long utcWhenConnected;

void setup()
{
  Wire.begin();
  Serial.begin(9600);

  pinMode(LIGHTSENSORPIN, INPUT);
  pinMode(STATUSLEDPIN, OUTPUT);

  CCS811Core::CCS811Core::CCS811_Status_e returnCode = myCCS811.beginWithStatus();
  if (returnCode != CCS811Core::CCS811_Stat_SUCCESS)
  {
    Serial.println("Problem with CCS811");
    printDriverError(returnCode);
  }/*
  else
  {
    Serial.println("CCS811 online");
  }*/

  myBME280.settings.commInterface = I2C_MODE;
  myBME280.settings.I2CAddress = 0x77;
  myBME280.settings.runMode = 3;
  myBME280.settings.tStandby = 0;
  myBME280.settings.filter = 4;
  myBME280.settings.tempOverSample = 5;
  myBME280.settings.pressOverSample = 5;
  myBME280.settings.humidOverSample = 5;

  delay(10);
  byte id = myBME280.begin();
  if (id != 0x60)
  {
    Serial.println("Problem with BME280");
  }/*
  else
  {
    Serial.println("BME280 online");
  }*/
}

float readLightSensor()
{
  return analogRead(LIGHTSENSORPIN) * 0.9765625;
}

void printData()
{
  Serial.print("(");
  Serial.print(getTime());
  Serial.print(",");
  Serial.print(myCCS811.getCO2());
  Serial.print(",");
  Serial.print(myCCS811.getTVOC());
  Serial.print(",");
  Serial.print(myBME280.readTempF(), 1);
  Serial.print(",");
  Serial.print(myBME280.readFloatPressure(), 2);
  Serial.print(",");
  Serial.print(myBME280.readFloatHumidity(), 0);
  Serial.print(",");
  Serial.print(readLightSensor());
  Serial.println(")");
}

void printDriverError(CCS811Core::CCS811_Status_e errorCode)
{
  switch (errorCode)
  {
  case CCS811Core::CCS811_Stat_SUCCESS:
    Serial.print("SUCCESS");
    break;
  case CCS811Core::CCS811_Stat_ID_ERROR:
    Serial.print("ID_ERROR");
    break;
  case CCS811Core::CCS811_Stat_I2C_ERROR:
    Serial.print("I2C_ERROR");
    break;
  case CCS811Core::CCS811_Stat_INTERNAL_ERROR:
    Serial.print("INTERNAL_ERROR");
    break;
  case CCS811Core::CCS811_Stat_NUM:
    Serial.print("NUMBER_ERROR");
    break;
  case CCS811Core::CCS811_Stat_GENERIC_ERROR:
    Serial.print("GENERIC_ERROR");
    break;
  default:
    Serial.print("Unspecified error.");
  }
}

unsigned long getTime()
{
  unsigned long elapsedTime = (millis() - millisWhenConnected) / 1000;
  return utcWhenConnected + elapsedTime;
}

void loop()
{
  if (!isConnected)
  {
    digitalWrite(STATUSLEDPIN, LOW);
    if (Serial.available())
    {
      String command = Serial.readStringUntil('\n');
      utcWhenConnected = command.toInt();
      millisWhenConnected = millis();
      isConnected = true;
    }
  }
  else
  {
    digitalWrite(STATUSLEDPIN, HIGH);
    if (myCCS811.dataAvailable())
    {
      myCCS811.readAlgorithmResults();
      printData();
    }
    else if (myCCS811.checkForStatusError())
    {
      Serial.println(myCCS811.getErrorRegister());
    }
    delay(2000);
  }
}
