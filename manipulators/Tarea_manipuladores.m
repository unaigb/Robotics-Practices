%Script para el calculo de las coordenadas del punto final de una serie de
%brazos mediante el uso del metodo Denavit-Hatenberg.
Q=[45 35 -15 25 45 -70];

%Primera articulacion.....
 d1=0.35;
 theta1=0.0+Q(1);
 a1=0.000;
 alpha1=90.0;
 
 theta1=theta1*pi/180;
 alpha1=alpha1*pi/180;
 
 Rtheta1=[cos(theta1) -sin(theta1) 0 0 
     sin(theta1) cos(theta1) 0 0
     0 0 1 0
     0 0 0 1];
 
 Td1=[1 0 0 0
      0 1 0 0
      0 0 1 d1
      0 0 0 1];
  
  Ta1=[1 0 0 a1
      0 1 0 0
      0 0 1 0 
      0 0 0 1];
  
  Ralpha1=[1 0 0 0 
      0 cos(alpha1) -sin(alpha1) 0
      0 sin(alpha1) cos(alpha1) 0
      0 0 0 1];
  
  A1=Rtheta1*Td1*Ta1*Ralpha1;
  
  %Segunda articulacion.....
 d2=0.0000;
 theta2=0.0+Q(2);
 a2=0.30;
 alpha2=0.0;
 
 theta2=theta2*pi/180;
 alpha2=alpha2*pi/180;
 
 Rtheta2=[cos(theta2) -sin(theta2) 0 0 
     sin(theta2) cos(theta2) 0 0
     0 0 1 0
     0 0 0 1];
 
 Td2=[1 0 0 0
      0 1 0 0
      0 0 1 d2
      0 0 0 1];
  
  Ta2=[1 0 0 a2
      0 1 0 0
      0 0 1 0 
      0 0 0 1];
  
  Ralpha2=[1 0 0 0 
      0 cos(alpha2) -sin(alpha2) 0
      0 sin(alpha2) cos(alpha2) 0
      0 0 0 1];
  
  A2=Rtheta2*Td2*Ta2*Ralpha2;
  
%Tercera articulacion.....
 d3=0.0000;
 theta3=0.0+Q(3);
 a3=0.3;
 alpha3=90.0;
 
 theta3=theta3*pi/180;
 alpha3=alpha3*pi/180;
 
 Rtheta3=[cos(theta3) -sin(theta3) 0 0 
     sin(theta3) cos(theta3) 0 0
     0 0 1 0
     0 0 0 1];
 
 Td3=[1 0 0 0
      0 1 0 0
      0 0 1 d3
      0 0 0 1];
  
  Ta3=[1 0 0 a3
      0 1 0 0
      0 0 1 0 
      0 0 0 1];
  
  Ralpha3=[1 0 0 0 
      0 cos(alpha3) -sin(alpha3) 0
      0 sin(alpha3) cos(alpha3) 0
      0 0 0 1];
  
  A3=Rtheta3*Td3*Ta3*Ralpha3;
  
 %Cuarta articulacion.....
 d4=-0.2000;
 theta4=0.0+Q(4);
 a4=0.0;
 alpha4=90.0;
 
 theta4=theta4*pi/180;
 alpha4=alpha4*pi/180;
 
 Rtheta4=[cos(theta4) -sin(theta4) 0 0 
     sin(theta4) cos(theta4) 0 0
     0 0 1 0
     0 0 0 1];
 
 Td4=[1 0 0 0
      0 1 0 0
      0 0 1 d4
      0 0 0 1];
  
  Ta4=[1 0 0 a4
      0 1 0 0
      0 0 1 0 
      0 0 0 1];
  
  Ralpha4=[1 0 0 0 
      0 cos(alpha4) -sin(alpha4) 0
      0 sin(alpha4) cos(alpha4) 0
      0 0 0 1];
  
  A4=Rtheta4*Td4*Ta4*Ralpha4;

  %Quinta articulacion.....
 d5=0.0000;
 theta5=0.0+Q(5);
 a5=0.3;
 alpha5=90.0;
 
 theta5=theta5*pi/180;
 alpha5=alpha5*pi/180;
 
 Rtheta5=[cos(theta5) -sin(theta5) 0 0 
     sin(theta5) cos(theta5) 0 0
     0 0 1 0
     0 0 0 1];
 
 Td5=[1 0 0 0
      0 1 0 0
      0 0 1 d5
      0 0 0 1];
  
  Ta5=[1 0 0 a5
      0 1 0 0
      0 0 1 0 
      0 0 0 1];
  
  Ralpha5=[1 0 0 0 
      0 cos(alpha5) -sin(alpha5) 0
      0 sin(alpha5) cos(alpha5) 0
      0 0 0 1];
  
  A5=Rtheta5*Td5*Ta5*Ralpha5;

  %Sexta articulacion.....
 d6=0.0000;
 theta6=0.0+Q(6);
 a6=0.3;
 alpha6=0.0;
 
 theta6=theta6*pi/180;
 alpha6=alpha6*pi/180;
 
 Rtheta6=[cos(theta6) -sin(theta6) 0 0 
     sin(theta6) cos(theta6) 0 0
     0 0 1 0
     0 0 0 1];
 
 Td6=[1 0 0 0
      0 1 0 0
      0 0 1 d6
      0 0 0 1];
  
  Ta6=[1 0 0 a6
      0 1 0 0
      0 0 1 0 
      0 0 0 1];
  
  Ralpha6=[1 0 0 0 
      0 cos(alpha6) -sin(alpha6) 0
      0 sin(alpha6) cos(alpha6) 0
      0 0 0 1];
  
  A6=Rtheta6*Td6*Ta6*Ralpha6;

A0=[1 0 0 0
    0 1 0 0
    0 0 1 0
    0 0 0 1];
  
  Afinal=A0*A1*A2*A3*A4*A5*A6;

  x=Afinal*[0 0 0 1]'