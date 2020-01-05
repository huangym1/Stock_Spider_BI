# 沪深个股爬虫+FineBI分析
## 项目背景
了解并掌握FineBI基本操作

## 爬取方法
- 使用requests+正则表达式爬取个股列表
- 使用网易财经网提供的接口爬取个股历史数据

## 项目步骤
1.爬取部分个股历史数据并存成本地excel文件  
![image](https://github.com/huangym1/Stock_Spider_BI/blob/master/images/stock.png)  
2.合并多个excel表
3.在FineBI创建业务包，并添加合并后的excel表
4.根据业务需求创建仪表板  
![image](https://github.com/huangym1/Stock_Spider_BI/blob/master/images/FineBI.png)

## TODO
- 获取全量沪深个股历史数据，并使用FineBI作行情的深入分析
- 获取全量基金历史数据，并使用FineBI进行分析
