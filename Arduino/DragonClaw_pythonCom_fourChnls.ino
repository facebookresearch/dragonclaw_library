///////////////////////////////////////////////////////// INITIALIZE VARIABLES /////////////////////////////////////////////////////////

const int V_PRESS_IN[] = {15,18,23,6,5};
const int V_PRESS_OUT[] = {14,16,20,21,22}; 
const int NUM_CHNL = 4;
const int LED = 13; // the pin that the LED is attached to
const byte NUM_CHAR = 18;

char incomingCharCmd[NUM_CHAR];
char tempCharCmd[NUM_CHAR];

//int flag = 1;
///int check_press = 0;
///int true_percent = 0;
///int percent_desired = 0;

float pressCmd[] = {0, 0, 0, 0}; //%
float pressRead[] = {0, 0, 0, 0}; //%

boolean newData = false;

///////////////////////////////////////////////////////// MAIN /////////////////////////////////////////////////////////

void setup() {
  
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  
  // check finger movement
  for (int ii = 0; ii < NUM_CHNL; ii++){
      pinMode(V_PRESS_OUT[ii],INPUT);
      pinMode(V_PRESS_IN[ii],OUTPUT);
      analogWrite(V_PRESS_IN[ii],256);
      digitalWrite(LED, HIGH);
      delay(500);
      analogWrite(V_PRESS_IN[ii],0);
      delay(100);
//          Serial.println("check00");

  }
//      Serial.println("check0");[]][[[[[[

}

void loop() {
  
  findStartEndMarkers() ;
  
  if (newData == true){
//    Serial.println("check1");
    strcpy(tempCharCmd, incomingCharCmd); //incoming data should be sent as [int,int,int,int] for % pressure in to [finger 1, finger 2, thumb, palm]
    parseData();
    updatePressure();
    newData = false;
  }

//    printData_ASCII();

    printData();
        

}

///////////////////////////////////////////////////////// FUNCTIONS /////////////////////////////////////////////////////////

void findStartEndMarkers() {
  
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '[';
    char endMarker = ']';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                incomingCharCmd[ndx] = rc;
                ndx++;
                if (ndx >= NUM_CHAR) {
                    ndx = NUM_CHAR - 1;
                }
            }
            else {
                incomingCharCmd[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }

}

void parseData() {

  char * strtokIdx; //index for strtok() 
  strtokIdx = strtok(tempCharCmd, ",");
  pressCmd[0] = atoi(strtokIdx);
  for (int ii = 1; ii < NUM_CHNL; ii++){
    strtokIdx = strtok(NULL, ",");
    pressCmd[ii] = atoi(strtokIdx);
  }
  
}

void updatePressure() {
  
  int map_input = 0;
  
  for(int ii = 0; ii < NUM_CHNL; ii++){
    map_input = map(pressCmd[ii],0,100,0,256);
    if(map_input > 256) map_input = 256;
//    Serial.println(map_input);
    analogWrite(V_PRESS_IN[ii],map_input);
//    delay(100);
  }
  
}

void printData(){

  int map_read = 0;

  float timestamp = micros();
  Serial.write((byte*)&timestamp,4);

  Serial.write((byte*)&pressCmd,sizeof(pressCmd));

  for (int ii = 0; ii < NUM_CHNL; ii++){
    map_read = analogRead(V_PRESS_OUT[ii]);
    pressRead[ii] = map(map_read,0,1023,0,100);
  }

  Serial.write((byte*)&pressRead,sizeof(pressRead));
  Serial.println("");


}

void printData_ASCII(){

  int map_read = 0;

  float timestamp = micros();
  Serial.print(timestamp);
  Serial.print(" :  ");
  for (int ii = 0; ii < NUM_CHNL; ii++){
     Serial.print(pressCmd[ii]);
     Serial.print("  ");
  }
  Serial.print(" --> ");

  for (int ii = 0; ii < NUM_CHNL; ii++){
    map_read = analogRead(V_PRESS_OUT[ii]);
    pressRead[ii] = map(map_read,0,1023,0,100);
    Serial.print(pressRead[ii]);
    Serial.print("  ");
  }
  Serial.println("");
}























    //  prints: commanded /pressure(%) actual pressure(%)
//  Serial.print(micros());
//  Serial.print(" /");
//
//  for (int ii = 0; ii < NUM_CHNL; ii++){
////    Serial.write((byte*)pressCmd[ii],sizeof(pressCmd));
//    Serial.write("/t");
//  }


//// writes binary data
//for (int ii = 0; ii < NUM_CHNL; ii++){
//    Serial.write((byte*)pressCmd[ii], sizeof(pressCmd[ii]));
//}
//
//for (int ii = 0; ii < NUM_CHNL; ii++){
//    map_read = analogRead(V_PRESS_OUT[ii]);
//    pressRead[ii] = map(map_read,0,1023,0,100);
//    Serial.write((byte*)pressRead[ii], sizeof(pressRead[ii]));
//}
  
