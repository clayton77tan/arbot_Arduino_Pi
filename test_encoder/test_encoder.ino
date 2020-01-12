/*#include <SPI.h>

  // using two incompatible SPI devices, A and B. Incompatible means that they need different SPI_MODE
  const int slaveAPin = 12; // MISO pin

  // set up the speed, data order and data mode
  SPISettings settingsA(10000000, MSBFIRST, SPI_MODE1);

  uint8_t stat, val1;
  uint16_t result=0;

  void setup() {
  // set the Slave Select Pins as outputs:
  pinMode (slaveAPin, OUTPUT);
  // initialize SPI:
  SPI.begin();
  Serial.begin(9600);

   for(int i=0;i<10;i++){

        // read three bytes from device A
  SPI.beginTransaction(settingsA);
  digitalWrite (slaveAPin, LOW);
  // reading only, so data sent does not matter
  stat = SPI.transfer(0);
  val1 = SPI.transfer(0);

  digitalWrite (slaveAPin, HIGH);
  SPI.endTransaction();
  // if stat is 1 or 2, send val1 or val2 else zero
  if (stat == 1) {
   result = val1;
  } else {
   result = 0;
  }
  Serial.println(stat);

    }
  }


  void loop() {

  /*
  // read three bytes from device A
  SPI.beginTransaction(settingsA);
  digitalWrite (slaveAPin, LOW);
  // reading only, so data sent does not matter
  stat = SPI.transfer(0);
  val1 = SPI.transfer(0);

  digitalWrite (slaveAPin, HIGH);
  SPI.endTransaction();
  // if stat is 1 or 2, send val1 or val2 else zero
  if (stat == 1) {
   result = val1;
  } else {
   result = 0;
  }
  Serial.println(stat);
  //Serial.println(result);

  }
*/

#include <SPI.h>
#include <Servo.h>
Servo myservo;  // create servo object to control a servo
int potpin = 0;  // analog pin used to connect the potentiometer
int val;    // variable to read the value from the analog pin


unsigned int reading = 0;

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

//Op Arduino: D10 CS, D11 MOSI, D12 MISO, D13 SCK
//SPISettings settings(2000000, MSBFIRST, SPI_MODE1);
SPISettings settings(SPI_CLOCK_DIV4, MSBFIRST, SPI_MODE1);

uint8_t pos = 0;
uint16_t angle;
boolean toggle0 = 0;

void setup() {
  //pinMode(4, OUTPUT);

  /*
    cli();//stop interrupts
    //set timer0 interrupt at 2kHz
    TCCR0A = 0;// set entire TCCR2A register to 0
    TCCR0B = 0;// same for TCCR2B
    TCNT0  = 0;//initialize counter value to 0
    // set compare match register for 2khz increments
    OCR0A = 175;// = (16*10^6) / (2000*64) - 1 (must be <256)
    // turn on CTC mode
    TCCR0A |= (1 << WGM01);
    // Set CS01 and CS00 bits for 64 prescaler
    TCCR0B |= (1 << CS01) | (1 << CS00);
    // enable timer compare interrupt
    TIMSK0 |= (1 << OCIE0A);
    sei();//allow interrupts
  */

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
}
/*
  ISR(TIMER0_COMPA_vect){//timer0 interrupt 2kHz toggles pin 8
  //generates pulse wave of frequency 2kHz/2 = 1kHz (takes two cycles for full wave- toggle high then toggle low)
  if (toggle0){
    digitalWrite(4,HIGH);
    toggle0 = 0;
  }
  else{
    digitalWrite(4,LOW);
    toggle0 = 1;
  }
//myservo.write(0);
//Serial.println("here");
//angle=AS5047P_Read( AS5047P_select_pin, ANGLECOM) & 0x3FFF;
//angle=map(angle,1745, 9545, 0,180);
//Serial.println(angle);
}*/



uint8_t decrement = 0;
void loop()
{
  myservo.write(pos);
  delay(10);
  angle = AS5047P_Read( AS5047P_select_pin, ANGLECOM) & 0x3FFF;
  angle = map(angle, 1745, 9545, 0, 180);
  Serial.print("pos: "); Serial.print(pos);
  Serial.print("   angle: "); Serial.println(angle);

  if (decrement) {
    if (pos == 0) {
      decrement = 0;
    } else {
      pos--;
    }
  }
  if(decrement == 0){
    if(pos == 125){
      decrement = 1;
      pos--;
    }else{
      pos++;
    }
  }

  /*
    angle=AS5047P_Read( AS5047P_select_pin, ANGLECOM) & 0x3FFF;
    angle=map(angle,1745, 9545, 0,180);
  */
  //Serial.println(angle);
  //delay(2000);
    //myservo.write(120);
    /*
      angle=AS5047P_Read( AS5047P_select_pin, ANGLECOM) & 0x3FFF;
      angle=map(angle,1745, 9545, 0,180);
    */
    //Serial.println(angle);
    //delay(2000);
  }

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
