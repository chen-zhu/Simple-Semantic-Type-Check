import ast
from pprint import pprint
import copy
from test_cases import test_cases

#thanks to the Python AST lib https://docs.python.org/3/library/ast.html

def is_num(node):
    if isinstance(node, ast.Num):
        return True
    return False

def is_bool(node):
    try:
        if type(ast.literal_eval(node)) == bool:
            return True
    except:
        return False
    return False 

#I had to separate + * from <= because AST Parser gives us two different type of tree nodes.
def is_op(node):
    try:
        if isinstance(node.op, ast.Mult) or isinstance(node.op, ast.Add):
            return True
    except:
        return False
    return False

def is_compare(node):
    try:
        if isinstance(node.ops[0], ast.LtE) or isinstance(node.ops[0], ast.Gt): 
            return True
    except: 
        return False
    return False

def is_if(node):
    try:
        if node.func.id == "If": 
            return True
    except: 
        return False
    return False

def type_check(node): 
    #if the current node is int or bool, directly return their type! 
    if is_num(node):
        return "Int"
    elif is_bool(node): 
        return "Bool"
    #if the node is add or multi, 
    elif is_op(node): 
        #the left and right type check must be both INT only! 
        if type_check(node.left) == "Int" and type_check(node.right) == "Int": 
            return "Int"
        else: 
            return 'Incorrect Type Detected.'
    #if compare, 
    elif is_compare(node):
        #then the left and right type check must be both INT~~ 
        if type_check(node.left) == "Int" and type_check(node.comparators[0]) == "Int": 
            return "Bool"
        else: 
            return 'Incorrect Type Detected.'
    #encounter IF block. 
    elif is_if(node):
        #IF Block's AST has three nodes: condition (arg0), arg1, arg2

        #in order to proceed, condition must have type BOOLEAN. Do recursively check on condition~  
        if type_check(node.args[0]) == "Bool": 
            op1 = type_check(node.args[1])
            op2 = type_check(node.args[2])
            #According to IF Type Check rule, both arg1 and arg2 must have the same type.
            if (op1 == op2) and (not op1 == 'Incorrect Type Detected.'):
                return op1
            else: 
                return "Incorrect Type Detected. "
        else: 
            return 'Incorrect Type Detected.'
    else: 
        return 'Incorrect Type Detected.'


#this function keeps going to the bttm and calculate & replace node to generate a new tree. 
#Calculating & Repalcing should only happen once in each step up function.
#we split op and compare because these two totally different python.ast structure!
def semantic_step_up(node): 
    #if this node is num/bool, no need to step & replace.
    if is_num(node) or is_bool(node):
        return node#do nothing
    elif is_op(node): #if add and multi, left&right all int, then call & replace.
        left = node.left
        right = node.right

        #always perform check on left fist. then right branch if left has no + * <=...

        #Check left side. if + * <= symbol, then recursively step on this branch.
        if is_op(left) or is_compare(left): #left is op also.
            #perform shallow copy here & conduct replacement on left side.
            node_cp = copy.copy(node)
            node_cp.left = semantic_step_up(left)
            return node_cp

        #Check right side. If also op/compare, do recursively step on right branch.
        elif is_op(right) or is_compare(right):
            node_cp = copy.copy(node)
            node_cp.right = semantic_step_up(right)
            return node_cp

        #if left and right are INT, then we can do calculation and step and return new node with results 
        elif is_num(left) and is_num(right):
            #calculate and replace current node!
            if isinstance(node.op, ast.Mult):
                return ast.Num(left.n * right.n)
            elif isinstance(node.op, ast.Add):
                return ast.Num(left.n + right.n)

        else: 
            raise Exception("Invalid Step - op.")

    #Same as is_op block above.
    elif is_compare(node):
        left = node.left
        right = node.comparators[0]

        if is_op(left) or is_compare(left): #left is op also.
            node_cp = copy.copy(node)
            node_cp.left = semantic_step_up(left)
            return node_cp

        elif is_op(right) or is_compare(right):
            node_cp = copy.copy(node)
            node_cp.comparators = [semantic_step_up(right)]
            return node_cp

        #else, if left and right all num, then compare directly!
        elif is_num(left) and is_num(right):
            if isinstance(node.ops[0], ast.LtE): 
                return ast.NameConstant(left.n <= right.n)
            elif isinstance(node.ops[0], ast.Gt):
                return ast.NameConstant(left.n > right.n)

        else: 
            raise Exception("Invalid Step - compare.")

    elif is_if(node):
        #first of all, check args[0], which is condition~
        condition = node.args[0]
        #if condition is + * <=, then recursively call on condition. 
        if is_op(condition) or is_compare(condition): 
            node_cp = copy.copy(node)
            node_cp.args[0] = semantic_step_up(condition)
            return node_cp
        elif is_bool(condition): 
            #if condition is boolean, we can pick arg1 or arg2 based on Bool value. 
            #no type check on arg1 and arg2 at this moment.
            if ast.literal_eval(condition) == True: 
                return node.args[1]
            else: 
                return node.args[2]
        else:
            #print(ast.dump(node))
            raise Exception("Invalid Step - if condition - semantically wrong.") 

    else: 
        raise Exception("Invalid Step. No Matching Found.")


#def debug(): 
    #tree = ast.parse('If(True, 2+3, 4+5)', mode='eval')
    #dumb = ast.dump(tree.body)
    #print(dumb)
    #dumb = ast.dump(tree.body.args[0])
    #print(type(ast.literal_eval(tree.body.args[0])))
    #print(type(tree.body.args[0].value))
    #tree = ast.parse('If(2<=3, 2+3, 4+5)', mode='eval')
    #dumb = ast.dump(tree.body)
    #print(is_if(tree.body))
    #print(dumb)
    

    #tree = ast.parse('3<=25', mode='eval')
    #dumb = ast.dump(tree.body)
    #print(dumb)
    #dumb = ast.dump(tree.body.left)
    #print(dumb) #print(tree.body.left.n)
    #dumb = ast.dump(tree.body.ops[0])
    #print(dumb)
    #print(isinstance(tree.body.ops[0], ast.LtE))
    #dumb = ast.dump(tree.body.comparators[0])
    #print(dumb)
"""
    print("\n")
    tree = ast.parse('True', mode='eval')
    dumb = ast.dump(tree.body)
    print(is_bool(tree.body))
    #print(isinstance(tree.body.op, ast.Mult))
    print(dumb)


    print("\n")
    tree = ast.parse('3*2', mode='eval')
    dumb = ast.dump(tree.body)
    print(isinstance(tree.body.op, ast.Mult))
    print(dumb)

    print("\n")
    print("\n")
    tree = ast.parse('3+1<=25+1', mode='eval')
    dumb = ast.dump(tree.body)
    print(dumb)
    dumb = ast.dump(tree.body.left)
    print(dumb) #print(tree.body.left.n)
    dumb = ast.dump(tree.body.ops[0])
    print(dumb)
    print(isinstance(tree.body.ops[0], ast.LtE))
    dumb = ast.dump(tree.body.comparators[0])
    print(dumb)
"""

if __name__ == "__main__":
    test_cases = test_cases()
    for test in test_cases:
        print("\n------------------------ Next Test: ---------------------------")
        tree = ast.parse(test[0], mode='eval').body
        print(test[0] + ": ")
        type_check_ret = type_check(tree)
        
        semantic_failed = False
        print("\nORIGINAL TREE STRUCTURE: \n   > " + ast.dump(tree) + "\n\nSTEPS: ")
        try:
            while not (is_num(tree) or is_bool(tree)):
                tree = semantic_step_up(tree)
                dumb = ast.dump(tree)
                print("   > " + dumb)
        except:
            semantic_failed = True

        print("\nTEST RESULTS:")
        if type_check_ret == test[2]:
            print("---> TYPE CHECK RESULT [ASSERTED]. RETURN TYPE: [" + type_check_ret + "]")
        else:
            print("---> TYPE CHECK RESULT DID NOT PASS TEST. PLEASE REFER TO test_cases.py. Ret Type: " + type_check_ret)

        if semantic_failed:
            print("---> SEMANTIC CHECK FAILED. AST COULD NOT BE STEPPED. SEMANTIC CHECK TERMINATED")
        else:     
            if ast.literal_eval(tree) == test[1]:
                print("---> SEMANTIC CHECK RESULT [ASSERTED]. RETURN VALUE: [" + str(ast.literal_eval(tree)) + "]")
            else:
                print("---> SEMANTIC CHECK RESULT DID NOT PASS TEST. PLEASE REFER TO test_cases.py. Ret Value: " + str(ast.literal_eval(tree)))

    print("\n")



    #debug()
    #exp = "2 + 3 * 2 * 2 + 1 + 1"
    #tree = ast.parse(exp, mode='eval').body
    #print(type_check(tree))
    #dumb = ast.dump(tree)
    #print(dumb)
    #while not (is_num(tree) or is_bool(tree)):
    #    tree = semantic_step_up(tree)
    #    dumb = ast.dump(tree)
    #    print(dumb)







