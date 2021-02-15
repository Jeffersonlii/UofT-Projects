############### wed quiz ########### 

#q1
SXY = 0.6
SYY = 0.8
answer = SXY / SYY # = 0.75 

#2 
SYY = 0.8
SXX = 1.2
SXY = 0.6
beta1 = SXY / SYY 
SSE = SYY - beta1^2 * SXX
sigma2 = SSE / 10 # 0.0125

#3
#option 3

#4
n = 20
r = -0.6
answer = r * (sqrt(n-2))/sqrt(1-r^2) # -3.18

#5 
pt(answer, 18)*2 # 0.005

#6
b_1hat = -2.22
stde = 0.2092
alpha = 1- 0.98/2

upperlim = b_1hat + pt(1-alpha/2, 23) * stde # -2.59

#7
# = 1.992
