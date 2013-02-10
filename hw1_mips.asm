	.text
main:
	li $v0,5
	syscall
	move $t0,$v0
		# value of n in $t0
	move $t3,$t0
		# $t3 has n for intermediate purpose
	li $t1,0
	blt $t3,$t1,exit #exit if 
	li $t2,0 #Using $t2 for sum == power of 2
	li $t4,0 #Using $t4 for quotient
	li $t5,2#Using $t5 for 2
	
loop:
	div $t3,$t5
	mflo $t3			
	add $t2,$t2,$t3
	beq $t3,0 ,printt
	b loop

printt:
       move $a0,$t2
       li $v0,1
       syscall

exit:
	li $v0,10
	syscall
	
