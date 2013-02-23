        .text
	# a == $t0
	# b == $t1
	# c == $t2
	# d == $t3 also for -a
	# e == $t4 also for a-5
	# final == $t5 and $t6
main:																			
        li $v0,5	#INPUT
        syscall
        move $t0,$v0
                # value of a in $t0
       		#using $t1 for b
	add $t1,$t0,3
	
	add $t2,$t1,6
		
	neg $t3,$t0

	add $t3,$t1,$t3

	#=========== for e

	sub $t4,$t0,5

	mul $t4,$t4,$t3

	#------------------ Now Print

	mul $t5,$t0,4
	
	sub $t6,$t3,$t5
	
	move $a0,$t6    # PRINT
        li $v0,1
        syscall

#exit
        li $v0,10	#EXIT
        syscall

