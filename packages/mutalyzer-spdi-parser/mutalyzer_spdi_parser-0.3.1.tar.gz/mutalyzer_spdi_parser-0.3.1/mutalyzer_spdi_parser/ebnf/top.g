description: reference ":" position ":" (deleted_sequence | deleted_length)? ":" inserted_sequence?

reference: ID reference? | "(" ID reference? ")"

position: NUMBER

deleted_sequence: sequence

deleted_length: NUMBER

inserted_sequence: sequence

sequence: D_SEQUENCE | R_SEQUENCE | P_SEQUENCE

ID: (LETTER | DIGIT) (LETTER | DIGIT | "." | "_" | "-")*

LETTER: UCASE_LETTER | LCASE_LETTER

DIGIT: "0".."9"

LCASE_LETTER: "a".."z"

UCASE_LETTER: "A".."Z"

NUMBER: DIGIT+

D_SEQUENCE: D_NT+

D_NT: "A" | "C" | "G" | "T" | "B" | "D" | "H" | "K" | "M"
     | "N" | "R" | "S" | "V" | "W" | "Y"

R_SEQUENCE: R_NT+

R_NT: "a" | "c" | "g" | "u" | "b" | "d" | "h" | "k" | "m"
    | "n" | "r" | "s" | "v" | "w" | "y"

P_SEQUENCE: AA+

AA: "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I"
  | "K" | "L" | "M" | "N" | "P" | "Q" | "R" | "S" | "T"
  | "U" | "V" | "W" | "Y" | "Z"
  | "*"
  | "X"
