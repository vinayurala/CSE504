.data
space:	.asciiz "\n"
.text 

temp: 
	subu $sp, $sp, 40 
	sw $ra, 36($sp) 
	sw $fp, 32($sp) 
	sw $s7, 28($sp) 
	sw $s6, 24($sp) 
	sw $s5, 20($sp) 
	sw $s4, 16($sp) 
	sw $s3, 12($sp) 
	sw $s2, 8($sp) 
	sw $s1, 4($sp) 
	sw $s0, 0($sp) 
	li $t0, 2
	li $t6, 1

while_lid1:
	li $s7, 2
	bge $t0, $s7, end_while_lid1
	li $s7, 0
	beq $t6, $s7, end_while_lid1
	sub $t0, $t0, 1
	li $s6, 5
	li $s7 , 2
	div $s6 $s7
	mfhi $t2
	move $t6, $t2
	neg $t1, $t6
	add $t3, $a0, $t1
	move $a0, $t3
	b while_lid1

end_while_lid1:

do_while_lid1:

while_lid3:
li $s7, 10
blt $t6, $s7, end_while_lid2
li $s6, 4
li $s7, 3
mul $t5, $s6, $s7 
add $t4, $t6, $t5
move $t6, $t4

b while_lid3

end_while_lid2:
add $t7, $t0, 1
move $t0, $t7
li $s7, 2
bgt $t0, $s7, do_while_lid1
 li $v0 , 3  
 addu $sp, $sp, 40 
 lw $ra, -4($sp) 
 lw $fp, -8($sp) 
 lw $s7, -12($sp) 
 lw $s6, -16($sp)
 lw $s5, -20($sp) 
 lw $s4, -24($sp) 
 lw $s3, -28($sp) 
 lw $s2, -32($sp) 
 lw $s1, -36($sp) 
 lw $s0, -40($sp) 
 jr $ra 

main :
li $t9, 1
add $s0, $t6, 0
move $s0, $t9
add $s1, $t6, 4
li $s1, 1
li $t5, 1
li $t8, 1
add $t8, $t8, 1
mul $t2, $t5, $t8
li $s6, 5
add $t1, $s6, $t2
move $t7, $t1
sub $t5, $t5, 1
bgt $t9, $t7, else_lid1
li $t9, 1
li $s7, 0
blt $t8, $s7, end_if_lid2
li $t8, 0

end_if_lid2:
li $t7, 5
add $t4, $t9, $t7
move $t8, $t4

b end_if_lid1

else_lid1:
li $t7, 4
sub $t3, $t9, $t7
move $t8, $t3

end_if_lid1:
li $t8, 0

for_lid1:
li $s7, 10
blt $t8, $s7, end_for_lid1
add $t0, $t9, 4
move $t9, $t0
add $t8, $t8, 1

b for_lid1

end_for_lid1:

exit:
	li $v0, 10
	syscall

.data

num_main_obj_obj:	.word  3
 .align 4
class_main_obj_obj:	.space  12
size_arr:	.word  10
 .align 4
arr_arr:	.space  40

.data

