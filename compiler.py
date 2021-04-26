# Saee Saadat               97110263
# Alireza Hosseinpour       97110433

import scanner
import parser


while True:
    
    res = scanner.get_next_token()
    hasEnded = res[1]
    token = res[0]
              
    if hasEnded: 
        break
