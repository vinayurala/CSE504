.data
space:	.asciiz "\n"
.text 
 main:
	li $v0, 5
	syscall
move $t7, $v0
li $s6, 3
li $s7, 4
bge $s6, $s7, end_if_lid1
li $s7, 10
bne $t7, $s7, end_if_lid2
li $t7, 5

end_if_lid2:
li $s6, 5
li $s7, 2
mul $t0, $s6, $s7 
add $t4, $t7, $t0
move $t7, $t4

end_if_lid1:
li $s7, 4
neg $t1, $s7
li $s6, 2
add $t3, $s6, $t1
move $t5, $t3
add $t2, $t5, 2
move $t6, $t2
li $t7, 3
li $s7, 3
bge $t5, $s7, end_if_lid2
mul $t4, $t7, 2
move $t6, $t4

b end_if_lid3

else_lid1:
mul $s1, $t7, 1
move $t6, $s1

end_if_lid3:
li $t6, 2

while_lid1:
li $s7, 3
bge $t6, $s7, end_while_lid1
move $a0, $t6
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
add $s0, $t5, 2
move $t5, $s0
add $t9, $t7, 3
move $t7, $t9
add $s4, $t6, 1
move $t6, $s4

b while_lid1

end_while_lid1:
li $t6, 4

do_while_lid1:
li $s6, 3
add $s3, $s6, $t7
move $t7, $s3
li $s6, 5
li $s7, 2
mul $s2, $s6, $s7 
move $t5, $s2
li $s7, 3
blt $t6, $s7, do_while_lid1
li $t7, 3

for_lid1:
li $s7, 10
bge $t7, $s7, end_for_lid1
add $t8, $t5, 3
move $t5, $t8
add $t7, $t7, 1

b for_lid1

end_for_lid1:
move $a0, $t7
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
add $t8, $t6, $t5
move $a0, $t8
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
exit:
	li $v0, 10
	syscall
.data
