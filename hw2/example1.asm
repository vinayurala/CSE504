.data
space:	.asciiz "\n"
.text 
 main:
li $v0, 5
syscall
move $t7, $v0
add $t1, $t7, 2
move $t6, $t1
add $t0, $t7, $t6
move $t8, $t0
neg $t3, $t7
add $t2, $t3, 2
move $t5, $t2
mul $t4, $t7, 4
sub $t9, $t5, $t4
move $a0 $t9
li $v0, 1
syscall
addi $v0, $zero, 4
la $a0, space
syscall
li $v0, 10
syscall
