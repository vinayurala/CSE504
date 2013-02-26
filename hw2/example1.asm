		.text 
 main:
li $s0, 2
neg $t2, $s0
add $t3, $t2, 3
mul $t1, $t3, 5
move $t1, $t1
sub $t0, $t1, 2
move $t0, $t0
li $t5 3
li $t3 4
add $t2, $t3, $t5
move $t4, $t2
mul $t2, $t4, 2
move $t2, $t2
add $t2, $t2, $t4
sub $t2, $t2, $t3
add $t2, $t2, $t5
move $t2, $t2
move $a0 $t1
li $v0, 1
syscall
move $a0 $t0
li $v0, 1
syscall
move $a0 $t2
li $v0, 1
syscall
li $v0, 10
syscall
