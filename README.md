# llmperf-Tpot

针对性能测试的TPOT需要写一个脚本来从结果中计算指标，

公式：TPOT = （end_to_end_latency_s - ttft_s）/ （number_output_tokens-1），

需要先把每个请求的TPOT计算出来然后排序，找出25%，50%，75%，99.9%的TPOT