.data
space:	.asciiz "\n"
.data
error_stmt: .asciiz "Array out of bounds!!!"
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
  add $t1, $a0, $a1
move $t0, $t1
move $a0, $t0
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
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
la $t4, class_obj
add $t4, $t4, 0
move $t9, $t4
li $s6, 5
sw $s6, 0($t9)
la $t4, class_obj
add $t4, $t4, 4
move $s0, $t4
li $s6, 2
sw $s6, 0($s0)
la $t4, class_obj
add $t4, $t4, 0
move $t2, $t4
la $t4, class_obj
add $t4, $t4, 8
move $t8, $t4
sw $t3, 0($t8)
add $t3, $t2, 1
la $t4, class_obj
add $t4, $t4, 0
move $t7, $t4
la $t4, class_obj
add $t4, $t4, 4
move $t5, $t4
la $t4, class_obj
add $t4, $t4, 8
move $t6, $t4
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

lw $t7, 0($t7)
 move  $a0, $t7
lw $t5, 0($t5)
 move  $a1, $t5
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
 sw $v0, 0($t6)
la $t4, class_obj
add $t4, $t4, 0
move $t1, $t4
lw $t1, 0($t1)
move $a0, $t1
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
la $t4, class_obj
add $t4, $t4, 4
move $t0, $t4
lw $t0, 0($t0)
move $a0, $t0
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
la $t4, class_obj
add $t4, $t4, 8
move $s1, $t4
lw $s1, 0($s1)
move $a0, $s1
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
b exit
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
