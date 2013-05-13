.data
space:	.asciiz "\n"
.data
error_stmt: .asciiz "Array out of bounds!!!"
.text
myclasstemp: 
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
  move $t0, $a1
 move $v0 , $t0 
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
li $t7, 1
la $t4, class_obj
add $t4, $t4, 0
move $s1, $t4
sw $t7, 0($s1)
la $t4, class_obj
add $t4, $t4, 4
move $s0, $t4
li $s6, 1
sw $s6, 0($s0)
li $s6, 1
li $s7, 4
mul $t0, $s6, $s7 
la $s6, size_arr
lw $s6, 0($s6)
mul $s6, $s6, 4
bltz $t0, oob_error
bge $t0, $s6, oob_error
la $t1, arr_arr
add $t1, $t1, $t0
move $t9, $t1
li $s6, 0
sw $s6, 0($t9)
li $t9, 0
li $t3, 1
li $t6, 1
mul $t2, $t6, $t3
move $t5, $t2
 sub $sp, $sp, 56 
 sw $a3, 52($sp) 
 sw $a2, 48($sp) 
 sw $a1, 44($sp) 
 sw $a0, 40($sp) 
 sw $t9, 36($sp) 
 sw $t8, 32($sp) 
 sw $t7, 28($sp) 
 sw $t6, 24($sp) 
 sw $t5, 20($sp) 
 sw $t4, 16($sp) 
 sw $t3, 12($sp) 
 sw $t2, 8($sp) 
 sw $t1, 4($sp) 
 sw $t0, 0($sp) 

 move  $a0, $t5
 li $a1, 3
 li $a2, 4
jal temp 
 addu $sp, $sp, 56 
 lw $a3, -4($sp) 
 lw $a2, -8($sp) 
 lw $a1, -12($sp) 
 lw $a0, -16($sp) 
 lw $t9, -20($sp) 
 lw $t8, -24($sp) 
 lw $t7, -28($sp) 
 lw $t6, -32($sp) 
 lw $t5, -36($sp) 
 lw $t4, -40($sp) 
 lw $t3, -44($sp) 
 lw $t2, -48($sp) 
 lw $t1, -52($sp) 
 lw $t0, -56($sp)
 move $t7 , $v0
move $t8, $t6
 sub $sp, $sp, 56 
 sw $a3, 52($sp) 
 sw $a2, 48($sp) 
 sw $a1, 44($sp) 
 sw $a0, 40($sp) 
 sw $t9, 36($sp) 
 sw $t8, 32($sp) 
 sw $t7, 28($sp) 
 sw $t6, 24($sp) 
 sw $t5, 20($sp) 
 sw $t4, 16($sp) 
 sw $t3, 12($sp) 
 sw $t2, 8($sp) 
 sw $t1, 4($sp) 
 sw $t0, 0($sp) 

 move  $a1, $t8
jal myclasstemp 
 addu $sp, $sp, 56 
 lw $a3, -4($sp) 
 lw $a2, -8($sp) 
 lw $a1, -12($sp) 
 lw $a0, -16($sp) 
 lw $t9, -20($sp) 
 lw $t8, -24($sp) 
 lw $t7, -28($sp) 
 lw $t6, -32($sp) 
 lw $t5, -36($sp) 
 lw $t4, -40($sp) 
 lw $t3, -44($sp) 
 lw $t2, -48($sp) 
 lw $t1, -52($sp) 
 lw $t0, -56($sp)
 move $t5 , $v0
add $t8, $t6, 1
move $a0, $t5
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
move $a0, $t7
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
b exit
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
exit:
	li $v0, 10
	syscall
oob_error:
	la $a0, error_stmt
	li $v0, 4
	syscall
.data
.data
num_obj:	.word  3
 .align 4
class_obj:	.space  12
size_arr:	.word  10
 .align 4
arr_arr:	.space  40
