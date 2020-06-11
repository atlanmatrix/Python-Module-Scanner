# What's this?
This is a python modules analysis tool.

## Usage
Before you start, you should copy ```./default/config.py``` file to ```./``` diretory and modify the default configuration.

```shell
cp ./default/config.py ./
vim ./config.py
```

### Show all modules used in your projects
```shell
python app.py
```

## Todo list
- 忽略注释中的导入语句
- ~~忽略导入的本地模块~~
- 读取 pip 已安装的模块进行安装的优化
- 模块重复引入时进行警告⚠️
- 对可合并的 from ... import 语句进行提示
- 对通配符引入提供建议
