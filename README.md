# One Sample Test 

Python code to give the confidence interval for a one sample test. 
Uses z and t-distributions, without the need of look-up tables
Data can be extracted any column in an ascii for csv files.

Can be run directly [here](https://www.kaggle.com/code/steviemooncat/one-sample-test)

E.g. 
30 data points ranging from 80740 to 117313.0, mean = 100200.37, SD = 11285.48 (pop) 11478.41 (samp)

Plot histogram [y/n]? n

Level of confidence [e.g. 95, 99, 99.9% - 3 sigma is 99.75]? 99

Sample size >= 30 so using z-value

For 99.00% confidence, z = 2.570, giving mean diff of 100200.37 +/- 5384.80 (94815.57 to 105585.17)

-----------------------------------------------------------------------------------------------------

For two sample version see https://github.com/steviecurran/two-sample

![](https://raw.githubusercontent.com/steviecurran/one-sample/refs/heads/main/salaries.dat-histo.png)
