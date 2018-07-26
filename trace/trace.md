# 溯源报告
报告ID： {{ id }}

|项目|值|
| ------  | ----------- |
| 发起时间 |  {{ start_time }} |
| 完成时间 | {{ finish_time }} |
| 洋葱地址 | {{ tor_address }} |
| 网站名称 | {{ site_name }} |
| IP地址  | {{ ip_address }} |
| 国家地区 | {{ country }} |
| 服务类型 | {{ service_type }} |


# 详细信息

## 探测路径参数：

{{ client_ip }} ->
{% for i in path %}
{{ i }} -> 
{% endfor %}
{{ ip_address }}

接收任务客户端:

|项目|值|
| ---- | --- |
{% for i in clients %}| Client {{ loop.index }} | {{ i }} |
{% endfor %}

连接信息:

|项目|值|
| ---- | --- |
| stream id | {{ stream_id }} |
| cric id 1 | {{ circ_id[0] }} |
| cric id 2 | {{ circ_id[1] }} |
| cric id 3 | {{ circ_id[2] }} |
| cric id 4 | {{ circ_id[3] }} |

## 目标IP详情

{{ details }}
