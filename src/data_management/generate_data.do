/*
Needs some explanation.
*/



// Header do-file with path definitions, those end up in global macros.
include project_paths
log using `"${PATH_OUT_DATA}/log/`1'.log"', replace


// Read in the model controls
 // measurements, transition ve json file'lari okuyacak.
do `"${PATH_OUT_MODEL_SPECS}/measurements"'
do `"${PATH_OUT_MODEL_SPECS}/transitions"'
do `"${PATH_OUT_MODEL_SPECS}/true_prior"'

set obs 4000
gen caseid = _n
set seed 12345

gen x1 = uniform()
gen x2 = 1
forvalues K = 1 / 3 {
	
	gen fac`K'1  = sqrt(${var_p_`K'})*invnorm(uniform())
}

forvalues N = 1 / 9 {

    gen y`N'1  = ${beta1_`N'}*x1 + ${beta2_`N'}*x2 + ${z_`N'}*${factor_`N'} + ///
				 sqrt(${var_`N'})*invnorm(uniform())
}

local t = 2
	while `t' < 9 {
	local j = `t'-1

	gen fac1`t' = (${lambda_1}/${phi_1})*log(${gamma1_1}*exp(${phi_1}* ///
				   ${lambda_1}*fac1`j') + ${gamma2_1}*exp(${phi_1}*fac2`j') +  ///
				   ${gamma3_1}*exp(${phi_1}*fac3`j')) + ///
				   ${var_u_1}*invnorm(uniform()) 
	gen fac2`t' = ${gamma2_2}*fac2`j' + ${var_u_2}*invnorm(uniform())   
	gen fac3`t'= fac3`j'
	
	

forvalues N = 1 / 6 {
	
		gen y`N'`t'  = ${beta1_`N'}*x1 + ${beta2_`N'}*x2 + ${z_`N'}*${factor_`N'}`t' + ///
					 sqrt(${var_`N'})*invnorm(uniform())
		}
		forvalues N = 7 / 9 { // measurements y7, y8, and y9 are constants
		
		gen y`N'`t' = y`N'`j'
		}
		*drop fac1`j' fac2`j' fac3`j'
		local t = `t' + 1
}

keep caseid fac1* fac2* fac3* y1* y2* y3* y4* y5* y6* y7* y8* y9* x1 x2 
reshape long y1 y2 y3 y4 y5 y6 y7 y8 y9, i(caseid) j(period)
save `"${PATH_OUT_DATA}/data_gen"', replace


*outfile using data.raw, w replace

exit
