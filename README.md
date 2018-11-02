# ApiTest
[![Build Status](https://travis-ci.org/cooleasyhan/apitest.svg?branch=master)](https://travis-ci.org/cooleasyhan/apitest)


## 特性
1. 利用requests发送http请求
2. 支持自定义python function，用于token计算，加密等操作 apitest/func.py:g
3. 数据设定支持jinja2模板 (自定义function--f.xx  引用已填写数据 v.xx )
    - 录入当前时间
        - {{ f.unix_time() }}
    - 计算token 
        - {{ f.token(v.source_system_code, v.token2, v.timestamp) }}
    - 根据row_cnt生成json串 
        - [{%for i in range(v.row_cnt)%}   {"name":"test"} {% if not loop.last %},  {%endif%} {%endfor%} ]
    - 下划线开头的参数不会被传送，仅用于计算
4. 支持结果检验
5. 支持locust压测
6. 提供http接口一键测试相应testcase  /api/run
7. 用例复制


## 截图

### 测试用例管理
![tc_edit](screenshort/tc_edit.jpeg)
![tc_edit](screenshort/tc_edit2.jpeg)
![tc_actions](screenshort/tc_actions.jpeg)

### 用例结果展示
![tc_rpt1](screenshort/tc_rpt1.jpeg)
![tc_rpt2](screenshort/tc_rpt2.jpeg)

### 项目管理
![proj_edit](screenshort/proj_edit.jpeg)
![proj_actions](screenshort/proj_actions.jpeg)
 