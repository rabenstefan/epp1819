clear
set mem 400m
cd C:\Users\ASUS\Desktop\chs_ex2

set obs 4000
gen caseid = _n

gen x1 = uniform()
gen x2 = 1
gen f11  = sqrt(0.2)*invnorm(uniform())
gen f21  = sqrt(0.2)*invnorm(uniform())
gen f31  = sqrt(0.2)*invnorm(uniform())

gen e11  = sqrt(0.5)*invnorm(uniform())
gen e21  = sqrt(0.5)*invnorm(uniform())
gen e31  = sqrt(0.5)*invnorm(uniform())
gen e41  = sqrt(0.5)*invnorm(uniform())
gen e51  = sqrt(0.5)*invnorm(uniform())
gen e61  = sqrt(0.5)*invnorm(uniform())
gen e71  = sqrt(0.5)*invnorm(uniform())
gen e81  = sqrt(0.5)*invnorm(uniform())
gen e91  = sqrt(0.5)*invnorm(uniform())

gen y11  = 1.0*x1 + 1.0*x2 + 1.0*f11 + e11
gen y21  = 1.0*x1 + 1.0*x2 + 1.2*f11 + e21
gen y31  = 1.0*x1 + 1.0*x2 + 1.4*f11 + e31
gen y41  = 1.0*x1 + 1.0*x2 + 1.0*f21 + e41
gen y51  = 1.0*x1 + 1.0*x2 + 0.8*f21 + e51
gen y61  = 1.0*x1 + 1.0*x2 + 0.6*f21 + e61
gen y71  = 1.0*x1 + 1.0*x2 + 1.0*f31 + e71
gen y81  = 1.0*x1 + 1.0*x2 + 1.2*f31 + e81
gen y91  = 1.0*x1 + 1.0*x2 + 0.8*f31 + e91

local t = 2
	while `t' < 9 {
	local j = `t'-1
	gen u1`t'  = sqrt(0.1)*invnorm(uniform())
	gen u2`t'  = sqrt(0.1)*invnorm(uniform())
	gen a = exp(-0.5*f1`j')
	gen b = exp(-0.5*f2`j')
	gen c = exp(-0.5*f3`j')
	gen f1`t'  = (-1.0/0.5)*log(0.6*a + 0.2*b + 0.2*c) + u1`t'
	gen f2`t'  =  0.6*f2`j'	+ u2`t'
	gen f3`t'  =  1.0*f3`j'
	gen e1`t'  = sqrt(0.5)*invnorm(uniform())
	gen e2`t'  = sqrt(0.5)*invnorm(uniform())
	gen e3`t'  = sqrt(0.5)*invnorm(uniform())
	gen e4`t'  = sqrt(0.5)*invnorm(uniform())
	gen e5`t'  = sqrt(0.5)*invnorm(uniform())
	gen e6`t'  = sqrt(0.5)*invnorm(uniform())
	gen y1`t'  = 1.0*x1 + 1.0*x2 + 1.0*f1`t' + e1`t'
	gen y2`t'  = 1.0*x1 + 1.0*x2 + 1.2*f1`t' + e2`t'
	gen y3`t'  = 1.0*x1 + 1.0*x2 + 1.4*f1`t' + e3`t'
	gen y4`t'  = 1.0*x1 + 1.0*x2 + 1.0*f2`t' + e4`t'
	gen y5`t'  = 1.0*x1 + 1.0*x2 + 0.8*f2`t' + e5`t'
	gen y6`t'  = 1.0*x1 + 1.0*x2 + 0.6*f2`t' + e6`t'
	gen y7`t'  = y7`j'
	gen y8`t'  = y8`j'
	gen y9`t'  = y9`j'
	drop a b c
	local t = `t' + 1
}

gen eQ1 = sqrt(1.0)*invnorm(uniform())
gen Q1 = 1.0*x1 + 1.0*x2 + 1.0*f18 + eQ1

keep caseid f1* f2* f3* y1* y2* y3* y4* y5* y6* y7* y8* y9* Q1 x1 x2 
reshape long y1 y2 y3 y4 y5 y6 y7 y8 y9, i(caseid) j(period)

gen dy1 = 1
gen dy2 = 1
gen dy3 = 1
gen dy4 = 1
gen dy5 = 1
gen dy6 = 1
gen dy7 = 1
gen dy8 = 1
gen dy9 = 1
gen dQ1 = 1

order caseid period y1 y2 y3 y4 y5 y6 y7 y8 y9 Q1 dy1 dy2 dy3 dy4 dy5 dy6 dy7 dy8 dy9 dQ1 x1 x2
sort caseid period
save data, replace

*outfile using data.raw, w replace
