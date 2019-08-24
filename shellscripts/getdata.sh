#! /bin/bash
# use this script for downloading Golestan CAPTCHA
for ((i=25000;i < 1000000;i+=1000)){
 for ((j=0;j < 1000;j++)){
	 wget -x "http://www.rrk.ir/HttpHandler/Captcha.ashx?w=185&h=92&bc=ffffff&rnd=220316349&c=mpUvE5UJ2dN0w00U6Wx44g==" -O ./pics/$(($i+$j)).jpg &
   }
}
exit 0
