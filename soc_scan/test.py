# coding: utf-8

from pymongo import MongoClient
import json





Mongo = MongoDB('192.168.12.124', 27017, 'xunfeng', 'scan', 'scan123')


# 搜索页
def Search():
    '''
    @app.route('/filter')
    @logincheck
    def Search():
    return render_template('search.html')
    '''
    pass


# 删除所有
def Deleteall():
    '''
    @app.route('/deleteall', methods=['post'])
    @logincheck
    @anticsrf
    def Deleteall():
        Mongo.coll['Task'].remove({})
        return 'success'
    '''
    pass


# 搜索结果页
def Main():
    '''
    q = request.args.get('q', '')
    page = int(request.args.get('page', '1'))
    plugin = Mongo.coll['Plugin'].find()  # 插件列表
    plugin_type = plugin.distinct('type')  # 插件类型列表
    if q:  # 基于搜索条件显示结果
        result = q.strip().split(';')
        query = querylogic(result)
        cursor = Mongo.coll['Info'].find(query).sort('time', -1).limit(page_size).skip((page - 1) * page_size)
        return render_template('main.html', item=cursor, plugin=plugin, itemcount=cursor.count(),
                               plugin_type=plugin_type, query=q)
    else:  # 自定义，无任何结果，用户手工添加
        return render_template('main.html', item=[], plugin=plugin, itemcount=0, plugin_type=plugin_type)
    '''

    plugin = Mongo.coll['Plugin'].find()  # 插件列表
    plugin_type = plugin.distinct('type')  # 插件类型列表
    for item in plugin:
        print item
    query = {}
    cursor = Mongo.coll['Info'].find(query).limit(10)
    for item in cursor:
        print item


if __name__ == '__main__':
    # 搜索结果页
    Main()
