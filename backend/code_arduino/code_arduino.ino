#define pin 11
//const unsigned int MAX_MESSAGE_LENGTH = 12;
String data;
int value;
int power;

void setup() {
 Serial.begin(9600);
 pinMode(pin, OUTPUT);
 digitalWrite(pin, LOW);
}

void loop() {
  
  if (Serial.available()>0) {
    data = Serial.readStringUntil('\n');
    value = data.toInt();
    
    if(value == 0){
      digitalWrite(pin, LOW);
      Serial.println(" Heater off");
    }
      
    if (value == 1){
      digitalWrite(pin, HIGH);
      Serial.print(value);
      Serial.println(" Heater off");
    }
      
    else{
      analogWrite(pin, value);
      power = map(value, 0, 255, 0, 100);
      Serial.print(power);
      Serial. println("% Heater power");
    }
      
  }
  /*
 //Check to see if anything is available in the serial receive buffer
 while (Serial.available() > 0)
 {
   //Create a place to hold the incoming message
   static char message[MAX_MESSAGE_LENGTH];
   static unsigned int message_pos = 0;

   //Read the next available byte in the serial receive buffer
   char inByte = Serial.read();

   //Message coming in (check not terminating character) and guard for over message size
   if ( inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) )
   {
     //Add the incoming byte to our message
     message[message_pos] = inByte;
     message_pos++;
   }
   //Full message received...
   else
  {
   //Add null character to string
   message[message_pos] = '\0';
  
   //Print the message (or do other things)
   //Serial.println(message);
   //Or convert to integer and print
   int number = atoi(message);
   Serial.println(number);
   if(number == 0)
    digitalWrite(pin, LOW);
   if (number == 1)
    digitalWrite(pin, HIGH);
   else
    analogWrite(pin, number);
  
   //Reset for the next message
   message_pos = 0;
  }
 }
 */
}
