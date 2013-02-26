.data
	space:	.asciiz "\n"
.text 
 main:
li $v0, 5
syscall
move $t4, $v0
add $t1, $t4, 2
move $t9, $t1
add $t0, $t9, $t4
move $t5, $t0
neg $t3, $t4
add $t2, $t3, 2
move $t7, $t2
li $s8, 2
div $t4, $s8
mfhi $t5
move $t8, $t5
mul $t4, $t4, 4
sub $t6, $t4, $t7
move $a0 $t6
li $v0, 1
syscall
addi $v0, $zero, 4
la $a0, space
syscall
move $a0 $t8
li $v0, 1
syscall
addi $v0, $zero, 4
la $a0, space
syscall
li $v0, 10
syscall
