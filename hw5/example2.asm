.data
space:	.asciiz "\n"
.text 
.data
error_stmt: .asciiz "Array out of bounds!!!"
main :
li $t8, 2
li $t9, 3
li $s0, 1
li $t8, 1
li $s0, 4
sub $t0, $s0, 5
sub $t2, $t8, $t0
move $t9, $t2
mul $t1, $t9, 4
la $s6, size_d
lw $s6, 0($s6)
mul $s6, $s6, 4
bltz $t1, oob_error
bge $t1, $s6, oob_error
la $t7, arr_d
add $t7, $t7, $t1
move $s2, $t7
add $t3, $s0, $t8
sw $t3, 0($s2)
li $s6, 0
li $s7, 4
mul $t5, $s6, $s7 
la $s6, size_d
lw $s6, 0($s6)
mul $s6, $s6, 4
bltz $t5, oob_error
bge $t5, $s6, oob_error
la $t7, arr_d
add $t7, $t7, $t5
move $t4, $t7
add $t6, $t4, $t8
move $t9, $t6
add $s1, $s0, $t8
move $a0, $s1
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
exit:
	li $v0, 10
	syscall
oob_error:
	la $a0, error_stmt
	li $v0, 4
	syscall
.data
.data
size_d:	.word  10
 .align 4
arr_d:	.space  40
