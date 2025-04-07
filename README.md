Flask + Python3.6 + BootStrap + MySql + Redis 实现的接口自动化测试平台。

1.安装依赖包
    pip3 install -r requirements.txt
2.更改配置文件
    config文件中MySql、Redis、测试环境等相关配置文件
3.运行
    python manage.py run即可 成功可以访问



初始数据库数据：
INSERT INTO `qatools`.`interface` (`id`, `interfaceDescription`, `interfaceURL`, `request_method`, `creator`, `add_time`, `mender`, `edit_time`, `module`) VALUES (1, '接口描述1', '/case/show', 'get', 'zhao', '2023-07-25 20:57:27', 'zhao', '2023-07-25 20:57:29', 'case');
INSERT INTO `qatools`.`interface` (`id`, `interfaceDescription`, `interfaceURL`, `request_method`, `creator`, `add_time`, `mender`, `edit_time`, `module`) VALUES (2, '接口描述2', '/user/login', 'post', 'zhao', '2023-07-25 20:57:10', 'zhao', '2023-07-25 20:57:18', '登录');
INSERT INTO `qatools`.`interface` (`id`, `interfaceDescription`, `interfaceURL`, `request_method`, `creator`, `add_time`, `mender`, `edit_time`, `module`) VALUES (3, '添加case', '/case/add', 'post', 'zhao', '2023-07-25 21:07:08', 'zhao', '2023-07-25 21:07:14', 'case');
INSERT INTO `qatools`.`case` (`id`, `caseDescription`, `request`, `response`, `creator`, `add_time`, `mender`, `edit_time`, `module`, `flowID`, `InterfaceID`) VALUES (2, 'case查询', '', '{\'查询成功\'}', 'zhao', '2023-07-25 21:04:14', 'zhao', '2023-07-25 21:04:20', 'case', '1', 1);
INSERT INTO `qatools`.`case` (`id`, `caseDescription`, `request`, `response`, `creator`, `add_time`, `mender`, `edit_time`, `module`, `flowID`, `InterfaceID`) VALUES (3, 'case添加', '{\'case添加的参数\'}', '{\'添加成功\'}', 'zhao', '2023-07-25 21:06:17', 'zhao', '2023-07-25 21:06:22', 'case', '1', 3);
INSERT INTO `qatools`.`flow` (`id`, `flowDescription`, `case_list`, `creator`, `add_time`, `mender`, `edit_time`, `module`) VALUES (1, '添加case', '[2,3]', 'zhao', '2023-07-25 21:05:25', 'zhao', '2023-07-25 21:05:30', 'case');









# qatools
