.data
space:	.asciiz "\n"
.data
error_stmt: .asciiz "Array out of bounds!!!"
.text
c1func1: 
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
  li $t3, 1
mul $t0, $a1, $a2
add $t2, $t3, $t0
move $t1, $t2
move $a0, $t3
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
move $a0, $a1
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
move $a0, $a2
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
move $a0, $t1
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
 move $v0 , $t1 
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
c2func1: 
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
  add $t4, $t3, 0
move $a2, $t4
mul $t1, $a1, $a2
sub $t2, $a3, $t1
move $t0, $t2
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
la $t1, class_c1obj
add $t1, $t1, 32
move $t9, $t1
li $t7, 1
li $t5, 2
la $t1, class_c1obj
add $t1, $t1, 32
move $t2, $t1
add $t8, $t2, 0
li $t8, 3
move $a0, $t7
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
move $a0, $t5
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
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

 move  $a1, $t7
 move  $a2, $t5
jal c1func1 
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
 move $t6 , $v0
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

 move  $a1, $t7
 move  $a2, $t5
 move  $a3, $t6
jal c2func1 
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
 move $t4 , $v0
la $t3, class_c2obj
add $t3, $t3, 0
move $s0, $t3
li $s6, 1
sw $s6, 0($s0)
la $t3, class_c2obj
add $t3, $t3, 8
move $s1, $t3
li $s6, 4
sw $s6, 0($s1)
la $t3, class_c2obj
add $t3, $t3, 0
move $t0, $t3
lw $t0, 0($t0)
move $a0, $t0
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
move $a0, $t6
	li $v0, 1
	syscall
	addi $v0, $zero, 4
	la $a0, space
	syscall
move $a0, $t4
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
num_c1obj:	.word  2
 .align 4
class_c1obj:	.space  8
num_t6:	.word  2
 .align 4
class_t6:	.space  8
num_c2obj:	.word  3
 .align 4
class_c2obj:	.space  12
