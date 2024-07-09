# EL9115 interactive config


Authors: Prince John, Jon Elson

Interactive configuration tool for EL9115 Analog Video Delay IC series.  


The SPI configuration is write only. An 8 bit word is written in each transaction, I've specified the word structure below.

 Data word `$[b_7 b_6 b_5 b_4 b_3 b_2 b_1 b_0] `$

 `$b_7 b_6$` are the register address bits. And bits `$ b_5 b_4 b_3 b_2 b_1 b_0 $` set the delay value. 
