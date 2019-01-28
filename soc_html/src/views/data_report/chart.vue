<template>
    <div class="pos-r">
        <div :id="id" :style="'width:'+width+';height:150px;margin:0 auto;'"
             v-if="(type!='number') && (type!='table') && (type!='scatter') && (type!='loop') && (type!='funnel')"></div>
        <div :style="'width:'+width+';height:150px;margin:0 auto;'" v-if="type=='number'">
            <div style="padding-top:40px;">
                <p class="ys-info-color textC">{{name}}</p>
                <p class="textC" v-if="unit != MODULE"><span class="font36 m-r-5">{{total}}</span>个</p>
                <p class="textC" v-if="unit == MODULE"><span class="font36 m-r-5">{{changeUnit(total)}}</span></p>
            </div>
        </div>
        <div v-if="type=='table'" style="word-break: keep-all;white-space: nowrap">
            <table class="ys-table">
                <thead>
                <tr>
                    <th>序号</th>
                    <th v-for="row in splice_tool(info.labels)" track-by="$index">{{row}}</th>
                </tr>
                </thead>
                <tbody v-if="info.data && info.data.length">
                <tr v-for="list in splice_tool(info.data)">
                    <td>{{$index + 1}}</td>
                    <td v-for="colCon in list.data"
                        track-by="$index">
                        {{colCon}}
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
        <!-- 散点图 -->
        <scatter-chart v-if="type=='scatter'"
                       :height="'150'"
                       :id="id"
                       :unit="unit == MODULE && name != '会话拒绝统计' ? 'band' : 'number'"
                       :datas="datas"></scatter-chart>
        <!-- 环形图 -->
        <loop-chart v-if="type=='loop'"
                    :height="'150'"
                    :datas="datas"
                    :id="id"
                    :name="name"></loop-chart>
    </div>
</template>
<style scoped>

</style>
<script>
    let echarts = require('echarts/lib/echarts');
    let collect = require('collect.js')
    import scatterChart from '../../components/chart/scatter-chart'
    import lingBarChart from '../../components/chart/ling-bar-chart'
    import loopChart from '../../components/chart/loop'

    export default {
        name: "template-chart",
        props: {
            width: {
                default: '95%'
            },
            type: {
                default: "line"
            },
            info: {},
            name: "",
            unit: {
                default: "number"
            }
        },
        data() {
            return {
                barColor: ['#4993fd', '#3a9be5', '#27a6c6', '#12b2a3', '#03bb89'],
                prevId: "",
                chart: '',
                str: '',
                timer: '',
                MODULE: 'band'      //网络数据模块
            }
        },
        computed: {
            datas: function () {
                if (this.info.labels && this.info.labels.length) {
                    let y = {};
                    for (let i = 0; i < this.info.data.length; i++) {
                        y[this.info.data[i].name] = this.info.data[i].data;
                    }
                    let obj = {
                        'x': {
                            '日期': this.info.labels
                        },
                        'y': y
                    }
                    return obj;
                } else {
                    return {};
                }
            },
            id: function () {
                return this.type + "-template-chart-" + this.str;
            },
            total: function () {
                let num = 0;
                for (let x in this.info.data) {
                    num += collect(this.info.data[x].data).sum()
                }
                return num;
            },
        },
        ready() {
            this.initStr();
        },
        methods: {
            initStr() {
                var str = "";
                for (var i = 0; i < 6; i++) {
                    var num = Math.random() * 9;
                    num = parseInt(num, 10);
                    str += num;
                }
                this.str = str;
            },
            setChart() {
                if (this.chart) {
                    this.chart.dispose();
                }
                if (this.type == "line") {
                    this.setLineChart()
                } else if (this.type == "pie") {
                    this.setPieChart()
                } else if (this.type == "bar_x") {
                    this.setBarXChart()
                } else if (this.type == "bar_y") {
                    this.setBarYChart()
                } else if (this.type == "bar_pile_x") {
                    this.setBarXChart()
                } else if (this.type == "bar_pile_y") {
                    this.setBarYChart()
                } else if (this.type == "number") {
                    this.setNumberChart()
                }
            },
            setLineChart() {
                if (!document.getElementById(this.id)) return false;
                let self = this;
                let curInfo = this.info;
                let curSeries = [];
                let xData = [];
                for (let x in curInfo.data) {
                    curSeries.push({
                        data: curInfo.data[x].data,
                        type: 'line',
                        name: curInfo.data[x].name
                    })
                }
                for (let x in curInfo.labels) {
                    xData.push(curInfo.labels[x])
                }
                this.chart = echarts.init(document.getElementById(this.id));
                let option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            lineStyle: {
                                color: "#dfdfe7",
                                opacity: 0.2
                            },
                        },
                        formatter: function (params) {
                            let str = params[0].name
                            for (var i = 0; i < params.length; i++) {
                                if (self.unit == self.MODULE && self.name != '会话拒绝统计') {
                                    str += "<br/>" + params[i].seriesName + ":" + self.changeUnit(params[i].value)
                                } else {
                                    str += "<br/>" + params[i].seriesName + ":" + self.changeWanUnit(params[i].value)
                                }
                            }
                            return str
                        },
                    },
                    grid: {
                        top: 10,
                        bottom: 10,
                        left: 30,
                        right: 30,
                        containLabel: true
                    },
                    calculable: true,
                    color: ['rgba(0,189,133,0.8)', 'rgba(233,97,87,0.8)', 'rgba(218,187,97,0.8)', 'rgba(74,146,255,0.8)'],
                    xAxis: {
                        type: 'category',
                        data: xData,
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        },
                        axisTick: {
                            show: false,
                        },
                        axisLabel: {textStyle: {color: "#dfdfe7"}}
                    },
                    yAxis: {
                        type: 'value',
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        },
                        axisTick: {
                            show: false,
                        },
                        splitNumber: 5,
                        axisLabel: {
                            textStyle: {color: "#dfdfe7"},
                            formatter: function (value) {
                                if (self.unit == self.MODULE && self.name != '会话拒绝统计') {
                                    return self.changeUnit(value);
                                } else {
                                    return self.changeWanUnit(value);
                                }
                            },
                        },//y轴坐标的字颜色
                        splitLine: {
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        }
                    },
                    series: curSeries
                };
                this.chart.setOption(option);
                window.addEventListener('resize', this.chart)
            },
            setPieChart() {
                if (!document.getElementById(this.id)) return false;
                let self = this;
                let curInfo = this.info;
                let curSeries = [];
                let legentData = [];
                if (curInfo.data.length > 1) {
                    for (let x in curInfo.data) {
                        let sum = 0;
                        curInfo.data[x].data.forEach(function (val) {
                            sum += val
                        })
                        curSeries.push({
                            name: curInfo.data[x].name,
                            value: sum,
                        });
                        legentData.push(curInfo.data[x].name)
                    }
                } else if (curInfo.data.length == 1) {
                    curInfo.data[0].data.forEach(function (val, x) {
                        curSeries.push({
                            name: curInfo.labels[x],
                            value: curInfo.data[0].data[x],
                        });
                    })
                    legentData = [].concat(curInfo.labels);
                }
                this.chart = echarts.init(document.getElementById(this.id));
                let option = {
                    tooltip: {
                        trigger: 'item',
                        formatter: function (params) {
                            let str = '';
                            if (self.unit == self.MODULE && self.name != '会话拒绝统计') {
                                str =params.name + ":" + self.changeUnit(params.value) + '(' + params.percent + '%)'
                            } else {
                                str = params.name + ":" + self.changeWanUnit(params.value) + '(' + params.percent + '%)'
                            }
                            return str
                        },
                    },
                    color: ['#00bd85','#e96157','#dabb61','#0c67ff','#4a92ff','#8375d0','#5dc962','#008974','#b06cae','#8375d0'],
                    grid: {
                        top: '30',
                        bottom: '20',
                        left: 30,
                        right: 30,
                        containLabel: true
                    },
                    legend: {
                        show: true,
                        x: 'center',
                        y: 'bottom',
                        bottom: 3,
                        data: legentData,
                        textStyle: {
                            color: "#f2f2f2"
                        },
                        itemWidth: 10,
                        itemHeight: 10,
                        itemGap: 10
                    },
                    series: [
                        {
                            name: "",
                            type: 'pie',
                            radius: ['23%', '67%'],
                            center: ['50%', '40%'],
                            data: curSeries,
                            itemStyle: {
                                normal: {
                                    opacity: 0.8
                                }
                            },
                            label: {
                                normal: {
                                    show: false
                                }
                            }
                        }
                    ]
                };
                this.chart.setOption(option);
                window.addEventListener('resize', this.chart)
            },
            setBarXChart() {
                if (!document.getElementById(this.id)) return false;
                let self = this;
                let curInfo = this.info;
                let curSeries = [];
                let xData = [];
                for (let x in curInfo.data) {
                    let obj = {
                        name: curInfo.data[x].name,
                        type: 'bar',
                        barMaxWidth: 20,
                        data: curInfo.data[x].data,
                    };
                    if (self.type == 'bar_pile_x') {
                        obj.stack = '总量'
                    }
                    curSeries.push(obj)
                }
                for (let x in curInfo.labels) {
                    xData.push(curInfo.labels[x])
                }
                this.chart = echarts.init(document.getElementById(this.id));
                let option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        },
                        formatter: function (params) {
                            let str = params[0].name
                            for (var i = 0; i < params.length; i++) {
                                if (self.unit == self.MODULE && self.name != '会话拒绝统计') {
                                    str += "<br/>" + params[i].seriesName + ":" + self.changeUnit(params[i].value)
                                } else {
                                    str += "<br/>" + params[i].seriesName + ":" + self.changeWanUnit(params[i].value)
                                }
                            }
                            return str
                        },
                    },
                    legend: {
                        show: false
                    },
                    grid: {
                        top: '10',
                        bottom: '0',
                        left: 30,
                        right: 30,
                        containLabel: true
                    },
                    calculable: true,
                    color: ['rgba(0,189,133,0.8)', 'rgba(233,97,87,0.8)', 'rgba(218,187,97,0.8)', 'rgba(74,146,255,0.8)'],
                    xAxis: [
                        {
                            type: 'category',
                            data: xData,
                            axisLine: {
                                show: true,
                                lineStyle: {
                                    color: "#46578e",
                                    opacity: "0.75"
                                }
                            },
                            axisTick: {
                                show: false,
                            },
                            axisLabel: {textStyle: {color: "#dfdfe7"}},//x轴坐标的字颜色
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            axisLine: {
                                show: true,
                                lineStyle: {
                                    color: "#46578e",
                                    opacity: "0.75"
                                }
                            },
                            axisTick: {
                                show: false,
                            },
                            splitNumber: 5,
                            axisLabel: {
                                textStyle: {color: "#dfdfe7"},
                                formatter: function (value) {
                                    if (self.unit == self.MODULE && self.name != '会话拒绝统计') {
                                        return self.changeUnit(value);
                                    } else {
                                        return self.changeWanUnit(value);
                                    }
                                },
                            },//y轴坐标的字颜色
                            splitLine: {
                                lineStyle: {
                                    color: "#46578e",
                                    opacity: "0.75"
                                }
                            }
                        }
                    ],
                    series: curSeries
                };
                this.chart.setOption(option);
                window.addEventListener('resize', this.chart)
            },
            setBarYChart() {
                if (!document.getElementById(this.id)) return false;
                let self = this;
                let curInfo = this.info;
                let curSeries = [];
                let yData = [];
                for (let x in curInfo.data) {
                    let obj = {
                        name: curInfo.data[x].name,
                        type: 'bar',
                        barMaxWidth: 20,
                        data: curInfo.data[x].data,
                    }
                    if (self.type == 'bar_pile_y') {
                        obj.stack = '总量'
                    }
                    curSeries.push(obj);
                }
                for (let x in curInfo.labels) {
                    yData.push(curInfo.labels[x])
                }
                this.chart = echarts.init(document.getElementById(this.id));
                let option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                        },
                        formatter: function (params) {
                            let str = params[0].name
                            for (var i = 0; i < params.length; i++) {
                                if (self.unit == self.MODULE && self.name != '会话拒绝统计') {
                                    str += "<br/>" + params[i].seriesName + ":" + self.changeUnit(params[i].value)
                                } else {
                                    str += "<br/>" + params[i].seriesName + ":" + self.changeWanUnit(params[i].value)
                                }
                            }
                            return str
                        },
                    },
                    grid: {
                        top: '10',
                        bottom: '0',
                        left: 30,
                        right: 30,
                        containLabel: true
                    },
                    color: ['rgba(0,189,133,0.8)', 'rgba(233,97,87,0.8)', 'rgba(218,187,97,0.8)', 'rgba(74,146,255,0.8)'],
                    xAxis: {
                        type: 'value',
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        },
                        axisTick: {
                            show: false,
                        },
                        splitNumber: 5,
                        splitLine: {
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        },
                        axisLabel: {
                            textStyle: {color: "#93a6d8"}, formatter: function (value) {
                                if (self.unit == self.MODULE && self.name != '会话拒绝统计') {
                                    return self.changeUnit(value);
                                } else {
                                    return self.changeWanUnit(value);
                                }
                            },
                        },//x轴坐标的字颜色
                    },
                    yAxis: {
                        type: 'category',
                        data: yData,
                        axisLine: {
                            show: true,
                            lineStyle: {
                                color: "#46578e",
                                opacity: "0.75"
                            }
                        },
                        axisTick: {
                            show: false,
                        },
                        axisLabel: {
                            textStyle: {color: "#93a6d8"},
                        },//x轴坐标的字颜色
                    },
                    series: curSeries
                };
                this.chart.setOption(option);
                window.addEventListener('resize', this.chart)
            },
            setNumberChart() {
            },
            initChart() {
                let self = this;
                let repeat = setInterval(function () {
                    if (document.getElementById(self.id)) {
                        self.setChart();
                        clearInterval(repeat)
                    }
                }, 300)
                let resizeRepeat = setInterval(function () {
                    if (document.getElementById(self.id)) {
                        var EleResize = {
                            _handleResize: function (e) {
                                var ele = e.target || e.srcElement;
                                var trigger = ele.__resizeTrigger__;
                                if (trigger) {
                                    var handlers = trigger.__z_resizeListeners;
                                    if (handlers) {
                                        var size = handlers.length;
                                        for (var i = 0; i < size; i++) {
                                            var h = handlers[i];
                                            var handler = h.handler;
                                            var context = h.context;
                                            handler.apply(context, [e]);
                                        }
                                    }
                                }
                            },
                            _removeHandler: function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (handlers) {
                                    var size = handlers.length;
                                    for (var i = 0; i < size; i++) {
                                        var h = handlers[i];
                                        if (h.handler === handler && h.context === context) {
                                            handlers.splice(i, 1);
                                            return;
                                        }
                                    }
                                }
                            },
                            _createResizeTrigger: function (ele) {
                                var obj = document.createElement('object');
                                obj.setAttribute('style',
                                    'display: block; position: absolute; top: 0; left: 0; height: 100%; width: 100%; overflow: hidden;opacity: 0; pointer-events: none; z-index: -1;');
                                obj.onload = EleResize._handleObjectLoad;
                                obj.type = 'text/html';
                                ele.appendChild(obj);
                                obj.data = 'about:blank';
                                return obj;
                            },
                            _handleObjectLoad: function (evt) {
                                this.contentDocument.defaultView.__resizeTrigger__ = this.__resizeElement__;
                                this.contentDocument.defaultView.addEventListener('resize', EleResize._handleResize);
                            }
                        };
                        if (document.attachEvent) {//ie9-10
                            EleResize.on = function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (!handlers) {
                                    handlers = [];
                                    ele.__z_resizeListeners = handlers;
                                    ele.__resizeTrigger__ = ele;
                                    ele.attachEvent('onresize', EleResize._handleResize);
                                }
                                handlers.push({
                                    handler: handler,
                                    context: context
                                });
                            };
                            EleResize.off = function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (handlers) {
                                    EleResize._removeHandler(ele, handler, context);
                                    if (handlers.length === 0) {
                                        ele.detachEvent('onresize', EleResize._handleResize);
                                        delete  ele.__z_resizeListeners;
                                    }
                                }
                            }
                        } else {
                            EleResize.on = function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (!handlers) {
                                    handlers = [];
                                    ele.__z_resizeListeners = handlers;

                                    if (getComputedStyle(ele, null).position === 'static') {
                                        ele.style.position = 'relative';
                                    }
                                    var obj = EleResize._createResizeTrigger(ele);
                                    ele.__resizeTrigger__ = obj;
                                    obj.__resizeElement__ = ele;
                                }
                                handlers.push({
                                    handler: handler,
                                    context: context
                                });
                            };
                            EleResize.off = function (ele, handler, context) {
                                var handlers = ele.__z_resizeListeners;
                                if (handlers) {
                                    EleResize._removeHandler(ele, handler, context);
                                    if (handlers.length === 0) {
                                        var trigger = ele.__resizeTrigger__;
                                        if (trigger) {
                                            trigger.contentDocument.defaultView.removeEventListener('resize', EleResize._handleResize);
                                            ele.removeChild(trigger);
                                            delete ele.__resizeTrigger__;
                                        }
                                        delete  ele.__z_resizeListeners;
                                    }
                                }
                            }
                        }
                        var resizeDiv = document.getElementById(self.id);
                        EleResize.on(resizeDiv, function () {
                        });
                        clearInterval(resizeRepeat)
                    }
                }, 300)
            },
            // 截取数组前五
            splice_tool(arr) {
                if (!arr.length) return arr;
                if (arr.length <= 5) {
                    return arr;
                } else {
                    return arr.slice(0, 5)
                }
            },
            changeUnit(val) {
                if (val < 1024) {
                    return val + "b"
                } else if (val >= 1024 && val < 1024 * 1024) {
                    val = (val / 1024).toFixed(1);
                    return val + "Kb"
                } else if (val >= 1024 * 1024 && val < 1024 * 1024 * 1024) {
                    val = (val / (1024 * 1024)).toFixed(1);
                    return val + "Mb"
                } else if (val >= 1024 * 1024 * 1024) {
                    val = (val / (1024 * 1024 * 1024)).toFixed(1);
                    return val + "Gb"
                }
            },
            changeWanUnit(val) {
                if (val < 10000) {
                    return val
                } else if (val >= 10000 && val < 10000 * 10000) {
                    val = (val / 10000).toFixed(1);
                    return val + "万"
                } else if (val >= 10000 * 10000 && val < 10000 * 10000 * 10000) {
                    val = (val / (10000 * 10000)).toFixed(1);
                    return val + "亿"
                } else {
                    val = (val / (10000 * 10000 * 10000)).toFixed(1);
                    return val + "万亿"
                }
            },
        },
        components: {
            scatterChart,
            lingBarChart,
            loopChart,
        },
        watch: {
            'id': function () {
                if (this.id && this.info.labels) {
                    this.setChart()
                }
            },
        }
    }
</script>