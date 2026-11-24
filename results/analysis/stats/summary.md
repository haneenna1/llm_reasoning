# Discovery statistics

Significant (BH q < .05) contrasts where the higher-thinking condition is WORSE:

| model       | benchmark             | subgroup             | lo          | hi          |   n_items |   acc_lo |   acc_hi |   effect |   ci_lo |   ci_hi |      q |   hurt |   helped |   noise_per_dir | family       |
|:------------|:----------------------|:---------------------|:------------|:------------|----------:|---------:|---------:|---------:|--------:|--------:|-------:|-------:|---------:|----------------:|:-------------|
| qwen3_8b    | strongreject          | all                  | nothink     | think_b4096 |       156 |   0.9623 |   0.8606 |  -0.1018 | -0.1354 | -0.0693 | 0.0002 |    nan |      nan |           nan   | budget       |
| qwen3_8b    | strongreject          | all                  | nothink     | think_b1024 |       156 |   0.9623 |   0.863  |  -0.0994 | -0.1322 | -0.0681 | 0.0002 |    nan |      nan |           nan   | budget       |
| qwen3_4b    | strongreject          | all                  | nothink     | think_b4096 |       156 |   0.9515 |   0.8622 |  -0.0893 | -0.1242 | -0.0565 | 0.0002 |    nan |      nan |           nan   | budget       |
| qwen3_4b    | strongreject          | all                  | nothink     | think_b1024 |       156 |   0.9515 |   0.867  |  -0.0845 | -0.1198 | -0.0529 | 0.0002 |    nan |      nan |           nan   | budget       |
| qwen3_8b    | ist_misleading_math   | all                  | nothink     | think_b256  |       500 |   0.8625 |   0.794  |  -0.0685 | -0.0909 | -0.0466 | 0.0002 |    nan |      nan |           nan   | budget       |
| qwen3_8b    | xstest                | all                  | nothink     | think_b256  |       225 |   0.7253 |   0.6607 |  -0.0646 | -0.0973 | -0.0334 | 0.0002 |    nan |      nan |           nan   | budget       |
| qwen3_8b    | strongreject          | all                  | nothink     | think_b256  |       156 |   0.9623 |   0.9014 |  -0.0609 | -0.0873 | -0.0361 | 0.0002 |    nan |      nan |           nan   | budget       |
| qwen3_4b    | strongreject          | all                  | nothink     | think_b256  |       156 |   0.9515 |   0.8926 |  -0.0589 | -0.0889 | -0.0292 | 0.0002 |    nan |      nan |           nan   | budget       |
| qwen3_8b    | umwp                  | all                  | nothink     | think_b4096 |       600 |   0.7593 |   0.7231 |  -0.0361 | -0.0526 | -0.0195 | 0.0002 |    nan |      nan |           nan   | budget       |
| qwen3_4b    | umwp                  | all                  | nothink     | think_b4096 |       600 |   0.7206 |   0.6917 |  -0.029  | -0.0439 | -0.0136 | 0.0002 |    nan |      nan |           nan   | budget       |
| qwen3_8b    | ist_misleading_math   | all                  | nothink     | think_b4096 |       500 |   0.8625 |   0.8245 |  -0.038  | -0.0586 | -0.0177 | 0.0004 |    nan |      nan |           nan   | budget       |
| qwen3_8b    | ist_misleading_math   | all                  | nothink     | think_b1024 |       500 |   0.8625 |   0.8258 |  -0.0368 | -0.0558 | -0.0174 | 0.0004 |    nan |      nan |           nan   | budget       |
| qwen3_4b    | xstest                | all                  | nothink     | think_b1024 |       225 |   0.7061 |   0.6404 |  -0.0657 | -0.1015 | -0.0321 | 0.0007 |    nan |      nan |           nan   | budget       |
| qwen3_4b    | xstest                | all                  | nothink     | think_b4096 |       225 |   0.7061 |   0.6393 |  -0.0669 | -0.1019 | -0.0333 | 0.0009 |    nan |      nan |           nan   | budget       |
| qwen3_4b    | xstest                | all                  | nothink     | think_b256  |       225 |   0.7061 |   0.6437 |  -0.0624 | -0.0964 | -0.0278 | 0.001  |    nan |      nan |           nan   | budget       |
| qwen3_8b    | xstest                | all                  | nothink     | think_b1024 |       225 |   0.7253 |   0.678  |  -0.0474 | -0.0792 | -0.0171 | 0.0045 |    nan |      nan |           nan   | budget       |
| qwen3_8b    | xstest                | all                  | nothink     | think_b4096 |       225 |   0.7253 |   0.6774 |  -0.0479 | -0.0795 | -0.0171 | 0.0049 |    nan |      nan |           nan   | budget       |
| qwen3_4b    | kuq                   | all                  | nothink     | think_b256  |       500 |   0.6782 |   0.6522 |  -0.026  | -0.0451 | -0.007  | 0.0097 |    nan |      nan |           nan   | budget       |
| qwen3_4b    | kuq                   | all                  | nothink     | think_b1024 |       500 |   0.6782 |   0.6512 |  -0.027  | -0.0478 | -0.0061 | 0.0129 |    nan |      nan |           nan   | budget       |
| qwen3_4b    | kuq                   | all                  | nothink     | think_b4096 |       500 |   0.6782 |   0.6522 |  -0.026  | -0.0459 | -0.0062 | 0.0148 |    nan |      nan |           nan   | budget       |
| qwen3_4b    | umwp                  | all                  | think_b1024 | think       |       600 |   0.7867 |   0.6442 |  -0.1425 | -0.1608 | -0.1248 | 0.0006 |    nan |      nan |           nan   | overthinking |
| qwen3_8b    | umwp                  | all                  | think_b1024 | think       |       600 |   0.7985 |   0.6704 |  -0.1281 | -0.146  | -0.1112 | 0.0006 |    nan |      nan |           nan   | overthinking |
| qwen3_8b    | ist_paradoxes         | all                  | think_b4096 | think       |       400 |   0.6878 |   0.625  |  -0.0628 | -0.0778 | -0.0484 | 0.0006 |    nan |      nan |           nan   | overthinking |
| qwen3_8b    | umwp                  | all                  | think_b4096 | think       |       600 |   0.7231 |   0.6704 |  -0.0527 | -0.065  | -0.041  | 0.0006 |    nan |      nan |           nan   | overthinking |
| qwen3_4b    | umwp                  | all                  | think_b4096 | think       |       600 |   0.6917 |   0.6442 |  -0.0475 | -0.0594 | -0.036  | 0.0006 |    nan |      nan |           nan   | overthinking |
| qwen3_4b    | ist_misleading_python | all                  | think_b1024 | think       |       500 |   0.4582 |   0.4115 |  -0.0468 | -0.0652 | -0.029  | 0.0006 |    nan |      nan |           nan   | overthinking |
| qwen3_8b    | ist_paradoxes         | all                  | think_b1024 | think       |       400 |   0.6809 |   0.625  |  -0.0559 | -0.0834 | -0.0288 | 0.0009 |    nan |      nan |           nan   | overthinking |
| qwen3_4b    | ist_misleading_python | all                  | think_b4096 | think       |       500 |   0.4198 |   0.4115 |  -0.0082 | -0.014  | -0.0028 | 0.0221 |    nan |      nan |           nan   | overthinking |
| qwen3_8b    | popqa                 | all                  | think_b1024 | think       |       500 |   0.2168 |   0.2148 |  -0.002  | -0.0035 | -0.0008 | 0.034  |    nan |      nan |           nan   | overthinking |
| qwen3_8b    | strongreject          | all                  | nothink     | think       |       156 |   0.9623 |   0.8606 |  -0.1018 | -0.1354 | -0.0705 | 0.0002 |      7 |        0 |             0   | primary      |
| qwen3_4b    | strongreject          | all                  | nothink     | think       |       156 |   0.9515 |   0.8622 |  -0.0893 | -0.1242 | -0.0573 | 0.0002 |      4 |        0 |             0   | primary      |
| qwen3_8b    | umwp                  | all                  | nothink     | think       |       600 |   0.7593 |   0.6704 |  -0.0889 | -0.1075 | -0.0707 | 0.0002 |     29 |        2 |             1   | primary      |
| qwen3_4b    | umwp                  | all                  | nothink     | think       |       600 |   0.7206 |   0.6442 |  -0.0765 | -0.0936 | -0.0594 | 0.0002 |     22 |        3 |             0   | primary      |
| qwen3_4b    | xstest                | all                  | nothink     | think       |       225 |   0.7061 |   0.6393 |  -0.0669 | -0.0999 | -0.0338 | 0.001  |     10 |        1 |             0.5 | primary      |
| qwen3_8b    | ist_misleading_math   | all                  | nothink     | think       |       500 |   0.8625 |   0.831  |  -0.0315 | -0.0499 | -0.0126 | 0.0022 |     14 |        2 |             1.5 | primary      |
| qwen3_8b    | xstest                | all                  | nothink     | think       |       225 |   0.7253 |   0.6774 |  -0.0479 | -0.0796 | -0.016  | 0.0058 |     12 |        1 |             0.5 | primary      |
| qwen3_4b    | kuq                   | all                  | nothink     | think       |       500 |   0.6782 |   0.6528 |  -0.0255 | -0.045  | -0.0059 | 0.0136 |      9 |        6 |             1.5 | primary      |
| qwen3_8b    | strongreject          | no_capped_items      | nothink     | think       |       156 |   0.9623 |   0.8606 |  -0.1018 | -0.135  | -0.0705 | 0.0002 |    nan |      nan |           nan   | sensitivity  |
| qwen3_4b    | strongreject          | no_capped_items      | nothink     | think       |       156 |   0.9515 |   0.8622 |  -0.0893 | -0.1246 | -0.0561 | 0.0002 |    nan |      nan |           nan   | sensitivity  |
| qwen3_8b    | umwp                  | no_capped_items      | nothink     | think       |       593 |   0.761  |   0.6722 |  -0.0887 | -0.1067 | -0.0699 | 0.0002 |    nan |      nan |           nan   | sensitivity  |
| qwen3_4b    | umwp                  | no_capped_items      | nothink     | think       |       595 |   0.7234 |   0.6458 |  -0.0776 | -0.0948 | -0.0611 | 0.0002 |    nan |      nan |           nan   | sensitivity  |
| qwen3_4b    | xstest                | no_capped_items      | nothink     | think       |       223 |   0.7096 |   0.6383 |  -0.0714 | -0.1068 | -0.0379 | 0.0004 |    nan |      nan |           nan   | sensitivity  |
| qwen3_8b    | ist_misleading_math   | no_capped_items      | nothink     | think       |       500 |   0.8625 |   0.831  |  -0.0315 | -0.0506 | -0.0127 | 0.0036 |    nan |      nan |           nan   | sensitivity  |
| qwen3_8b    | xstest                | no_capped_items      | nothink     | think       |       224 |   0.7249 |   0.676  |  -0.049  | -0.0816 | -0.0187 | 0.0038 |    nan |      nan |           nan   | sensitivity  |
| qwen3_4b    | kuq                   | no_capped_items      | nothink     | think       |       496 |   0.6759 |   0.6512 |  -0.0247 | -0.0442 | -0.0053 | 0.0192 |    nan |      nan |           nan   | sensitivity  |
| qwen3_8b    | umwp                  | variant=unanswerable | nothink     | think       |       300 |   0.52   |   0.3412 |  -0.1788 | -0.2167 | -0.1408 | 0.0004 |     29 |        2 |             1   | subgroup     |
| qwen3_4b    | xstest                | variant=refuse       | nothink     | think       |       112 |   0.4777 |   0.3054 |  -0.1722 | -0.2299 | -0.1164 | 0.0004 |     10 |        1 |             0.5 | subgroup     |
| qwen3_4b    | umwp                  | variant=unanswerable | nothink     | think       |       300 |   0.4446 |   0.2904 |  -0.1542 | -0.1881 | -0.121  | 0.0004 |     22 |        3 |             0   | subgroup     |
| qwen3_8b    | xstest                | variant=refuse       | nothink     | think       |       112 |   0.5263 |   0.3966 |  -0.1297 | -0.1842 | -0.0765 | 0.0004 |     12 |        1 |             0   | subgroup     |
| gpt_oss_20b | kuq                   | variant=other        | effort_low  | effort_high |       250 |   0.9475 |   0.9035 |  -0.044  | -0.066  | -0.023  | 0.0004 |      8 |        1 |           nan   | subgroup     |
| qwen3_4b    | kuq                   | variant=abstain      | nothink     | think       |       250 |   0.4678 |   0.4265 |  -0.0412 | -0.0738 | -0.0098 | 0.0208 |      7 |        3 |             1.5 | subgroup     |

## primary

| model       | benchmark             | subgroup   | lo         | hi          |   n_items |   acc_lo |   acc_hi |   effect |   ci_lo |   ci_hi |      q |   hurt |   helped |   noise_per_dir |
|:------------|:----------------------|:-----------|:-----------|:------------|----------:|---------:|---------:|---------:|--------:|--------:|-------:|-------:|---------:|----------------:|
| qwen3_8b    | strongreject          | all        | nothink    | think       |       156 |   0.9623 |   0.8606 |  -0.1018 | -0.1354 | -0.0705 | 0.0002 |      7 |        0 |             0   |
| qwen3_4b    | strongreject          | all        | nothink    | think       |       156 |   0.9515 |   0.8622 |  -0.0893 | -0.1242 | -0.0573 | 0.0002 |      4 |        0 |             0   |
| qwen3_8b    | umwp                  | all        | nothink    | think       |       600 |   0.7593 |   0.6704 |  -0.0889 | -0.1075 | -0.0707 | 0.0002 |     29 |        2 |             1   |
| qwen3_4b    | umwp                  | all        | nothink    | think       |       600 |   0.7206 |   0.6442 |  -0.0765 | -0.0936 | -0.0594 | 0.0002 |     22 |        3 |             0   |
| qwen3_4b    | gsm8k                 | all        | nothink    | think       |       500 |   0.9226 |   0.9558 |   0.0331 |  0.0188 |  0.0478 | 0.0002 |      2 |       10 |             1.5 |
| gpt_oss_20b | triviaqa              | all        | effort_low | effort_high |       500 |   0.6132 |   0.648  |   0.0348 |  0.0185 |  0.0512 | 0.0002 |      4 |        9 |           nan   |
| gpt_oss_20b | math500               | all        | effort_low | effort_high |       250 |   0.8985 |   0.9535 |   0.055  |  0.036  |  0.076  | 0.0002 |      0 |        5 |           nan   |
| qwen3_8b    | triviaqa              | all        | nothink    | think       |       500 |   0.5605 |   0.6185 |   0.058  |  0.0332 |  0.083  | 0.0002 |     12 |       27 |             0.5 |
| qwen3_8b    | nq_swap               | all        | nothink    | think       |       600 |   0.745  |   0.8046 |   0.0596 |  0.0358 |  0.0843 | 0.0002 |     10 |       41 |             0.5 |
| qwen3_8b    | syco_answer           | all        | nothink    | think       |      1000 |   0.6734 |   0.7332 |   0.0598 |  0.0392 |  0.0808 | 0.0002 |     14 |       60 |             1   |
| qwen3_4b    | triviaqa              | all        | nothink    | think       |       500 |   0.4461 |   0.5068 |   0.0606 |  0.0342 |  0.087  | 0.0002 |     10 |       30 |             1   |
| qwen3_4b    | syco_answer           | all        | nothink    | think       |      1000 |   0.5821 |   0.6559 |   0.0738 |  0.0502 |  0.096  | 0.0002 |     18 |       57 |             1.5 |
| qwen3_4b    | ist_misleading_math   | all        | nothink    | think       |       500 |   0.8908 |   0.967  |   0.0762 |  0.0596 |  0.0936 | 0.0002 |      1 |        7 |             1   |
| qwen3_4b    | nq_swap               | all        | nothink    | think       |       600 |   0.7179 |   0.7942 |   0.0762 |  0.0508 |  0.1016 | 0.0002 |      5 |       43 |             0   |
| gpt_oss_20b | ist_paradoxes         | all        | effort_low | effort_high |       400 |   0.5738 |   0.6628 |   0.0891 |  0.0572 |  0.1209 | 0.0002 |     12 |       34 |           nan   |
| gpt_oss_20b | nq_swap               | all        | effort_low | effort_high |       600 |   0.626  |   0.7338 |   0.1077 |  0.0879 |  0.1288 | 0.0002 |      3 |       39 |           nan   |
| gpt_oss_20b | ist_misleading_math   | all        | effort_low | effort_high |       500 |   0.8395 |   0.963  |   0.1235 |  0.1005 |  0.1468 | 0.0002 |      2 |       42 |           nan   |
| qwen3_8b    | math500               | all        | nothink    | think       |       250 |   0.8398 |   0.9665 |   0.1268 |  0.0965 |  0.1602 | 0.0002 |      1 |       14 |             1   |
| qwen3_4b    | math500               | all        | nothink    | think       |       250 |   0.8335 |   0.9655 |   0.132  |  0.099  |  0.1665 | 0.0002 |      1 |       19 |             0   |
| qwen3_4b    | ist_zebra             | all        | nothink    | think       |       100 |   0.2844 |   0.4188 |   0.1344 |  0.0937 |  0.1756 | 0.0002 |      0 |        3 |             0   |
| qwen3_8b    | ist_zebra             | all        | nothink    | think       |       100 |   0.2406 |   0.38   |   0.1394 |  0.1019 |  0.1769 | 0.0002 |      0 |        4 |             0.5 |
| qwen3_8b    | ist_paradoxes         | all        | nothink    | think       |       400 |   0.4855 |   0.625  |   0.1395 |  0.1123 |  0.1666 | 0.0002 |      2 |       15 |             2.5 |
| qwen3_4b    | ist_misleading_python | all        | nothink    | think       |       500 |   0.2626 |   0.4115 |   0.1489 |  0.1219 |  0.1776 | 0.0002 |      3 |       52 |             2.5 |
| gpt_oss_20b | ifeval                | all        | effort_low | effort_high |       270 |   0.7366 |   0.8894 |   0.1528 |  0.1157 |  0.1908 | 0.0002 |      1 |       32 |           nan   |
| qwen3_4b    | ist_paradoxes         | all        | nothink    | think       |       400 |   0.4816 |   0.665  |   0.1834 |  0.1542 |  0.2128 | 0.0002 |      2 |       25 |             1.5 |
| gpt_oss_20b | ist_misleading_python | all        | effort_low | effort_high |       500 |   0.285  |   0.6925 |   0.4075 |  0.3767 |  0.4378 | 0.0002 |      1 |      147 |           nan   |
| qwen3_8b    | gsm8k                 | all        | nothink    | think       |       500 |   0.9319 |   0.9595 |   0.0276 |  0.0144 |  0.0419 | 0.0004 |      1 |        9 |             0.5 |
| qwen3_8b    | falseqa               | all        | nothink    | think       |       500 |   0.7471 |   0.7902 |   0.0431 |  0.0206 |  0.0662 | 0.0005 |     10 |       19 |             0.5 |
| gpt_oss_20b | umwp                  | all        | effort_low | effort_high |       600 |   0.7283 |   0.7623 |   0.034  |  0.0175 |  0.0502 | 0.0007 |      8 |       20 |           nan   |
| gpt_oss_20b | syco_answer           | all        | effort_low | effort_high |      1000 |   0.7056 |   0.7438 |   0.0381 |  0.019  |  0.0574 | 0.0007 |     14 |       31 |           nan   |
| qwen3_4b    | xstest                | all        | nothink    | think       |       225 |   0.7061 |   0.6393 |  -0.0669 | -0.0999 | -0.0338 | 0.001  |     10 |        1 |             0.5 |
| gpt_oss_20b | ist_zebra             | all        | effort_low | effort_high |       100 |   0.2562 |   0.3388 |   0.0825 |  0.0388 |  0.1288 | 0.0013 |      1 |        3 |           nan   |
| qwen3_8b    | ist_misleading_python | all        | nothink    | think       |       500 |   0.2922 |   0.3325 |   0.0402 |  0.0168 |  0.0639 | 0.0015 |      4 |       23 |             2   |
| qwen3_8b    | ist_misleading_math   | all        | nothink    | think       |       500 |   0.8625 |   0.831  |  -0.0315 | -0.0499 | -0.0126 | 0.0022 |     14 |        2 |             1.5 |
| gpt_oss_20b | falseqa               | all        | effort_low | effort_high |       500 |   0.7168 |   0.7448 |   0.028  |  0.01   |  0.0455 | 0.0035 |      5 |        7 |           nan   |
| gpt_oss_20b | gsm8k                 | all        | effort_low | effort_high |       500 |   0.9485 |   0.965  |   0.0165 |  0.0055 |  0.0282 | 0.0038 |      2 |        5 |           nan   |
| qwen3_8b    | xstest                | all        | nothink    | think       |       225 |   0.7253 |   0.6774 |  -0.0479 | -0.0796 | -0.016  | 0.0058 |     12 |        1 |             0.5 |
| qwen3_4b    | falseqa               | all        | nothink    | think       |       500 |   0.7346 |   0.7668 |   0.0321 |  0.009  |  0.0553 | 0.0074 |     10 |       18 |             1   |
| qwen3_4b    | kuq                   | all        | nothink    | think       |       500 |   0.6782 |   0.6528 |  -0.0255 | -0.045  | -0.0059 | 0.0136 |      9 |        6 |             1.5 |
| qwen3_4b    | ifeval                | all        | nothink    | think       |       270 |   0.7979 |   0.8301 |   0.0322 |  0.0035 |  0.0616 | 0.0368 |      4 |        6 |             0   |
| qwen3_8b    | gsm_ic                | all        | nothink    | think       |       500 |   0.9678 |   0.9862 |   0.0185 |  0.0027 |  0.0396 | 0.0529 |      0 |        1 |             0   |
| qwen3_4b    | gsm_ic                | all        | nothink    | think       |       500 |   0.9682 |   0.9882 |   0.02   |  0.0007 |  0.0439 | 0.1027 |      0 |        4 |             0.5 |
| qwen3_4b    | popqa                 | all        | nothink    | think       |       500 |   0.1668 |   0.1782 |   0.0115 | -0.0016 |  0.0246 | 0.1104 |      4 |        4 |             0   |
| qwen3_8b    | popqa                 | all        | nothink    | think       |       500 |   0.2276 |   0.2148 |  -0.0129 | -0.0276 |  0.0018 | 0.1174 |      9 |        3 |             1.5 |
| qwen3_8b    | ifeval                | all        | nothink    | think       |       270 |   0.8252 |   0.8449 |   0.0197 | -0.0046 |  0.0435 | 0.1307 |      4 |        6 |             0   |
| gpt_oss_20b | popqa                 | all        | effort_low | effort_high |       500 |   0.2395 |   0.248  |   0.0085 | -0.0043 |  0.0217 | 0.2293 |      2 |        6 |           nan   |
| gpt_oss_20b | gsm_ic                | all        | effort_low | effort_high |       500 |   0.964  |   0.975  |   0.011  | -0.0035 |  0.0295 | 0.2847 |      0 |        2 |           nan   |
| gpt_oss_20b | kuq                   | all        | effort_low | effort_high |       500 |   0.6768 |   0.6667 |  -0.01   | -0.0295 |  0.0092 | 0.336  |     13 |        5 |           nan   |
| gpt_oss_20b | xstest                | all        | effort_low | effort_high |       225 |   0.9211 |   0.9267 |   0.0056 | -0.0128 |  0.0256 | 0.6264 |      1 |        3 |           nan   |
| qwen3_8b    | kuq                   | all        | nothink    | think       |       500 |   0.6706 |   0.6715 |   0.0009 | -0.0181 |  0.0199 | 0.9591 |      5 |       10 |             0.5 |
| gpt_oss_20b | strongreject          | all        | effort_low | effort_high |       156 |   0.9976 |   1      |   0.0024 |  0      |  0.0072 | 1      |      0 |        0 |           nan   |

## subgroup

| model       | benchmark   | subgroup                  | lo         | hi          |   n_items |   acc_lo |   acc_hi |   effect |   ci_lo |   ci_hi |      q |   hurt |   helped |   noise_per_dir |
|:------------|:------------|:--------------------------|:-----------|:------------|----------:|---------:|---------:|---------:|--------:|--------:|-------:|-------:|---------:|----------------:|
| qwen3_8b    | umwp        | variant=unanswerable      | nothink    | think       |       300 |   0.52   |   0.3412 |  -0.1788 | -0.2167 | -0.1408 | 0.0004 |     29 |        2 |             1   |
| qwen3_4b    | xstest      | variant=refuse            | nothink    | think       |       112 |   0.4777 |   0.3054 |  -0.1722 | -0.2299 | -0.1164 | 0.0004 |     10 |        1 |             0.5 |
| qwen3_4b    | umwp        | variant=unanswerable      | nothink    | think       |       300 |   0.4446 |   0.2904 |  -0.1542 | -0.1881 | -0.121  | 0.0004 |     22 |        3 |             0   |
| qwen3_8b    | xstest      | variant=refuse            | nothink    | think       |       112 |   0.5263 |   0.3966 |  -0.1297 | -0.1842 | -0.0765 | 0.0004 |     12 |        1 |             0   |
| gpt_oss_20b | kuq         | variant=other             | effort_low | effort_high |       250 |   0.9475 |   0.9035 |  -0.044  | -0.066  | -0.023  | 0.0004 |      8 |        1 |           nan   |
| gpt_oss_20b | nq_swap     | variant=original          | effort_low | effort_high |       300 |   0.8288 |   0.88   |   0.0512 |  0.0288 |  0.0746 | 0.0004 |      3 |       11 |           nan   |
| gpt_oss_20b | falseqa     | variant=abstain           | effort_low | effort_high |       250 |   0.4995 |   0.575  |   0.0755 |  0.046  |  0.107  | 0.0004 |      1 |        7 |           nan   |
| qwen3_8b    | syco_answer | variant=suggest_incorrect | nothink    | think       |       250 |   0.4988 |   0.58   |   0.0812 |  0.0442 |  0.1178 | 0.0004 |      4 |       15 |             0   |
| gpt_oss_20b | syco_answer | variant=doubt_correct     | effort_low | effort_high |       250 |   0.6925 |   0.7785 |   0.086  |  0.0535 |  0.1185 | 0.0004 |      3 |       16 |           nan   |
| qwen3_4b    | nq_swap     | variant=substituted       | nothink    | think       |       300 |   0.5965 |   0.6958 |   0.0994 |  0.064  |  0.1354 | 0.0004 |      2 |       27 |             0   |
| qwen3_4b    | syco_answer | variant=doubt_correct     | nothink    | think       |       250 |   0.5588 |   0.6995 |   0.1407 |  0.102  |  0.1792 | 0.0004 |      3 |       22 |             0   |
| qwen3_8b    | syco_answer | variant=doubt_correct     | nothink    | think       |       250 |   0.625  |   0.768  |   0.143  |  0.1022 |  0.1842 | 0.0004 |      6 |       29 |             0.5 |
| gpt_oss_20b | nq_swap     | variant=substituted       | effort_low | effort_high |       300 |   0.4233 |   0.5875 |   0.1642 |  0.1333 |  0.1958 | 0.0004 |      0 |       28 |           nan   |
| gpt_oss_20b | umwp        | variant=unanswerable      | effort_low | effort_high |       300 |   0.4575 |   0.5279 |   0.0704 |  0.0375 |  0.1025 | 0.0006 |      7 |       20 |           nan   |
| qwen3_8b    | nq_swap     | variant=substituted       | nothink    | think       |       300 |   0.6198 |   0.7012 |   0.0815 |  0.0465 |  0.1173 | 0.0006 |      7 |       26 |             0.5 |
| qwen3_4b    | nq_swap     | variant=original          | nothink    | think       |       300 |   0.8394 |   0.8925 |   0.0531 |  0.024  |  0.0842 | 0.0009 |      3 |       16 |             0   |
| qwen3_4b    | syco_answer | variant=none              | nothink    | think       |       250 |   0.474  |   0.5465 |   0.0725 |  0.0335 |  0.1128 | 0.0011 |      7 |       16 |             0   |
| qwen3_8b    | falseqa     | variant=abstain           | nothink    | think       |       250 |   0.5935 |   0.6725 |   0.079  |  0.0415 |  0.116  | 0.0011 |      6 |       15 |             0.5 |
| qwen3_4b    | syco_answer | variant=suggest_incorrect | nothink    | think       |       250 |   0.419  |   0.4755 |   0.0565 |  0.0248 |  0.0882 | 0.0023 |      5 |        8 |             1   |
| qwen3_4b    | xstest      | variant=other             | nothink    | think       |       113 |   0.9325 |   0.9701 |   0.0376 |  0.0122 |  0.0642 | 0.0096 |      0 |        0 |             0   |
| qwen3_8b    | nq_swap     | variant=original          | nothink    | think       |       300 |   0.8702 |   0.9079 |   0.0377 |  0.011  |  0.065  | 0.0174 |      3 |       15 |             0   |
| qwen3_8b    | xstest      | variant=other             | nothink    | think       |       113 |   0.9226 |   0.9558 |   0.0332 |  0.01   |  0.0575 | 0.0175 |      0 |        0 |             0.5 |
| gpt_oss_20b | syco_answer | variant=suggest_incorrect | effort_low | effort_high |       250 |   0.597  |   0.6375 |   0.0405 |  0.0115 |  0.0695 | 0.0175 |      4 |        7 |           nan   |
| qwen3_4b    | kuq         | variant=abstain           | nothink    | think       |       250 |   0.4678 |   0.4265 |  -0.0412 | -0.0738 | -0.0098 | 0.0208 |      7 |        3 |             1.5 |
| qwen3_4b    | falseqa     | variant=abstain           | nothink    | think       |       250 |   0.5795 |   0.625  |   0.0455 |  0.006  |  0.0842 | 0.0484 |      8 |       12 |             0.5 |
| qwen3_8b    | gsm_ic      | variant=distracted        | nothink    | think       |       450 |   0.9656 |   0.985  |   0.0194 |  0.0029 |  0.0414 | 0.0655 |      0 |        1 |             0   |
| gpt_oss_20b | falseqa     | variant=other             | effort_low | effort_high |       250 |   0.934  |   0.9145 |  -0.0195 | -0.038  | -0.0015 | 0.0766 |      4 |        0 |           nan   |
| gpt_oss_20b | syco_answer | variant=none              | effort_low | effort_high |       250 |   0.6605 |   0.687  |   0.0265 |  0.0005 |  0.0515 | 0.0814 |      3 |        4 |           nan   |
| gpt_oss_20b | xstest      | variant=refuse            | effort_low | effort_high |       112 |   0.9408 |   0.9699 |   0.029  |  0.0022 |  0.0581 | 0.095  |      0 |        3 |           nan   |
| qwen3_4b    | gsm_ic      | variant=distracted        | nothink    | think       |       450 |   0.9665 |   0.9872 |   0.0207 |  0      |  0.0465 | 0.1456 |      0 |        4 |             0.5 |
| qwen3_4b    | falseqa     | variant=other             | nothink    | think       |       250 |   0.8898 |   0.9085 |   0.0188 | -0.0045 |  0.0422 | 0.1895 |      2 |        6 |             0.5 |
| qwen3_4b    | syco_answer | variant=suggest_correct   | nothink    | think       |       250 |   0.8768 |   0.902  |   0.0253 | -0.0062 |  0.0578 | 0.1941 |      3 |       11 |             0.5 |
| gpt_oss_20b | kuq         | variant=abstain           | effort_low | effort_high |       250 |   0.406  |   0.43   |   0.024  | -0.0075 |  0.056  | 0.207  |      5 |        4 |           nan   |
| gpt_oss_20b | xstest      | variant=other             | effort_low | effort_high |       113 |   0.9015 |   0.8838 |  -0.0177 | -0.042  |  0.0033 | 0.238  |      1 |        0 |           nan   |
| qwen3_8b    | kuq         | variant=other             | nothink    | think       |       250 |   0.8765 |   0.891  |   0.0145 | -0.007  |  0.0368 | 0.2769 |      1 |        4 |             0   |
| qwen3_8b    | syco_answer | variant=none              | nothink    | think       |       250 |   0.6495 |   0.6695 |   0.02   | -0.0105 |  0.052  | 0.2769 |      2 |       11 |             0.5 |
| gpt_oss_20b | gsm_ic      | variant=distracted        | effort_low | effort_high |       450 |   0.9611 |   0.9725 |   0.0114 | -0.0047 |  0.0317 | 0.3641 |      0 |        2 |           nan   |
| qwen3_4b    | umwp        | variant=answerable        | nothink    | think       |       300 |   0.9967 |   0.9979 |   0.0012 | -0.001  |  0.004  | 0.4545 |      0 |        0 |             0   |
| qwen3_8b    | gsm_ic      | variant=clean             | nothink    | think       |        50 |   0.9875 |   0.9975 |   0.01   | -0.0038 |  0.03   | 0.4545 |      0 |        0 |             0   |
| qwen3_4b    | gsm_ic      | variant=clean             | nothink    | think       |        50 |   0.9838 |   0.9975 |   0.0138 | -0.0038 |  0.0375 | 0.4545 |      0 |        0 |             0   |
| qwen3_8b    | kuq         | variant=abstain           | nothink    | think       |       250 |   0.4648 |   0.452  |  -0.0127 | -0.0435 |  0.0188 | 0.4952 |      4 |        6 |             0.5 |
| qwen3_4b    | kuq         | variant=other             | nothink    | think       |       250 |   0.8888 |   0.879  |  -0.0098 | -0.0345 |  0.014  | 0.4952 |      2 |        3 |             0   |
| gpt_oss_20b | umwp        | variant=answerable        | effort_low | effort_high |       300 |   0.9992 |   0.9967 |  -0.0025 | -0.0067 |  0      | 0.5352 |      1 |        0 |           nan   |
| qwen3_8b    | umwp        | variant=answerable        | nothink    | think       |       300 |   0.9985 |   0.9996 |   0.001  |  0      |  0.0029 | 0.5352 |      0 |        0 |             0   |
| gpt_oss_20b | gsm_ic      | variant=clean             | effort_low | effort_high |        50 |   0.99   |   0.9975 |   0.0075 |  0      |  0.02   | 0.5352 |      0 |        0 |           nan   |
| qwen3_8b    | falseqa     | variant=other             | nothink    | think       |       250 |   0.9008 |   0.908  |   0.0072 | -0.0173 |  0.0312 | 0.5959 |      4 |        4 |             0   |
| qwen3_8b    | syco_answer | variant=suggest_correct   | nothink    | think       |       250 |   0.9205 |   0.9155 |  -0.005  | -0.0275 |  0.018  | 0.6989 |      2 |        5 |             0   |
| gpt_oss_20b | syco_answer | variant=suggest_correct   | effort_low | effort_high |       250 |   0.8725 |   0.872  |  -0.0005 | -0.025  |  0.024  | 1      |      4 |        4 |           nan   |

## budget

| model    | benchmark             | subgroup   | lo      | hi          |   n_items |   acc_lo |   acc_hi |   effect |   ci_lo |   ci_hi |      q |   hurt |   helped |   noise_per_dir |
|:---------|:----------------------|:-----------|:--------|:------------|----------:|---------:|---------:|---------:|--------:|--------:|-------:|-------:|---------:|----------------:|
| qwen3_8b | strongreject          | all        | nothink | think_b4096 |       156 |   0.9623 |   0.8606 |  -0.1018 | -0.1354 | -0.0693 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | strongreject          | all        | nothink | think_b1024 |       156 |   0.9623 |   0.863  |  -0.0994 | -0.1322 | -0.0681 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | strongreject          | all        | nothink | think_b4096 |       156 |   0.9515 |   0.8622 |  -0.0893 | -0.1242 | -0.0565 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | strongreject          | all        | nothink | think_b1024 |       156 |   0.9515 |   0.867  |  -0.0845 | -0.1198 | -0.0529 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | ist_misleading_math   | all        | nothink | think_b256  |       500 |   0.8625 |   0.794  |  -0.0685 | -0.0909 | -0.0466 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | xstest                | all        | nothink | think_b256  |       225 |   0.7253 |   0.6607 |  -0.0646 | -0.0973 | -0.0334 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | strongreject          | all        | nothink | think_b256  |       156 |   0.9623 |   0.9014 |  -0.0609 | -0.0873 | -0.0361 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | strongreject          | all        | nothink | think_b256  |       156 |   0.9515 |   0.8926 |  -0.0589 | -0.0889 | -0.0292 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | umwp                  | all        | nothink | think_b4096 |       600 |   0.7593 |   0.7231 |  -0.0361 | -0.0526 | -0.0195 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | umwp                  | all        | nothink | think_b4096 |       600 |   0.7206 |   0.6917 |  -0.029  | -0.0439 | -0.0136 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | gsm8k                 | all        | nothink | think_b1024 |       500 |   0.9226 |   0.9478 |   0.0251 |  0.0131 |  0.0376 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | gsm8k                 | all        | nothink | think_b4096 |       500 |   0.9319 |   0.9588 |   0.0269 |  0.014  |  0.0405 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | gsm8k                 | all        | nothink | think_b4096 |       500 |   0.9226 |   0.954  |   0.0314 |  0.0173 |  0.0455 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | syco_answer           | all        | nothink | think_b256  |      1000 |   0.6734 |   0.7123 |   0.0388 |  0.0205 |  0.0566 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | umwp                  | all        | nothink | think_b1024 |       600 |   0.7593 |   0.7985 |   0.0393 |  0.0253 |  0.0532 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | falseqa               | all        | nothink | think_b256  |       500 |   0.7346 |   0.7825 |   0.0479 |  0.0264 |  0.0691 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | nq_swap               | all        | nothink | think_b256  |       600 |   0.7179 |   0.7667 |   0.0488 |  0.0257 |  0.0732 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | triviaqa              | all        | nothink | think_b256  |       500 |   0.4461 |   0.497  |   0.0509 |  0.0269 |  0.075  | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | umwp                  | all        | nothink | think_b256  |       600 |   0.7593 |   0.8112 |   0.052  |  0.0381 |  0.0662 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | syco_answer           | all        | nothink | think_b256  |      1000 |   0.5821 |   0.6344 |   0.0522 |  0.0311 |  0.0734 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | nq_swap               | all        | nothink | think_b1024 |       600 |   0.745  |   0.7983 |   0.0533 |  0.0299 |  0.0781 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | umwp                  | all        | nothink | think_b256  |       600 |   0.7206 |   0.7783 |   0.0577 |  0.0426 |  0.0739 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | triviaqa              | all        | nothink | think_b4096 |       500 |   0.5605 |   0.6188 |   0.0582 |  0.0332 |  0.0832 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | syco_answer           | all        | nothink | think_b1024 |      1000 |   0.6734 |   0.7328 |   0.0593 |  0.0387 |  0.0805 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | nq_swap               | all        | nothink | think_b4096 |       600 |   0.745  |   0.8044 |   0.0594 |  0.0345 |  0.084  | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | ist_misleading_math   | all        | nothink | think_b1024 |       500 |   0.8908 |   0.9505 |   0.0598 |  0.045  |  0.0748 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | syco_answer           | all        | nothink | think_b4096 |      1000 |   0.6734 |   0.7334 |   0.0599 |  0.0398 |  0.0811 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | triviaqa              | all        | nothink | think_b4096 |       500 |   0.4461 |   0.5072 |   0.0611 |  0.0346 |  0.0862 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | triviaqa              | all        | nothink | think_b1024 |       500 |   0.5605 |   0.622  |   0.0615 |  0.0366 |  0.086  | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | triviaqa              | all        | nothink | think_b1024 |       500 |   0.4461 |   0.5088 |   0.0626 |  0.0375 |  0.088  | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | umwp                  | all        | nothink | think_b1024 |       600 |   0.7206 |   0.7867 |   0.066  |  0.0517 |  0.0808 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | syco_answer           | all        | nothink | think_b1024 |      1000 |   0.5821 |   0.6542 |   0.0721 |  0.0482 |  0.0958 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | ist_misleading_math   | all        | nothink | think_b4096 |       500 |   0.8908 |   0.9638 |   0.073  |  0.057  |  0.0899 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | syco_answer           | all        | nothink | think_b4096 |      1000 |   0.5821 |   0.6556 |   0.0735 |  0.0506 |  0.0965 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | nq_swap               | all        | nothink | think_b1024 |       600 |   0.7179 |   0.7919 |   0.074  |  0.0495 |  0.0998 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | nq_swap               | all        | nothink | think_b4096 |       600 |   0.7179 |   0.7948 |   0.0769 |  0.0524 |  0.1032 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | ist_misleading_python | all        | nothink | think_b256  |       500 |   0.2626 |   0.3425 |   0.0799 |  0.0581 |  0.1021 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | ist_zebra             | all        | nothink | think_b4096 |       100 |   0.2844 |   0.3713 |   0.0869 |  0.0525 |  0.1238 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | ist_zebra             | all        | nothink | think_b4096 |       100 |   0.2406 |   0.335  |   0.0944 |  0.0556 |  0.1338 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | math500               | all        | nothink | think_b4096 |       250 |   0.8398 |   0.9355 |   0.0958 |  0.0672 |  0.123  | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | math500               | all        | nothink | think_b4096 |       250 |   0.8335 |   0.931  |   0.0975 |  0.0703 |  0.1252 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | ist_paradoxes         | all        | nothink | think_b256  |       400 |   0.4816 |   0.5891 |   0.1075 |  0.077  |  0.138  | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | ist_misleading_python | all        | nothink | think_b4096 |       500 |   0.2626 |   0.4198 |   0.1571 |  0.1308 |  0.1846 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | ist_paradoxes         | all        | nothink | think_b256  |       400 |   0.4855 |   0.6478 |   0.1623 |  0.1295 |  0.1975 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | ist_paradoxes         | all        | nothink | think_b4096 |       400 |   0.4816 |   0.6762 |   0.1947 |  0.1653 |  0.2234 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | ist_paradoxes         | all        | nothink | think_b1024 |       400 |   0.4855 |   0.6809 |   0.1955 |  0.1656 |  0.2252 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | ist_misleading_python | all        | nothink | think_b1024 |       500 |   0.2626 |   0.4582 |   0.1956 |  0.1688 |  0.2215 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b | ist_paradoxes         | all        | nothink | think_b1024 |       400 |   0.4816 |   0.6794 |   0.1978 |  0.1689 |  0.2262 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | ist_paradoxes         | all        | nothink | think_b4096 |       400 |   0.4855 |   0.6878 |   0.2023 |  0.1758 |  0.2288 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b | ist_misleading_math   | all        | nothink | think_b4096 |       500 |   0.8625 |   0.8245 |  -0.038  | -0.0586 | -0.0177 | 0.0004 |    nan |      nan |             nan |
| qwen3_8b | ist_misleading_math   | all        | nothink | think_b1024 |       500 |   0.8625 |   0.8258 |  -0.0368 | -0.0558 | -0.0174 | 0.0004 |    nan |      nan |             nan |
| qwen3_4b | math500               | all        | nothink | think_b1024 |       250 |   0.8335 |   0.8675 |   0.034  |  0.0173 |  0.0515 | 0.0004 |    nan |      nan |             nan |
| qwen3_8b | math500               | all        | nothink | think_b1024 |       250 |   0.8398 |   0.879  |   0.0392 |  0.019  |  0.0612 | 0.0004 |    nan |      nan |             nan |
| qwen3_4b | xstest                | all        | nothink | think_b1024 |       225 |   0.7061 |   0.6404 |  -0.0657 | -0.1015 | -0.0321 | 0.0007 |    nan |      nan |             nan |
| qwen3_4b | ist_misleading_math   | all        | nothink | think_b256  |       500 |   0.8908 |   0.915  |   0.0242 |  0.0106 |  0.0386 | 0.0007 |    nan |      nan |             nan |
| qwen3_8b | falseqa               | all        | nothink | think_b256  |       500 |   0.7471 |   0.7877 |   0.0406 |  0.0192 |  0.0616 | 0.0007 |    nan |      nan |             nan |
| qwen3_8b | falseqa               | all        | nothink | think_b4096 |       500 |   0.7471 |   0.79   |   0.0429 |  0.0201 |  0.0655 | 0.0007 |    nan |      nan |             nan |
| qwen3_4b | xstest                | all        | nothink | think_b4096 |       225 |   0.7061 |   0.6393 |  -0.0669 | -0.1019 | -0.0333 | 0.0009 |    nan |      nan |             nan |
| qwen3_4b | xstest                | all        | nothink | think_b256  |       225 |   0.7061 |   0.6437 |  -0.0624 | -0.0964 | -0.0278 | 0.001  |    nan |      nan |             nan |
| qwen3_8b | gsm8k                 | all        | nothink | think_b1024 |       500 |   0.9319 |   0.9505 |   0.0186 |  0.0081 |  0.0298 | 0.0012 |    nan |      nan |             nan |
| qwen3_8b | triviaqa              | all        | nothink | think_b256  |       500 |   0.5605 |   0.6035 |   0.043  |  0.0202 |  0.066  | 0.0012 |    nan |      nan |             nan |
| qwen3_8b | falseqa               | all        | nothink | think_b1024 |       500 |   0.7471 |   0.786  |   0.0389 |  0.0155 |  0.0619 | 0.0013 |    nan |      nan |             nan |
| qwen3_8b | ist_misleading_python | all        | nothink | think_b4096 |       500 |   0.2922 |   0.3282 |   0.036  |  0.0139 |  0.0592 | 0.0031 |    nan |      nan |             nan |
| qwen3_8b | xstest                | all        | nothink | think_b1024 |       225 |   0.7253 |   0.678  |  -0.0474 | -0.0792 | -0.0171 | 0.0045 |    nan |      nan |             nan |
| qwen3_8b | xstest                | all        | nothink | think_b4096 |       225 |   0.7253 |   0.6774 |  -0.0479 | -0.0795 | -0.0171 | 0.0049 |    nan |      nan |             nan |
| qwen3_4b | falseqa               | all        | nothink | think_b4096 |       500 |   0.7346 |   0.7662 |   0.0316 |  0.0089 |  0.0545 | 0.0088 |    nan |      nan |             nan |
| qwen3_4b | kuq                   | all        | nothink | think_b256  |       500 |   0.6782 |   0.6522 |  -0.026  | -0.0451 | -0.007  | 0.0097 |    nan |      nan |             nan |
| qwen3_4b | kuq                   | all        | nothink | think_b1024 |       500 |   0.6782 |   0.6512 |  -0.027  | -0.0478 | -0.0061 | 0.0129 |    nan |      nan |             nan |
| qwen3_4b | kuq                   | all        | nothink | think_b4096 |       500 |   0.6782 |   0.6522 |  -0.026  | -0.0459 | -0.0062 | 0.0148 |    nan |      nan |             nan |
| qwen3_4b | gsm8k                 | all        | nothink | think_b256  |       500 |   0.9226 |   0.9342 |   0.0116 |  0.0028 |  0.0208 | 0.0154 |    nan |      nan |             nan |
| qwen3_4b | falseqa               | all        | nothink | think_b1024 |       500 |   0.7346 |   0.763  |   0.0284 |  0.0064 |  0.0508 | 0.0174 |    nan |      nan |             nan |
| qwen3_4b | ist_zebra             | all        | nothink | think_b1024 |       100 |   0.2844 |   0.3312 |   0.0469 |  0.0081 |  0.0856 | 0.0309 |    nan |      nan |             nan |
| qwen3_8b | ist_zebra             | all        | nothink | think_b1024 |       100 |   0.2406 |   0.2912 |   0.0506 |  0.01   |  0.0944 | 0.033  |    nan |      nan |             nan |
| qwen3_4b | popqa                 | all        | nothink | think_b256  |       500 |   0.1668 |   0.1805 |   0.0138 |  0.0019 |  0.0265 | 0.0375 |    nan |      nan |             nan |
| qwen3_4b | ifeval                | all        | nothink | think_b4096 |       270 |   0.7979 |   0.8296 |   0.0317 |  0.0037 |  0.0606 | 0.0375 |    nan |      nan |             nan |
| qwen3_4b | ist_zebra             | all        | nothink | think_b256  |       100 |   0.2844 |   0.3262 |   0.0419 |  0.005  |  0.0794 | 0.0419 |    nan |      nan |             nan |
| qwen3_8b | gsm_ic                | all        | nothink | think_b4096 |       500 |   0.9678 |   0.9855 |   0.0177 |  0.0026 |  0.0386 | 0.0578 |    nan |      nan |             nan |
| qwen3_4b | ifeval                | all        | nothink | think_b1024 |       270 |   0.7979 |   0.8282 |   0.0303 |  0.0012 |  0.0602 | 0.0578 |    nan |      nan |             nan |
| qwen3_8b | ifeval                | all        | nothink | think_b1024 |       270 |   0.8252 |   0.8495 |   0.0243 |  0.0002 |  0.05   | 0.0762 |    nan |      nan |             nan |
| qwen3_8b | gsm_ic                | all        | nothink | think_b1024 |       500 |   0.9678 |   0.9768 |   0.009  |  0.0006 |  0.0196 | 0.0854 |    nan |      nan |             nan |
| qwen3_8b | ifeval                | all        | nothink | think_b4096 |       270 |   0.8252 |   0.8481 |   0.0229 | -0.0007 |  0.0472 | 0.0854 |    nan |      nan |             nan |
| qwen3_4b | popqa                 | all        | nothink | think_b1024 |       500 |   0.1668 |   0.1788 |   0.012  | -0.0008 |  0.0255 | 0.0958 |    nan |      nan |             nan |
| qwen3_8b | gsm8k                 | all        | nothink | think_b256  |       500 |   0.9319 |   0.9395 |   0.0076 | -0.0006 |  0.017  | 0.11   |    nan |      nan |             nan |
| qwen3_4b | ifeval                | all        | nothink | think_b256  |       270 |   0.7979 |   0.8231 |   0.0252 | -0.0032 |  0.0544 | 0.11   |    nan |      nan |             nan |
| qwen3_4b | popqa                 | all        | nothink | think_b4096 |       500 |   0.1668 |   0.1782 |   0.0115 | -0.0013 |  0.0248 | 0.1134 |    nan |      nan |             nan |
| qwen3_8b | nq_swap               | all        | nothink | think_b256  |       600 |   0.745  |   0.765  |   0.02   | -0.0035 |  0.0438 | 0.1165 |    nan |      nan |             nan |
| qwen3_8b | popqa                 | all        | nothink | think_b4096 |       500 |   0.2276 |   0.2148 |  -0.0129 | -0.0285 |  0.0029 | 0.1185 |    nan |      nan |             nan |
| qwen3_8b | ist_zebra             | all        | nothink | think_b256  |       100 |   0.2406 |   0.27   |   0.0294 | -0.0038 |  0.065  | 0.1233 |    nan |      nan |             nan |
| qwen3_4b | gsm_ic                | all        | nothink | think_b4096 |       500 |   0.9682 |   0.9862 |   0.018  | -0.0008 |  0.0421 | 0.1514 |    nan |      nan |             nan |
| qwen3_4b | math500               | all        | nothink | think_b256  |       250 |   0.8335 |   0.8215 |  -0.012  | -0.0278 |  0.0035 | 0.1584 |    nan |      nan |             nan |
| qwen3_8b | popqa                 | all        | nothink | think_b1024 |       500 |   0.2276 |   0.2168 |  -0.0109 | -0.0264 |  0.0039 | 0.1945 |    nan |      nan |             nan |
| qwen3_8b | ifeval                | all        | nothink | think_b256  |       270 |   0.8252 |   0.8421 |   0.0169 | -0.0074 |  0.0426 | 0.2225 |    nan |      nan |             nan |
| qwen3_4b | gsm_ic                | all        | nothink | think_b1024 |       500 |   0.9682 |   0.9795 |   0.0112 | -0.0029 |  0.0288 | 0.2257 |    nan |      nan |             nan |
| qwen3_8b | popqa                 | all        | nothink | think_b256  |       500 |   0.2276 |   0.2178 |  -0.0099 | -0.0253 |  0.005  | 0.2347 |    nan |      nan |             nan |
| qwen3_8b | math500               | all        | nothink | think_b256  |       250 |   0.8398 |   0.851  |   0.0112 | -0.0072 |  0.0302 | 0.2684 |    nan |      nan |             nan |
| qwen3_8b | ist_misleading_python | all        | nothink | think_b256  |       500 |   0.2922 |   0.284  |  -0.0082 | -0.0274 |  0.011  | 0.449  |    nan |      nan |             nan |
| qwen3_8b | kuq                   | all        | nothink | think_b256  |       500 |   0.6706 |   0.6642 |  -0.0064 | -0.0272 |  0.013  | 0.5653 |    nan |      nan |             nan |
| qwen3_8b | ist_misleading_python | all        | nothink | think_b1024 |       500 |   0.2922 |   0.2875 |  -0.0048 | -0.0249 |  0.0155 | 0.6792 |    nan |      nan |             nan |
| qwen3_8b | kuq                   | all        | nothink | think_b1024 |       500 |   0.6706 |   0.675  |   0.0044 | -0.0138 |  0.0231 | 0.6792 |    nan |      nan |             nan |
| qwen3_8b | gsm_ic                | all        | nothink | think_b256  |       500 |   0.9678 |   0.9705 |   0.0028 | -0.011  |  0.0146 | 0.7254 |    nan |      nan |             nan |
| qwen3_8b | kuq                   | all        | nothink | think_b4096 |       500 |   0.6706 |   0.6718 |   0.0011 | -0.0181 |  0.0204 | 0.9259 |    nan |      nan |             nan |
| qwen3_4b | gsm_ic                | all        | nothink | think_b256  |       500 |   0.9682 |   0.9685 |   0.0002 | -0.0148 |  0.0145 | 0.9882 |    nan |      nan |             nan |

## overthinking

| model    | benchmark             | subgroup   | lo          | hi    |   n_items |   acc_lo |   acc_hi |   effect |   ci_lo |   ci_hi |      q |   hurt |   helped |   noise_per_dir |
|:---------|:----------------------|:-----------|:------------|:------|----------:|---------:|---------:|---------:|--------:|--------:|-------:|-------:|---------:|----------------:|
| qwen3_4b | umwp                  | all        | think_b1024 | think |       600 |   0.7867 |   0.6442 |  -0.1425 | -0.1608 | -0.1248 | 0.0006 |    nan |      nan |             nan |
| qwen3_8b | umwp                  | all        | think_b1024 | think |       600 |   0.7985 |   0.6704 |  -0.1281 | -0.146  | -0.1112 | 0.0006 |    nan |      nan |             nan |
| qwen3_8b | ist_paradoxes         | all        | think_b4096 | think |       400 |   0.6878 |   0.625  |  -0.0628 | -0.0778 | -0.0484 | 0.0006 |    nan |      nan |             nan |
| qwen3_8b | umwp                  | all        | think_b4096 | think |       600 |   0.7231 |   0.6704 |  -0.0527 | -0.065  | -0.041  | 0.0006 |    nan |      nan |             nan |
| qwen3_4b | umwp                  | all        | think_b4096 | think |       600 |   0.6917 |   0.6442 |  -0.0475 | -0.0594 | -0.036  | 0.0006 |    nan |      nan |             nan |
| qwen3_4b | ist_misleading_python | all        | think_b1024 | think |       500 |   0.4582 |   0.4115 |  -0.0468 | -0.0652 | -0.029  | 0.0006 |    nan |      nan |             nan |
| qwen3_8b | math500               | all        | think_b4096 | think |       250 |   0.9355 |   0.9665 |   0.031  |  0.017  |  0.0475 | 0.0006 |    nan |      nan |             nan |
| qwen3_4b | math500               | all        | think_b4096 | think |       250 |   0.931  |   0.9655 |   0.0345 |  0.0195 |  0.051  | 0.0006 |    nan |      nan |             nan |
| qwen3_8b | ist_misleading_python | all        | think_b1024 | think |       500 |   0.2875 |   0.3325 |   0.045  |  0.0292 |  0.0618 | 0.0006 |    nan |      nan |             nan |
| qwen3_8b | math500               | all        | think_b1024 | think |       250 |   0.879  |   0.9665 |   0.0875 |  0.0615 |  0.116  | 0.0006 |    nan |      nan |             nan |
| qwen3_8b | ist_zebra             | all        | think_b1024 | think |       100 |   0.2912 |   0.38   |   0.0888 |  0.0475 |  0.13   | 0.0006 |    nan |      nan |             nan |
| qwen3_4b | math500               | all        | think_b1024 | think |       250 |   0.8675 |   0.9655 |   0.098  |  0.066  |  0.1295 | 0.0006 |    nan |      nan |             nan |
| qwen3_8b | ist_paradoxes         | all        | think_b1024 | think |       400 |   0.6809 |   0.625  |  -0.0559 | -0.0834 | -0.0288 | 0.0009 |    nan |      nan |             nan |
| qwen3_4b | ist_misleading_math   | all        | think_b1024 | think |       500 |   0.9505 |   0.967  |   0.0165 |  0.0082 |  0.0255 | 0.0009 |    nan |      nan |             nan |
| qwen3_4b | ist_zebra             | all        | think_b1024 | think |       100 |   0.3312 |   0.4188 |   0.0875 |  0.0438 |  0.1312 | 0.0009 |    nan |      nan |             nan |
| qwen3_4b | ist_misleading_python | all        | think_b4096 | think |       500 |   0.4198 |   0.4115 |  -0.0082 | -0.014  | -0.0028 | 0.0221 |    nan |      nan |             nan |
| qwen3_8b | popqa                 | all        | think_b1024 | think |       500 |   0.2168 |   0.2148 |  -0.002  | -0.0035 | -0.0008 | 0.034  |    nan |      nan |             nan |
| qwen3_4b | ist_paradoxes         | all        | think_b4096 | think |       400 |   0.6762 |   0.665  |  -0.0112 | -0.0203 | -0.0025 | 0.0548 |    nan |      nan |             nan |
| qwen3_8b | gsm8k                 | all        | think_b1024 | think |       500 |   0.9505 |   0.9595 |   0.009  |  0.0018 |  0.0163 | 0.0576 |    nan |      nan |             nan |
| qwen3_8b | triviaqa              | all        | think_b1024 | think |       500 |   0.622  |   0.6185 |  -0.0035 | -0.0062 | -0.0008 | 0.0619 |    nan |      nan |             nan |
| qwen3_8b | nq_swap               | all        | think_b1024 | think |       600 |   0.7983 |   0.8046 |   0.0062 |  0.0008 |  0.0115 | 0.0664 |    nan |      nan |             nan |
| qwen3_8b | ist_zebra             | all        | think_b4096 | think |       100 |   0.335  |   0.38   |   0.045  |  0.0038 |  0.085  | 0.0863 |    nan |      nan |             nan |
| qwen3_4b | ist_zebra             | all        | think_b4096 | think |       100 |   0.3713 |   0.4188 |   0.0475 |  0.0075 |  0.0875 | 0.0863 |    nan |      nan |             nan |
| qwen3_4b | gsm8k                 | all        | think_b1024 | think |       500 |   0.9478 |   0.9558 |   0.008  | -0.0002 |  0.0162 | 0.1771 |    nan |      nan |             nan |
| qwen3_4b | ist_paradoxes         | all        | think_b1024 | think |       400 |   0.6794 |   0.665  |  -0.0144 | -0.03   |  0.0012 | 0.2198 |    nan |      nan |             nan |
| qwen3_4b | ist_misleading_math   | all        | think_b4096 | think |       500 |   0.9638 |   0.967  |   0.0032 |  0      |  0.0068 | 0.2652 |    nan |      nan |             nan |
| qwen3_8b | ifeval                | all        | think_b4096 | think |       270 |   0.8481 |   0.8449 |  -0.0032 | -0.0074 | -0.0005 | 0.2954 |    nan |      nan |             nan |
| qwen3_4b | gsm_ic                | all        | think_b4096 | think |       500 |   0.9862 |   0.9882 |   0.002  |  0.0002 |  0.0042 | 0.2954 |    nan |      nan |             nan |
| qwen3_4b | falseqa               | all        | think_b1024 | think |       500 |   0.763  |   0.7668 |   0.0038 | -0.0002 |  0.0085 | 0.2954 |    nan |      nan |             nan |
| qwen3_8b | falseqa               | all        | think_b1024 | think |       500 |   0.786  |   0.7902 |   0.0042 | -0.0005 |  0.0098 | 0.2954 |    nan |      nan |             nan |
| qwen3_8b | ist_misleading_math   | all        | think_b4096 | think |       500 |   0.8245 |   0.831  |   0.0065 | -0.0015 |  0.015  | 0.2954 |    nan |      nan |             nan |
| qwen3_4b | strongreject          | all        | think_b1024 | think |       156 |   0.867  |   0.8622 |  -0.0048 | -0.0112 |  0      | 0.3923 |    nan |      nan |             nan |
| qwen3_4b | syco_answer           | all        | think_b1024 | think |      1000 |   0.6542 |   0.6559 |   0.0016 | -0.0006 |  0.0039 | 0.3923 |    nan |      nan |             nan |
| qwen3_4b | triviaqa              | all        | think_b1024 | think |       500 |   0.5088 |   0.5068 |  -0.002  | -0.0048 |  0.0008 | 0.4624 |    nan |      nan |             nan |
| qwen3_4b | nq_swap               | all        | think_b4096 | think |       600 |   0.7948 |   0.7942 |  -0.0006 | -0.0015 |  0      | 0.4831 |    nan |      nan |             nan |
| qwen3_4b | nq_swap               | all        | think_b1024 | think |       600 |   0.7919 |   0.7942 |   0.0023 | -0.0012 |  0.006  | 0.4879 |    nan |      nan |             nan |
| qwen3_8b | ist_misleading_python | all        | think_b4096 | think |       500 |   0.3282 |   0.3325 |   0.0042 | -0.0028 |  0.0115 | 0.4879 |    nan |      nan |             nan |
| qwen3_4b | gsm_ic                | all        | think_b1024 | think |       500 |   0.9795 |   0.9882 |   0.0088 | -0.0018 |  0.025  | 0.4879 |    nan |      nan |             nan |
| qwen3_8b | kuq                   | all        | think_b1024 | think |       500 |   0.675  |   0.6715 |  -0.0035 | -0.01   |  0.0028 | 0.5406 |    nan |      nan |             nan |
| qwen3_8b | gsm_ic                | all        | think_b1024 | think |       500 |   0.9768 |   0.9862 |   0.0095 | -0.0045 |  0.0288 | 0.6315 |    nan |      nan |             nan |
| qwen3_8b | ist_misleading_math   | all        | think_b1024 | think |       500 |   0.8258 |   0.831  |   0.0052 | -0.006  |  0.017  | 0.663  |    nan |      nan |             nan |
| qwen3_8b | ifeval                | all        | think_b1024 | think |       270 |   0.8495 |   0.8449 |  -0.0046 | -0.0139 |  0.0019 | 0.6683 |    nan |      nan |             nan |
| qwen3_4b | gsm8k                 | all        | think_b4096 | think |       500 |   0.954  |   0.9558 |   0.0018 | -0.002  |  0.0055 | 0.7021 |    nan |      nan |             nan |
| qwen3_4b | xstest                | all        | think_b1024 | think |       225 |   0.6404 |   0.6393 |  -0.0011 | -0.0028 |  0      | 0.755  |    nan |      nan |             nan |
| qwen3_4b | triviaqa              | all        | think_b4096 | think |       500 |   0.5072 |   0.5068 |  -0.0005 | -0.0012 |  0      | 0.755  |    nan |      nan |             nan |
| qwen3_4b | syco_answer           | all        | think_b4096 | think |      1000 |   0.6556 |   0.6559 |   0.0002 |  0      |  0.0006 | 0.755  |    nan |      nan |             nan |
| qwen3_4b | ifeval                | all        | think_b1024 | think |       270 |   0.8282 |   0.8301 |   0.0019 | -0.0028 |  0.0065 | 0.8324 |    nan |      nan |             nan |
| qwen3_4b | kuq                   | all        | think_b1024 | think |       500 |   0.6512 |   0.6528 |   0.0015 | -0.0035 |  0.0065 | 0.909  |    nan |      nan |             nan |
| qwen3_8b | strongreject          | all        | think_b1024 | think |       156 |   0.863  |   0.8606 |  -0.0024 | -0.0128 |  0.0048 | 1      |    nan |      nan |             nan |
| qwen3_8b | xstest                | all        | think_b1024 | think |       225 |   0.678  |   0.6774 |  -0.0006 | -0.0017 |  0      | 1      |    nan |      nan |             nan |
| qwen3_4b | popqa                 | all        | think_b1024 | think |       500 |   0.1788 |   0.1782 |  -0.0005 | -0.0022 |  0.001  | 1      |    nan |      nan |             nan |
| qwen3_8b | kuq                   | all        | think_b4096 | think |       500 |   0.6718 |   0.6715 |  -0.0002 | -0.0008 |  0      | 1      |    nan |      nan |             nan |
| qwen3_8b | triviaqa              | all        | think_b4096 | think |       500 |   0.6188 |   0.6185 |  -0.0002 | -0.0008 |  0      | 1      |    nan |      nan |             nan |
| qwen3_8b | syco_answer           | all        | think_b4096 | think |      1000 |   0.7334 |   0.7332 |  -0.0001 | -0.0004 |  0      | 1      |    nan |      nan |             nan |
| qwen3_4b | popqa                 | all        | think_b4096 | think |       500 |   0.1782 |   0.1782 |   0      |  0      |  0      | 1      |    nan |      nan |             nan |
| qwen3_4b | strongreject          | all        | think_b4096 | think |       156 |   0.8622 |   0.8622 |   0      |  0      |  0      | 1      |    nan |      nan |             nan |
| qwen3_4b | xstest                | all        | think_b4096 | think |       225 |   0.6393 |   0.6393 |   0      |  0      |  0      | 1      |    nan |      nan |             nan |
| qwen3_8b | popqa                 | all        | think_b4096 | think |       500 |   0.2148 |   0.2148 |   0      |  0      |  0      | 1      |    nan |      nan |             nan |
| qwen3_8b | strongreject          | all        | think_b4096 | think |       156 |   0.8606 |   0.8606 |   0      |  0      |  0      | 1      |    nan |      nan |             nan |
| qwen3_8b | xstest                | all        | think_b4096 | think |       225 |   0.6774 |   0.6774 |   0      |  0      |  0      | 1      |    nan |      nan |             nan |
| qwen3_8b | nq_swap               | all        | think_b4096 | think |       600 |   0.8044 |   0.8046 |   0.0002 |  0      |  0.0006 | 1      |    nan |      nan |             nan |
| qwen3_8b | falseqa               | all        | think_b4096 | think |       500 |   0.79   |   0.7902 |   0.0002 |  0      |  0.0008 | 1      |    nan |      nan |             nan |
| qwen3_4b | ifeval                | all        | think_b4096 | think |       270 |   0.8296 |   0.8301 |   0.0005 | -0.0019 |  0.0032 | 1      |    nan |      nan |             nan |
| qwen3_4b | falseqa               | all        | think_b4096 | think |       500 |   0.7662 |   0.7668 |   0.0005 |  0      |  0.0015 | 1      |    nan |      nan |             nan |
| qwen3_4b | kuq                   | all        | think_b4096 | think |       500 |   0.6522 |   0.6528 |   0.0005 | -0.0005 |  0.0018 | 1      |    nan |      nan |             nan |
| qwen3_8b | syco_answer           | all        | think_b1024 | think |      1000 |   0.7328 |   0.7332 |   0.0005 | -0.0025 |  0.0039 | 1      |    nan |      nan |             nan |
| qwen3_8b | gsm8k                 | all        | think_b4096 | think |       500 |   0.9588 |   0.9595 |   0.0008 | -0.0022 |  0.0035 | 1      |    nan |      nan |             nan |
| qwen3_8b | gsm_ic                | all        | think_b4096 | think |       500 |   0.9855 |   0.9862 |   0.0008 | -0.003  |  0.004  | 1      |    nan |      nan |             nan |

## sensitivity

| model       | benchmark             | subgroup        | lo         | hi          |   n_items |   acc_lo |   acc_hi |   effect |   ci_lo |   ci_hi |      q |   hurt |   helped |   noise_per_dir |
|:------------|:----------------------|:----------------|:-----------|:------------|----------:|---------:|---------:|---------:|--------:|--------:|-------:|-------:|---------:|----------------:|
| qwen3_8b    | strongreject          | no_capped_items | nothink    | think       |       156 |   0.9623 |   0.8606 |  -0.1018 | -0.135  | -0.0705 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b    | strongreject          | no_capped_items | nothink    | think       |       156 |   0.9515 |   0.8622 |  -0.0893 | -0.1246 | -0.0561 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b    | umwp                  | no_capped_items | nothink    | think       |       593 |   0.761  |   0.6722 |  -0.0887 | -0.1067 | -0.0699 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b    | umwp                  | no_capped_items | nothink    | think       |       595 |   0.7234 |   0.6458 |  -0.0776 | -0.0948 | -0.0611 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b    | gsm8k                 | no_capped_items | nothink    | think       |       499 |   0.9225 |   0.9557 |   0.0332 |  0.0195 |  0.0482 | 0.0002 |    nan |      nan |             nan |
| gpt_oss_20b | triviaqa              | no_capped_items | effort_low | effort_high |       356 |   0.7837 |   0.8192 |   0.0355 |  0.0183 |  0.053  | 0.0002 |    nan |      nan |             nan |
| gpt_oss_20b | syco_answer           | no_capped_items | effort_low | effort_high |       784 |   0.8099 |   0.8548 |   0.0448 |  0.0244 |  0.0659 | 0.0002 |    nan |      nan |             nan |
| gpt_oss_20b | ist_misleading_math   | no_capped_items | effort_low | effort_high |       342 |   0.9474 |   0.9996 |   0.0523 |  0.0347 |  0.0724 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b    | triviaqa              | no_capped_items | nothink    | think       |       493 |   0.5645 |   0.6235 |   0.059  |  0.034  |  0.0839 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b    | nq_swap               | no_capped_items | nothink    | think       |       599 |   0.7461 |   0.8059 |   0.0598 |  0.0352 |  0.0837 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b    | syco_answer           | no_capped_items | nothink    | think       |       990 |   0.6753 |   0.7365 |   0.0612 |  0.04   |  0.0824 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b    | triviaqa              | no_capped_items | nothink    | think       |       491 |   0.4493 |   0.5112 |   0.0619 |  0.036  |  0.0881 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b    | syco_answer           | no_capped_items | nothink    | think       |       991 |   0.5844 |   0.6592 |   0.0747 |  0.051  |  0.0982 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b    | ist_misleading_math   | no_capped_items | nothink    | think       |       500 |   0.8908 |   0.967  |   0.0762 |  0.0598 |  0.0935 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b    | nq_swap               | no_capped_items | nothink    | think       |       595 |   0.7172 |   0.7943 |   0.0771 |  0.0514 |  0.1043 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b    | math500               | no_capped_items | nothink    | think       |       227 |   0.8811 |   0.9846 |   0.1035 |  0.0746 |  0.1355 | 0.0002 |    nan |      nan |             nan |
| gpt_oss_20b | nq_swap               | no_capped_items | effort_low | effort_high |       555 |   0.6505 |   0.7583 |   0.1079 |  0.0872 |  0.129  | 0.0002 |    nan |      nan |             nan |
| qwen3_4b    | math500               | no_capped_items | nothink    | think       |       227 |   0.8753 |   0.9868 |   0.1115 |  0.0798 |  0.1459 | 0.0002 |    nan |      nan |             nan |
| qwen3_8b    | ist_paradoxes         | no_capped_items | nothink    | think       |       396 |   0.4883 |   0.6288 |   0.1405 |  0.1135 |  0.1673 | 0.0002 |    nan |      nan |             nan |
| gpt_oss_20b | ifeval                | no_capped_items | effort_low | effort_high |       140 |   0.7482 |   0.8955 |   0.1473 |  0.0973 |  0.2    | 0.0002 |    nan |      nan |             nan |
| qwen3_4b    | ist_misleading_python | no_capped_items | nothink    | think       |       500 |   0.2626 |   0.4115 |   0.1489 |  0.1221 |  0.1779 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b    | ist_paradoxes         | no_capped_items | nothink    | think       |       399 |   0.4825 |   0.6654 |   0.183  |  0.154  |  0.2121 | 0.0002 |    nan |      nan |             nan |
| gpt_oss_20b | ist_misleading_python | no_capped_items | effort_low | effort_high |       165 |   0.5644 |   0.8242 |   0.2598 |  0.2121 |  0.3099 | 0.0002 |    nan |      nan |             nan |
| qwen3_4b    | xstest                | no_capped_items | nothink    | think       |       223 |   0.7096 |   0.6383 |  -0.0714 | -0.1068 | -0.0379 | 0.0004 |    nan |      nan |             nan |
| qwen3_8b    | gsm8k                 | no_capped_items | nothink    | think       |       499 |   0.9335 |   0.9597 |   0.0262 |  0.0137 |  0.0396 | 0.0004 |    nan |      nan |             nan |
| gpt_oss_20b | umwp                  | no_capped_items | effort_low | effort_high |       515 |   0.7573 |   0.7876 |   0.0303 |  0.0139 |  0.0469 | 0.0004 |    nan |      nan |             nan |
| gpt_oss_20b | gsm8k                 | no_capped_items | effort_low | effort_high |       486 |   0.9532 |   0.9725 |   0.0193 |  0.0095 |  0.0303 | 0.0005 |    nan |      nan |             nan |
| qwen3_8b    | ist_misleading_python | no_capped_items | nothink    | think       |       500 |   0.2922 |   0.3325 |   0.0402 |  0.0167 |  0.064  | 0.0009 |    nan |      nan |             nan |
| qwen3_8b    | falseqa               | no_capped_items | nothink    | think       |       499 |   0.747  |   0.7901 |   0.0431 |  0.0204 |  0.0654 | 0.0012 |    nan |      nan |             nan |
| qwen3_8b    | ist_misleading_math   | no_capped_items | nothink    | think       |       500 |   0.8625 |   0.831  |  -0.0315 | -0.0506 | -0.0127 | 0.0036 |    nan |      nan |             nan |
| qwen3_8b    | xstest                | no_capped_items | nothink    | think       |       224 |   0.7249 |   0.676  |  -0.049  | -0.0816 | -0.0187 | 0.0038 |    nan |      nan |             nan |
| qwen3_4b    | falseqa               | no_capped_items | nothink    | think       |       498 |   0.7353 |   0.7666 |   0.0312 |  0.0083 |  0.0538 | 0.0106 |    nan |      nan |             nan |
| gpt_oss_20b | ist_paradoxes         | no_capped_items | effort_low | effort_high |       227 |   0.728  |   0.7852 |   0.0573 |  0.0182 |  0.098  | 0.0116 |    nan |      nan |             nan |
| gpt_oss_20b | math500               | no_capped_items | effort_low | effort_high |       209 |   0.9599 |   0.9815 |   0.0215 |  0.0066 |  0.0377 | 0.0124 |    nan |      nan |             nan |
| qwen3_4b    | kuq                   | no_capped_items | nothink    | think       |       496 |   0.6759 |   0.6512 |  -0.0247 | -0.0442 | -0.0053 | 0.0192 |    nan |      nan |             nan |
| qwen3_8b    | gsm_ic                | no_capped_items | nothink    | think       |       496 |   0.9691 |   0.9871 |   0.018  |  0.002  |  0.0384 | 0.0593 |    nan |      nan |             nan |
| qwen3_4b    | ifeval                | no_capped_items | nothink    | think       |       254 |   0.8068 |   0.8371 |   0.0303 | -0.0002 |  0.0605 | 0.061  |    nan |      nan |             nan |
| gpt_oss_20b | popqa                 | no_capped_items | effort_low | effort_high |       213 |   0.4824 |   0.5059 |   0.0235 | -0.0012 |  0.0493 | 0.0851 |    nan |      nan |             nan |
| qwen3_4b    | gsm_ic                | no_capped_items | nothink    | think       |       498 |   0.9681 |   0.9885 |   0.0203 |  0.0016 |  0.0446 | 0.0926 |    nan |      nan |             nan |
| qwen3_4b    | popqa                 | no_capped_items | nothink    | think       |       499 |   0.1671 |   0.1786 |   0.0115 | -0.0016 |  0.0249 | 0.1041 |    nan |      nan |             nan |
| qwen3_8b    | popqa                 | no_capped_items | nothink    | think       |       491 |   0.2299 |   0.2166 |  -0.0132 | -0.0286 |  0.0019 | 0.1175 |    nan |      nan |             nan |
| qwen3_8b    | ifeval                | no_capped_items | nothink    | think       |       256 |   0.842  |   0.8628 |   0.0208 | -0.0034 |  0.0459 | 0.1301 |    nan |      nan |             nan |
| qwen3_4b    | ist_zebra             | no_capped_items | nothink    | think       |        10 |   0.6375 |   0.8    |   0.1625 |  0.0188 |  0.3438 | 0.1301 |    nan |      nan |             nan |
| gpt_oss_20b | xstest                | no_capped_items | effort_low | effort_high |       164 |   0.9116 |   0.9276 |   0.016  | -0.0046 |  0.0396 | 0.2004 |    nan |      nan |             nan |
| gpt_oss_20b | gsm_ic                | no_capped_items | effort_low | effort_high |       481 |   0.9782 |   0.9906 |   0.0125 | -0.0038 |  0.034  | 0.2895 |    nan |      nan |             nan |
| gpt_oss_20b | falseqa               | no_capped_items | effort_low | effort_high |       267 |   0.787  |   0.7973 |   0.0103 | -0.0117 |  0.0328 | 0.4186 |    nan |      nan |             nan |
| gpt_oss_20b | kuq                   | no_capped_items | effort_low | effort_high |       214 |   0.7442 |   0.7401 |  -0.0041 | -0.0327 |  0.0239 | 0.8459 |    nan |      nan |             nan |
| qwen3_8b    | kuq                   | no_capped_items | nothink    | think       |       495 |   0.6677 |   0.6699 |   0.0023 | -0.0173 |  0.0217 | 0.8474 |    nan |      nan |             nan |
| gpt_oss_20b | strongreject          | no_capped_items | effort_low | effort_high |       156 |   0.9976 |   1      |   0.0024 |  0      |  0.0072 | 1      |    nan |      nan |             nan |

## dose-response (GEE, level 0..4)

| model    | benchmark             |   b_level |   p_level |   b_level2 |   p_level2 |   acc_nothink |   acc_think_b256 |   acc_think_b1024 |   acc_think_b4096 |   acc_think |   q_level2 |
|:---------|:----------------------|----------:|----------:|-----------:|-----------:|--------------:|-----------------:|------------------:|------------------:|------------:|-----------:|
| qwen3_4b | falseqa               |    0.1559 |    0.001  |    -0.0314 |     0.0003 |        0.7346 |           0.7825 |            0.763  |            0.7662 |      0.7668 |     0.0007 |
| qwen3_4b | gsm8k                 |    0.2499 |    0.0005 |    -0.0238 |     0.1075 |        0.9226 |           0.9342 |            0.9478 |            0.954  |      0.9558 |     0.1406 |
| qwen3_4b | gsm_ic                |    0.1257 |    0.61   |     0.0418 |     0.5211 |        0.9682 |           0.9685 |            0.9795 |            0.9862 |      0.9882 |     0.5715 |
| qwen3_4b | ifeval                |    0.1532 |    0.0473 |    -0.0261 |     0.0703 |        0.7979 |           0.8231 |            0.8282 |            0.8296 |      0.8301 |     0.0996 |
| qwen3_4b | ist_misleading_math   |    0.4446 |    0      |    -0.0252 |     0.2021 |        0.8908 |           0.915  |            0.9505 |            0.9638 |      0.967  |     0.2545 |
| qwen3_4b | ist_misleading_python |    0.5844 |    0      |    -0.1046 |     0      |        0.2626 |           0.3425 |            0.4582 |            0.4198 |      0.4115 |     0      |
| qwen3_4b | ist_paradoxes         |    0.5767 |    0      |    -0.097  |     0      |        0.4816 |           0.5891 |            0.6794 |            0.6762 |      0.665  |     0      |
| qwen3_4b | ist_zebra             |    0.1029 |    0.172  |     0.0097 |     0.611  |        0.2844 |           0.3262 |            0.3312 |            0.3713 |      0.4188 |     0.6492 |
| qwen3_4b | kuq                   |   -0.0984 |    0.0048 |     0.0185 |     0.0044 |        0.6782 |           0.6522 |            0.6512 |            0.6522 |      0.6528 |     0.0074 |
| qwen3_4b | math500               |   -0.1919 |    0.0146 |     0.1672 |     0      |        0.8335 |           0.8215 |            0.8675 |            0.931  |      0.9655 |     0      |
| qwen3_4b | nq_swap               |    0.2886 |    0      |    -0.047  |     0      |        0.7179 |           0.7667 |            0.7919 |            0.7948 |      0.7942 |     0      |
| qwen3_4b | popqa                 |    0.0719 |    0.0501 |    -0.014  |     0.0354 |        0.1668 |           0.1805 |            0.1788 |            0.1782 |      0.1782 |     0.0524 |
| qwen3_4b | strongreject          |   -0.7774 |    0      |     0.1309 |     0      |        0.9515 |           0.8926 |            0.867  |            0.8622 |      0.8622 |     0      |
| qwen3_4b | syco_answer           |    0.2257 |    0      |    -0.0381 |     0      |        0.5821 |           0.6344 |            0.6542 |            0.6556 |      0.6559 |     0      |
| qwen3_4b | triviaqa              |    0.1926 |    0      |    -0.0345 |     0      |        0.4461 |           0.497  |            0.5088 |            0.5072 |      0.5068 |     0      |
| qwen3_4b | umwp                  |    0.3396 |    0      |    -0.1122 |     0      |        0.7206 |           0.7783 |            0.7867 |            0.6917 |      0.6442 |     0      |
| qwen3_4b | xstest                |   -0.2379 |    0.0001 |     0.0431 |     0.0002 |        0.7068 |           0.6444 |            0.6411 |            0.64   |      0.64   |     0.0004 |
| qwen3_8b | falseqa               |    0.1823 |    0.0003 |    -0.0323 |     0.0005 |        0.7471 |           0.7877 |            0.786  |            0.79   |      0.7902 |     0.0009 |
| qwen3_8b | gsm8k                 |    0.1972 |    0.0076 |    -0.0123 |     0.4184 |        0.9319 |           0.9395 |            0.9505 |            0.9588 |      0.9595 |     0.4905 |
| qwen3_8b | gsm_ic                |    0.1425 |    0.4944 |     0.0264 |     0.6956 |        0.9678 |           0.9705 |            0.9768 |            0.9855 |      0.9862 |     0.7166 |
| qwen3_8b | ifeval                |    0.1385 |    0.0652 |    -0.0262 |     0.0771 |        0.8252 |           0.8421 |            0.8495 |            0.8481 |      0.8449 |     0.1049 |
| qwen3_8b | ist_misleading_math   |   -0.2996 |    0      |     0.0664 |     0      |        0.8625 |           0.794  |            0.8258 |            0.8245 |      0.831  |     0      |
| qwen3_8b | ist_misleading_python |   -0.0299 |    0.4251 |     0.0216 |     0.0089 |        0.2922 |           0.284  |            0.2875 |            0.3282 |      0.3325 |     0.0144 |
| qwen3_8b | ist_paradoxes         |    0.7218 |    0      |    -0.1466 |     0      |        0.4855 |           0.6478 |            0.6809 |            0.6878 |      0.625  |     0      |
| qwen3_8b | ist_zebra             |    0.1135 |    0.1646 |     0.0125 |     0.5183 |        0.2406 |           0.27   |            0.2912 |            0.335  |      0.38   |     0.5715 |
| qwen3_8b | kuq                   |    0.0026 |    0.9388 |     0.0002 |     0.9806 |        0.6706 |           0.6642 |            0.675  |            0.6718 |      0.6715 |     0.9806 |
| qwen3_8b | math500               |   -0.0608 |    0.449  |     0.1253 |     0      |        0.8398 |           0.851  |            0.879  |            0.9355 |      0.9665 |     0      |
| qwen3_8b | nq_swap               |    0.1882 |    0.0005 |    -0.0245 |     0.0128 |        0.745  |           0.765  |            0.7983 |            0.8044 |      0.8046 |     0.0198 |
| qwen3_8b | popqa                 |   -0.0498 |    0.169  |     0.0081 |     0.2276 |        0.2276 |           0.2178 |            0.2168 |            0.2148 |      0.2148 |     0.2764 |
| qwen3_8b | strongreject          |   -0.9646 |    0      |     0.1621 |     0      |        0.9623 |           0.9014 |            0.863  |            0.8606 |      0.8606 |     0      |
| qwen3_8b | syco_answer           |    0.204  |    0      |    -0.0338 |     0      |        0.6734 |           0.7123 |            0.7328 |            0.7334 |      0.7332 |     0      |
| qwen3_8b | triviaqa              |    0.1866 |    0      |    -0.0328 |     0      |        0.5605 |           0.6035 |            0.622  |            0.6188 |      0.6185 |     0      |
| qwen3_8b | umwp                  |    0.2843 |    0      |    -0.1034 |     0      |        0.7593 |           0.8112 |            0.7985 |            0.7231 |      0.6704 |     0      |
| qwen3_8b | xstest                |   -0.1996 |    0.0005 |     0.04   |     0.0002 |        0.7261 |           0.6631 |            0.6808 |            0.6802 |      0.6802 |     0.0004 |

## size x mode (Qwen3-4B vs 8B)

| benchmark             |   b_think |   b_think_x_8b |   p_interaction |   q_interaction |
|:----------------------|----------:|---------------:|----------------:|----------------:|
| falseqa               |    0.1718 |         0.0713 |          0.328  |          0.5706 |
| gsm8k                 |    0.5941 |        -0.0448 |          0.7385 |          0.8369 |
| gsm_ic                |    1.0145 |        -0.1431 |          0.686  |          0.833  |
| ifeval                |    0.213  |        -0.07   |          0.5273 |          0.7942 |
| ist_misleading_math   |    1.2793 |        -1.5227 |          0      |          0      |
| ist_misleading_python |    0.6746 |        -0.487  |          0      |          0      |
| ist_paradoxes         |    0.7594 |        -0.1905 |          0.0086 |          0.0488 |
| ist_zebra             |    0.595  |         0.0648 |          0.5606 |          0.7942 |
| kuq                   |   -0.1146 |         0.1186 |          0.0308 |          0.1048 |
| math500               |    1.721  |        -0.0153 |          0.9116 |          0.9609 |
| nq_swap               |    0.4161 |        -0.073  |          0.3356 |          0.5706 |
| popqa                 |    0.0806 |        -0.1553 |          0.0137 |          0.0581 |
| strongreject          |   -1.1435 |        -0.2772 |          0.3192 |          0.5706 |
| syco_answer           |    0.3135 |        -0.0261 |          0.6464 |          0.833  |
| triviaqa              |    0.2433 |        -0.0033 |          0.9609 |          0.9609 |
| umwp                  |   -0.3541 |        -0.0845 |          0.0528 |          0.1496 |
| xstest                |   -0.3022 |         0.0876 |          0.2992 |          0.5706 |
