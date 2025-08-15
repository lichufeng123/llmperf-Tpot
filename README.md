# llmperf-Tpot

## 针对性能测试的TPOT需要写一个脚本来从结果中计算指标并统计各个分位中的值

1.首先需要先从**个体请求级别的详细性能数据**文件deepseekr1_4000_1500_individual_responses.json计算**TPOT**= （end_to_end_latency_s - ttft_s）/ （number_output_tokens-1）

计算TPOT采取以下两年忽略干扰数据：

- 过滤 `number_output_tokens = 0` 的异常请求，避免除以 0；
- 减去 **TTFT**（生成首token延迟），只计算 decode 部分耗时



2.每个请求的TPOT计算出来后根据升序排序，找出25%，50%，75%，99.9%的TPOT。



- 定位分位方法： ***\*"线性插值法"（linear interpolation of ranks）， 在 N 个有序数据中，有 N−1 个“间隔”可插值，分位数通常落在这些间隔之间，因此分位数的位置应该按 p × (N - 1) 来算\****
  - 举例：总共148个数，找p25的数，实际上找的是处于第25个间隔的数，通过特殊公式计算这个数
- 分位数value计算方式：lower + (upper - lower) × fraction 
  - 举例：p25 = values[36] + 0.75 × (values[37] - values[36])