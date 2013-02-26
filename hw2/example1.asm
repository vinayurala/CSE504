.data
	space:	.asciiz "\n"
.text 
 main:
li $v0, 5
syscall
move $t0, $v0
add $t5, $t0, 2
move $t4, $t5
add $t4, $t4, $t0
move $t5, $t4
neg $t7, $t0
add $t3, $t7, 2
move $t2, $t3
li $s8, 2
div $t0, $s8
mfhi $t9
move $t3, $t9
li $s8, 2
div $t0, $s8
mflo $t8
move $t6, $t8
add $t1, $t3, 1
move $t1, $t1
mul $t0, $t0, 4
sub $t2, $t0, $t2
move $a0 $t2
li $v0, 1
syscall
addi $v0, $zero, 4
la $a0, space
syscall
move $a0 $t1
li $v0, 1
syscall
addi $v0, $zero, 4
la $a0, space
syscall
move $a0 $t6
li $v0, 1
syscall
addi $v0, $zero, 4
la $a0, space
syscall
li $v0, 10
syscall
