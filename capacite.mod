set PINTADE ordered;
set SURFACE ordered;

param cost {PINTADE} >= 0;
param f_min {PINTADE} >= 0, default 0;
param f_max {j in PINTADE} >= f_min[j], default Infinity;

param n_min {SURFACE} >= 0, default 0;
param n_max {i in SURFACE} >= n_max[i], default Infinity;

param amt {SURFACE,PINTADE} >= 0;

# --------------------------------------------------------

var Buy {j in PINTADE} integer >= f_min[j], <= f_max[j];

# --------------------------------------------------------

maximize Total_Cost:  sum {j in PINTADE} nombre[j] * Buy[j];

minimize Surface_Amt {i in SURFACE}: sum {j in PINTADE} amt[i,j] * Buy[j];

# --------------------------------------------------------

subject to Diet {i in SURFACE}:
   n_min[i] <= sum {j in PINTADE} amt[i,j] * Buy[j] <= n_max[i];
