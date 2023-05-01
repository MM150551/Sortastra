#include <ShiftOutX.h>
#include <ShiftPinNo.h>
#include <math.h>
int clearPin = 10; 
int latchClock = 11; 
int serialData = 12;  
int shiftClock = 13;  
int clearPin2 = 6; 
int latchClock2 = 7; 
int serialData2 = 8;  
int shiftClock2 = 9; 
unsigned long long B, arr[64]={1,9,18,27,33,52,60},M=0,N=0;
shiftOutX regOne(latchClock,serialData,shiftClock,MSBFIRST,4);
shiftOutX regtow(latchClock2,serialData2,shiftClock2,MSBFIRST,4);
//--------------------
unsigned long long power(int j){
  unsigned long long P=2;
  if(j==0){return 0;}
   else{ for(int k=1;k<j;k++){
      P = P*2;
       }return P;}}

unsigned long long control_1(unsigned long long a[64]){
 unsigned long long M=0;
   for(int i=0;i<64;i++){ 
     for(int j=0; j<32; j++){
      if(j==1){if(a[i]==j){M = M + 2;}}       
      else{ if(a[i]==j){M = M + power(j);}}  
    }
    }
    return M;
}
unsigned long long control_2(unsigned long long a[64]){
unsigned long long N=0;
   for(int i=0;i<64;i++){ 
     for(int j=32; j<64; j++){
      if(j==32){if(a[i]==j){N = N + power(j-32);}}       
      else{if(a[i]==j){
        N = N + power(j-32);}}  
       //Serial.println(i); 
       //Serial.println((pow(2,j-34))+1); 
       //Serial.println(N);
    } 
    }
    return N;
}
//-------------------

void setup() {   
   Serial.begin(9600);
  pinMode(clearPin, OUTPUT);
  pinMode(shiftClock, OUTPUT);
  pinMode(latchClock, OUTPUT);
  pinMode(serialData, OUTPUT);
  pinMode(clearPin2, OUTPUT);
  pinMode(shiftClock2, OUTPUT);
  pinMode(latchClock2, OUTPUT);
  pinMode(serialData2, OUTPUT);


  digitalWrite(clearPin, LOW); 
  digitalWrite(clearPin, HIGH);
  digitalWrite(clearPin2, LOW); 
  digitalWrite(clearPin2, HIGH); 
}


void loop() { 
   M=control_1(arr);
   N=control_2(arr);
   digitalWrite(clearPin, HIGH);
   digitalWrite(clearPin2, HIGH);       
   digitalWrite(latchClock, LOW);
   digitalWrite(latchClock2, LOW);           
   shiftOut_32(serialData, shiftClock, MSBFIRST,M);  
   shiftOut_32(serialData2, shiftClock2, MSBFIRST,N);    
   digitalWrite(latchClock, HIGH);   
   digitalWrite(latchClock2, HIGH);    
   delay(5000); 
   digitalWrite(clearPin, LOW); 
   digitalWrite(clearPin2, LOW); 
   digitalWrite(latchClock, LOW);
   digitalWrite(latchClock2, LOW);       
   digitalWrite(latchClock, HIGH); 
   digitalWrite(latchClock2, HIGH);    
   delay(5000); 
}
