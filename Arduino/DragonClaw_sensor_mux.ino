#include <Wire.h>
#include <MLX90393.h> //From https://github.com/tedyapo/arduino-MLX90393 by Theodore Yapo
#include <SparkFun_I2C_Mux_Arduino_Library.h> //Click here to get the library: http://librarymanager/All#SparkFun_I2C_Mux

QWIICMUX myMux;

MLX90393 mlx0;
MLX90393 mlx1;
MLX90393 mlx2;
MLX90393 mlx3;
MLX90393 mlx4;

//TODO change to pointers
MLX90393::txyz data0 = {0,0,0,0}; //Create a structure, called data, of four floats (t, x, y, and z)
MLX90393::txyz data1 = {0,0,0,0};
MLX90393::txyz data2 = {0,0,0,0};
MLX90393::txyz data3 = {0,0,0,0};
MLX90393::txyz data4 = {0,0,0,0};
MLX90393::txyz data5 = {0,0,0,0};
MLX90393::txyz data6 = {0,0,0,0};

MLX90393::txyz* data[7] = {&data0, &data1, &data2, &data3, &data4, &data5, &data6};

uint8_t mlx0_i2c = 0x10;
uint8_t mlx1_i2c = 0x11;
uint8_t mlx2_i2c = 0x0C;
uint8_t mlx3_i2c = 0x0D;
uint8_t mlx4_i2c = 0x0E;

byte status;

void setup()
{
  Serial.begin(250000);
  while (!Serial) {
    delay(5);
  }
  Wire.begin();
  Wire.setClock(400000);
  delay(50);

  if (myMux.begin() == false)
  {
    Serial.println("Mux not detected. Freezing...");
    while (1);
  }
  Serial.println("Mux detected");

  //setup first finger
  myMux.setPort(0);
  status = mlx0.begin(mlx0_i2c, -1, Wire);
  Serial.print("Start status: 0x");
  if(status < 0x10) Serial.print("0"); //Pretty output
  Serial.println(status, BIN);
  
  status = mlx1.begin(mlx1_i2c, -1, Wire);
  Serial.print("Start status: 0x");
  if(status < 0x10) Serial.print("0"); 
  Serial.println(status, BIN);
  //gain and digital filtering set up in the begin() function. 
  mlx0.startBurst(0xF);
  mlx1.startBurst(0xF);

  //setup second finger
  myMux.setPort(1);
  status = mlx0.begin(mlx0_i2c, -1, Wire);
  Serial.print("Start status: 0x");
  if(status < 0x10) Serial.print("0"); //Pretty output
  Serial.println(status, BIN);
  
  status = mlx1.begin(mlx1_i2c, -1, Wire);
  Serial.print("Start status: 0x");
  if(status < 0x10) Serial.print("0"); 
  Serial.println(status, BIN);  
  //gain and digital filtering set up in the begin() function. 
  mlx0.startBurst(0xF);
  mlx1.startBurst(0xF);
  
  //setup thumb
  myMux.setPort(2);
  status = mlx2.begin(mlx2_i2c, -1, Wire);
  Serial.print("Start status: 0x");
  if(status < 0x10) Serial.print("0"); //Pretty output
  Serial.println(status, BIN);
  
  status = mlx3.begin(mlx3_i2c, -1, Wire);
  Serial.print("Start status: 0x");
  if(status < 0x10) Serial.print("0"); 
  Serial.println(status, BIN);

  status = mlx4.begin(mlx4_i2c, -1, Wire);
  Serial.print("Start status: 0x");
  if(status < 0x10) Serial.print("0"); 
  Serial.println(status, BIN);
  mlx2.startBurst(0xF);
  mlx3.startBurst(0xF);
  mlx4.startBurst(0xF);
  
}

void loop()
{

  myMux.setPort(0);
  mlx0.readBurstData(data0); //Read the values from the sensor
  mlx1.readBurstData(data1); 

  myMux.setPort(1);
  mlx0.readBurstData(data2); //Read the values from the sensor
  mlx1.readBurstData(data3); 
  
  myMux.setPort(2);
  mlx2.readBurstData(data4); 
  mlx3.readBurstData(data5); 
  mlx4.readBurstData(data6); 

//  uncomment to change data stream to binary
  for(int idx=0; idx<7; idx++){
    Serial.write((byte*)&data[idx], sizeof(data[idx]));
  } 

//  // comment/uncomment to change data stream to ASCII
//  for(int idx=0; idx<7; idx++){
//    Serial.print(data[idx]->x);
//    Serial.print("\t");
//    Serial.print(data[idx]->y);
//    Serial.print("\t");
//    Serial.print(data[idx]->z);
//    Serial.print("\t");
//    Serial.print(data[idx]->t);
//    Serial.print("\t");
//  } 
  
  Serial.println();
  delay(20);
}
