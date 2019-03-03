/*
In the file "data_management.do", we organize the generated data "data_gen.dta"
to conform the second normal form.

First, we generate "data_table_1" including generated variable factorid. 
factorid is an identification of each factor in the dataset in a way that
the first digit represent the id of a child (caseid in the original data), the 
second digit stands for factor number (1, 2, 3) and th third digit represents the
time period. 
Each factor is matched with corresponding measurements 1, 2 and 3. The variable 
"true" stands for the "true" value of factor derived from the simulated data. 

Second, we form a table "data_table_2" that matches the factorid with factor number, period and
caseid. This enables to refrain from the repetiton of constant factor, fac3, in
the data.

Third, "data_table_2" presents the time-invariant controls for each observation
(caseid).

Finally, we merged the data via factorid. 


*/
include project_paths
log using `"${PATH_OUT_DATA}/log/`1'.log"', replace


use `"${PATH_OUT_DATA}/source_data/data_gen"'

reshape long y1 y2 y3 y4 y5 y6 fac1 fac2 fac3, i(caseid) j(t)

preserve //generation of data_table_1 with factorid specification including 
rename y1 meas11
rename y4 meas12
rename y78 meas13
rename y2 meas21
rename y5 meas22
rename y88 meas23
rename y3 meas31
rename y6 meas32
rename y98 meas33
reshape long meas1 meas2 meas3 , i(caseid t) j(f_nr)

sort caseid f_nr t

gen dummy = _n
keep if (inrange(mod(dummy, 24), 1, 16) | mod(dummy, 24) ==0) 
tostring caseid f_nr t, replace
gen factor_id = caseid + f_nr + t
destring factor_id f_nr caseid t, replace

gen true_fac = .
forvalues i = 1 / 3{
	replace true_fac = fac`i' if f_nr == `i'
}


keep factor_id meas1 meas2 meas3 true_fac 
order factor_id meas1 meas2 meas3 true_fac 

save `"${PATH_OUT_DATA}/tables/data_table_1"', replace
restore

preserve //generation of data_table_2

drop fac1 fac2 fac3 
keep caseid t 
tostring caseid t, replace
gen fac1 = caseid + "1" + t
gen fac2 = caseid + "2" + t
gen fac3 = caseid + "3" + "8"
gen x1 = caseid + "1"
gen x2 = caseid + "2"
destring fac1 fac2 fac3 caseid t x1 x2, replace
save `"${PATH_OUT_DATA}/tables/data_table_2"', replace
restore

preserve
gen N= _n
keep if mod(N, 8)==1
keep caseid x1 x2
reshape long x, i(caseid) j(control)
tostring caseid control, replace
gen cont_id = caseid + control
destring cont_id, replace

keep cont_id x
rename x control
order cont_id control
save `"${PATH_OUT_DATA}/tables/data_table_3"', replace
restore

exit
