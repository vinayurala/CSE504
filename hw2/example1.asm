.data
space:	.asciiz "\n"
.text 
 main:
li $s0, 2
neg $t1, $s0
add $t2, $t1, 3
mul $t0, $t2, 5
move $t1, $t0
sub $t3, $t1, 2
move $t0, $t3
li $t9 3
li $t2 4
add $t5, $t9, $t2
move $t3, $t5
mul $t4, $t3, 2
move $t8, $t4
add $t7, $t3, $t8
sub $t6, $t2, $t7
add $t2, $t9, $t6
move $t9, $t2
move $a0 $t1
li $v0, 1
syscall
addi $v0, $zero, 4
la $a0, space
syscall
move $a0 $t0
li $v0, 1
syscall
addi $v0, $zero, 4
la $a0, space
syscall
move $a0 $t9
li $v0, 1
syscall
addi $v0, $zero, 4
la $a0, space
syscall
li $v0, 10
syscall
