
def test_cases():
	cases = [
		#Sample element---> [exp, corresct_ret_value, 'ret_type'], 
		
		#**********Basic Test Cases [ASSERTED]**********

		['1', 1, 'Int'], 
		['True', True, 'Bool'], 
		['False', False, 'Bool'],

		['1 + 2 + 3 + 4', 10, 'Int'], #add1
		['1 + (2 + 3)', 6, 'Int'], #add2
		['1 + 2', 3, 'Int'], #add3

		['2 * 2 * 3 * 4', 48, 'Int'], #mul1
		['2 * (2 * 3)', 12, 'Int'], #mul2
		['2 * 3', 6, 'Int'], #mul3

		['8 <= 7', False, 'Bool'], #rel4
		['8 <= 8', True, 'Bool'], #rel3
		['8 <= 9', True, 'Bool'], #rel3
		['( 2 + 3 ) <= ( 3 + 4)', True, 'Bool'], #rel1		
		['8 <= ( 3 + 4)', False, 'Bool'], #rel2

		['If (2<=3, 1 + 2, 2 + 3)', 3, 'Int'], #if1
		['If (True, 1 + 2, 2 + 3)', 3, 'Int'], #if2
		['If (False, 1 + 2, 2 + 3)', 5, 'Int'], #if3
		
		#**********Synthetic Test Cases [ASSERTED]**********

		['1 + 2 * 3 + 4 * 5', 27, 'Int'],
		['1 + 2 * 3 + 4 * 5 <= 1 + 2 * 3 + 4 * 5', True, 'Bool'],
		['1 + 2 * 3 + 4 * 5 <= 2 + 2 * 3 + 4 * 5', True, 'Bool'],
		['3 + 2 * 3 + 4 * 5 <= 1 + 2 * 3 + 4 * 5', False, 'Bool'],
		['If (1 + 2 * 3 + 4 * 5 <= 2 + 2 * 3 + 4 * 5, 1, 2)', 1, 'Int'],
		['If (3 + 2 * 3 + 4 * 5 <= 1 + 2 * 3 + 4 * 5, 1, 2)', 2, 'Int'],
		['If (3 + 2 * 3 + 4 * 5 <= 1 + 2 * 3 + 4 * 5, 1, 2)', 2, 'Int'],
		['If (3 + 2 * 3 + 4 * 5 <= 1 + 2 * 3 + 4 * 5, 1, 2)', 2, 'Int'],
		['If (True, If (False, 3, 4), 2)', 4, 'Int'],
		['If (True, If (2+3 <= 3+2, 1*2, 2+2), 2)', 2, 'Int'],
		['If (False, If (2+3 <= 3+2, 1*2, 2+2), 3)', 3, 'Int'],
		['If (False, If (2+3 <= 3+2, 1*2, 2+2), If (6 <= 7, 8*8+9+10, 9+9*2))', 83, 'Int'],

		
		#**********Test Cases With Wrong Type/Semantic [NOT/PARTIAL ASSERTED]**********

		#Disobey Type Rules: NUM, BOOL1 & BOOL2
		#The following case should fail Type Check due to invalid type. Semantic check shoudld 
		#also fail because the script could not detect num and bool type when diving into AST.
		['"abcdefg"', 'XX', 'Incorrect Type Detected.'],

		#Disobey Type Rules: ADD
		#The following cases should fail Both Type and Semantic Check because AST tree cannot be stepped due
		#to the wrong data type.
		['"1" + 2', 'XX', 'Incorrect Type Detected.'], 
		['True + 2', 'XX', 'Incorrect Type Detected.'], 
		['1 + ("ABC" + 3)', 'XX', 'Incorrect Type Detected.'],

		#Disobey Type Rules: MUL
		#The folloiwng cases should fail both Type and Semantic Check because AST tree cannot be stepped due
		#to the wrong data type.
		['"1" * 2', 'XX', 'Incorrect Type Detected.'],
		['True * 2', 'XX', 'Incorrect Type Detected.'], 

		#Disobey Type Rules: REL
		#The folliwng case should fail both Type and Semantic Check because AST tree cannot be stepped due
		#to the wrong data type. 
		['672 <= "ABC"', 'XX', 'Incorrect Type Detected.'],
		['672 <= False', 'XX', 'Incorrect Type Detected.'],

		#Disobey Type Rules: MUL & REL
		#The folliwng case should fail both Type and Semantic Check. 
		['672 + 1 <= False + 1', 'XX', 'Incorrect Type Detected.'],

		#Disobey Type Rules: IF
		#The following case should fail both Type and Semantic Check.
		['If (1, 1, 2)', 'XX', 'Incorrect Type Detected.'],

		#Disobey Type Rules: IF
		#The following cases should fail Type Check.
		#Ex. args[1] and args[2] have two differnet types. 
		['If (True, If (False, True, 4), 2)', 4, 'Incorrect Type Detected.'],
		['If (False, If (2+3 <= 3+2, 1*2, 2+2), If (6 <= 7, True, False))', True, 'Bool'],

	]

	return cases







