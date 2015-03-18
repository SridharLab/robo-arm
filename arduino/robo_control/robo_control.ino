// Demo Code for SerialCommand Library
// Craig Versek, Jan 2014
// based on code from Steven Cogswell, May 2011

#include <SerialCommand.h>
#include <ax12.h>
enum SERVOS {ZERO, YAW, SHOULDER_1, SHOULDER_2, ARM_1, ARM_2, WRIST};


#define arduinoLED 0   // Arduino LED on board
#define SERVO_BAUDRATE 1000000
#define TORQUE_DEFAULT 0

SerialCommand sCmd(Serial);         // The demo SerialCommand object, initialize with any Stream object

void setup() {
    //SetPosition(2,562);
    //SetPosition(3,472);
    Serial.begin(115200);
    //delay(1000);
    
    initialize();
    //`SetPosition(6,512);
    pinMode(arduinoLED, OUTPUT);      // Configure the onboard LED for output
    digitalWrite(arduinoLED, LOW);    // default to LED off
  // Setup callbacks for SerialCommand commands
  sCmd.addCommand("TE",    TORQUE_enable);     // Turns on
  sCmd.addCommand("OFF",   LED_off);         // Turns LED off
  sCmd.addCommand("HELLO", sayHello);        // Echos the string argument back
  sCmd.addCommand("P",     processCommand);  // Converts two arguments to integers and echos them back
  sCmd.addCommand("GP",    GET_POS);
  sCmd.addCommand("SP",    SET_POS);
  sCmd.setDefaultHandler(unrecognized);      // Handler for command that isn't matched  (says "What?")
  Serial.println("Ready");
}

void loop() {
  sCmd.readSerial();     // We don't do much, just process serial commands
}

void initialize() {
    //ax12SetRegister(WRIST,AX_BAUD_RATE,1000000);
    //ax12Init(SERVO_BAUDRATE);
/*    for (int i =0; i <=5; i++) {*/
/*        set_servos(i);*/
/*    }*/
}
    

    
    
/*    ax12SetRegister(YAW, AX_TORQUE_ENABLE, TORQUE_DEFAULT);*/
/*    ax12SetRegister(SHOULDER_1, AX_TORQUE_ENABLE, TORQUE_DEFAULT);*/
/*    ax12SetRegister(SHOULDER_2, AX_TORQUE_ENABLE, TORQUE_DEFAULT);*/
/*    ax12SetRegister(ARM_1, AX_TORQUE_ENABLE, TORQUE_DEFAULT);*/
/*    ax12SetRegister(ARM_1, AX_TORQUE_ENABLE, TORQUE_DEFAULT);*/
/*    ax12SetRegister(ARM, AX_RETURN_DELAY_TIME,250);*/
/*    ax12SetRegister(Shoulder, AX_RETURN_DELAY_TIME,250);*/
/*    ax12SetRegister(ROLL, AX_RETURN_DELAY_TIME,250);*/
/*    ax12SetRegister(arm2, AX_RETURN_DELAY_TIME,250);*/
/*}*/


void set_servos (int id) {
    setTX(id);
    int checksum = ~((id + 8 +AX_WRITE_DATA + AX_RETURN_DELAY_TIME+ (250&0xff) + (1&0xff) +((1&0xff)>>8) + (1023&0xff) + ((1023&0xff00)>>8))%256);
    ax12writeB(0xFF);
    ax12writeB(0xFF);
    ax12writeB(id);
    ax12writeB(8);
    ax12writeB(AX_WRITE_DATA);
    ax12writeB(AX_RETURN_DELAY_TIME);
    ax12writeB(250&0xff);
    ax12writeB(1&0xff);
    ax12writeB((1&0xff)>>8);
    ax12writeB(1023&0xff);
    ax12writeB((1023&0xff)>>8);
    ax12writeB(checksum);
    setRX(id);
}

void TORQUE_enable(SerialCommand this_scmd) {
  char *arg;
  int servo;
  arg = this_scmd.next();
  servo = atoi(arg);
  digitalWrite(arduinoLED, HIGH);
  this_scmd.println(ax12GetRegister(servo, AX_RETURN_DELAY_TIME,1));
}

void GET_POS(SerialCommand this_scmd) {
  digitalWrite(arduinoLED,LOW);
  char *arg;
  int servo, servo_pos;
  arg= this_scmd.next();
  servo = atoi(arg);
  this_scmd.print(arg);
  this_scmd.print(" ");
  servo_pos = read_pos(servo);
  //position_1 this_scmd.next();
  this_scmd.println(servo_pos);
  
}
int read_pos (int servo) {
    return GetPosition(servo);
}

void SET_POS(SerialCommand this_scmd) {
  SetPosition(3,600);
  digitalWrite(arduinoLED,HIGH);
  char *arg;
  int servo,servo_pos, position_1;
  arg = this_scmd.next();
  servo=atoi(arg);
  //this_scmd.print(servo);
  arg = this_scmd.next();
  servo_pos = atoi(arg);
  position_1= int(servo_pos);
  //this_scmd.print(" ");
  this_scmd.println(position_1);
  //delayMicroseconds(5);
  //ax12SetRegister2(servo,AX_WRITE_DATA, position_1);
  move_servo(servo, servo_pos);
  delayMicroseconds(5);
}

void move_servo(int servo, int pos){
    SetPosition(servo,pos);
}



void LED_off(SerialCommand this_scmd) {
  this_scmd.println("LED off");
  digitalWrite(arduinoLED, LOW);
}

void sayHello(SerialCommand this_scmd) {
  char *arg;
  arg = this_scmd.next();    // Get the next argument from the SerialCommand object buffer
  if (arg != NULL) {    // As long as it existed, take it
    this_scmd.print("Hello ");
    this_scmd.println(arg);
  }
  else {
    this_scmd.println("Hello, whoever you are");
  }
}


void processCommand(SerialCommand this_scmd) {
  int aNumber;
  char *arg;

  this_scmd.println("We're in processCommand");
  arg = this_scmd.next();
  if (arg != NULL) {
    aNumber = atoi(arg);    // Converts a char string to an integer
    this_scmd.print("First argument was: ");
    this_scmd.println(aNumber);
  }
  else {
    this_scmd.println("No arguments");
  }

  arg = this_scmd.next();
  if (arg != NULL) {
    aNumber = atol(arg);
    this_scmd.print("Second argument was: ");
    this_scmd.println(aNumber);
  }
  else {
    this_scmd.println("No second argument");
  }
}

// This gets set as the default handler, and gets called when no other command matches.
void unrecognized(const char *command, SerialCommand this_scmd) {
  this_scmd.print("Did not recognize \"");
  this_scmd.print(command);
  this_scmd.println("\" as a command.");
}
