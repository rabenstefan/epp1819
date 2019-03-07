/*
In this file "generate_data.do", the source data as well as the control 
variables are simulated. 

 The file requires to be called with a model specification as the argument,
a corresponding do-file must exist in ${PATH_OUT_MODEL_SPECS}. That file needs
to define globals:
    
    * ${obs} - number of bservations in the sample
    * ${rnd_seed} - random seed set for the random number generation
    * ${period} - number of periods factors and measurements are observed
	
Four .json files in ${PATH_IN_MODEL_SPECS} provide the parameters for variables. 
The definition of transition and measurement equations are drawn from the CHS 
replication files.

The simulated data is stored as "data_gen.dta" in ${PATH_OUT_DATA}.
*/



// Header do-file with path definitions, those end up in global macros.
include project_paths
log using `"${PATH_OUT_DATA}/log/`1'.log"', replace


// Read in the model controls

do `"${PATH_OUT_MODEL_SPECS}/measurements"'
do `"${PATH_OUT_MODEL_SPECS}/transitions"'
do `"${PATH_OUT_MODEL_SPECS}/true_prior"'
do `"${PATH_OUT_MODEL_SPECS}/smoother"'

set obs ${obs}
set seed ${rnd_seed}
gen caseid = _n


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
scalar T = ${period}
	while `t' <= T { 
	local j = `t'-1 

	forvalues F = 1 / 2 {
		
		*generate fac1 and fac2 for each period.
		gen fac`F'`t' = (${lambda_`F'}/${phi_`F'})*log(${gamma1_`F'}*exp(${phi_`F'}* ///
				   ${lambda_`F'}*fac1`j') + ${gamma2_`F'}*exp(${phi_`F'}*fac2`j') + ///
				   ${gamma3_1}*exp(${phi_1}*fac3`j')) + ///
				   ${var_u_`F'}*invnorm(uniform()) 
		}
	
		gen fac3`t'= fac3`j'
	
	

	forvalues N = 1 / 6 { 
	
		gen y`N'`t'  = ${beta1_`N'}*x1 + ${beta2_`N'}*x2 + 			/// 
						${z_`N'}*${factor_`N'}`t' +				 	///
						sqrt(${var_`N'})*invnorm(uniform())
	} 
		forvalues N = 7 / 9 {  // measurements y7, y8, and y9 are constants
		
		gen y`N'`t' = y`N'`j' 
		} 
		local t = `t' + 1 
} 

*drop the repeated values of fac3, y7 and y8
keep caseid fac1* fac2* fac38 y1* y2* y3* y4* y5* y6* y78 y88 y98 x1 x2 
order caseid fac1* fac2* fac38 y1* y2* y3* y4* y5* y6* y78 y88 y98 x1 x2 
save `"${PATH_OUT_DATA}/source_data/data_gen"', replace



exit









