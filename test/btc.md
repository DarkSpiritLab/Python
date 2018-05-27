# 区块链转账示警
|内容|值|
| ----- | ---- |
| 币种 | {{ coin_type }} |
|监控账户 | {{ receive_account }} |
{% if onion_site %} |洋葱地址 | {{ onion_site }} | {% endif %}
{% if username %} |相关用户 | {{ username }} | {% endif %}
|接收金额 | {{ send_amount }} |
|发现时间 |{{ time }}|
|货币 |{{ currency }} |


# 详情
|内容|值|
| ---  |  ----- |
|大小   | {{ size }} bytes |
|转出账户 | {% for i in output_accounts %} {{ i }}<br/> {% endfor %} |
|转入账户 | {% for i in input_accounts %} {{ i }}<br/> {% endfor %} |
|交易哈希 | {{ hash }} |
|重量 | {{ weight }} |
|转出金额 | {{ recv_amount }} |
|手续费 | {{ fees }} |
|块号 |{{ block_height }}|
|区块时间戳 | {{ block_time }} |


详情： [点击查看]( https://blockchain.info/tx/ 

{{ url }})
资金流向图： [点击查看](https://blockchain.info/tree/ 

{{ tx_id }})
