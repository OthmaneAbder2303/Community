# Python Program to perform addition 
# of two complex numbers using binary 
# + operator overloading.

from math import sqrt

class complex:
        # a complex number :: x = a + i*b 
    def __init__(self, a, b):
        self.a = a
        self.b = b

     # adding two objects 
    def __add__(self, other):
        return self.a + other.a, self.b + other.b
    
    def __gt__(self, other):
        if(sqrt(pow(self.a, 2) + pow(self.b, 2)) > sqrt(pow(other.a, 2) + pow(other.b, 2))):
            return True
        else:
            return False
        
    def __eq__(self, other):
        if(self.a == other.a & self.b == other.b):
            return "Both are equal"
        else:
            return "Not equal"
    
    def __str__(self):
        return 'some text'
    

nb = complex(2, 3)
print(nb)
 
    
'''
Operator	Magic Method

+	__add__(self, other)
–	__sub__(self, other)
*	__mul__(self, other)
/	__truediv__(self, other)
//	__floordiv__(self, other)
%	__mod__(self, other)
**	__pow__(self, other)
>>	__rshift__(self, other)
<<	__lshift__(self, other)
&	__and__(self, other)
|	__or__(self, other)
^	__xor__(self, other)
Comparison Operators:
Operator	Magic Method
<	__lt__(self, other)
>	__gt__(self, other)
<=	__le__(self, other)
>=	__ge__(self, other)
==	__eq__(self, other)
!=	__ne__(self, other)
Assignment Operators:

Operator	Magic Method
-=	__isub__(self, other)
+=	__iadd__(self, other)
*=	__imul__(self, other)
/=	__idiv__(self, other)
//=	__ifloordiv__(self, other)
%=	__imod__(self, other)
**=	__ipow__(self, other)
>>=	__irshift__(self, other)
<<=	__ilshift__(self, other)
&=	__iand__(self, other)
|=	__ior__(self, other)
^=	__ixor__(self, other)
'''