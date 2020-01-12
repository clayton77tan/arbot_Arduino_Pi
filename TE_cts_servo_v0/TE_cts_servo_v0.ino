#include <SPI.h>
#include <Servo.h>

// AS4047P Registers
#define AS5047P_select_pin 10

/** volatile **/
#define NOP 0x0000
#define ERRFL 0x0001
#define PROG   0x0003
#define DIAAGC 0x3FFC
#define CORDICMAG 0x3FFD
#define ANGLEUNC  0x3FFE
#define ANGLECOM  0x3FFF

/** non-volatile **/
#define ZPOSM 0x0016
#define ZPOSL 0x0017
#define SETTINGS1 0x0018
#define SETTINGS2 0x0019

#define RD  0x40    // bit 14 "1" is Read + parity even
#define WR  0x3F    //bit 14 ="0" is Write

// From matlab
#define MIN 7
#define MAX 16381
#define STOP 91

//Op Arduino: D10 CS, D11 MOSI, D12 MISO, D13 SCK
//SPISettings settings(2000000, MSBFIRST, SPI_MODE1);
SPISettings settings(SPI_CLOCK_DIV4, MSBFIRST, SPI_MODE1);

/********************************************************************************
   GLOBAL VARIABLES
********************************************************************************/
Servo myservo;  // create servo object to control a servo
uint8_t pos = 0;
uint16_t angle = 450;
uint8_t decrement = 0;
uint8_t target = 150;
/********************************************************************************
   SETUP
********************************************************************************/
void setup() {

  pinMode(AS5047P_select_pin, OUTPUT);

  SPI.begin();
  SPI.setDataMode(SPI_MODE1); // properties chip
  SPI.setBitOrder(MSBFIRST);  //properties chip

  Serial.begin(115200);  // start serial for output
  Serial.println(" AS5047P:");

  AS5047P_Write( AS5047P_select_pin , SETTINGS1, 0x0001); //DJL was 0x0004);
  AS5047P_Write( AS5047P_select_pin , SETTINGS2, 0x0000);
  AS5047P_Write( AS5047P_select_pin , ZPOSM, 0x0000); // is it really possible to initially set angle at 0 degrees??
  AS5047P_Write( AS5047P_select_pin , ZPOSL, 0x0000);

  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo.write(0);

  /*
    calibration sequence: got to zero degreees
  */

  while (angle != 0) {
    angle = AS5047P_Read( AS5047P_select_pin, ANGLECOM) & 0x3FFF;
    angle = map(angle, MIN, MAX, 0, 360); // map to degreees
    myservo.write(97);
    Serial.println(angle);
  }
  myservo.detach();
  Serial.println("At zero degrees");
  delay(3000);
  myservo.attach(9);
}
/********************************************************************************
   LOOP
********************************************************************************/
void loop()
{
  angle = AS5047P_Read( AS5047P_select_pin, ANGLECOM) & 0x3FFF;
  angle = map(angle, MIN, MAX, 0, 360); // map to degreees
  Serial.print(angle);
  if (angle != target) {
    
    Serial.println("    searching");
    myservo.write(85);
  } else if(angle == target) {

    //while (angle == ()) {
      //myservo.write(180);
      //delay(10);
      myservo.write(STOP);
      myservo.detach();
      angle = AS5047P_Read( AS5047P_select_pin, ANGLECOM) & 0x3FFF;
      angle = map(angle, MIN, MAX, 0, 360); // map to degreees
      Serial.print(angle);
      Serial.println("found it");
      //delay(5000);
      while(1);
    }
    else ;
  
  //myservo.write(92);
  /*
    myservo.write(85); // speed of servo rotation
    angle = AS5047P_Read( AS5047P_select_pin, ANGLECOM) & 0x3FFF;
    //angle=map(angle, 0, 16383, 0, 1023); // map to ten bit
    angle = map(angle, MIN, MAX, 0, 360); // map to degreees
    //Serial.print("pos: "); Serial.print(pos);
    //Serial.print("   angle: ");
    Serial.println(angle);
    //delay(1000);
  */
}

/********************************************************************************
   ENCODER FUNCTIONS (THANK YOU DOUGH)
********************************************************************************/
void DumpRegisterValues()
{
  Serial.print("NOP: "); Serial.println(AS5047P_Read( AS5047P_select_pin, NOP) & 0x3FFF, BIN); // strip bit 14..15
  Serial.print("ERRFL: "); Serial.println(AS5047P_Read( AS5047P_select_pin, ERRFL) & 0x3FFF, BIN); // strip bit 14..15
  Serial.print("PROG: "); Serial.println(AS5047P_Read( AS5047P_select_pin, PROG) & 0x3FFF, BIN); // strip bit 14..15
  Serial.print("DIAAGC: "); Serial.println(AS5047P_Read( AS5047P_select_pin, DIAAGC) & 0x3FFF, BIN); // strip bit 14..15

  Serial.print("CORDICMAG: "); Serial.println(AS5047P_Read( AS5047P_select_pin, CORDICMAG) & 0x3FFF, DEC); // strip bit 14..15
  Serial.print("ANGLEUNC: "); Serial.println(AS5047P_Read( AS5047P_select_pin, ANGLEUNC) & 0x3FFF, DEC); // strip bit 14..15
  Serial.print("ANGLECOM: "); Serial.println(AS5047P_Read( AS5047P_select_pin, ANGLECOM) & 0x3FFF, DEC); // strip bit 14..15

  Serial.print("ZPOSM: "); Serial.println(AS5047P_Read( AS5047P_select_pin, ZPOSM) & 0x3FFF, BIN); // strip bit 14..15
  Serial.print("ZPOSL: "); Serial.println(AS5047P_Read( AS5047P_select_pin, ZPOSL) & 0x3FFF, BIN); // strip bit 14..15
  Serial.print("SETTINGS1: "); Serial.println(AS5047P_Read( AS5047P_select_pin, SETTINGS1) & 0x3FFF, BIN); // strip bit 14..15
  Serial.print("SETTINGS2: "); Serial.println(AS5047P_Read( AS5047P_select_pin, SETTINGS2) & 0x3FFF, BIN); // strip bit 14..15
}

// ************************Write to AS5047P **************************
void AS5047P_Write( int SSPin, int address, int value)
{
  // take the SS pin low to select the chip:
  SPI.beginTransaction(settings);
  digitalWrite(SSPin, LOW);

  Serial.println(value, HEX);

  //  send in the address via SPI:

  byte v_l = address & 0x00FF;
  byte v_h = (unsigned int)(address & 0x3F00) >> 8;

  if (parity(address & 0x3F) == 1) v_h = v_h | 0x80; // set parity bit
  //v_h = v_h & (WR | 0x80);  // its  a write command and don't change the parity bit (0x80)

  Serial.print( " parity:  "); Serial.println(parity(address & 0x3F));
  Serial.print(v_h, HEX); Serial.print(" A ");  Serial.println(v_l, HEX);

  SPI.transfer(v_h);
  SPI.transfer(v_l);

  digitalWrite(SSPin, HIGH);
  SPI.endTransaction();

  delay(2);

  SPI.beginTransaction(settings);
  digitalWrite(SSPin, LOW);

  //  send value via SPI:

  v_l = value & 0x00FF;
  v_h = (unsigned int)(value & 0x3F00) >> 8;

  if (parity(value & 0x3F) == 1) v_h = v_h | 0x80; // set parity bit
  //v_h = v_h & (WR | 0x80); // its a write command and don't change the parity bit (0x80)

  Serial.print(v_h, HEX); Serial.print(" D ");  Serial.println(v_l, HEX);

  SPI.transfer(v_h);
  SPI.transfer(v_l);

  // take the SS pin high to de-select the chip:
  digitalWrite(SSPin, HIGH);
  SPI.endTransaction();
}

//*******************Read from AS5047P ********************************
unsigned int AS5047P_Read( int SSPin, unsigned int address)
{
  unsigned int result = 0;   // result to return

  byte res_h = 0;
  byte res_l = 0;

  // take the SS pin low to select the chip:
  SPI.beginTransaction(settings);
  digitalWrite(SSPin, LOW);

  //  send in the address and value via SPI:
  byte v_l = address & 0x00FF;
  byte v_h = (unsigned int)(address & 0x3F00) >> 8;

  if (parity(address | (RD << 8)) == 1) v_h = v_h | 0x80; // set parity bit

  v_h = v_h | RD; // its  a read command

  // Serial.print( " parity:  ");Serial.println(parity(address | (RD <<8)));
  // Serial.print(v_h, HEX); Serial.print(" A ");  Serial.print(v_l, HEX);  Serial.print(" >> ");

  res_h = SPI.transfer(v_h);
  res_l = SPI.transfer(v_l);

  digitalWrite(SSPin, HIGH);
  SPI.endTransaction();

  delay(2);

  SPI.beginTransaction(settings);
  digitalWrite(SSPin, LOW);

  //if (parity(0x00 | (RD <<8))==1) res_h = res_h | 0x80;  // set parity bit
  //res_h = res_h | RD;

  res_h = (SPI.transfer(0x00));
  res_l = SPI.transfer(0x00);

  res_h = res_h & 0x3F;  // filter bits outside data

  //Serial.print(res_h, HEX);   Serial.print(" R  ");  Serial.print(res_l, HEX);   Serial.print("  ");

  digitalWrite(SSPin, HIGH);
  SPI.endTransaction();

  return (result = (res_h << 8) | res_l);
}

//*******************check parity ******************************************
int parity(unsigned int x) {
  int parity = 0;
  while (x > 0) {
    parity = (parity + (x & 1)) % 2;
    x >>= 1;
  }
  return (parity);
}
