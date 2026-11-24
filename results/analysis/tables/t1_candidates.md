| test   | model    | benchmark           | contrast            |   items |   lo % |   hi % | effect pp [95% CI]   | BH q   | flips hurt/helped   | in test   |
|:-------|:---------|:--------------------|:--------------------|--------:|-------:|-------:|:---------------------|:-------|:--------------------|:----------|
| P1     | Qwen3-4B | StrongREJECT        | think − nothink     |     156 |   95.2 |   86.2 | -8.9 [-12.4, -5.7]   | <.001  | 4/0                 | yes       |
| P1     | Qwen3-8B | StrongREJECT        | think − nothink     |     156 |   96.2 |   86.1 | -10.2 [-13.5, -7.1]  | <.001  | 7/0                 | yes       |
| P2     | Qwen3-4B | XSTest (refuse)     | think − nothink     |     112 |   47.8 |   30.5 | -17.2 [-23.0, -11.6] | <.001  | 10/1                | yes       |
| P2     | Qwen3-8B | XSTest (refuse)     | think − nothink     |     112 |   52.6 |   39.7 | -13.0 [-18.4, -7.6]  | <.001  | 12/1                | yes       |
| P3     | Qwen3-4B | UMWP (unanswerable) | think − nothink     |     300 |   44.5 |   29   | -15.4 [-18.8, -12.1] | <.001  | 22/3                | yes       |
| P3     | Qwen3-8B | UMWP (unanswerable) | think − nothink     |     300 |   52   |   34.1 | -17.9 [-21.7, -14.1] | <.001  | 29/2                | yes       |
| P4     | Qwen3-4B | Misleading math     | think − nothink     |     500 |   89.1 |   96.7 | +7.6 [+6.0, +9.4]    | <.001  | 1/7                 | context   |
| P4     | Qwen3-8B | Misleading math     | think − nothink     |     500 |   86.2 |   83.1 | -3.1 [-5.0, -1.3]    | 0.002  | 14/2                | yes       |
| P5     | Qwen3-4B | UMWP                | think − think_b1024 |     600 |   78.7 |   64.4 | -14.2 [-16.1, -12.5] | <.001  | –                   | yes       |
| P5     | Qwen3-8B | UMWP                | think − think_b1024 |     600 |   79.9 |   67   | -12.8 [-14.6, -11.1] | <.001  | –                   | yes       |
| P6     | Qwen3-4B | Paradoxes           | think − think_b4096 |     400 |   67.6 |   66.5 | -1.1 [-2.0, -0.2]    | 0.05   | –                   | context   |
| P6     | Qwen3-8B | Paradoxes           | think − think_b4096 |     400 |   68.8 |   62.5 | -6.3 [-7.8, -4.8]    | <.001  | –                   | yes       |
| P7     | Qwen3-4B | Misleading python   | think − think_b1024 |     500 |   45.8 |   41.2 | -4.7 [-6.5, -2.9]    | <.001  | –                   | yes       |
| P7     | Qwen3-8B | Misleading python   | think − think_b1024 |     500 |   28.7 |   33.2 | +4.5 [+2.9, +6.2]    | <.001  | –                   | context   |
