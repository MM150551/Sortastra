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
int clearPin3 = 2; 
int latchClock3 = 3; 
int serialData3 = 4;  
int shiftClock3 = 5;
int clearPin4 = A3; 
int latchClock4 = A4; 
int serialData4 = A5;  
int shiftClock4 = 1;
unsigned long long B, arr[128]={1,9,18,27,33,52,60},M=0,N=0,Q=0,W=0;
shiftOutX regOne(latchClock,serialData,shiftClock,MSBFIRST,4);
shiftOutX regtow(latchClock2,serialData2,shiftClock2,MSBFIRST,4);
shiftOutX regthree(latchClock3,serialData3,shiftClock3,MSBFIRST,4);
shiftOutX regfour(latchClock4,serialData4,shiftClock4,MSBFIRST,4);
//--------------------
unsigned long long power(int j){
  unsigned long long P=2;
  if(j==0){return 0;}
   else{ for(int k=1;k<j;k++){
      P = P*2;
       }return P;}}

unsigned long long control_1(unsigned long long a[128]){
 unsigned long long M=0;
   for(int i=0;i<128;i++){ 
     for(int j=0; j<32; j++){
      if(j==1){if(a[i]==j){M = M + 2;}}       
      else{ if(a[i]==j){M = M + power(j);}}  
    }
    }
    return M;
}
unsigned long long control_2(unsigned long long a[128]){
unsigned long long N=0;
   for(int i=0;i<128;i++){ 
     for(int j=32; j<64; j++){
      if(j==32){if(a[i]==j){N = N + power(j-32);}}       
      else{if(a[i]==j){
        N = N + power(j-32);}}  
    } 
    }
    return N;
}
unsigned long long control_3(unsigned long long a[128]){
unsigned long long Q=0;
   for(int i=0;i<128;i++){ 
     for(int j=64; j<96; j++){
      if(j==32){if(a[i]==j){Q = Q + power(j-64);}}       
      else{if(a[i]==j){
        Q = Q + power(j-64);}}  
    } 
    }
    return Q;
}
unsigned long long control_4(unsigned long long a[128]){
unsigned long long W=0;
   for(int i=0;i<128;i++){ 
     for(int j=96; j<128; j++){
      if(j==32){if(a[i]==j){W = W + power(j-96);}}       
      else{if(a[i]==j){
        W = W + power(j-96);}}  
    } 
    }
    return W;
}
//-------------------

void setup() {   
  pinMode(clearPin, OUTPUT);
  pinMode(shiftClock, OUTPUT);
  pinMode(latchClock, OUTPUT);
  pinMode(serialData, OUTPUT);
  pinMode(clearPin2, OUTPUT);
  pinMode(shiftClock2, OUTPUT);
  pinMode(latchClock2, OUTPUT);
  pinMode(serialData2, OUTPUT);
  pinMode(clearPin3, OUTPUT);
  pinMode(shiftClock3, OUTPUT);
  pinMode(latchClock3, OUTPUT);
  pinMode(serialData3, OUTPUT);
  pinMode(clearPin4, OUTPUT);
  pinMode(shiftClock4, OUTPUT);
  pinMode(latchClock4, OUTPUT);
  pinMode(serialData4, OUTPUT);

  digitalWrite(clearPin, LOW); 
  digitalWrite(clearPin, HIGH);
  digitalWrite(clearPin2, LOW); 
  digitalWrite(clearPin2, HIGH);
  digitalWrite(clearPin3, LOW); 
  digitalWrite(clearPin3, HIGH);
  digitalWrite(clearPin4, LOW); 
  digitalWrite(clearPin4, HIGH);  
}


void loop() { 
   M=control_1(arr);
   N=control_2(arr);
   Q=control_3(arr);
   W=control_4(arr);
   digitalWrite(clearPin, HIGH);
   digitalWrite(clearPin2, HIGH);
   digitalWrite(clearPin3, HIGH);
   digitalWrite(clearPin4, HIGH);       
   digitalWrite(latchClock, LOW);
   digitalWrite(latchClock2, LOW);
   digitalWrite(latchClock3, LOW);
   digitalWrite(latchClock4, LOW);           
   shiftOut_32(serialData, shiftClock, MSBFIRST,M);  
   shiftOut_32(serialData2, shiftClock2, MSBFIRST,N);
   shiftOut_32(serialData3, shiftClock3, MSBFIRST,Q);  
   shiftOut_32(serialData4, shiftClock4, MSBFIRST,W);     
   digitalWrite(latchClock, HIGH);   
   digitalWrite(latchClock2, HIGH); 
   digitalWrite(latchClock3, HIGH);   
   digitalWrite(latchClock4, HIGH);   
   delay(5000); 
   digitalWrite(clearPin, LOW); 
   digitalWrite(clearPin2, LOW);
   digitalWrite(clearPin3, LOW); 
   digitalWrite(clearPin4, LOW);  
   digitalWrite(latchClock, LOW);
   digitalWrite(latchClock2, LOW);
   digitalWrite(latchClock3, LOW);
   digitalWrite(latchClock4, LOW);       
   digitalWrite(latchClock, HIGH); 
   digitalWrite(latchClock2, HIGH); 
   digitalWrite(latchClock3, HIGH); 
   digitalWrite(latchClock4, HIGH);   
   delay(5000); 
}
