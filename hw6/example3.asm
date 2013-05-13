.data
space:	.asciiz "\n"
.data
error_stmt: .asciiz "Array out of bounds!!!"
.text
Af1: 
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
  li $t0, 10
add $t1, $a1, $t0
move $a0, $t1
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
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
Af2: 
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
  add $t0, $a1, $a2
move $t1, $t0
move $a0, $t1
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
 move $v0 , $a1 
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
li $t0, 10
li $t1, 20
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

 move  $a1, $t0
 move  $a2, $t1
jal Af2 
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
 move $t0 , $v0
move $a0, $t0
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
num_obj:	.word  1
 .align 4
class_obj:	.space  4
