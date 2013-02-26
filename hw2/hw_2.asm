        .text
main:                                                                                                                                  
	#1
	li $t2,2
	neg $t2,$t2
	
	#2
	add $t3,$t2,3

	#3
	mul $t4,$t3,5
	
	#4  $t4 == x
	
	#5
	sub $t5,$t4,2
	
	#6  y == $t5
	
	#7
	li $t0,3	# $t0 for a
	
	#8
	sw $t0,var1	#var1 == a
	
	#9
        li $t0,4        # $t0 for b

        #10
        sw $t0,var2     #var2 == b

	#11
	lw $t0,var1
	
	#12
	lw $t1,var2
	
	#13
	add $t6,$t0,$t1
	
	#14
		#$t6 for c
	#15
	sw $t6,var3
	
	#16
	lw $t1,var3
	
	#17
	mul $t7,$t1,2
	
	#18
		#$t7 == d
	#19
	lw $t1,var3
	
	#20
	add $t8,$t1,$t7
	
	#21
	lw $t1,var2
	
	#22
	sub $t9,$t1,$t8
	
	#23
	sw $t9,var4	#$t9 == var4
	
	#24
	lw $t1,var4
	
	#25
	lw $t2,var1
	
	#26
	add $t0,$t1,$t2
	
	#27
	# $t0 used for e
	
	#28
	 move $a0,$t4    # PRINT x
        li $v0,1
        syscall
	
	 move $a0,$t5    # PRINT y
        li $v0,1
        syscall

	 move $a0,$t0    # PRINT e
        li $v0,1
        syscall

#exit
        li $v0,10       #EXIT
	syscall

	.data

var1:	.word 0
var2: 	.word 0
var3: 	.word 0
var4:	.word 0
