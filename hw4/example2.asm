.data
space:	.asciiz "\n"
.text 
 main:
	li $v0, 5
	syscall
move $t4, $v0
li $t5, 1
add $t1, $t4, 2
mul $t0, $t4, 4
la $s6, size_d
lw $s6, 0($s6)
mul $s6, $s6, 4
bltz $t0, exit
bge $t0, $s6, exit
la $t3, arr_d
add $t3, $t3, $t0
move $t7, $t3
sw $t1, 0($t7)
mul $t2, $t4, 4
la $s6, size_d
lw $s6, 0($s6)
mul $s6, $s6, 4
bltz $t2, exit
bge $t2, $s6, exit
la $t3, arr_d
add $t3, $t3, $t2
move $t6, $t3
lw $t6, 0($t6)
move $a0, $t6
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
exit:
	li $v0, 10
	syscall
.data
size_d:	.word  10
 .align 4
arr_d:	.space  40
